import json

import pandas as pd
from shapely.geometry import shape, GeometryCollection, Point
import geopy.distance

oldest_date=min(df['date'])


# Creamos un array con los distintos productos
products = ["gasoline_95E5",
            "gasoline_95E5_premium",
            "gasoline_98E5",
            "gasoline_98E10",
            "diesel_A",
            "diesel_B",
            "diesel_premium",
            "bioetanol",
            "biodiesel",
            "lpg",
            "cng",
            "lng",
            "hydrogen"]




# Para no machacar el original
df_parsed = df.copy()
df_parsed=df_parsed.fillna(0)




#Adaptado de https://www.bde.es/webbde/es/estadis/infoest/temas/sb_ipc.html
cpi = pd.read_excel('data/raw/be2501.xlsx')
df_parsed=pd.merge(df_parsed.assign(grouper=df_parsed['date'].dt.to_period('M')),
               cpi.assign(grouper=cpi['date'].dt.to_period('M')),
               how='left', on='grouper', suffixes=('', '_y')).drop(columns=['grouper', 'date_y'])

base_cpi=df_parsed[df_parsed["date"] == oldest_date]["vivienda_agua_electricidad_combustibles"].iloc[1]

for prod in products:
    df_parsed[prod+'_adj']=df_parsed[prod]*df_parsed["vivienda_agua_electricidad_combustibles"].divide(base_cpi)

df_distance = df_parsed.groupby('station_id').first().reset_index()[['station_id', 'longitude', 'latitude']]

def minDistance(station, df):
    minDistance=float('inf')
    for index, station_df in df[df['station_id']!=station['station_id']].iterrows():

        distance = geopy.distance.geodesic((station['longitude'], station['latitude']),
                                           (station_df['longitude'], station_df['latitude'])).km
        if distance < minDistance:
            minDistance = distance
    return minDistance

df_distance['min_distance'] = df_distance.apply(lambda x : minDistance(x, df_distance), axis = 1)
df_distance=df_distance.drop(columns = ['longitude', 'latitude'])

df_parsed=df_parsed.merge(df_distance, left_on='station_id', right_on='station_id')

#print(df_parsed)

#https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/madrid-districts.geojson
with open('data/raw/madrid-districts.geojson', 'r') as f:
    js = json.load(f)

def addDistrict(long, lat):
    point = Point(long, lat)

    district = "Not Madrid"
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            district = feature["properties"]["name"]
            break
    return district



df_parsed['district'] =df_parsed.apply(lambda x : addDistrict(x['longitude'], x['latitude']), axis =1 )
#print(df_parsed)

# https://data.metabolismofcities.org/library/maps/35568/view/
neighbourhood_names = pd.read_csv('data/raw/madrid-neighbourhoods-names.csv')
with open('data/raw/madrid-neighbourhoods.geojson', 'r') as f:
    neighbourhood = json.load(f)

def addNeighbourhood(long, lat):
    point = Point(long, lat)
    neigh = "Not Madrid"
    i=0
    for feature in neighbourhood['features']:
        polygon = shape(feature)
        if polygon.contains(point):
            neigh = neighbourhood_names.loc[i, "Name"]
            break
        i=i+1
    return neigh



df_parsed['neighbourhood'] =df_parsed.apply(lambda x : addNeighbourhood(x['longitude'], x['latitude']), axis =1 )


# Eliminamos las columnas de geolocalización que resultan redundantes al trabajar únicamente con la ciudad de Madrid.
df_parsed = df_parsed.drop(columns=['province_name',
                                    'region_name',
                                    'municipality_id',
                                    'municipality_name',
                                    'province_id',
                                    'region_id',
                                    'town'])

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
cols = list(df_parsed.columns)
df_parsed[cols] = df_parsed.groupby('station_id')[cols].bfill()
df_parsed[cols] = df_parsed.groupby('station_id')[cols].ffill()




# Creamos un diccionario para tipificar los distintos tipos de horario.
schedule_dict = {
    "L-D: 05:00-23:00": "L-D",
    "L-D: 05:59-23:59": "L-D",
    "L-D: 06:00-00:00": "L-D",
    "L-D: 06:00-01:30": "L-D",
    "L-D: 06:00-22:00": "L-D",
    "L-D: 06:00-23:00": "L-D",
    "L-D: 06:00-23:59": "L-D",
    "L-D: 06:30-22:30": "L-D",
    "L-D: 07:00-21:30": "L-D",
    "L-D: 07:00-23:00": "L-D",
    "L-D: 12:00-20:00": "L-D",
    "L-D: 24H": "24H",
    "L-J: 06:30-23:00; V: 06:45-22:45; S: 06:45-14:45": "L-D",
    "L-S: 00:00-14:00": "L-S",
    "L-S: 06:00-22:00": "L-S",
    "L-S: 06:30-21:30; D: 08:00-14:00": "L-D",
    "L-S: 07:00-19:00": "L-S",
    "L-S: 07:00-21:00": "L-S",
    "L-S: 07:00-21:00; D: 09:00-14:00": "L-D",
    "L-S: 07:00-21:00; D: 9:00-14:00": "L-D",
    "L-V: 06:00-21:00": "L-V",
    "L-V: 06:00-21:00; S: 08:00-20:00; D: 09:00-15:00": "L-D",
    "L-V: 06:00-22:00; S-D: 08:00-20:00": "L-D",
    "L-V: 06:00-22:00; S-D: 10:00-19:00": "L-D",
    "L-V: 06:00-22:00; S: 07:00-15:00": "L-S",
    "L-V: 06:00-22:00; S: 07:00-15:00; D: 08:00-16:00": "L-D",
    "L-V: 06:00-23:45; S-D: 07:00-23:00": "L-D",
    "L-V: 07:00-21:00; S: 08:00-14:00": "L-S",
    "L-V: 07:00-21:00; S: 08:00-14:30; D: 09:00-15:00": "L-D",
    "L-V: 07:00-21:00; S: 09:00-14:00": "L-S",
    "L-V: 07:00-21:00; S: 09:00-15:00": "L-S",
    "L-V: 07:00-21:00; S: 09:30-14:30": "L-S",
    "L-V: 07:00-21:30; S: 07:00-14:00": "L-S",
    "L-V: 07:00-21:30; S: 08:00-15:00": "L-S",
    "L-V: 07:00-21:30; S: 08:00-15:30": "L-S",
    "L-V: 07:00-21:30; S: 09:00-14:00": "L-S",
    "L-V: 07:00-21:45; S: 08:15-13:45": "L-S",
    "L-V: 07:00-22:00; S-D: 09:00-21:00": "L-D",
    "L-V: 07:00-22:00; S: 08:00-15:00": "L-S",
    "L-V: 07:00-22:00; S: 08:00-21:00": "L-S",
    "L-V: 07:00-22:00; S: 09:00-14:00": "L-S",
    "L-V: 07:00-22:00; S: 09:00-15:00": "L-S",
    "L-V: 07:30-20:30; S: 08:00-14:00": "L-S",
    "L-V: 07:30-21:00; S: 07:30-14:30; D: 09:00-14:00": "L-D",
    "L-V: 07:30-21:00; S: 08:00-14:30": "L-S",
    "L-V: 07:30-21:00; S: 08:00-15:00; D: 09:00-15:00": "L-D",
    "L-V: 07:30-21:00; S: 08:30-14:45": "L-S",
    "L-V: 07:30-21:00; S: 09:30-14:30": "L-S",
    "L-V: 07:30-21:30; S: 08:00-15:00": "L-S",
    "L-X: 07:00-23:00; J: 07:00-23:59; V-S: 00:00-23:59; D: 00:00-23:00": "L-D",
    "L: 24H": "L",
    "S: 08:00-15:00": "S"
}

# Creamos nueva columna con el horario tipificado.
df_parsed['schedule_parsed'] = df_parsed['schedule'].map(schedule_dict)


# Creamos nueva columna con el nombre tipificado
name_dict = {
    'ALCAMPO' :"OTROS",
    'ALHAMBRA-BLANCA ' :"OTROS",
    'ALIARA ENERGIA':"OTROS",
    'BALLENOIL' :"BALLENOIL" ,
    'BEROIL LAS ROSAS':"OTROS",
    'BP ' :"BP",
    'BP A42 CHEYPER' :"BP",
    'BP CARABANCHEL' :"BP",
    'BP E.S. NAVALCARRO':"BP",
    'BP FERMIN FERNANDEZ':"BP",
    'BP GUADALCANAL 365' :"BP",
    'BP ISLA AZUL':"BP",
    'BP MADRID - AV DAROCA' :"BP",
    'BP MAYORAZGO 365':"BP",
    'BP SAN PEDRO MD' :"BP",
    'BP SAN PEDRO MI':"BP",
    'BP' :"BP",
    'CAMPSA':"OTROS",
    'CARREFOUR' :"CARREFOUR" ,
    'CEPSA VALLECAS-LA ATALAYUELA 365':"CEPSA" ,
    'CEPSA-ELF' :"CEPSA" ,
    'CEPSA' :"CEPSA" ,
    'COMERCIAL SAMA':"OTROS",
    'DST ' :"OTROS",
    'DST' :"OTROS",
    'E.LECLERC' :"OTROS",
    'GALP' :"GALP" ,
    'GALP&GO' :"GALP",
    'GHC' :"OTROS",
    'HAM TRES CANTOS' :"OTROS",
    'HUSCO S.L.' :"OTROS",
    'ION +' :"OTROS",
    'LOW COST REPOST' :"OTROS",
    'MADRID WETAXI GLP':"OTROS",
    'NATURGY ' :"NATURGY " ,
    'NATURGY' :"NATURGY" ,
    'OIL A42 A-42 KM 9,8  DIR. MADRID' :"OTROS",
    'PADRE-BLANCA':"OTROS",
    'PLENOIL':"PLENOIL",
    'POWER3OIL'  :"OTROS",
    'Q8' :"OTROS",
    'REPSOL BUTANO':"REPSOL" ,
    'REPSOL' :"REPSOL" ,
    'REPSOL. ESTACIÓN SUR DE AUTOBUSES DE MADRID' :"REPSOL" ,
    'SHELL' :"SHELL" ,
    'SHELL ATALAYUELA 365':"SHELL",
    'SIOMN GRUP' :"OTROS",
    'STAR PETROLEUM' :"OTROS",
    'SUPECO':"OTROS",
    'VIRGEN-BLANCA ' :"OTROS"
}

df_parsed['name_parsed'] = df_parsed['name'].map(name_dict)


products = ["gasoline_95E5",
            "gasoline_95E5_premium",
            "gasoline_98E5",
            "gasoline_98E10",
            "diesel_A",
            "diesel_B",
            "diesel_premium",
            "bioetanol",
            "biodiesel",
            "lpg",
            "cng",
            "lng",
            "hydrogen"]

df_parsed['num_combustibles']=df_parsed[products].astype(bool).sum(axis=1)

# Separamos el dataset en función de los tipos de producto que ofrecen las gasolineras.
# Eliminamos las observaciones que no contienen sendos productos.
df_parsed= df_parsed.fillna(0)
df_gasoline_95E5         = df_parsed[df_parsed['gasoline_95E5'] != 0]
df_gasoline_95E5_premium = df_parsed[df_parsed['gasoline_95E5_premium'] != 0]
df_gasoline_98E5         = df_parsed[df_parsed['gasoline_98E5'] != 0]
df_gasoline_98E10        = df_parsed[df_parsed['gasoline_98E10'] != 0]
df_diesel_A              = df_parsed[df_parsed['diesel_A'] != 0]
df_diesel_B              = df_parsed[df_parsed['diesel_B'] != 0]
df_diesel_premium        = df_parsed[df_parsed['diesel_premium'] != 0]
df_bioetanol             = df_parsed[df_parsed['bioetanol'] != 0]
df_biodiesel             = df_parsed[df_parsed['biodiesel'] != 0]
df_lpg                   = df_parsed[df_parsed['lpg'] != 0]
df_cng                   = df_parsed[df_parsed['cng'] != 0]
df_lng                   = df_parsed[df_parsed['lng'] != 0]
df_hydrogen              = df_parsed[df_parsed['hydrogen'] != 0]

dict_df_products = {}
for producto in products:
    dict_df_products[producto]=df_parsed[df_parsed[producto] != 0]

pickle.dump(dict_df_products, open("data/output/diccionario_df_productos", "wb"))
pickle.dump(df_parsed, open("data/output/df_parsed", "wb"))

print('fin')

