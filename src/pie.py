import plotly.express as px
from dictionaries import *
import plotly.graph_objects as go



def crearPie(df):
    fig=go.Figure()
    if(len(df)):
        df_parsed=df
        last_date=max(df_parsed['date'])
        fig = px.pie(df_parsed[df_parsed['date'] == last_date],
                     values = 'station_id',
                     names = 'name_parsed',
                     title = 'Reparto de gasolineras por empresa',
                     color = 'name_parsed',
                     labels = {'name_parsed':'Company',
                            'station_id':'Gasolineras'},
                     color_discrete_map = name_colors)
        fig.update_traces(textposition='inside',
                          textinfo = 'percent+label',
                          showlegend=False)
    return fig