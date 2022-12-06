import numpy as np
from dictionaries import *
import plotly.graph_objects as go
import plotly.express as px
from skimage import io

def crearViolinEmpresas(df_violin, product):
    fig = go.Figure()
    if len(df_violin):
        df_violin = df_violin.replace(0, np.nan)
        df_violin = df_violin.sort_values(['station_id', 'date'], ascending=False).groupby('station_id',
                                                                                           as_index=False).first()
        df_violin = df_violin[['date'] + products]

        fig = go.Figure()

        fig.add_trace(go.Violin(y=df_violin[product],
                                name=products_titles[product],
                                box_visible=True,
                                meanline_visible=True))

        fig.update_layout(#title_text="Distribución de precio por combustible",
                          yaxis_zeroline=True)

    return fig
