# -*- coding: utf-8 -*-

import plotly.io as pio
pio.renderers.default='browser'

datapath = './data/raw/*.parquet'

exec(open('src/read_data.py').read())
df = df.head()
print(df.columns)
exec(open('src/mapa.py').read())