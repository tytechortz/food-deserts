import pandas as pd
import numpy as np
from dash import Dash, html, dcc, Input, Output, State, ctx, dash_table
import dash_bootstrap_components as dbc
from datetime import date
import geopandas as gpd


from figures_utilities import (
    get_figure
)

from utilities import (
    get_grocery_stores,
    get_block_data
)


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
                    for i in ["Safeway", "King Sooper", "Sprouts", "Walmart SC", "Walmart NM", "Whole Foods", "Trader Joes", "Target", "Save A Lot", "Sams", "Natural Grocers", "Costco", "Lowes", "El Mercado De Colorado" ]
                ],
                value=["Safeway", "King Sooper", "Sprouts", "Walmart SC", "Walmart NM", "Whole Foods", "Trader Joes", "Target", "Save A Lot", "Sams", "Natural Grocers", "Costco", "Lowes", "El Mercado De Colorado" ],
                inline=True
            ),
        ], width=6),
        dbc.Col([
            dcc.Input(
                id='buffer',
                type='number',
                value=1.6,
                step=.1,
                placeholder='Input radius in km'
            ),
        ], width=2),
        dbc.Col([
            dcc.Slider(0, .5, value=.1,
                marks={
                    0: {'label': '0', 'style': {'color': 'white'}},
                    .1: {'label': '.1', 'style': {'color': 'white'}},
                    .2: {'label': '.2', 'style': {'color': 'white'}},
                    .3: {'label': '.3', 'style': {'color': 'white'}},
                    .4: {'label': '.4', 'style': {'color': 'white'}},
                    .5: {'label': '.5', 'style': {'color': 'white'}},
                },
                id = 'poverty',
            ),
        ], width=4),
    ]),
    dbc.Row([
        html.Div([
            dbc.Card(
                dcc.Graph(id='fd-map', figure=blank_fig(500))),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='pop')
       ]),
       dbc.Col([
            html.Div(id='poverty-level')
       ]),
    ]),
    dcc.Store(id='geo-data', storage_type='memory'),
    dcc.Store(id='grocery-stores', storage_type='memory')
])

@app.callback(
        Output('pop', 'children'),
        Input('poverty', 'value'),
        Input('geo-data', 'data'))
def get_pop(buffer, gd):

    gd = gpd.read_file(gd)

    # print(gd)
    # print(gd.columns)
    df = gd[['TRACTCE20', 'GEOID20','Total']]
    # print(df)
    df2 = gd.groupby("TRACTCE20")['Total'].sum()
    # print(df2)
    pop = df2.sum()
    

    return html.Div([
        dbc.Card([
            dbc.CardBody(
                [
                    html.H4('Population', className='text-center'),
                    html.H4('{:,}'.format(pop))
                ]
            )
        ])
    ])

@app.callback(
        Output('poverty-level', 'children'),
        Input('poverty', 'value'))
def get_poverty_level(poverty):

    pov = poverty

    return html.Div([
        dbc.Card([
            dbc.CardBody(
                [
                    html.H4('Percentage in Poverty', className='text-center'),
                    html.H4('{:,}'.format(pov))
                ]
            )
        ])
    ])



@app.callback(
    Output("geo-data", 'data'),
    Output("grocery-stores", 'data'),
    Input("buffer", "value"),
    Input("poverty", "value"),
    Input("stores", "value"))      
def get_geo_data(radius, poverty, stores):
    buffer = radius *1000

    df = get_grocery_stores()
    df = df[df['Store'].isin(stores)]

    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.X, df.Y), crs="EPSG:4326" 
    )
    
    gdf['geometry'] = gdf.geometry.to_crs("epsg:26913")
    # print(gdf)
    geo_data = get_block_data()
    geo_data = geo_data.to_crs("EPSG:26913")
    
    gdf['geometry'] = gdf.geometry.buffer(buffer)
    
    gwb = gpd.overlay(geo_data, gdf, how="difference")
    gwb = gwb.to_crs("epsg:4326")
    blocks = gwb['GEOID20']
      
    gd = geo_data[geo_data['GEOID20'].isin(blocks)]
    gd = gd.to_crs("epsg:4326")
    gd['color'] = 1
    
    gd = gd[gd['pct_pov'] > poverty]
    

    return gd.to_json(), df.to_json()



@app.callback(
    Output("fd-map", "figure"),
    Input("geo-data", "data"),
    Input("grocery-stores", "data"))
def update_Choropleth(geo_data, grocery_stores):
    df = pd.read_json(grocery_stores)

    gd = gpd.read_file(geo_data)
   
    fig = get_figure(df, gd)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)


