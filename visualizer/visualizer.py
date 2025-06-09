"""
Module: visualizer.visualizer
Generate interactive plots in Streamlit or Plotly.
"""
import plotly.express as px
import pandas as pd

def plot_fluxes(df: pd.DataFrame):
    """Return a bar chart of top variable fluxes."""
    df2 = df.sort_values('flux_mean', key=abs, ascending=False).head(20)
    fig = px.bar(df2, x=df2.index, y='flux_mean', title='Top 20 Fluxes')
    return fig
