import dash
from dash.dependencies import Input,Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import datetime
from dateutil.parser import parse
import pytz
import plotly.express as px

from lib.helpers import *



colors = {

    'text' : '#7FDBFF',   #cian = 02edd6
    'background' : '#111111', #white = FFFFFF ; black  = 111111
    'plot_bgcolor' : 'LightSteelBlue',
    'background_h1' : '#FFFFFF',
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__)


def figure(region):
#	region = 'DE-50HZ'
	deltaDays = 0
	df_result = get_data_frame(region = region, deltaDays = deltaDays)
	fig = px.bar(df_result, x=df_result.index, y="Percentage Renewable",
	             color="Percentage Renewable",
	             color_continuous_scale=["#cfb97f","#00ff40"], #px.colors.sequential.Cividis_r || px.colors.sequential.Viridis .. there is a lot more to discover
	)
	fig.update_layout(
	    margin=dict(l=100, r=50, t=100, b=20),
	    paper_bgcolor="LightSteelBlue",
	    xaxis = dict(
	        tickformat  = "%H:00",
	        tickvals = df_result.index,
	        showgrid = True  
	    ),
	    yaxis = dict(
	    	showticklabels = False,
	    	range = [0,100]
	    	) 
	)
	return fig

app.layout = html.Div(
	style={
		'backgroundColor': colors['background'], 'textAlign' : 'center'
	},
	children = [
	# Header
		html.H1(
			"Renewable Energy Forecast",
			style = {
				'backgroundColor' : colors['background'],
				'textAlign' : 'center',
				'color' : colors['text']
			}
		),
		html.H4(
			'Select your Region',
			style = {
				'backgroundColor' : colors['background'],
				'textAlign' : 'center',
				'color' : colors['text']
			}
			),
    	dcc.Dropdown(
    		id = 'Dropdown',
        	options=[
        		{'label': 'Germany', 'value': 'DE'},
            	{'label': '50Hertz', 'value': 'DE-50HZ'},
            	{'label': 'TenneT', 'value': 'DE-TENNET'},
            	{'label': 'Amprion', 'value': 'DE-AMPRION'},
            	{'label': 'Transnet', 'value': 'DE-TRANSNET'}	
        	],
        	value='DE'
    	),
		html.Div(
			children = [
				dcc.Graph(
					id = 'chart_percentage_renewable',
					figure = figure('DE-TRANSNET')
				),
				dcc.Graph(
					id = 'chart_carbon_intensity',
					figure = figure('DE-TRANSNET')

				)
			],
		)
	]
)


@app.callback(
    [
    	Output(component_id='chart_percentage_renewable', component_property='figure'),
    	Output(component_id='chart_carbon_intensity', component_property='figure')
    ],
    [
    	Input(component_id='Dropdown', component_property='value')
    ]
)



def update_output_div(input_value):
    return figure(input_value),figure(input_value)


app.run_server(debug=True)