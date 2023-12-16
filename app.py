import pandas as pd
import numpy as np
from dash import Dash, html, dcc, Input, Output, State, ctx, dash_table
import dash_bootstrap_components as dbc
from datetime import date




from utilities import (
    get_grocery_stores,
    get_block_data
)

df = get_grocery_stores()

pop = get_block_data()
print(pop)


app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])

header = html.Div("Arapahoe County Food Deserts", className="h2 p-2 text-white bg-primary text-center")

bgcolor = "#f3f3f1"  # mapbox light map land color

template = {"layout": {"paper_bgcolor": bgcolor, "plot_bgcolor": bgcolor}}

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

def blank_fig(height):
    """
    Build blank figure with the requested height
    """
    return {
        "data": [],
        "layout": {
            "height": height,
            "template": template,
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
        },
    }



app.layout = dbc.Container([
    header,
    dbc.Row([
        dbc.Col([
            dcc.Checklist(
                id="stores",
                options=[
                    {"label": i, "value": i}
                    for i in ["Safeway", "King Sooper", "Sprouts", "Walmart SC"]
                ],
                value=["Safeway"],
                inline=True
            ),
        ], width=4),
    ]),

])



if __name__ == "__main__":
    app.run_server(debug=True, port=8080)


