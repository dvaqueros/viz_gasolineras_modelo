# -*- coding: utf-8 -*-

import plotly.io as pio
import pandas as pd
import pickle
import plotly.express as px
from itertools import product

pio.renderers.default='browser'
pd.options.display.max_columns = None
datapath = './data/raw/*.parquet'
seed = 123

# Read data
exec(open('src/read_data.py').read())

# Prepare dataset
exec(open('src/dataset.py').read())

# We clean the data
#exec(open('src/data_adaptation.py').read())

# Execute Exploratory Descriptive Analysis
# exec(open('src/exploratory_analysis.py').read())

# Execute Map Visualization
# exec(open('src/mapa2.py').read())

# exec(open('src/lineas.py').read())
# exec(open('src/violin.py').read())

# Execute Time Series Clustering
#product = "gasoline_95E5"
#exec(open('src/clustering_model.py').read())

#exec(open('src/main_dash.py').read())
