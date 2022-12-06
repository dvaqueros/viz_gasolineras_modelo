import sys
sys.path.append('src/')
import dictionaries
import mapa
import mapaDensidad
import mapaPrecio
import pie
import violin
import lineas


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

# Read geojsons
exec(open('src/dash_declarations.py').read())

# # Importamos los datos para cada combustible
# with open("data/output/diccionario_df_productos", 'rb') as f:
#     dict_df_products = pickle.load(f)
#
# Importamos los datos ya procesados
with open("data/output/df_parsed", 'rb') as f:
    df_parsed_1 = pickle.load(f)
#
# # Importamos los datos ya procesados
# with open("data/output/madrid-city", 'rb') as f:
#     city_border = pickle.load(f)

#dict_df=dict_df_products.copy()
#df=df_parsed.copy()
product="gasoline_95E5"

def getDropdownDistritos():
    #distritos = [dbc.DropdownMenuItem(v, id=v+'_id') for v in dictionaries.list_distritos]
    #distritos.append(dbc.DropdownMenuItem(divider=True))
    #distritos.append(dbc.DropdownMenuItem("Todos", id='Todos_distritos'))
    distritos = dictionaries.list_distritos
    distritos.insert(0, "Todos")
    return distritos


def filtrarDF(producto, distrito, start_date, end_date, barrio):

    if producto == 'comparativa':
        with open("data/output/df_parsed", 'rb') as f:
            df_parsed = pickle.load(f)
        return_df = df_parsed
    else:
        with open("data/output/diccionario_df_productos", 'rb') as f:
            dict_df_products = pickle.load(f)
        return_df = dict_df_products[producto]


    if len(return_df):
        if distrito != 'Todos':
            return_df = return_df[return_df['district']==distrito]

    if len(return_df):
        if barrio != 'Todos':
            return_df = return_df[return_df['neighbourhood']==barrio]

    if len(return_df):
        return_df = return_df[(return_df['date']>= start_date) & (return_df['date']<= end_date)]

    return return_df


def getMapa(id, prod, distrito, start_date, end_date, barrio):
    #print(id)
    df=filtrarDF(prod, distrito, start_date, end_date, barrio)
    if id == 'id_Localizacion':
        fig = mapa.crearMapaScatter(df)
    elif id == 'id_Densidad':
        # print(distrito)
        # print(barrio)
        # print(df[['district','neighbourhood']])
        fig = mapaDensidad.crearMapaDensidad(df)
    else:
        fig = mapaPrecio.crearMapaPrecio(df, prod)

    return fig



def getPie(prod, distrito, start_date, end_date, barrio):
    df = filtrarDF(prod, distrito, start_date, end_date, barrio)
    fig=pie.crearPie(df)
    return fig

def getViolinEmpresas(prod, distrito, start_date, end_date, barrio):
    df = filtrarDF(prod, distrito, start_date, end_date , barrio)
    fig=violin.crearViolinEmpresas(df, prod)
    return fig

def getLineas(prod, distrito, start_date, end_date, barrio):
    df = filtrarDF(prod, distrito, start_date, end_date, barrio)
    fig=lineas.crearLineas(df, prod)
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
                    min_date_allowed=min(df_parsed_1['date']),
                    max_date_allowed=max(df_parsed_1['date']),
                    start_date=min(df_parsed_1['date']),
                    end_date=max(df_parsed_1['date']),
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
                        value='Todos',
                        placeholder="Distrito",
                        clearable=False,
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="barrio-dd",
                        options=["Todos"],
                        value='Todos',
                        clearable=False,
                    )
                )
            ],
            id="row-dropdown-distritos",

        ),
        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            dbc.Tabs(
                                [
                                    dbc.Tab(label="95E5",             style={'padding': '0'},     tab_id="gasoline_95E5"),
                                    dbc.Tab(label="95E5 Premium",     style={'padding': '0'},     tab_id="gasoline_95E5_premium"),
                                    dbc.Tab(label="98E5",             style={'padding': '0'},     tab_id="gasoline_98E5"),
                                    #dbc.Tab(label="98E10",            style={'padding': '0'},     tab_id="gasoline_98E10"),
                                    dbc.Tab(label="Diesel A",         style={'padding': '0'},     tab_id="diesel_A"),
                                    dbc.Tab(label="Diesel B",         style={'padding': '0'},     tab_id="diesel_B"),
                                    dbc.Tab(label="Diesel Premium",   style={'padding': '0'},     tab_id="diesel_premium"),
                                    #dbc.Tab(label="Bioetanol",        style={'padding': '0'},     tab_id="bioetanol"),
                                    dbc.Tab(label="Biodiesel",        style={'padding': '0'},     tab_id="biodiesel"),
                                    dbc.Tab(label="LPG",              style={'padding': '0'},     tab_id="lpg"),
                                    dbc.Tab(label="CNG",              style={'padding': '0'},     tab_id="cng"),
                                    dbc.Tab(label="LNG",              style={'padding': '0'},     tab_id="lng"),
                                    #dbc.Tab(label="Hidrógeno",        style={'padding': '0'},     tab_id="hydrogen"),
                                    #dbc.Tab(label="Comparativa",      style={'padding': '0'},     tab_id="comparativa")
                                ],
                                id="tab_products",
                                active_tab="gasoline_95E5",
                                style=
                                    {
                                        "text-align":"center",
                                        "width": "100%",
                                        "margin-top": "1%",
                                        "font-size": "80%",
                                    }
                            )
                        ),
                        html.Br(),
                        html.Br(),
                        dbc.Row(
                            [
                                html.Div(
                                    id='divPlotMap',
                                    children=
                                        [
                                            html.H3("Mapas"),
                                            dbc.Card(
                                                [
                                                    dbc.Row(
                                                        dbc.Tabs(
                                                            [
                                                                dbc.Tab(label="Densidad",      tab_id="id_Densidad"),
                                                                dbc.Tab(label="Precio",        tab_id="id_Precio"),
                                                                dbc.Tab(label="Localizacion",  tab_id="id_Localizacion"),
                                                            ],
                                                            id="tab_mapas",
                                                            active_tab="id_Densidad",
                                                            style=
                                                                {
                                                                    "text-align":"center",
                                                                    "width": "100%",
                                                                    "margin-top": "1%",
                                                                    "font-size": "80%",
                                                                }
                                                        )

                                                    ),
                                                    dbc.Row(
                                                        dbc.CardBody(
                                                            [
                                                                    dcc.Graph(id="plotMap",
                                                                          figure=getMapa("id_Densidad", "gasoline_95E5", 'Todos', min(df_parsed_1['date']), max(df_parsed_1['date']), 'Todos'),
                                                                          style={'width': '100%', 'height': '100%'}),
                                                            ]
                                                        ),
                                                    )
                                                ],
                                                class_name='border-0'
                                            ),
                                        ]
                                )
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            html.Div(
                                id='divPlotPie',
                                children=
                                     [
                                         html.H3("Cuota del total de gasolineras por empresa"),
                                         dbc.Card(
                                             dbc.CardBody([
                                                 dcc.Graph(id="plotPie",
                                                           figure=getPie("gasoline_95E5", 'Todos', min(df_parsed_1['date']), max(df_parsed_1['date']), 'Todos'),
                                                           style={'width': '100%', 'height': '100%'}
                                                           )
                                             ]),
                                             class_name='border-0'
                                         ),

                                     ]
                            )
                        ),
                        html.Br(),
                        dbc.Row(
                            html.Div(
                                id='divPlotViolinEmpresas',
                                children=
                                     [
                                         html.H3("Distribución del precio"),
                                         dbc.Card(
                                             dbc.CardBody([
                                                 dcc.Graph(id="plotViolinEmpresas",
                                                           figure=getViolinEmpresas("gasoline_95E5", 'Todos',  min(df_parsed_1['date']), max(df_parsed_1['date']), 'Todos'),
                                                           style={'width': '100%', 'height': '100%'}
                                                           )
                                             ]),
                                             class_name='border-0'
                                         ),
                                     ]
                            )
                        ),
                        html.Br(),
                        dbc.Row(
                            html.Div(
                                id='divPlotLineas',
                                children=
                                     [
                                         html.H3("Evolución del precio"),
                                         dbc.Card(
                                             dbc.CardBody([
                                                 dcc.Graph
                                                    (
                                                        id="plotLineas",
                                                        figure=getLineas("gasoline_95E5", 'Todos',  min(df_parsed_1['date']), max(df_parsed_1['date']), 'Todos'),
                                                        style={'width': '100%', 'height': '100%'}
                                                    )
                                             ]),
                                             class_name='border-0'
                                         ),
                                     ]
                            )
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




# @app.callback( #Fechas slider
#     Output("fecha_init", "children"),
#     Output("fecha_end", "children"),
#     Input("slider-fechas", 'value'),
# )
# def fechasInitEndSlider(min_max_date):
#     print(min_max_date)
#     return [min_max_date[0].strftime("%Y-%m-%d"),
#             min_max_date[1].strftime("%Y-%m-%d"),]



@app.callback( #Mapa a mostrara
    Output("plotMap", "figure"),
    Output("plotPie", "figure"),
    Output("plotViolinEmpresas", "figure"),
    Output("plotLineas", "figure"),
    Input("tab_mapas", 'active_tab'),
    Input("tab_products", 'active_tab'),
    Input("district-dd", 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input("barrio-dd", 'value'),
)
def selectTabMap(active_tab_map, active_tab_prod, distrito, start_date, end_date, barrio):
    return [getMapa(active_tab_map, active_tab_prod, distrito, start_date, end_date, barrio),
            getPie(active_tab_prod, distrito, start_date, end_date, barrio),
            getViolinEmpresas(active_tab_prod, distrito, start_date, end_date, barrio),
            getLineas(active_tab_prod, distrito, start_date, end_date, barrio)]

@app.callback( # Barrios por distrito dd
    Output("barrio-dd", "options"),
    Input("district-dd", 'value'),
)
def barriosDeDistrito(distrito):
    if distrito != 'Todos':
        return dictionaries.dict_district_neigh[distrito]
    else:
        return ["Todos"]

@app.callback( # Barrios por distrito dd
    Output("barrio-dd", "value"),
    Input("district-dd", 'value'),
    Input("barrio-dd", 'value')
)
def barriosDeDistrito(distrito, barrio):
    if distrito == 'Todos':
        return "Todos"
    else:
        return barrio



if __name__ == "__main__":
    app.title = "GeoPortal"
    app.config.suppress_callback_exceptions = False
    app.run_server(debug=True, port=8080)




#exec(open('src/dash_main.py').read())