"""
Entrypoint for MetaboSim pipeline.
"""
import argparse
from input_loader.loader import load_gene_list, load_pathway_map, load_drug_targets
from parser_engine.parser import parse_reaction_graph
from core_model.model import build_stoichiometric_matrix
from simulator.simulator import run_flux_balance
from analyzer.analyzer import analyze_flux
from contextualizer.contextualizer import integrate_context
from output.exporter import export_results


def main():
    parser = argparse.ArgumentParser(description='Run MetaboSim pipeline')
    parser.add_argument('--genes', required=True, help='Path to upregulated genes list')
    parser.add_argument('--map', dest='map_file', required=True, help='Path to metabolic map file')
    parser.add_argument('--knockout', help='Gene to knockout')
    parser.add_argument('--drug_targets', help='CSV of drug targets')
    parser.add_argument('--output_json', default='results.json')
    parser.add_argument('--output_csv', default=None)
    args = parser.parse_args()

    genes = load_gene_list(args.genes)
    drug_targets = load_drug_targets(args.drug_targets) if args.drug_targets else None
    model = load_pathway_map(args.map_file)
    # optional: reaction_graph = parse_reaction_graph(model)
    solution = run_flux_balance(model, knockout=args.knockout, drug_targets=drug_targets)
    context_sol = integrate_context(solution, genes)
    df = analyze_flux(context_sol)
    export_results(df, args.output_json, args.output_csv, sbml_model=None)

if __name__ == '__main__':
    main()
