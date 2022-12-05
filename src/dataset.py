import json
import pandas as pd
from shapely.geometry import shape, GeometryCollection, Point
import geopy.distance

oldest_date = min(df['date'])

# Para no machacar el original
df_parsed = df.copy()

#####
# Añadimos el IPC mensual para posteriormente calcular los precios ajustados

# Cogemos los datos del IPC del Banco de España
# Adaptado de https://www.bde.es/webbde/es/estadis/infoest/temas/sb_ipc.html
cpi = pd.read_excel('data/raw/be2501.xlsx')

# Se lo añadimos a nuestros datos, teniendo en cuenta que los del mismo mes-año tienen el mismo
df_parsed = pd.merge(df_parsed.assign(grouper=df_parsed['date'].dt.to_period('M')),
                     cpi.assign(grouper=cpi['date'].dt.to_period('M')),
                     how='left', on='grouper', suffixes=('', '_y')).drop(columns=['grouper', 'date_y'])

# Cogemos el IPC de la fecha más antigua
base_cpi = df_parsed[df_parsed["date"] == oldest_date]["vivienda_agua_electricidad_combustibles"].iloc[1]

# Calculamos los precios ajustados
for prod in products:
    df_parsed[prod+'_adj'] = df_parsed[prod]*df_parsed["vivienda_agua_electricidad_combustibles"].divide(base_cpi)


#####
# Calculamos la distancia de la gasolinera más cercana.

# Cogemos únicamente las gasolineras y sus localizaciones
df_distance = df_parsed.groupby('station_id').first().reset_index()[['station_id', 'longitude', 'latitude']]

# Función para calcular las distancias mínimas
def minDistance(station, df):
    """
    Parameters:
    l: str. id de la gasolinera
    df: DataFrame. dataframe con el station_id, longitud y latitude

    Output:
    minDistance: int. Distancia a la gasolinera más cercana
    """
    minDistance = float('inf')

    for index, station_df in df[df['station_id']!=station['station_id']].iterrows():
        distance = geopy.distance.geodesic((station['longitude'], station['latitude']),
                                           (station_df['longitude'], station_df['latitude'])).km
        if distance < minDistance:
            minDistance = distance

    return minDistance


# Añadimos la distancias mínimas al dataset
df_distance['min_distance'] = df_distance.apply(lambda x : minDistance(x, df_distance), axis = 1)
df_distance = df_distance.drop(columns=['longitude', 'latitude'])
df_parsed = df_parsed.merge(df_distance, left_on='station_id', right_on='station_id')


####
# Añadimos el distrito de cada gasolinera
# https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/madrid-districts.geojson
with open('data/raw/madrid-districts.geojson', 'r') as f:
    js = json.load(f)


# Función para automatizar la asignación del distrito de la gasolinera
def addDistrict(long, lat):
    """
    Parameters:
    long: float. coordenada longitud de la gasolinera
    lat: float. coordenada latitud de la gasolinera

    Output:
    district: str. distrito de la gasolinera
    """
    point = Point(long, lat)

    district = "Not Madrid"
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            district = feature["properties"]["name"]
            break
    return district


df_parsed['district'] = df_parsed.apply(lambda x : addDistrict(x['longitude'], x['latitude']), axis =1 )


####
# Añadimos el barrio de cada gasolinera
# https://data.metabolismofcities.org/library/maps/35568/view/
neighbourhood_names = pd.read_csv('data/raw/madrid-neighbourhoods-names.csv')
with open('data/raw/madrid-neighbourhoods.geojson', 'r') as f:
    neighbourhood = json.load(f)


# Función para automatizar la asignación del barrio de la gasolinera
def addNeighbourhood(long, lat):
    """
    Parameters:
    long: float. coordenada longitud de la gasolinera
    lat: float. coordenada latitud de la gasolinera

    Output:
    neigh: str. barrio de la gasolinera
    """
    point = Point(long, lat)
    neigh = "Not Madrid"
    i = 0
    for feature in neighbourhood['features']:
        polygon = shape(feature)
        if polygon.contains(point):
            neigh = neighbourhood_names.loc[i, "Name"]
            break
        i = i+1
    return neigh


df_parsed['neighbourhood'] = df_parsed.apply(lambda x : addNeighbourhood(x['longitude'], x['latitude']), axis =1 )


####
# Eliminamos las columnas de geolocalización que resultan redundantes al trabajar únicamente con la ciudad de Madrid.
df_parsed = df_parsed.drop(columns=['province_name',
                                    'region_name',
                                    'municipality_id',
                                    'municipality_name',
                                    'province_id',
                                    'region_id',
                                    'town'])


####
# Dado que hay fechas que faltan, vamos a rellenar el df en dichas fechas con el último valor disponible.

# Creamos un dataset de apoyo con dos columnas.
# Los valores son el producto cartesiano de las estaciones y fechas únicas
stations = df_parsed['station_id'].unique()
date = df_parsed['date'].unique()
print('hola')
sta_dates = pd.DataFrame(list(product(stations, date)),
                         columns=['station_id', 'date'])
print('adios')
# Se añaden el resto de columnas del dataset original. Valor es NaN.
sta_dates = sta_dates.reindex(columns=df_parsed.columns)

# Establecemos en el df original y en el de apoyo el mismo índice: station_id y date.
df_parsed = df_parsed.set_index(['station_id', 'date'])
sta_dates = sta_dates.set_index(['station_id', 'date'])

# Luego borramos del df de apoyo las tuplas station_id-date ya presentes.
sta_dates = sta_dates.drop(df_parsed.index)

# Concatenamos ambos df y restablecemos el índice
df_parsed = pd.concat([df_parsed, sta_dates]).sort_index()
df_parsed = df_parsed.reset_index()

# Rellenamos los valores ausentes con la última observación disponible.
# df_parsed.replace('0',np.nan)
cols = list(df_parsed.columns)
df_parsed[cols] = df_parsed.groupby('station_id')[cols].bfill()
df_parsed[cols] = df_parsed.groupby('station_id')[cols].ffill()
# aa = df_parsed


####
# Creamos nueva columna con el horario tipificado.
df_parsed['schedule_parsed'] = df_parsed['schedule'].map(schedule_dict)


# Creamos nueva columna con la compañía tipificada.
df_parsed['name_parsed'] = df_parsed['name'].map(name_dict)


# Creamos nueva columna con el número distintos de combustibles que tiene cada gasolinera.
df_parsed['num_combustibles'] = df_parsed[products].astype(bool).sum(axis=1)

df_parsed= df_parsed.fillna(0)
# Separamos el dataset en función de los tipos de producto que ofrecen las gasolineras.
# Eliminamos las observaciones que no contienen sendos productos.
dict_df_products = {}
for producto in products:
    dict_df_products[producto] = df_parsed[df_parsed[producto] != 0]

# Guardamos los conjuntos de datos en binarios
pickle.dump(dict_df_products, open("data/output/diccionario_df_productos", "wb"))
pickle.dump(df_parsed, open("data/output/df_parsed", "wb"))

print('dataset fin')




# df_gasoline_95E5         = df_parsed[df_parsed['gasoline_95E5'] != 0]
# df_gasoline_95E5_premium = df_parsed[df_parsed['gasoline_95E5_premium'] != 0]
# df_gasoline_98E5         = df_parsed[df_parsed['gasoline_98E5'] != 0]
# df_gasoline_98E10        = df_parsed[df_parsed['gasoline_98E10'] != 0]
# df_diesel_A              = df_parsed[df_parsed['diesel_A'] != 0]
# df_diesel_B              = df_parsed[df_parsed['diesel_B'] != 0]
# df_diesel_premium        = df_parsed[df_parsed['diesel_premium'] != 0]
# df_bioetanol             = df_parsed[df_parsed['bioetanol'] != 0]
# df_biodiesel             = df_parsed[df_parsed['biodiesel'] != 0]
# df_lpg                   = df_parsed[df_parsed['lpg'] != 0]
# df_cng                   = df_parsed[df_parsed['cng'] != 0]
# df_lng                   = df_parsed[df_parsed['lng'] != 0]
# df_hydrogen              = df_parsed[df_parsed['hydrogen'] != 0]

