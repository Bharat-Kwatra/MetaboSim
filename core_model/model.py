"""
Module: core_model.model
Construct stoichiometric matrix and compartments.
"""
import pandas as pd
import cobra


def build_stoichiometric_matrix(model: cobra.Model) -> pd.DataFrame:
    """Returns stoichiometric matrix (metabolites x reactions)."""
    met_ids = [m.id for m in model.metabolites]
    rxn_ids = [r.id for r in model.reactions]
    S = pd.DataFrame(0, index=met_ids, columns=rxn_ids)
    for rxn in model.reactions:
        for met, coeff in rxn.metabolites.items():
            S.at[met.id, rxn.id] = coeff
    return S
