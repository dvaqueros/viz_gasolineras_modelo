import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import numpy as np
from dictionaries import *
from geojsons import *
import plotly.express as px
from skimage import io

def crearMapaPrecio(df_mapa, product):
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
        if product != 'comparativa':

            # Elegimos un rango de fechas
            date_init = datetime(2022, 1, 1)
            date_end = datetime(2022, 1, 15)

            # Hago copia para no cargarme el original
            df_mapa = df_mapa.replace(0, np.nan)
            df_mapa = df_mapa[(df_mapa['date'] > date_init) & (df_mapa['date'] < date_end)]

            dct = {
                'number': 'mean',
                'object': lambda col: col.mode() if col.nunique() == 1 else np.nan,
            }

            # https://stackoverflow.com/questions/71209488/pandas-dataframe-groupby-mean-including-string-columns
            groupby_cols = ['station_id', 'neighbourhood']
            dct = {k: v for i in
                   [{col: agg for col in df_mapa.select_dtypes(tp).columns.difference(groupby_cols)} for tp, agg in dct.items()] for
                   k, v in i.items()}
            df_mapa = df_mapa.groupby(groupby_cols, as_index=False).agg(**{k: (k, v) for k, v in dct.items()})


            fig = go.Figure(go.Choroplethmapbox(geojson=city_border, locations=["Madrid"],
                                z=[0],
                                colorscale="Blues",
                                zmin=0,
                                zmax=0,
                                showscale=False,
                                marker_opacity=0.1,
                                marker_line_width=2))

            fig.add_trace(go.Choroplethmapbox(geojson=neighbourhood_borders, locations=np.sort(df_mapa.neighbourhood.unique()),
                                    z=df_mapa.groupby("neighbourhood", as_index=False).agg({product: 'mean'})[product],
                                    colorscale="tealgrn_r",
                                    zmin=min(df_mapa.groupby("neighbourhood", as_index=False).agg({product: 'mean'})[product]),
                                    zmax=max(df_mapa.groupby("neighbourhood", as_index=False).agg({product: 'mean'})[product]),
                                    marker_opacity=0.9, marker_line_width=0))

            fig.update_layout(mapbox_style="open-street-map",
                              margin={"r": 0, "t": 0, "l": 0, "b": 0},
                              mapbox=dict(accesstoken=mapbox_access_token,
                                          center=dict(lat=40.48, lon=-3.72),
                                          style='light',
                                          zoom=9.1),
                              title="Precio medio de" + products_titles[product] + " por barrio")
            return fig
        else:
            img = io.imread('resources/travolta.gif')
            fig = px.imshow(img)
            #fig.update_layout(width=400, height=400)
            fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
            return fig
    return fig