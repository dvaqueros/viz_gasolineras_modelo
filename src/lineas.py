
#Hago copia para no cargarme el original
df_lineas = df.copy()
df_lineas = df_lineas[['date', 'gasoline_95E5', 'diesel_A']]
#Voy a coger la ultima fecha de cada gasolinera para solo pintar un punto
df_lineas = df_lineas.groupby(['date'], group_keys=True).mean().reset_index()

print(df_lineas)
fig = px.line(df_lineas, x='date', y=['gasoline_95E5', 'diesel_A'])

# Show plot
fig.show()


