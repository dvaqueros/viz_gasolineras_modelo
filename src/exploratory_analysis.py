# -*- coding: utf-8 -*-

df['date']=df['date'].dt.strftime('%d%m%Y')

# Initial data analysis and null values filling
print('     ')
print('#########################################################')
print('     DATA TYPE, NON-NULL VARIABLES AND MEMORY USAGE')
print('#########################################################')
print('     ')
print(df['province_name'].unique())
print(df.info())
print('     ')
print('---------- Filling NaN ...')
df= df.fillna(0)
print('---------- NaN remaining:', df.isnull().sum().sum())
print('     ')

# Download selected dataset into .csv

df.to_csv('datos.csv')

print('#########################################################')
print('          EXPLORATORY DESCRIPTIVE ANALYSIS')
print('#########################################################')
print('     ')

print(df.describe())

print('     ')
print('---------- Number of stations per town:')
print('     ')
print(df.groupby("town")[['station_id']].count())
print('Mean: ', df.groupby("town")[['station_id']].count().mean())

print('     ')
print('---------- Number of stations in the province:')
print('     ')
print(df['station_id'].unique().size)