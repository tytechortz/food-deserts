import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import geopandas as gpd


Arap_outline = gpd.read_file('/Users/jamesswank/Python_Projects/Situational_Awareness_v2/us-county-boundaries')



def get_Choropleth(df, gd, marker_opacity, marker_line_width, marker_line_color, fig=None):
    print(gd['geometry'])
    print(gd.columns)
    print(gd)
    
    if fig is None:
        fig = go.Figure(
            
        )

    fig.add_trace(
        go.Choroplethmapbox(
            geojson=eval(gd['geometry'].to_json()),
            # geojson=gd,
            locations=gd.index,
            z=gd['AWATER20'],
            marker_opacity = marker_opacity,
            marker_line_width = marker_line_width,
            marker_line_color = marker_line_color,
            # customdata=gwb["GEOID20"],
            hoverinfo='z',
            colorscale='fall',
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
            showlegend=False,
            hovertemplate='<br>'.join([
            'Store: %{customdata}',
            ]),
        )
    )

    return fig

# def get_map(df, ):

#     fig = go.Figure()
  

    

#     return fig


def get_figure(df, gd):

    # print(df)
    fig = get_Choropleth(df, gd, marker_opacity=1,
                         marker_line_width=1, marker_line_color='#6666cc')
    
    layer = [
            {
                "source": Arap_outline["geometry"].__geo_interface__,
                "type": "line",
                "color": "red"
            }
        ]
    
    
    fig.update_layout(mapbox_style="carto-positron", 
                            mapbox_zoom=10.4,
                            mapbox_layers=layer,
                            mapbox_center={"lat": 39.65, "lon": -104.8},
                            margin={"r":0,"t":0,"l":0,"b":0},
                            autosize=True,
                            uirevision='constant'),
    
                        
    
    # if len(geo_tracts_highlights) != 0:
    #     fig = get_Choropleth(df, geo_tracts_highlights, marker_opacity=1.0,
    #                          marker_line_width=3, marker_line_color='aqua', fig=fig)
    

    return fig