import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import geopandas as gpd


Arap_outline = gpd.read_file('/Users/jamesswank/Python_Projects/Situational_Awareness_v2/us-county-boundaries')



def get_Choropleth(df, gd, marker_opacity, marker_line_width, marker_line_color, fig=None):
    
    
    if fig is None:
        fig = go.Figure(
            
        )

    fig.add_trace(
        go.Choroplethmapbox(
            geojson=eval(gd['geometry'].to_json()),
            # geojson=gd,
            locations=gd.index,
            z=gd['color'],
            marker_opacity = marker_opacity,
            marker_line_width = marker_line_width,
            marker_line_color = marker_line_color,
            # customdata=gwb["GEOID20"],
            showscale=False,
            hoverinfo='z',
            colorscale='blues',
            zmax=1,
            zmin=1
        )
    )
    

    fig.add_trace(
        go.Scattermapbox(
            lat=df['Y'],
            lon=df['X'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=5,
                color='red'
            ),
            customdata=df.Store,
            showlegend=True,
            hovertemplate='<br>'.join([
            'Store: %{customdata}',
            ]),
            name='Grocery Store'
        )
    )

    return fig



def get_figure(df, gd):

    fig = get_Choropleth(df, gd, marker_opacity=1,
                         marker_line_width=.1, marker_line_color='#6666cc')
    
    layer = [
            {
                "source": Arap_outline["geometry"].__geo_interface__,
                "type": "line",
                "color": "blue"
            }
        ]
    
    
    fig.update_layout(mapbox_style="carto-positron", 
                            mapbox_zoom=10.4,
                            mapbox_layers=layer,
                            mapbox_center={"lat": 39.65, "lon": -104.8},
                            margin={"r":0,"t":0,"l":0,"b":0},
                            autosize=True,
                            uirevision='constant'),
    
                        
    

    return fig