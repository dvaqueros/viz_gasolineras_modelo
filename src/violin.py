import numpy as np
from dictionaries import *
import plotly.graph_objects as go
import plotly.express as px
from skimage import io

def crearViolinEmpresas(df_violin, product):
    if product != 'comparativa':

        df_violin = df_violin.replace(0, np.nan)
        df_violin = df_violin.sort_values(['station_id', 'date'], ascending = False).groupby('name_parsed', as_index = False).first()
        df_violin = df_violin[['date'] + products + ['name_parsed']]


        fig = go.Figure()

        for company in df_violin['name_parsed']:
            fig.add_trace(go.Violin(
                                    y = df_violin[df_violin['name_parsed']==company][product],
                                    name = company,
                                    box_visible = True,
                                    meanline_visible = True ))
        fig.update_layout(title_text="Distribución de precio de " + products_titles[product] + " por compañia", yaxis_zeroline=True)
        return fig

    else:
        img = io.imread('resources/travolta.gif')
        fig = px.imshow(img)
        #fig.update_layout(width=400, height=400)
        fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
        return fig