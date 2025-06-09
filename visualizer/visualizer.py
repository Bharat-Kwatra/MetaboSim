import pandas as pd
import plotly.express as px

def plot_fluxes(df: pd.DataFrame):
    """Return a bar chart of top 20 fluxes."""
    
    # Check if the 'flux' column exists before trying to plot
    if 'flux' not in df.columns:
        # Return an empty figure with a message if the data is not as expected
        fig = px.bar(title="No flux data to display.")
        fig.update_layout(
            xaxis = dict(
                visible = False
            ),
            yaxis = dict(
                visible = False
            )
        )
        return fig

    # FIX: Sort by the correct column name 'flux' instead of 'flux_mean'
    # We use abs() to find the reactions with the largest flux, regardless of direction
    df2 = df.reindex(df['flux'].abs().sort_values(ascending=False).index).head(20)
    
    # Create the plot using the correct column name
    fig = px.bar(df2, x=df2.index, y='flux', title='Top 20 Reaction Fluxes')
    fig.update_layout(
        xaxis_title="Reaction ID",
        yaxis_title="Flux Rate (mmol/gDW/hr)",
        xaxis_tickangle=-45
    )
    return fig
