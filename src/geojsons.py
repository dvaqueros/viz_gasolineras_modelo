import json
import pandas as pd
import pickle
from dataset import *


# https://chart-studio.plotly.com/~empet/15238/tips-to-extract-data-from-a-geojson-di/#/
# Aquí explica que una lista de features tenga las siguientes claves: ['type',  'geometry']
# Hay que cambiar la estructura

# geojson del municipio de Madrid
with open('data/raw/madrid-city.geojson', 'r') as f:
    city_border = json.load(f)

city_border['features'][0]['geometry'] = city_border['features'][0].copy()
city_border['features'][0]['type'] = "Feature"
city_border['features'][0]['id'] = "Madrid"
del city_border['features'][0]['coordinates']


# geojson de los barrios de Madrid
neighbourhood_names = pd.read_csv('data/raw/madrid-neighbourhoods-names.csv')
with open('data/raw/madrid-neighbourhoods.geojson', 'r') as f:
    neighbourhood_borders = json.load(f)
for i in range(len(neighbourhood_borders['features'])):
    neighbourhood_borders['features'][i]['geometry']=neighbourhood_borders['features'][i].copy()
    neighbourhood_borders['features'][i]['type']="Feature"
    neighbourhood_borders['features'][i]['id']=neighbourhood_names.loc[i, 'Name']
    del neighbourhood_borders['features'][i]['coordinates']


pickle.dump(city_border, open("data/output/madrid-city", "wb"))
pickle.dump(neighbourhood_borders, open("data/output/madrid-neighbourhoods", "wb"))

