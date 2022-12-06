from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import chart_studio
import datetime
# from functions import locations

username = 'Yugen02'
api_key = 'Vvda56TicCWGrr6OLqd8'

chart_studio.tools.set_credentials_file(username=username,api_key=api_key)

import chart_studio as py
import chart_studio.tools as tls

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
# df = pd.read_csv('https://raw.githubusercontent.com/Yugen02/Dash_board_Regina/master/regina_dashboard/02_data_preparation/Casos_Region_Exacta.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/Yugen02/Dash_board_Regina/Efrain/regina_dashboard/02_data_preparation/dataset/BD_COVID19_PRELIMINAR_MARTES_15_DE_JUNIO_2021.csv')

# del df2["Unnamed: 0"]

df2['DATE'] = pd.to_datetime(df2['FIS'], errors='coerce')

df2['MES'] = df2['DATE'].dt.month_name()
df2['SEMANA'] = df2['DATE'].dt.isocalendar().week


def variables(variable_x, variable_y):
    data_X = []
    data_Y = []
    count = []
    for v_y in pd.unique(variable_y):
        for v_x in pd.unique(variable_x):
            df1 = df2.loc[(variable_x == v_x) & (variable_y == v_y)]
            rows = len(df1.axes[0])
            
            data_X.append(v_x)
            data_Y.append(v_y)
            count.append(rows) 
            # print(df1)
            # print("CASOS {}".format(rows))
    data_variables = pd.DataFrame({'x': data_X, 'y': data_Y,
                            'Casos': count})
    data_variables = data_variables.sort_values(by=['x'])
    return data_variables
    # print(data_variables)




## LISTA DE DROP DOWN

drop_D = ['TIPO DE PACIENTE','EDAD','GRUPO DE EDAD','SEXO','REGION','DISTRITO','MES','SEMANA']

drop_G_x = ['REGION','DISTRITO']
drop_G_y = ['EDAD','GRUPO DE EDAD','SEXO']


app = Dash(__name__)
#'#111111'
colors = {
    'background':'white',
    'text': '#7FDBFF'
}

# datos = variables(df2['REGION'],df2['SEXO'])


# lat = [9.4165,9.4165, 8.3971129,8.3971129,8.4604873,8.4604873,9.3553005,9.3553005,8.2158991,8.2158991,9.057822904338451,9.057822904338451,7.8432774,7.8432774,7.8773471,7.8773471,8.999729497842978,8.999729497842978,8.48621,8.48621,9.0329592,9.0329592,9.078862,9.078862,8.9898564,8.9898564,9.0551061,9.0551061,8.2414131,8.2414131]
# lon= [-82.5207,-82.5207,-82.3223443,-82.3223443,-80.4305652,-80.4305652,-79.8974085,-79.8974085,-78.0172551,-78.0172551,-77.89447750948364,-77.89447750948364,-80.7587705,-80.7587705,-80.4290617,-80.4290617,-79.51171356618619,-79.51171356618619,-81.73081,-81.73081,-79.4710178,-79.4710178,-79.4719702,-79.4719702,-79.6793267,-79.6793267,-79.4933063,-79.4933063,8.2414131,8.2414131]

# datos.insert(3, "Longitud", lon, True)
# datos.insert(4, "Latitud", lat, True)
# # print(datos)

# px.set_mapbox_access_token('pk.eyJ1IjoieXVnZW4wMiIsImEiOiJjbGFnMHJiY3AwdWlrM25vOXRwMG1uaHA1In0.6nnPpOKyl5QsmfGBNcb75Q')

# fig2 = px.scatter_mapbox(datos,
#                         lon = datos['Longitud'],
#                         lat = datos['Latitud'],
#                         zoom = 5,
#                         hover_name=datos['y'],
#                         color = datos['x'],
#                         size = datos['Casos'],
#                         size_max=75
#                         )


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

        html.H1(
        children='VISUALIZACIÓN DEL COMPORTAMIENTO COVID-19 EN PANAMÁ',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),


    html.Div([
        
        html.Div([
            dcc.Dropdown(
                sorted(drop_D),
                'GRUPO DE EDAD',
                id='xaxis-column',
                style={
                'textAlign': 'center',
            }
            )
        ]
        ,style={'width': '45%', 'display': 'inline-block'}
        ),

        html.Div([
            dcc.Dropdown(
                sorted(drop_D),
                'SEXO',
                id='yaxis-column',
                style={
                'textAlign': 'center',
            }
            )
        ]
        ,style={'width': '45%', 'display': 'inline-block', 'padding': '0 20'})
    ], style={
        'padding': '10px 5px'
    }),






    html.Div(children='Grupo de Investigación en Tecnologías Avanzadas de Telecomunicación y Procesamiento de Señales', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph1'
    ),


    html.Div([
        
        html.Div([
            dcc.Dropdown(
                sorted(drop_G_x),
                'REGION',
                id='xaxis-column-g',
                style={
                'textAlign': 'center',
            }
            )
        ]
        ,style={'width': '45%', 'display': 'inline-block'}
        ),

        html.Div([
            dcc.Dropdown(
                sorted(drop_G_y),
                'SEXO',
                id='yaxis-column-g',
                style={
                'textAlign': 'center',
            }
            )
        ]
        ,style={'width': '45%', 'display': 'inline-block', 'padding': '0 20'})
    ], style={
        'padding': '10px 5px'
    }),


    dcc.Graph(
        id='example-graph2',
    )

])






@app.callback(
    Output('example-graph1', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'))

def update_graph1(xaxis_column_n, yaxis_colum_n):

    datos = variables(df2[xaxis_column_n],df2[yaxis_colum_n])     
    # print(variables(xaxis_column_n,yaxis_colum_n))

    # dff = df[df['Region'] == xaxis_column_n]

    fig = px.scatter(datos, x=datos['x'],
                     y=datos['Casos'],
                     hover_name=datos['y'],
                     color=datos['y'], 
                     size_max=100,
                     labels = {'x':xaxis_column_n,'y':yaxis_colum_n,'color':yaxis_colum_n,'hover_name':'Corregimiento'}
                     )



    fig.add_layout_image(
        dict(
            source="http://gitts.utp.ac.pa/wp-content/uploads/2021/08/Update-Logo-GITTS.png",
            xref="paper", yref="paper",
            x=10, y=10,
            sizex=20, sizey=20,
            xanchor="right", yanchor="bottom"
        )
    )

    # fig.update_layout(
    #     plot_bgcolor=colors['background'],
    #     paper_bgcolor=colors['background'],
    #     font_color=colors['text']
    # )
    
    fig.update_traces(marker_size=14)

    fig.update_yaxes(title = 'NUMERO DE CASOS')

    fig.update_xaxes(title = xaxis_column_n)



    # fig.update_yaxes(title=[xaxis_column_n]['Casos'])

    return fig


@app.callback(
    Output('example-graph2', 'figure'),
    Input('xaxis-column-g', 'value'),
    Input('yaxis-column-g', 'value'))

def update_graph2(xaxis_column_g, yaxis_colum_g):

    datos = variables(df2[xaxis_column_g],df2[yaxis_colum_g])


    lat = [9.4165,9.4165, 8.3971129,8.3971129,8.4604873,8.4604873,9.3553005,9.3553005,8.2158991,8.2158991,9.057822904338451,9.057822904338451,7.8432774,7.8432774,7.8773471,7.8773471,8.999729497842978,8.999729497842978,8.48621,8.48621,9.0329592,9.0329592,9.078862,9.078862,8.9898564,8.9898564,9.0551061,9.0551061,8.2414131,8.2414131]
    lon= [-82.5207,-82.5207,-82.3223443,-82.3223443,-80.4305652,-80.4305652,-79.8974085,-79.8974085,-78.0172551,-78.0172551,-77.89447750948364,-77.89447750948364,-80.7587705,-80.7587705,-80.4290617,-80.4290617,-79.51171356618619,-79.51171356618619,-81.73081,-81.73081,-79.4710178,-79.4710178,-79.4719702,-79.4719702,-79.6793267,-79.6793267,-79.4933063,-79.4933063,8.2414131,8.2414131]

    datos.insert(3, "Longitud", lon, True)
    datos.insert(4, "Latitud", lat, True)
    # print(datos)

    px.set_mapbox_access_token('pk.eyJ1IjoieXVnZW4wMiIsImEiOiJjbGFnMHJiY3AwdWlrM25vOXRwMG1uaHA1In0.6nnPpOKyl5QsmfGBNcb75Q')

    fig = px.scatter_mapbox(datos,
                        lon = datos['Longitud'],
                        lat = datos['Latitud'],
                        zoom = 5,
                        hover_name=datos['y'],
                        color = datos['x'],
                        size = datos['Casos'],
                        size_max=75
                        )

    return fig



if __name__ == '__main__':

    app.run_server(debug=True)









