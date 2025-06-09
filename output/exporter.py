"""
Module: output.exporter
Export results to JSON, CSV, and SBML.
"""
import json
import pandas as pd
import cobra


def export_results(df: pd.DataFrame, json_path: str, csv_path: str = None, sbml_model: cobra.Model = None):
    """Write DataFrame to JSON/CSV and model to SBML if provided."""
    df.to_json(json_path, orient='split')
    if csv_path:
        df.to_csv(csv_path)
    if sbml_model:
        cobra.io.write_sbml_model(sbml_model, json_path.replace('.json', '.xml'))
