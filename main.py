# -*- coding: utf-8 -*-

import plotly.io as pio
import pandas as pd

pio.renderers.default='browser'
pd.options.display.max_columns = None
datapath = './data/raw/*.parquet'

# Read data and fill Nan
exec(open('src/read_data.py').read())

# Execute Exploratory Descriptive Analysis
exec(open('src/exploratory_analysis.py').read())

# Execute Map Visualization
## exec(open('src/mapa.py').read())