import streamlit as st
import pandas as pd
from input_loader.loader import load_gene_list, load_pathway_map, load_drug_targets
from simulator.simulator import run_flux_balance
from contextualizer.contextualizer import integrate_context
from analyzer.analyzer import analyze_flux
from visualizer.visualizer import plot_fluxes

st.title("🔬 MetaboSim: Metabolic Simulation Toolkit")

genes_file = st.file_uploader("Upload gene list (.txt)", type="txt")
map_file = st.file_uploader("Upload SBML or JSON model", type=["xml","sbml","json"])
drug_file = st.file_uploader("Upload drug targets (.csv)", type="csv")
knockout_gene = st.text_input("Knockout gene (optional)")

if st.button("Run Simulation"):
    if genes_file and map_file:
        genes = load_gene_list(genes_file)
        drug_targets = load_drug_targets(drug_file) if drug_file else None
        model = load_pathway_map(map_file)
        sol = run_flux_balance(model, knockout=knockout_gene, drug_targets=drug_targets)
        sol2 = integrate_context(sol, genes)
        df = analyze_flux(sol2)
        st.success("Simulation complete!")
        st.plotly_chart(plot_fluxes(df), use_container_width=True)
        st.download_button("Download results CSV", df.to_csv().encode(), "fluxes.csv")
    else:
        st.error("Please upload both gene list and model.")
