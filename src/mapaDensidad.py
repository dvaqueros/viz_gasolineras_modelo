import plotly.graph_objects as go
from geojsons import *
import numpy as np
import plotly.express as px
from skimage import io


def crearMapaDensidad(df_mapa):
    #Voy a coger la ultima fecha de cada gasolinera para solo pintar un punto
    df_mapa = df_mapa.sort_values(['station_id', 'date'], ascending = False).groupby('station_id', as_index = False).first()
    mapbox_access_token = 'pk.eyJ1IjoiZWlzZW5oZXJyIiwiYSI6ImNsYXByaWNqajEzOHAzeG4wYTV6NDZ4aDIifQ.oGCZPVxl5y6Zyg8MJWTypQ'

    fig = go.Figure()
    fig.add_trace(go.Choroplethmapbox(geojson=city_border, locations=["Madrid"],
                                      z=[0],
                                      colorscale="Blues",
                                      zmin=0,
                                      zmax=0,
                                      showscale=False,
                                      marker_opacity=0.1,
                                      marker_line_width=2))
    fig.update_layout(mapbox_style="open-street-map",
                      margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox=dict(accesstoken=mapbox_access_token,
                                  center=dict(lat=40.48, lon=-3.72),
                                  style='light',
                                  zoom=9.1))

    if len(df_mapa):
        fig = go.Figure(go.Choroplethmapbox(geojson=city_border, locations=["Madrid"],
                            z=[0],
                            colorscale="Blues",
                            zmin=0,
                            zmax=0,
                            showscale=False,
                            marker_opacity=0.1,
                            marker_line_width=2))


        fig.add_trace(go.Choroplethmapbox(geojson=neighbourhood_borders, locations=np.sort(df_mapa.neighbourhood.unique()),
                                            z = df_mapa.groupby("neighbourhood",as_index = False).count()['station_id'],
                                            colorscale = "tealgrn_r",
                                            zmin = 0,
                                            zmax = max(df_mapa.groupby("neighbourhood",as_index = False).count()['station_id']),
                                            marker_opacity = 0.9, marker_line_width=0))

        fig.update_layout(mapbox_style = "open-street-map",
                          margin = {"r":0,"t":0,"l":0,"b":0},
                          mapbox = dict(accesstoken = mapbox_access_token,
                                      center=dict(lat=40.48, lon = -3.72),
                                      style = 'light',
                                      zoom = 9.1))

    return fig