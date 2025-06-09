import pandas as pd
from cobra.flux_analysis import flux_variability_analysis

def analyze_flux(model, solution):
    """
    Performs Flux Variability Analysis (FVA) on the simulation results.

    Args:
        model (cobra.Model): The model that was simulated.
        solution (cobra.Solution): The solution object from the simulation.

    Returns:
        pandas.DataFrame: A DataFrame with reaction fluxes and variability.
    """
    if solution.status != 'optimal':
        print("   - Skipping FVA as the solution is not optimal.")
        return pd.DataFrame({'flux': solution.fluxes})
        
    # Use the model passed directly into the function
    fva_result = flux_variability_analysis(
        model, model.reactions, fraction_of_optimum=0.95
    )
    
    # Combine results into a single DataFrame
    df = pd.DataFrame({
        'flux': solution.fluxes,
        'minimum': fva_result['minimum'],
        'maximum': fva_result['maximum']
    })
    
    return df.sort_values(by='flux', ascending=False)
