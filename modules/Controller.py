from modules.submodules.DataHandler import DataHandler
from modules.View import View


class Controller:

    def __init__(self, pd, relativedelta, os, pytz, datetime, API_KEY, EntsoePandasClient, html, dcc, go, textwrap, px,
                 app, Input, Output, dash):

        self.Output = Output
        self.Input = Input
        self.View = View(html, dcc, go, app, textwrap, px)
        app.layout = self.View.get_layout()
        self.DataHandler = DataHandler(pd, relativedelta, os, pytz, datetime, API_KEY, EntsoePandasClient)

        # push data into figures on init:
        # therefore : prepare metadata
        start, end = self.DataHandler.get_day_times()
        metadata = {
            'region': 'DE',
            'start': start,
            'end': end,
        }
        figure_list = {
            'energy_produced': ['live entsoe', 'forecast entsoe', 'forecast statistical'],
            'energy_percentage': ['forecast statistical', 'live entsoe'],
            'energy_carbon_intensity': ['live entsoe', 'forecast statistical']
        }

        # push data into figures
        self.update_all_figures(figure_list, metadata)

        # create callbacks for range slider
        @app.callback(
            [
                Output('fig_energy_composition', 'figure'),
                Output('range-slider', 'marks'),
                Output('range-slider','max')
            ],
            [
                Input(component_id='Dropdown', component_property='value'),
                Input(component_id='range-slider', component_property='value')
            ]
        )
        def update_output_div(selected_dropdown_value, selected_slider_value):
            start_time, end_time = self.DataHandler.get_live_daytimes()
            slider_style = {'font_size': 14, 'font_type': "Courier New, monospace"}
            range_slider_style = dict(fontFamily=slider_style['font_type'], fontSize=slider_style['font_size'], )
            times = [start_time + relativedelta(hours=x) for x in range(end_time.hour+1)]
            range_slider_marks = {x.hour: {'label': times[i].strftime('%H:%M'), 'style': range_slider_style} for i, x in
                                  enumerate(times)}

            slider_start_time, slider_end_time = self.DataHandler.get_slider_times(selected_slider_value)

            # override global times
            metadata_slider = metadata
            metadata_slider['region'] = selected_dropdown_value
            metadata_slider['start'] = slider_start_time
            metadata_slider['end'] = slider_end_time

            self.update_all_figures({'energy_composition': ['live entsoe']}, metadata_slider)
            return [self.View.figures['energy_composition'], range_slider_marks, end_time.hour]

        # create callbacks for each figure/modal ...
        for id in ['fig_energy_produced', 'fig_energy_carbon_intensity', 'fig_energy_percentage',
                   'fig_energy_composition']:
            # Create show/hide callbacks for each info modal
            @app.callback([Output(f"{id}-modal", 'style'), Output(f"{id}-div", 'style')],
                          [Input(f'show-{id}-modal', 'n_clicks'),
                           Input(f'close-{id}-modal', 'n_clicks')])
            def toggle_modal(n_show, n_close):
                ctx = dash.callback_context
                if ctx.triggered and ctx.triggered[0]['prop_id'].startswith('show-'):
                    return {"display": "block"}, {'zIndex': 1003}
                else:
                    return {"display": "none"}, {'zIndex': 0}

        @app.callback(
            Output('fig_energy_produced', 'figure'),
            Output('fig_energy_carbon_intensity', 'figure'),
            Output('fig_energy_percentage', 'figure'),
            Input('Dropdown', 'value')
        )
        def update_figure(selected_dropdown_value):
            start, stop = self.DataHandler.get_day_times()
            print(start,stop)
            metadata['region'] = selected_dropdown_value
            metadata['start'] = start
            metadata['stop'] = stop
            self.update_all_figures(figure_list, metadata)
            return self.View.figures['energy_produced'], self.View.figures['energy_carbon_intensity'], \
                   self.View.figures['energy_percentage']

    def update_all_figures(self, figure_list, metadata):
        for figure in figure_list:
            if figure == 'energy_percentage':
                for trace in figure_list[figure]:
                    data_type, forecast_type = trace.split()
                    metadata['data_type'] = data_type
                    metadata['forecast_type'] = forecast_type
                    try:
                        df = self.DataHandler.get_percentage(metadata)
                        self.View.update_figure(df, 'energy_percentage', trace)
                    except:
                        print('trace : ' + trace + ' no data yet!')

            if figure == 'energy_produced':
                for trace in figure_list[figure]:
                    data_type, forecast_type = trace.split()
                    metadata['data_type'] = data_type
                    metadata['forecast_type'] = forecast_type
                    # print(metadata['data_type'])
                    try:
                        df = self.DataHandler.get_data(metadata=metadata)
                        self.View.update_figure(df, 'energy_produced', trace)
                    except:
                        print('trace : ' + trace + ' no data yet!')

            if figure == 'energy_composition':
                for trace in figure_list[figure]:
                    data_type, forecast_type = trace.split()
                    metadata['data_type'] = data_type
                    metadata['forecast_type'] = forecast_type
                    try:
                        df = self.DataHandler.get_data(metadata=metadata)
                        self.View.update_pie(df)
                    except:
                        print('trace : ' + trace + ' no data yet!')

            if figure == 'energy_carbon_intensity':
                for trace in figure_list[figure]:
                    data_type, forecast_type = trace.split()
                    metadata['data_type'] = data_type
                    metadata['forecast_type'] = forecast_type
                    try:
                        df = self.DataHandler.get_gC02(metadata=metadata)
                        self.View.update_figure(df, 'energy_carbon_intensity', trace)
                    except:
                        print('trace : ' + trace + 'no data yet!')
