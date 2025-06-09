import argparse
from input_loader.loader import load_gene_list, load_pathway_map, load_drug_targets
from simulator.simulator import run_flux_balance
from analyzer.analyzer import analyze_flux
from contextualizer.contextualizer import integrate_context
from output.exporter import export_results
import cobra

def main():
    parser = argparse.ArgumentParser(description='Run MetaboSim pipeline')
    parser.add_argument('--genes', required=True, help='Path to upregulated genes list')
    parser.add_argument('--map', dest='map_file', required=True, help='Path to metabolic map file')
    parser.add_argument('--knockout', default=None, help='Gene to knockout')
    parser.add_argument('--drug_targets', default=None, help='CSV of drug targets')
    parser.add_argument('--output_json', default='results.json')
    parser.add_argument('--output_csv', default=None)
    args = parser.parse_args()

    # 1. Load all inputs
    print("--- MetaboSim Pipeline Started ---")
    print("1. Loading inputs...")
    model = load_pathway_map(args.map_file)
    upregulated_genes = load_gene_list(args.genes)
    drug_targets = load_drug_targets(args.drug_targets) if args.drug_targets else None

    # 2. Set the model's environment for aerobic growth
    print("2. Setting up the simulation environment...")
    try:
        model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0  # Glucose
        model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0   # Oxygen
        model.reactions.get_by_id("EX_pi__e").lower_bound = -100.0  # Phosphate
        model.reactions.get_by_id("EX_nh4__e").lower_bound = -100.0 # Ammonia
        print("   - Provided Glucose, Oxygen, Phosphate, and Ammonia.")
    except KeyError as e:
        # Fallback for older model ID versions
        try:
             model.reactions.get_by_id("EX_glc_e").lower_bound = -10.0
             model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
             model.reactions.get_by_id("EX_pi_e").lower_bound = -100.0
             model.reactions.get_by_id("EX_nh4_e").lower_bound = -100.0
             print("   - Provided Glucose, Oxygen, Phosphate, and Ammonia (using fallback IDs).")
        except KeyError as e_fallback:
            print(f"   - Warning: Could not find an essential exchange reaction: {e_fallback}")


    # 3. Set the objective function
    print("3. Setting model objective...")
    try:
        model.objective = model.reactions.get_by_id("BIOMASS_Ecoli_core_w_GAM")
        print("   - Objective set to biomass reaction.")
    except KeyError:
        print("   - Warning: Could not find biomass reaction 'BIOMASS_Ecoli_core_w_GAM'.")

    # 4. Run Flux Balance Analysis
    print("4. Running Flux Balance Analysis...")
    solution = run_flux_balance(model, knockout=args.knockout, drug_targets=drug_targets)

    # 5. Check if the simulation was successful
    if solution.status != 'optimal':
        print(f"\n--- Simulation Failed ---")
        print(f"The simulation was not optimal. Status: {solution.status}")
        return

    print(f"   - Base simulation successful. Objective value: {solution.objective_value:.4f}")

    # 6. Contextualize the model
    print("5. Contextualizing model with gene list...")
    contextualized_model = integrate_context(model, upregulated_genes)

    # 7. Analyze the final model's flux
    print("6. Analyzing final fluxes...")
    final_solution = contextualized_model.optimize()
    if final_solution.status != 'optimal':
         print(f"   - Warning: Contextualized model was not optimal. Analyzing base solution instead.")
         df = analyze_flux(model, solution)
    else:
         print(f"   - Contextualized simulation successful. Objective value: {final_solution.objective_value:.4f}")
         df = analyze_flux(contextualized_model, final_solution)

    # 8. Export the final results
    print(f"7. Exporting results to {args.output_json}...")
    export_results(df, args.output_json, args.output_csv)
    print("--- Pipeline Finished Successfully ---")

if __name__ == '__main__':
    main()
