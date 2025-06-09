"""
Module: input_loader.loader
Loading gene lists, pathway maps, variant annotations, and drug-target info.
"""
import os
from typing import List, Dict
import pandas as pd
import cobra


def load_gene_list(path: str) -> List[str]:
    """Read a gene list from a text file (one gene per line)."""
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def load_drug_targets(path: str) -> Dict[str, float]:
    """Load drug target CSV with columns: gene, inhibition_coefficient."""
    df = pd.read_csv(path)
    return dict(zip(df['gene'], df['inhibition_coefficient']))


def load_pathway_map(path: str) -> cobra.Model:
    """Load a metabolic model from SBML or JSON using COBRApy."""
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.xml', '.sbml']:
        return cobra.io.read_sbml_model(path)
    if ext == '.json':
        return cobra.io.load_json_model(path)
    raise NotImplementedError(f"Unsupported format: {ext}")
