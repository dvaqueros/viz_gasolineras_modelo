# -*- coding: utf-8 -*-

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