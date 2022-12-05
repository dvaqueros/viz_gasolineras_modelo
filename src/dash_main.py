import sys
sys.path.append('src')
import dictionaries


import dash, logging, pickle
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import numpy as np
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from PIL import Image


def getDropdownDistritos():
    distritos = [dbc.DropdownMenuItem(v, id=v+'_id') for v in dictionaries.list_distritos]
    distritos.append(dbc.DropdownMenuItem(divider=True))
    distritos.append(dbc.DropdownMenuItem("Todos", id='Todos_distritos'))

    return distritos

def getDistritos(distrito):

    if distrito == 'Todos':
        distritos = ['Arganzuela', 'Barajas', 'Carabanchel', 'Centro', 'Chamartin', 'Chamberi', 'Ciudad Lineal', 'Fuencarral-El Pardo', 'Hortaleza', 'Latina', 'Moncloa-Aravaca', 'Moratalaz', 'Puente de Vallecas', 'Retiro', 'Salamanca', 'San Blas', 'Tetuan', 'Usera', 'Vicalvaro', 'Villa de Vallecas', 'Villaverde']
    else:
        distritos = [distrito]
    return distritos



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
                    dbc.DropdownMenu(
                        id='distritos-dd',
                        label="Distritos",
                        children= getDropdownDistritos(),
                        align_end=False,
                    )
                ),
                dbc.Col(
                    dbc.DropdownMenu(
                        id='barrios-dd',
                        label="Barrios",
                        children=
                        [
                            dbc.DropdownMenuItem("No hay distrito seleccionado")
                        ],
                        align_end=False,
                    )
                )
            ],
            id="row-dropdown-distritos"
        )


    ],
    fluid=True
)

@app.callback(
    Output("barrios-dd", "children"),
    [Input(v+'_id', 'n_clicks') for v in list_distritos],
)
def barriosDeDistrito(*args):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = "all"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id in ["red", "blue", "green"]:
        df = data.loc[data["color"] == button_id, :]
    elif button_id in ["square", "circle"]:
        df = data.loc[data["shape"] == button_id, :]
    else:
        df = data

    return go.Figure(data=[go.Pie(labels=df["item"], values=df["qty"])])



if __name__ == "__main__":
    app.title = "GeoPortal"
    app.config.suppress_callback_exceptions = False
    app.run_server(debug=False, port=8080)




