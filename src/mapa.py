# -*- coding: utf-8 -*-

import plotly.graph_objects as go

#Hago copia para no cargarme el original
df_mapa = df_parsed.copy()
#Voy a coger la ultima fecha de cada gasolinera para solo pintar un punto
df_mapa = df_mapa.sort_values(['station_id', 'date'], ascending=False).groupby('station_id', as_index=False).first()

#Necesario para algunas funciones de Scattermapbox
mapbox_access_token = 'pk.eyJ1IjoiZWlzZW5oZXJyIiwiYSI6ImNsYXByaWNqajEzOHAzeG4wYTV6NDZ4aDIifQ.oGCZPVxl5y6Zyg8MJWTypQ'

fig = go.Figure()
for name in list(name_colors.keys()):
    df_mapa_1 = df_mapa[df_mapa['name_parsed']==name]
    fig.add_trace(go.Scattermapbox(
        name=name,
        mode="markers+text",
        lat=df_mapa_1["latitude"], lon=df_mapa_1["longitude"],  # color="black", size=3,
        marker=go.scattermapbox.Marker(
                size=8,
                #symbol="fuel",
                symbol="circle",
                color=name_colors[name],
                opacity=0.7)
        ))
fig.update_layout(mapbox_style="open-street-map",
                  margin={"r":0,"t":0,"l":0,"b":0},
                  mapbox=dict(accesstoken=mapbox_access_token,
                              center=dict(lat=40.42, lon=-3.72),
                              style='light',
                              zoom=10))




fig.show()

