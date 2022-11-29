from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = Dash(__name__)

colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

variables = [x for x in df.columns if x != "price_range"]

dict_variables = [{'value':var, "label": var} for var in variables]

# Crear opciones para las asignaturas
subjects = ["math score", "reading score", "writing score"]
options_dropdown_subjects = []
for subject in subjects:
    options_dropdown_subjects.append({'label': subject.split()[0].capitalize(), 'value': subject})

# Crear opciones para las variables categóricas

cols_checklist = ["gender","race/ethnicity","parental level of education", "lunch", "test preparation course"]

options_checklist = []
for col in cols_checklist:
    options_checklist.append({'value': col, 'label': col})


fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

##################################################################################################
##################################################################################################

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    
    html.H1( # Primera fila
            children = [
                "Trabajo 7: Prediccion de precios de gasolina"
            ],
        id = "titulo_trabajo",
        style = {
            "text-align": "center",
            "text-decoration": "underline",
            "backgroundColor": "white",
            "margin-bottom": "1px",
            "border-style": "outset",
            "border-color": "lightblue",
            "height": "55px"
        }
        ),
    
    dcc.Tabs(
           id = "tabs",
           children = [
               dcc.Tab(
                   id = "primer-tab",
                   value = "Descriptivo",
                   label = "Descriptivo",
                   style = {
                       "text-align": "center",
                       "backgroundColor": "lightblue",
                       "margin-bottom": "10px",
                       "border-style": "outset",
                       "border-color": "lightblue",
                       "height": "50px"
                   }
               ),
               dcc.Tab(
                   id = "segundo-tab",
                   value = "Modelo",
                   label = "Modelo",
                   style = {
                       "text-align": "center",
                       "backgroundColor": "lightblue",
                       "margin-bottom": "10px",
                       "border-style": "outset",
                       "border-color": "lightblue",
                       "height": "50px"
                   }
               )   
           ],
       ),
    
    html.Div(
            id = "resultado-tabulacion"
            ),
    # html.H2( # Segunda fila
    #         children = [
    #             "1) Comparativa de notas entre asignaturas y tipo de etnia"
    #         ],
    #         id = "subtitulo1",
    #         style ={
    #             "text-align": "left",
    #             "display": "block"
    #         }
    #     ),

    # html.Div( # Tercera fila
    #         children = [
    #             html.Div( # Bloque izquierdo
    #                 children = [
    #                     html.H3(
    #                         children = [
    #                             "Primer grupo a comparar"
    #                         ],
    #                         id = "primer_grupo",
    #                         style = {
    #                             "display": "block",
    #                             "text-align": "center"
    #                         }
    #                     ),
    #                     # dcc.Dropdown(
    #                     #     options = options_dropdown_race,
    #                     #     placeholder = "Selecciona una raza",
    #                     #     id = "dropdown_race",
    #                     #     style = {
    #                     #         "display": "block",
    #                     #         "width": "300px",
    #                     #         "margin-left": "10px"
    #                     #     }
    #                     # ),
    #                     dcc.Dropdown(
    #                         options = options_dropdown_subjects,
    #                         placeholder = "Selecciona una asignatura",
    #                         id = "dropdown_subject",
    #                         style = {
    #                             "display": "block",
    #                             "width": "300px",
    #                             "margin-left": "10px"
    #                         }
    #                     ),
    #                     # dcc.Graph(
    #                     #     id = "dropdown_figure",
    #                     #     style = {
    #                     #         "display": "none"
    #                     #     }
    #                     # )
    #                 ],
    #                 style = {
    #                     "width": "600px",
    #                     "height": "600px",
    #                     "display": "inline-block",
    #                     "border-style": "ridge",
    #                     "border-color": "black"
    #                 }, 
    #             ),

    #             html.Div( # Bloque derecho
    #                 children = [
    #                     html.H3(
    #                         children = [
    #                             "Segundo grupo a comparar"
    #                         ],
    #                         id = "segundo_grupo",
    #                         style = {
    #                             "display": "block",
    #                             "text-align": "center"
    #                         }
    #                     ),
    #                     # dcc.Dropdown(
    #                     #     options = options_dropdown_race,
    #                     #     placeholder = "Selecciona una raza",
    #                     #     id = "dropdown_race_2",
    #                     #     style = {
    #                     #         "display": "block",
    #                     #         "width": "300px",
    #                     #         "margin-left": "10px"
    #                     #     }
    #                     # ),
    #                     dcc.Dropdown(
    #                         options = options_dropdown_subjects,
    #                         placeholder = "Selecciona una asignatura",
    #                         id = "dropdown_subject_2",
    #                         style = {
    #                             "display": "block",
    #                             "width": "300px",
    #                             "margin-left": "10px"
    #                         }
    #                     ),
    #                     # dcc.Graph(
    #                     #     id = "dropdown_figure_2",
    #                     #     style = {
    #                     #         "display": "none"
    #                     #     }
    #                     # )
    #                 ],
    #                 style = {
    #                     "width": "600px",
    #                     "height": "600px",
    #                     "display": "inline-block",
    #                     "margin-left": "20px",
    #                     "border-style": "ridge",
    #                     "border-color": "black"
    #                 },
    #             ) 
    #         ]
    #     ),
    
    
])




@app.callback(
 [
     Output("resultado-tabulacion", "children"),
     Input("tabs", "value")
 ]
)
 
def layout_tabulacion(tab):

 if tab == "Descriptivo":
     return [
         html.Div(
                 children = [
                     html.H3(
                         id = "titulo-tab-1",
                         children = "Graficas descriptivas"
                     ),
                     
                     html.Div(
                        id = "descriptivo",
                        children = [
                            
                         dcc.Dropdown(
                             id = 'desplegable',
                             options = dict_variables,
                             placeholder = "Selecciona una variable",
                             value = variables[0]
                         ),
                        ]
                    )
                 ]
     )]
 
 elif tab == "Modelo":
     return [
             html.Div(
                     children = [
                         
                         html.H3(
                             id = "titulo-tab-2",
                            children = "Analisis del modelo"
                        ),
                         
                        html.Div(
                            id = "inferencias"
                        )
                     ]
             )]
 else:
     return [html.Div()]


if __name__ == '__main__':
    
    app.run_server(debug=True)