





df_lineas = df.copy()
#df_mapa = df_mapa.sort_values(['station_id', 'date'], ascending=False).groupby('station_id', as_index=False).first()

#print(df_lineas)
#print(df_lineas.groupby(['municipality_name', 'station_id']).count())

#No consigo que el product funcione con la tupla mun, station. Querria hacer el trio num, station, fecha
#mun_stations=df_lineas[['municipality_name', 'station_id']].drop_duplicates().apply(list)
stations = df_lineas['station_id'].unique()
date = df_lineas['date'].unique()
sta_dates = pd.DataFrame(list(product(stations, date)),
                     columns=['station_id', 'date'])

#sta_dates = df_lineas.reindex(sta_dates, fill_value=0)
sta_dates = sta_dates.reindex(columns=df_lineas.columns)

df_lineas = df_lineas.set_index(['station_id', 'date'])
sta_dates = sta_dates.set_index(['station_id', 'date'])
sta_dates = sta_dates.drop(df_lineas.index)

# print("Lineas")
# print(df_lineas)
# print("Fechas")
# print(sta_dates)

df_lineas = pd.concat([df_lineas, sta_dates]).sort_index()
df_lineas = df_lineas.reset_index()


# print(1)
cols = list(df_lineas.columns)
df_lineas[cols] = df_lineas.groupby('station_id')[cols].bfill()
df_lineas[cols] = df_lineas.groupby('station_id')[cols].ffill()

# print(2)
# print(df_lineas)
# print(3)
# print(df_lineas.groupby(['municipality_name', 'station_id']).count())

df = df_lineas
#df_lineas.to_csv('df_lineas.csv')
#fig.show()
