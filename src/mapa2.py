# -*- coding: utf-8 -*-

import plotly.graph_objects as go

#Hago copia para no cargarme el original
df_mapa = df.copy()
#Voy a coger la ultima fecha de cada gasolinera para solo pintar un punto
df_mapa = df_mapa.sort_values(['station_id', 'date'], ascending=False).groupby('station_id', as_index=False).first()

print(df_mapa)

#Necesario para algunas funciones de Scattermapbox
mapbox_access_token = 'pk.eyJ1IjoiZWlzZW5oZXJyIiwiYSI6ImNsYXByaWNqajEzOHAzeG4wYTV6NDZ4aDIifQ.oGCZPVxl5y6Zyg8MJWTypQ'

fig = go.Figure(go.Scattermapbox(
    mode="markers+text",
    lat=df_mapa["latitude"], lon=df_mapa["longitude"],  # color="black", size=3,
    marker=go.scattermapbox.Marker(
            size=8,
            symbol="fuel",
            opacity=0.7),
    #text=[df_mapa['name'][i] + '<br>' + df_mapa['station_id'][i] for i in range(len(df_mapa))] df_mapa.loc[i, 'name']
    hovertext=[df_mapa['name'][i] + '<br>' + str(df_mapa['station_id'][i]) for i in range(len(df_mapa))] #Hay que mejorar un poco la etiqueta
    ))
fig.update_layout(mapbox_style="open-street-map",
                  margin={"r":0,"t":0,"l":0,"b":0},
                  mapbox=dict(accesstoken=mapbox_access_token,
                              center=dict(lat=40.49, lon=-3.72),
                              style='light',
                              zoom=8))


'''
fig = px.scatter_mapbox(df_mapa, lat="latitude", lon="longitude",     #color="black", size=3,
                    marker = {'size': 20, 'symbol': "fuel"},
                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
fig.update_layout(mapbox_style="open-street-map",
                  margin={"r":0,"t":0,"l":0,"b":0})
'''


fig.show()

