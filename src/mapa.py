import plotly.graph_objects as go
from geojsons import *
from dictionaries import *
from mapaDensidad import *
import plotly.io as pio

# Hago copia para no cargarme el original
#df_mapa = df_parsed.copy()


def crearMapaScatter(df_mapa):
    # Unicamente cogemos los datos para la primera fecha
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

    if (len(df_mapa)):
        df_mapa = df_mapa.sort_values(['station_id', 'date'], ascending=False).groupby('station_id', as_index=False).first()

        fig = go.Figure()
        fig.add_trace(go.Choroplethmapbox(geojson=city_border, locations=["Madrid"],
                                          z=[0],
                                          colorscale="Blues",
                                          zmin=0,
                                          zmax=max(df_mapa.groupby("neighbourhood", as_index=False).count()['station_id']),
                                          showscale=False,
                                          marker_opacity=0.25,
                                          marker_line_width=2))


        for name in list(name_colors.keys()):
            df_mapa_1 = df_mapa[(df_mapa['name_parsed'] == name)]
            fig.add_trace(go.Scattermapbox(
                name=name,
                mode="markers+text",
                lat=df_mapa_1["latitude"], lon=df_mapa_1["longitude"],
                marker=go.scattermapbox.Marker(
                    size=df_mapa_1['num_combustibles'] * 3,
                    symbol="circle",
                    color=name_colors[name],
                    opacity=0.7)
            ))

        fig.update_layout(mapbox_style="open-street-map",
                          margin={"r": 0, "t": 0, "l": 0, "b": 0},
                          mapbox=dict(accesstoken=mapbox_access_token,
                                      center=dict(lat=40.48, lon = -3.72),
                                      style='light',
                                      zoom=9.1),
                          legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                          )
                          )

    return fig

