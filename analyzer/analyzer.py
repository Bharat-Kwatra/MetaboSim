"""
Module: analyzer.analyzer
Flux variability and bottleneck analyses.
"""
import pandas as pd
import cobra
from cobra.flux_analysis import flux_variability_analysis


def analyze_flux(solution: cobra.Solution) -> pd.DataFrame:
    """Summarize flux values and variability."""
    model = solution.model
    fva = flux_variability_analysis(model)
    df = pd.DataFrame({
        'flux_mean': solution.fluxes,
        'flux_min': fva['minimum'],
        'flux_max': fva['maximum']
    })
    return df
