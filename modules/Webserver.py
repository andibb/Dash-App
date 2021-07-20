from modules.View import View
class Webserver:

    def __init__(self,dash,html,dcc,go,px):
        app = dash.dash.Dash(__name__)
        self.View = View(html,dcc,go,app)
        app.layout = self.View.get_layout()
        if __name__ == 'modules.Webserver':
            app.run_server(debug=True)
            print("Webserver initiated")