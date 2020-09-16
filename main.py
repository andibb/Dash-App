# standard library imports
import datetime
from dateutil.relativedelta import relativedelta
import pytz #(not sure if it is third party or standard library)
import os
import base64
from textwrap import dedent


#third party library imports
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input,Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go


# local variable import
from helpers import *
from entsoe.entsoe import *

app = dash.Dash(__name__)


#data needed for the slider : 
dcc_slider_data      = get_data('DE-AMPRION',data_type='live')
slider_style         = {'font_size':14,'font_type':"Courier New, monospace"}
range_slider_style   = dict(fontFamily=slider_style['font_type'],fontSize=slider_style['font_size'],)
range_slider_values  = [dcc_slider_data.index.min().hour,dcc_slider_data.index.max().hour]
range_slider_marks   = {date.hour: {'label' : date.strftime('%H:%M'), 'style' : range_slider_style} for date in dcc_slider_data.index }  


#define function for model info overlay
def build_modal_info_overlay(id, side, content):
    """
    Build div representing the info overlay for a plot panel
    """
    div = html.Div([  # modal div
        html.Div([  # content div
            html.Div([
                html.H4([
                    "Info",
                    html.Img(
                        id=f'close-{id}-modal',
                        src="assets/times-circle-solid.svg",
                        n_clicks=0,
                        className='info-icon',
                        style=dict(margin = 0, width = '25px', height = '25px'),
                    ),
                ], className="container_title", style={'color': 'white'}),

                dcc.Markdown(
                    content
                ),
            ])
        ],
            className=f'modal-content {side}',
        ),
        html.Div(className='modal')
    ],
        id=f"{id}-modal",
        style={"display": "none"},
    )

    return div

app.layout = html.Div(
    className = 'grid-container',
    children=[

        build_modal_info_overlay('fig_energy_produced','bottom',dedent("""
            Chart showing the __**produced electric energy**__ for the selected region. The amount of produced electric energy 
            is displayed in Mega Watts for every hour of the current day. There are three different lines visible
            * A statistical forecast, calculated out of the past electric energy generation
            * A forecast from the [entsoe transparency platform](https://transparency.entsoe.eu/generation/r2/dayAheadAggregatedGeneration/show?name=&defaultValue=false&viewType=TABLE&areaType=CTA&atch=false&datepicker-day-offset-select-dv-date-from_input=D&dateTime.dateTime=13.08.2020+00:00|CET|DAYTIMERANGE&dateTime.endDateTime=13.08.2020+00:00|CET|DAYTIMERANGE&area.values=CTY|10Y1001A1001A83F!CTA|10YDE-VE-------2&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2))
            * And last but not least the [live energy generation](https://transparency.entsoe.eu/generation/r2/actualGenerationPerProductionType/show?name=&defaultValue=false&viewType=TABLE&areaType=CTA&atch=false&datepicker-day-offset-select-dv-date-from_input=D&dateTime.dateTime=13.08.2020+00:00|CET|DAYTIMERANGE&dateTime.endDateTime=13.08.2020+00:00|CET|DAYTIMERANGE&area.values=CTY|10Y1001A1001A83F!CTA|10YDE-VE-------2&productionType.values=B01&productionType.values=B02&productionType.values=B03&productionType.values=B04&productionType.values=B05&productionType.values=B06&productionType.values=B07&productionType.values=B08&productionType.values=B09&productionType.values=B10&productionType.values=B11&productionType.values=B12&productionType.values=B13&productionType.values=B14&productionType.values=B20&productionType.values=B15&productionType.values=B16&productionType.values=B17&productionType.values=B18&productionType.values=B19&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)). 
            """)),
        build_modal_info_overlay('fig_energy_intensity','bottom',dedent("""
            Chart showing the __**carbon intensity**__ of the produced electric energy for the selected region. Every generation type is associated to a specific gC02/KWh value:
            * Biomass : 50 
            * Fossil Brown coal/Lignite :1075
            * Fossil Gas : 500
            * Fossil Hard coal : 830
            * Fossil Oil : 900
            * Geothermal : 0
            * Hydro Water Reservoir : 23
            * Hydro Pumped Storage : 23
            * Hydro Run-of-river and poundage : 23
            * Nuclear : 10
            * Other : 500
            * Other renewable : 100
            * Solar : 50
            * Waste : 50
            * Wind Onshore : 18
            * Wind Offshore : 18

            The data is very questionable the source I am referencing to is the [Umwelt-Bundesamt](https://www.umweltbundesamt.de/publikationen/entwicklung-der-spezifischen-kohlendioxid-5)  
            """)),
        build_modal_info_overlay('fig_energy_percentage','bottom',dedent("""
            Chart showing the __**percentage of renewable energy**__ of the current electric energy mix. The data is taken from the statistic energy production forecast. The following energy sources count as renewable:
            * Biomass
            * Geothermal
            * Hydro Pumped Storage
            * Hydro Run-of-river and poundage
            * Solar
            * Wind Onshore
            * Wind Offshore
            * Other renewable
            """)),
        build_modal_info_overlay('fig_energy_composition','bottom',dedent("""
            Chart showing the __**composition of the generated electric energy**__. Renewable energy components are shown in green and non renewable in brown or grey.
            """)),
        html.Div(
            className="Area_0",
            children = [
                html.H1(
                    "Renewable Energy Forecast",
                ),
            ]
        ),
        html.Div(
            className = "Area_1",
            children = [
                html.Div(
                    className = "Area_1_l",
                    children = [
                        html.Div(
                            className='Area_1_l_top',
                            children=[
                                html.H4(
                                    'Select your Region',
                                ),
                                dcc.Dropdown(
                                    className = 'dropdown_region',
                                    id = 'Dropdown',
                                    options=[
                                        {'label': 'Germany', 'value': 'DE'},
                                        {'label': '50hertz', 'value': 'DE-50HZ'},
                                        {'label': 'TENNET', 'value': 'DE-TENNET'},
                                        {'label': 'amprion', 'value': 'DE-AMPRION'},
                                        {'label': 'EnBw', 'value': 'DE-TRANSNET'}   
                                    ],
                                    value='DE',
                                    placeholder = 'Select your Region...',
                                ),
                                html.Img(
                                    className = 'select-region-image',
                                    src = app.get_asset_url('regelzonen.png'), #os.path.abspath('.png'),
                                    alt = 'regelzonen_image',
                                )
                            ]
                        ),
                        
                    ]
                ),
                html.Div(
                    className = "Area_1_r",
                    id = 'fig_energy_produced-div',
                    children = [
                        html.Div(
                            className = 'container_title',
                            children = [
                                html.H4(
                                    [
                                        "produced energy",
                                        html.Img(
                                            id='show-fig_energy_produced-modal',
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className='info-icon',
                                            #style = dict(width='25px',height='25x')
                                        ),
                                    ] 
                                ),
                            ]
                        ),
                        dcc.Graph(
                            className = 'fig_energy_produced',
                            id = 'fig_energy_produced',
                            figure = fig_energy_produced('DE-TRANSNET'), #should be fig_energy_intensity
                        ) 
                    ]
                ),
            ]
        ),
        html.Div(
            className = "Area_2",
            children=[
                html.Div(
                    className = "Area_2_l",
                    id = 'fig_energy_intensity-div',
                    children = [
                        html.Div(
                            className = 'container_title',
                            children = [
                                html.H4(
                                    [
                                        "energy carbon intensity",
                                        html.Img(
                                            id='show-fig_energy_intensity-modal',
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className='info-icon',
                                            #style = dict(width='25px',height='25x')
                                        ),
                                    ] 
                                ),
                            ]
                        ),
                        dcc.Graph(
                            className = 'fig_energy_intensity',
                            id = 'fig_energy_intensity',
                            figure = fig_energy_intensity('DE-TRANSNET') #should be fig_energy_intensity
                        )   
                                        
                    ]
                ),
                html.Div(
                    className = "Area_2_r",
                    id = 'fig_energy_percentage-div',
                    children =[
                        html.Div(
                            className = 'container_title',
                            children = [
                                html.H4(
                                    [
                                        "percentage of renewable energy",
                                        html.Img(
                                            id='show-fig_energy_percentage-modal',
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className='info-icon',
                                            #style = dict(width='25px',height='25x')
                                        ),
                                    ] 
                                ),
                            ]
                        ),
                        dcc.Graph(
                            className = 'fig_energy_percentage',
                            id = 'fig_energy_percentage',
                            figure = fig_energy_percentage('DE-TRANSNET'),
                        ),

                    ],
                )
            ]
        ),
        html.Div(
            className = "Area_3",
            id = 'fig_energy_composition-div',
            children = [
                html.Div(
                    className = 'Area_3_l',
                    children = [
                        dcc.RangeSlider(
                            className = 'range_slider',
                            id = 'range-slider',
                            vertical = True,
                            allowCross = False,
                            count=1, #number of ranges to handle
                            min=range_slider_values[0],
                            max=range_slider_values[1],
                            value = range_slider_values,
                            marks = range_slider_marks 
                        )   
                    ]
                ),
                html.Div(
                    className = 'Area_3_r',
                    children = [
                        html.Div(   
                            className = 'container_title',
                            children = [
                                html.H4(
                                    [
                                        "energy composition",
                                        html.Img(
                                            id='show-fig_energy_composition-modal',
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className='info-icon',
                                            #style = dict(width='25px',height='25x')
                                        ),
                                    ] 
                                ),
                                dcc.Graph(
                                    className = 'fig_energy_composition',
                                    id = 'fig_energy_composition',
                                    figure = fig_energy_composition(region = 'DE-TRANSNET'),
                                )
                            ]
                        ),
                    ]
                )
            ],
        )
    ]
)

#create callbacks for figures
@app.callback(
    [
        Output(component_id='fig_energy_produced', component_property='figure'),
        Output(component_id='fig_energy_intensity', component_property='figure'),
        Output(component_id='fig_energy_percentage', component_property='figure'),
    ],
    [
        Input(component_id='Dropdown', component_property='value')
    ]
)
def update_output_div(selected_dropdown_value):
    #print('Dropdown updater')
    return fig_energy_produced(selected_dropdown_value),fig_energy_intensity(selected_dropdown_value),fig_energy_percentage(selected_dropdown_value)

#create callbacks for range slider
@app.callback(
    [
        Output(component_id='fig_energy_composition', component_property='figure')
        ],
    [
        Input(component_id='Dropdown',component_property='value'),
        Input(component_id='range-slider', component_property='value')
        ]
)
def update_output_div(selected_dropdown_value ,selected_slider_value):
    print(selected_dropdown_value)
    return [fig_energy_composition(region = selected_dropdown_value, input_value=selected_slider_value)]


# Create show/hide callbacks for each info modal
for id in ['fig_energy_produced','fig_energy_intensity','fig_energy_percentage','fig_energy_composition']:
    @app.callback([Output(f"{id}-modal", 'style'), Output(f"{id}-div", 'style')],
                  [Input(f'show-{id}-modal', 'n_clicks'),
                   Input(f'close-{id}-modal', 'n_clicks')])
    def toggle_modal(n_show, n_close):
        ctx = dash.callback_context
        if ctx.triggered and ctx.triggered[0]['prop_id'].startswith('show-'):
            return {"display": "block"}, {'zIndex': 1003}
        else:
            return {"display": "none"}, {'zIndex': 0}


if __name__ == '__main__':
    app.run_server(debug=True)