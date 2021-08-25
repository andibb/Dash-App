from modules.View import View
from modules.Controller import Controller
class Webserver:

    def __init__(self,dash,html,dcc,go,px,pd,relativedelta,os,pytz,datetime,API_KEY,EntsoePandasClient,textwrap,Input, Output):
        
        self.app = dash.dash.Dash(__name__)
        self.Controller = Controller(pd,relativedelta,os,pytz,datetime,API_KEY,EntsoePandasClient,html,dcc,go,textwrap,px,self.app,Input, Output,dash)
        
       #if __name__ == 'modules.Webserver':
            #self.app.run_server(host='0.0.0.0')
            #print("Webserver initiated")
