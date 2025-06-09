import cobra
import pandas as pd
import os

def load_gene_list(file_path: str) -> list:
    """Loads a list of genes from a text file, one gene per line."""
    with open(file_path, 'r') as f:
        # Read each line, strip whitespace, and ignore empty lines
        genes = [line.strip() for line in f if line.strip()]
    return genes

def load_drug_targets(file_path: str) -> dict:
    """
    Loads drug target information from a CSV file.
    The CSV must contain a column named 'target_reaction_id'.
    """
    if file_path is None:
        return None
    df = pd.read_csv(file_path)
    if 'target_reaction_id' in df.columns:
        # Creates a dictionary to block reactions, e.g., {'ACALD': 0.0}
        return dict(zip(df['target_reaction_id'], [0.0] * len(df)))
    else:
        raise ValueError("Drug target CSV must contain a 'target_reaction_id' column.")

def load_pathway_map(file_path: str) -> cobra.Model:
    """
    Loads a metabolic model from SBML or JSON, including gzipped files.
    """
    # This check now correctly handles gzipped and uncompressed SBML files
    if file_path.endswith(('.xml.gz', '.sbml.gz', '.xml', '.sbml')):
        return cobra.io.read_sbml_model(file_path)
    elif file_path.endswith(('.json.gz', '.json')):
        return cobra.io.load_json_model(file_path)
    else:
        # Get just the extension for a cleaner error message
        ext = "".join(os.path.splitext(file_path)[1:])
        raise NotImplementedError(f"Unsupported format: {ext}")
