"""
Module: contextualizer.contextualizer
Overlay expression and variant data onto flux results.
"""
from typing import List
import cobra


def integrate_context(solution: cobra.Solution, upregulated_genes: List[str]) -> cobra.Solution:
    """Adjust reaction bounds based on upregulated genes list."""
    model = solution.model.copy()
    for gene in upregulated_genes:
        for rxn in model.reactions.query(lambda r: gene in [g.id for g in r.genes]):
            rxn.upper_bound *= 2.0
    # re-run FBA after context integration
    return model.optimize()
