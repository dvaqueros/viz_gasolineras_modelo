# -*- coding: utf-8 -*-

import plotly.graph_objects as go

df_mapa = df.copy()
df_mapa = df_mapa.sort_values(['station_id', 'date'], ascending=False)\
                .groupby('station_id').first()
print(df_mapa)
# We build in plotly a scatterplot to observe the distribution of oil stations geographically
fig = go.Figure(data=go.Scattergeo(
        locationmode = 'country names',
        lon = df_mapa['longitude'],
        lat = df_mapa['latitude'],
        #text = df['text'],
        mode = 'markers',
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'octagon',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            
        )))

fig.update_layout(
        title = 'Gasolina',
        geo = dict(
            scope='europe',
            #projection_type='albers',
            resolution = 50,
            fitbounds='locations',
            showland = True,
            #landcolor = "rgb(250, 250, 250)",
            countrywidth = 0.5,
            subunitwidth = 0.5,
            showcountries=True,
            countrycolor="Black",
            showsubunits=False, 
            subunitcolor="Black")
    )

fig.show()

