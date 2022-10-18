# -*- coding: utf-8 -*-

import plotly.graph_objects as go

import pandas as pd

fig = go.Figure(data=go.Scattergeo(
        locationmode = 'europe',
        lon = df['long'],
        lat = df['lat'],
        text = df['text'],
        mode = 'markers',
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            
        )))

fig.update_layout(
        title = 'Gasolina',
        geo = dict(
            scope='europe',
            projection_type='europe',
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )
fig.show()