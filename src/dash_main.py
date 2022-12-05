


import dash, logging
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import numpy as np
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from PIL import Image
import pickle


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
                        label="Distritos",
                        children=
                            [
                                dbc.DropdownMenuItem("Action"),
                                dbc.DropdownMenuItem("Another action"),
                                dbc.DropdownMenuItem("Something else here"),
                                dbc.DropdownMenuItem(divider=True),
                                dbc.DropdownMenuItem("Todos"),
                            ],
                        align_end=False,
                    )
                ),
                dbc.Col(
                    dbc.DropdownMenu(
                        label="Distritos",
                        children=
                        [
                            dbc.DropdownMenuItem("Action"),
                            dbc.DropdownMenuItem("Another action"),
                            dbc.DropdownMenuItem("Something else here"),
                            dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem("Todos"),
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


if __name__ == "__main__":
    app.title = "GeoPortal"
    app.config.suppress_callback_exceptions = False
    app.run_server(debug=False, port=8080)




