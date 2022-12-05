import sys
sys.path.append('src/')
import dictionaries
import mapa

import time, datetime

import pickle
import dash, logging
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import numpy as np
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from PIL import Image


#####
# https://stackoverflow.com/questions/51063191/date-slider-with-plotly-dash-does-not-work




#######

# Importamos los datos para cada combustible
with open("data/output/diccionario_df_productos", 'rb') as f:
    dict_df_products = pickle.load(f)

# Importamos los datos ya procesados
with open("data/output/df_parsed", 'rb') as f:
    df_parsed = pickle.load(f)

# Importamos los datos ya procesados
with open("data/output/madrid-city", 'rb') as f:
    city_border = pickle.load(f)

df=df_parsed.copy()

def getDropdownDistritos():
    #distritos = [dbc.DropdownMenuItem(v, id=v+'_id') for v in dictionaries.list_distritos]
    #distritos.append(dbc.DropdownMenuItem(divider=True))
    #distritos.append(dbc.DropdownMenuItem("Todos", id='Todos_distritos'))
    distritos = dictionaries.list_distritos
    distritos.insert(0, "Todos")
    return distritos

def getDistritos(distrito):

    if distrito == 'Todos':
        distritos = ['Arganzuela', 'Barajas', 'Carabanchel', 'Centro', 'Chamartin', 'Chamberi', 'Ciudad Lineal', 'Fuencarral-El Pardo', 'Hortaleza', 'Latina', 'Moncloa-Aravaca', 'Moratalaz', 'Puente de Vallecas', 'Retiro', 'Salamanca', 'San Blas', 'Tetuan', 'Usera', 'Vicalvaro', 'Villa de Vallecas', 'Villaverde']
    else:
        distritos = [distrito]
    return distritos


def filtrarDF(distrito):

    if distrito == 'Todos':
        distritos = ['Arganzuela', 'Barajas', 'Carabanchel', 'Centro', 'Chamartin', 'Chamberi', 'Ciudad Lineal', 'Fuencarral-El Pardo', 'Hortaleza', 'Latina', 'Moncloa-Aravaca', 'Moratalaz', 'Puente de Vallecas', 'Retiro', 'Salamanca', 'San Blas', 'Tetuan', 'Usera', 'Vicalvaro', 'Villa de Vallecas', 'Villaverde']
    else:
        distritos = [distrito]
    return distritos


def getTabContent():
    fig=mapa.crearMapaScatter(df, city_border)
    return fig



app = dash.Dash(suppress_callback_exceptions=False,
                external_stylesheets=[dbc.themes.LUX])
app.title = "GeoPortal"

#logging.getLogger('werkzeug').setLevel(logging.INFO)
dash.register_page(__name__, path='/')


#df_dash = df_parsed

#fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = dbc.Container(
    [
        dbc.Row([ # Primera fila
            dbc.Col([ # Primera fila/primer bloque
                html.Img(src=Image.open('resources/gas-station-icon.png'),
                         style={
                             "width": "35%"
                         },
                         className="rounded mx-auto d-block"
                )
                ],
                width={"size": 2}
            ),
            dbc.Col([ # Primera fila/segundo bloque
                html.H1("Estudio de las gasolineras en la ciudad de Madrid",
                        style={
                            "fontSize": "50",
                            "horizontal-align": "center",
                            "textAlign": "center",
                            "color": "black",
                        }
                ),
                dcc.DatePickerRange(
                    id='date-picker',
                    min_date_allowed=min(df_parsed['date']),
                    max_date_allowed=max(df_parsed['date']),
                    start_date=min(df_parsed['date']),
                    end_date=max(df_parsed['date']),
                    style=
                        {
                            "text-align":"center",
                            "width": "100%",
                            "margin-top": "1%",
                        }
                )

            ]#,
                #width={"size": 8},
            ),
            dbc.Col([ # Primera fila/tercer bloque
                html.Img(src=Image.open('resources/madrid-logo.png'),
                         style={
                             "width": "35%",
                             "vertical-align": "center",
                                    "textAlign": "center",
                            "horizontal-align": "right"
                         },
                        className="rounded mx-auto d-block"
                )
                ],
                width={"size": 2}
            )
        ],
            id="cabecera-general",
            style={
                "padding-top": "1%",
            },
            justify="evenly"
        ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="district-dd",
                        options= getDropdownDistritos(),
                        placeholder="Distrito",
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="barrios-dd",
                        options=["Seleccione distrito"],
                        placeholder="Barrio",
                    )
                )
            ],
            id="row-dropdown-distritos"
        ),
        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Tabs([
                            dbc.Tab(label="95E5",         tab_id="id_gasoline_95E5"),
                            dbc.Tab(label="95E5 Premium", tab_id="id_gasoline_95E5_premium"),
                            dbc.Tab(label="98E5",         tab_id="id_gasoline_98E5"),
                            dbc.Tab(label="98E10",        tab_id="id_gasoline_98E10"),
                            dbc.Tab(label="Diesel A",              tab_id="id_diesel_A"),
                            dbc.Tab(label="Diesel B",              tab_id="id_diesel_B"),
                            dbc.Tab(label="Diesel Premium",        tab_id="id_diesel_premium"),
                            dbc.Tab(label="Bioetanol",             tab_id="id_bioetanol"),
                            dbc.Tab(label="Biodiesel",             tab_id="id_biodiesel"),
                            dbc.Tab(label="LPG",                   tab_id="id_lpg"),
                            dbc.Tab(label="CNG",                   tab_id="id_cng"),
                            dbc.Tab(label="LNG",                   tab_id="id_lng"),
                            dbc.Tab(label="Hidrógeno",             tab_id="id_hydrogen"),
                            dbc.Tab(label="Comparativa",           tab_id="id_comparativa")
                        ],
                            id="tabs",
                            active_tab="95E5",
                            style=
                                {
                                    "text-align":"center",
                                    "width": "100%",
                                    "margin-top": "1%",
                                }
                        ),
                        html.Div(id='tabs-content',
                                 children=
                                    [
                                        dbc.Card(
                                            dbc.CardBody([
                                                dcc.Graph(id="subplot-profitability",
                                                          figure=getTabContent(),
                                                          style={'width': '100%', 'height': '100%'})
                                            ]),
                                        )
                                    ]
                                 )
                    ],
                    style=
                        {
                            "text-align":"center",
                            "width": "100%",
                        }
                )
            ]
        ),
        html.Br(),

    ],
    fluid=True
)

@app.callback( # Barrios por distrito dd
    Output("barrios-dd", "options"),
    Input("district-dd", 'value')
)
def barriosDeDistrito(distrito):
    if distrito != 'Todos':
        return dictionaries.dict_district_neigh[distrito]
    else:
        return ["Seleccione distrito"]

@app.callback( #Fechas slider
    Output("fecha_init", "children"),
    Output("fecha_end", "children"),
    Input("slider-fechas", 'value'),
)
def fechasInitEndSlider(min_max_date):
    print(min_max_date)
    return [min_max_date[0].strftime("%Y-%m-%d"),
            min_max_date[1].strftime("%Y-%m-%d"),]





if __name__ == "__main__":
    app.title = "GeoPortal"
    app.config.suppress_callback_exceptions = False
    app.run_server(debug=False, port=8080)




#exec(open('src/dash_main.py').read())