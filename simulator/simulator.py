"""
Module: simulator.simulator
Flux balance analysis and perturbations.
"""
import cobra
from cobra.flux_analysis import pfba

def run_flux_balance(model: cobra.Model, knockout: str = None, drug_targets: dict = None) -> cobra.Solution:
    """Perform FBA or knock-out and drug perturbation simulations."""
    sim_model = model.copy()
    if knockout:
        if knockout in sim_model.genes:
            sim_model.genes.get_by_id(knockout).knock_out()
    if drug_targets:
        for gene, coeff in drug_targets.items():
            for rxn in sim_model.reactions:
                if gene in rxn.genes:
                    rxn.upper_bound *= coeff
    solution = pfba(sim_model)
    return solution
