import cobra
# The new, recommended function is imported directly
from cobra.manipulation import knock_out_model_genes

def run_flux_balance(model, knockout=None, drug_targets=None):
    """Runs flux balance analysis on the model."""
    sim_model = model.copy()

    if knockout:
        try:
            # FIX: Use the modern knock_out_model_genes function.
            # This function works "in place" but we use a model copy
            # to avoid modifying the original model.
            knock_out_model_genes(sim_model, [knockout])
            print(f"   - Successfully knocked out gene '{knockout}'.")
        except KeyError:
            print(f"   - Warning: Knockout gene '{knockout}' not found in model.")

    if drug_targets:
        print("   - Applying drug targets...")
        for target, value in drug_targets.items():
            try:
                # A value of 0 means blocking the reaction
                sim_model.reactions.get_by_id(target).lower_bound = value
                sim_model.reactions.get_by_id(target).upper_bound = value
                print(f"     - Blocked reaction '{target}'.")
            except KeyError:
                print(f"   - Warning: Drug target '{target}' not found in model.")

    # Use the standard, most robust FBA method.
    solution = sim_model.optimize()

    return solution
