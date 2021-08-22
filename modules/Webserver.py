from modules.View import View
from modules.Controller import Controller
class Webserver:

    def __init__(self,dash,html,dcc,go,px,pd,relativedelta,os,pytz,datetime,API_KEY,EntsoePandasClient,textwrap,Input, Output):
        
        app = dash.dash.Dash(__name__)
        self.Controller = Controller(pd,relativedelta,os,pytz,datetime,API_KEY,EntsoePandasClient,html,dcc,go,textwrap,px,app,Input, Output,dash)
        
        if __name__ == 'modules.Webserver':
            app.run_server(debug=True)
            print("Webserver initiated")