import dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.graph_objects as go
import numpy as np
import pandas as pd

data = pd.read_csv("dashboard_data.csv",index_col=0)
score_names = {'Grid score':'grid_score','HD score':'hd_score','Speed score':'speed_score',
                'Unidirectional AHV score':'unidir_ahv_score','Bidirectional AHV score':'bidir_ahv_score','Theta score':'theta_score'}
modulated_dict = {'grid_score':'grid_cell','hd_score':'hd_cell','speed_score':'speed_cell',
                'unidir_ahv_score':'unidir_ahv_cell','bidir_ahv_score':'bidir_ahv_cell','theta_score':'theta_cell'}

def add_colorlist(data,xlabel='speed_score',ylabel='theta_score',zlabel='grid_score'):
    colorlist = []
    
    for _,cell in data.iterrows():
        if cell[modulated_dict[xlabel]]==1 and cell[modulated_dict[ylabel]]==0 and cell[modulated_dict[zlabel]]==0:
            colorlist.append(f'{modulated_dict[xlabel]}')
        elif cell[modulated_dict[xlabel]]==0 and cell[modulated_dict[ylabel]]==1 and cell[modulated_dict[zlabel]]==0:
            colorlist.append(f'{modulated_dict[ylabel]}')
        elif cell[modulated_dict[xlabel]]==0 and cell[modulated_dict[ylabel]]==0 and cell[modulated_dict[zlabel]]==1:
            colorlist.append(f'{modulated_dict[zlabel]}')
        elif cell[modulated_dict[xlabel]]==1 and cell[modulated_dict[ylabel]]==1 and cell[modulated_dict[zlabel]]==0:
            colorlist.append(f'{modulated_dict[xlabel]} x {modulated_dict[ylabel]}')
        elif cell[modulated_dict[xlabel]]==0 and cell[modulated_dict[ylabel]]==1 and cell[modulated_dict[zlabel]]==1:
            colorlist.append(f'{modulated_dict[ylabel]} x {modulated_dict[zlabel]}')
        elif cell[modulated_dict[xlabel]]==1 and cell[modulated_dict[ylabel]]==0 and cell[modulated_dict[zlabel]]==1:
            colorlist.append(f'{modulated_dict[xlabel]} x {modulated_dict[zlabel]}')
        elif cell[modulated_dict[xlabel]]==1 and cell[modulated_dict[ylabel]]==1 and cell[modulated_dict[zlabel]]==1:
            colorlist.append(f'{modulated_dict[xlabel]} x {modulated_dict[xlabel]} x {modulated_dict[zlabel]}')
        else:
            colorlist.append('Non-modulated cell')

    data['color'] = colorlist

    return data

def make_3d_scatter(data,xlabel='speed_score',ylabel='theta_score',zlabel='grid_score'):
    scatterplot = px.scatter_3d(data, x=xlabel, y=ylabel, z=zlabel, width=1000,height=700, color='color')
    scatterplot.update_traces(marker={'size': 5})

    return scatterplot

data = add_colorlist(data)
fig = make_3d_scatter(data)
    
app = dash.Dash(__name__)
server = app.server

app.title = "MixSel dashboard"
title_text = "Explore mixed selectivity in the parahippocampal regions "
description_text = '''Select the score to plot on each axis from corresponding dropdown menu.
                      Each cell in the dataset will be displayed as a point with the corresponding scores as coordinates, 
                      and colored according to its classification as modulated/not-modulated by each of the correlates.'''


app.layout = html.Div(
    children=[
        html.H1(children=title_text,className="header-title"),
        html.P(children=description_text,className="header-description"
        ),
        html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(children=[
                        html.Div(children="X axis", className="menu-title"),
                        dcc.Dropdown(
                            id="x-axis-selector",
                            options=[
                                {"label": label, "value": value}
                                for label,value in score_names.items()
                            ],
                            value="speed_score",
                            clearable=False,
                            className="dropdown",
                        )],className = 'x_dropdown'),
                    html.Div(children=[
                        html.Div(children="Y axis", className="menu-title"),
                        dcc.Dropdown(
                            id="y-axis-selector",
                            options=[
                                {"label": label, "value": value}
                                for label,value in score_names.items()
                            ],
                            value="theta_score",
                            clearable=False,
                            className="dropdown",
                        )],className = 'y_dropdown'),

                    html.Div(children=[
                        html.Div(children="Z axis", className="menu-title"),
                        dcc.Dropdown(
                            id="z-axis-selector",
                            options=[
                                {"label": label, "value": value}
                                for label,value in score_names.items()
                            ],
                            value="grid_score",
                            clearable=False,
                            className="dropdown",
                        )],className = 'z_dropdown')

                ]
            ),
        ],
        className="menu",
        ),
        dcc.Graph(
            figure=fig,className="big-plot",id="3d-scatter"
        )   
        ]
)

@app.callback(
    Output("3d-scatter", "figure"),
    [
        Input("x-axis-selector", "value"),
        Input("y-axis-selector", "value"),
        Input("z-axis-selector", "value"),
    ],
)
def update_charts(x_label, y_label, z_label):
    new_data = add_colorlist(data,xlabel=x_label,ylabel=y_label,zlabel=z_label)
    new_scatter = make_3d_scatter(new_data,xlabel=x_label,ylabel=y_label,zlabel=z_label)  
    return new_scatter



if __name__ == "__main__":
    app.run_server(debug=True)