#Algo le pasa a los 0

df_violin = df.copy()
#Voy a coger la ultima fecha de cada gasolinera para solo pintar un punto
df_violin = df_violin[['date', 'gasoline_95E5', 'diesel_A']]


fig = go.Figure()

gas_type = ['gasoline_95E5', 'diesel_A']

for gas in gas_type:
    fig.add_trace(go.Violin(
                            y=df_violin[gas],
                            name=gas,
                            box_visible=True,
                            meanline_visible=True))

fig.show()
