from modules.submodules.CalcEngine import CalcEngine
from modules.submodules.DataHandler import DataHandler
from modules.submodules.entsoe.entsoe import EntsoePandasClient
from modules.Webserver import Webserver

from modules.Controller import Controller
from modules.View import View
from modules.Model import Model

import pytz
import datetime
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


from dateutil.relativedelta import relativedelta
import os
from dotenv import load_dotenv


# loads environment files .env
load_dotenv('.env')
API_KEY = os.getenv('API_KEY')

class DashApp:
    def __init__(self):
        self.Webserver = Webserver(dash,html,dcc,go,px)
        self.DataHandler = DataHandler(pd,relativedelta,os,pytz,datetime,API_KEY,EntsoePandasClient)
        print("DashApp Initiated")

DashApp = DashApp()

#print(DashApp.DataHandler.get_data_container(metada_grp_call))
# start,end = DashApp.DataHandler.get_day_times()
# metadata = {
#     'region' : 'DE',
#     'start' : start-relativedelta(days=0),
#     'end'    : end-relativedelta(days=0),
#     'data_type' : 'live',
#     'forecast_type' : 'statistical'
# }

# print(DashApp.DataHandler.get_data(metadata))

#    
# summ_gC02_per_KWh = np.zeros(len(df))
# for el in df.columns:
#     summ_gC02_per_KWh += self.calc_percentage(renewable_energies=[el])/100*lookup_c02_intesities[el]


# print(DashApp.DataHandler.get_percentage(metadata))
