import streamlit as st
import tempfile
import os
from input_loader.loader import load_gene_list, load_pathway_map, load_drug_targets
from simulator.simulator import run_flux_balance
from analyzer.analyzer import analyze_flux
from contextualizer.contextualizer import integrate_context
from visualizer.visualizer import plot_fluxes
import cobra

st.set_page_config(layout="wide", page_title="MetaboSim")

st.title("🔬 MetaboSim: Metabolic Simulation Pipeline")

# --- Sidebar for Uploads and Inputs ---
st.sidebar.header("1. Upload Your Files")
gene_file = st.sidebar.file_uploader("Upload Gene List (.txt)", type=['txt'])
map_file = st.sidebar.file_uploader("Upload Metabolic Map", type=['xml', 'sbml', 'json', 'gz'])

st.sidebar.header("2. Set Perturbations")
knockout_gene = st.sidebar.text_input("Enter Gene to Knockout (optional)")
drug_file = st.sidebar.file_uploader("Upload Drug Targets (.csv)", type=['csv'])

if st.sidebar.button("Run Simulation"):
    if gene_file and map_file:
        with st.spinner('Running simulation...'):
            # Create temporary files to hold the uploaded data
            temp_files_to_clean = []
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tfg:
                tfg.write(gene_file.getvalue())
                gene_file_path = tfg.name
                temp_files_to_clean.append(gene_file_path)

            map_suffix = "".join(os.path.splitext(map_file.name))
            with tempfile.NamedTemporaryFile(delete=False, suffix=map_suffix) as tfm:
                tfm.write(map_file.getvalue())
                map_file_path = tfm.name
                temp_files_to_clean.append(map_file_path)
            
            drug_file_path = None
            if drug_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tfd:
                    tfd.write(drug_file.getvalue())
                    drug_file_path = tfd.name
                    temp_files_to_clean.append(drug_file_path)

            # --- Full Simulation Pipeline ---
            st.info("1. Loading inputs...")
            model = load_pathway_map(map_file_path)
            upregulated_genes = load_gene_list(gene_file_path)
            drug_targets = load_drug_targets(drug_file_path) if drug_file_path else None
            
            st.info("2. Setting up simulation environment...")
            
            # --- ROBUST ENVIRONMENT SETUP ---
            # This new block sets each reaction individually to handle different model versions.
            try:
                # Set Objective
                model.objective = model.reactions.get_by_id("BIOMASS_Ecoli_core_w_GAM")
            except KeyError:
                try:
                    model.objective = model.reactions.get_by_id("Biomass_Ecoli_core_w_GAM")
                except KeyError as e:
                     st.error(f"Could not set biomass objective. A key reaction is missing: {e}")
                     st.stop()
            
            # Set Nutrients
            nutrient_reactions = {
                "EX_glc__D_e": -10.0, "EX_o2_e": -20.0, "EX_pi__e": -100.0, "EX_nh4__e": -100.0,
                "EX_glc_e": -10.0, "EX_o2_e": -20.0, "EX_pi_e": -100.0, "EX_nh4_e": -100.0 # Fallbacks
            }
            for rxn_id, uptake_rate in nutrient_reactions.items():
                try:
                    model.reactions.get_by_id(rxn_id).lower_bound = uptake_rate
                except KeyError:
                    pass # Ignore if a specific reaction ID doesn't exist

            st.write("   - Environment set up.")
            # --- END OF ROBUST SETUP ---

            st.info("3. Running Flux Balance Analysis...")
            solution = run_flux_balance(model, knockout=knockout_gene if knockout_gene else None, drug_targets=drug_targets)

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

            # Clean up all temporary files
            for f in temp_files_to_clean:
                os.remove(f)
    else:
        st.warning("Please upload both a gene list and a metabolic map.")

