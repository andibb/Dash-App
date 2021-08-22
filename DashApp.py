from modules.submodules.CalcEngine import CalcEngine
from modules.submodules.DataHandler import DataHandler
from modules.submodules.entsoe.entsoe import EntsoePandasClient
from modules.Webserver import Webserver

from modules.Controller import Controller
from modules.View import View

import pytz
import datetime
import pandas as pd

import textwrap

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
        self.Webserver = Webserver(dash,html,dcc,go,px,pd,relativedelta,os,pytz,datetime,API_KEY,EntsoePandasClient,textwrap,Input, Output)
        print("DashApp Initiated")

DashApp = DashApp()