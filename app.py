import streamlit as st
import tempfile
import os
from input_loader.loader import load_gene_list, load_pathway_map, load_drug_targets
from simulator.simulator import run_flux_balance
from analyzer.analyzer import analyze_flux
from contextualizer.contextualizer import integrate_context
from visualizer.visualizer import plot_fluxes

st.set_page_config(layout="wide", page_title="MetaboSim")

st.title("🔬 MetaboSim: Metabolic Simulation Pipeline")

st.sidebar.header("1. Upload Your Files")
gene_file = st.sidebar.file_uploader("Upload Gene List (.txt)", type=['txt'])

# FIX: Add '.gz' to the list of accepted file types
map_file = st.sidebar.file_uploader("Upload Metabolic Map", type=['xml', 'sbml', 'json', 'gz'])

st.sidebar.header("2. Set Perturbations")
knockout_gene = st.sidebar.text_input("Enter Gene to Knockout (optional)")

if st.sidebar.button("Run Simulation"):
    if gene_file and map_file:
        with st.spinner('Running simulation...'):
            # Create temporary files to hold the uploaded data
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tfg:
                tfg.write(gene_file.getvalue())
                gene_file_path = tfg.name
            
            # Get the correct suffix for the temp map file
            map_suffix = "".join(os.path.splitext(map_file.name))
            with tempfile.NamedTemporaryFile(delete=False, suffix=map_suffix) as tfm:
                tfm.write(map_file.getvalue())
                map_file_path = tfm.name

            # --- Full Simulation Pipeline ---
            st.info("1. Loading inputs...")
            model = load_pathway_map(map_file_path)
            upregulated_genes = load_gene_list(gene_file_path)
            
            st.info("2. Setting up simulation environment...")
            try:
                # Set up the environment for the BiGG model
                model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
                model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
                model.reactions.get_by_id("EX_pi__e").lower_bound = -100.0
                model.reactions.get_by_id("EX_nh4__e").lower_bound = -100.0
                model.objective = model.reactions.get_by_id("BIOMASS_Ecoli_core_w_GAM")
            except KeyError:
                # Fallback for older model versions
                model.reactions.get_by_id("EX_glc_e").lower_bound = -10.0
                model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
            
            st.info("3. Running Flux Balance Analysis...")
            solution = run_flux_balance(model, knockout=knockout_gene if knockout_gene else None)

            if solution.status == 'optimal':
                st.success(f"Simulation successful! Growth rate: {solution.objective_value:.4f}")
                
                st.info("4. Analyzing final fluxes...")
                df = analyze_flux(model, solution)
                
                st.info("5. Visualizing results...")
                fig = plot_fluxes(df)
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(df)
            else:
                st.error(f"Simulation failed. Status: {solution.status}")

            # Clean up temporary files
            os.remove(gene_file_path)
            os.remove(map_file_path)
    else:
        st.warning("Please upload both a gene list and a metabolic map.")
