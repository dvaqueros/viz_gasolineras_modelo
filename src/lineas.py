import plotly.express as px
from dictionaries import *
import plotly.graph_objects as go

def crearLineas(df_lineas, product):
    fig = go.Figure()
    if len(df_lineas):
        print(product)
        print(df_lineas)
        # Realizamos una media por fecha del precio del combustible en todas las gasolineras.
        #df_lineas = df_lineas.groupby(['date'], group_keys=True).mean().reset_index()
        df_lineas = df_lineas.groupby(['date'], as_index=False).agg({product: 'mean'})


        fig = px.line(df_lineas,
                      x='date',
                      y=[product],
                      color_discrete_sequence=[palette[0]],
                      labels={
                          "value": "Precio medio (€)",
                          "date": "Fecha",
                          "variable": "Combustible"
                      },
                      title='Serie temporal del precio de ' + product)

        fig.update_traces(mode="markers+lines", hovertemplate=None)
        fig.update_layout(hovermode="x")

    return fig
