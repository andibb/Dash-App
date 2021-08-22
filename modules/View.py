from modules.html_colors import colors_figures


class View:
    def __init__(self, html, dcc, go, app, textwrap, px):
        print("View initiated")
        self.html = html
        self.dcc = dcc
        self.go = go
        self.app = app
        self.textwrap = textwrap
        self.px = px

        self.figures = {}

        self.set_figure_energy_produced()
        self.set_figure_energy_percentage()
        self.set_figure_composition()
        self.set_figure_carbon_intensity()

        self.layout = self.set_layout()

    def update_pie(self, df):
        df_summ = df.sum()
        colors = {'Fossil Gas': 'brown',
                  'Fossil Brown coal/Lignite': 'brown',
                  'Nuclear': 'brown',
                  'Solar': 'green',
                  'Fossil Hard coal': 'brown',
                  'Wind Onshore': 'green',
                  'Biomass': 'green',
                  'Other': 'grey',
                  'Hydro Run-of-river and poundage': 'green',
                  'Hydro Pumped Storage': 'green',
                  'Other renewable': 'green',
                  'Waste': 'grey',
                  'Geothermal': 'green',
                  'Fossil Oil': 'brown',
                  'Wind Offshore': 'green',
                  'Hydro Water Reservoir': 'green'}
        colors_list = []
        for el in df_summ.index:
            colors_list.append(colors[el])
        # print(colors_list)
        self.figures['energy_composition'].update_traces(
            values=df_summ,
            labels=df_summ.index,
            # color = df_summ.index,
            marker={'colors': colors_list},
            selector=dict(name='live entsoe')  # "live data"
        )
        print('update figure : energy_composition @ trace : live entsoe')

    def update_figure(self, df, figure, trace):
        print('update figure : ' + figure + ' @ trace : ' + trace)
        try:
            self.figures[figure].update_traces(
                x=df.index,
                y=df.sum(axis=1),
                selector=dict(name=trace)  # "live data"
            )
        except KeyError as Key:
            print("KeyError: {0}".format(Key))
        except AttributeError:
            print('could not update data : ' + trace)
        except ValueError:
            self.figures[figure].update_traces(
                x=df.index,
                y=df,
                selector=dict(name=trace)  # "live data"
            )

    def set_figure_carbon_intensity(self):
        fig = self.go.Figure()

        fig.add_trace(
            self.go.Scatter(
                x=[],
                y=[],
                mode='lines+markers',
                name='forecast entsoe',
                line_color=colors_figures['forecast entsoe']
            )
        )
        fig.add_trace(
            self.go.Scatter(
                x=[],
                y=[],
                mode='lines+markers',
                name='forecast statistical',
                line_color=colors_figures['forecast statistical']
            )
        )
        fig.add_trace(
            self.go.Scatter(
                x=[],
                y=[],
                mode='lines+markers',
                name='live entsoe',
                line_color=colors_figures['live entsoe']
            )
        )
        fig.update_layout(
            # margin=dict(l=10, r=50, t=100, b=20),
            paper_bgcolor=colors_figures['paper_bgcolor'],
            plot_bgcolor=colors_figures['paper_bgcolor'],
            font=dict(
                family=colors_figures['font_type'],
                size=colors_figures['font_size'],
                # color="RebeccaPurple"
            ),
            xaxis=dict(
                tickformat="%H:00",
                # tickvals = df.index,
                showgrid=True,
                # range = [df.index[0]-relativedelta(hours=3),df.index[-1]-relativedelta(hours=1)],
            ),
            yaxis=dict(
                title='[gC02/kWh]',
                showticklabels=False,
                tickformat='%.1f',
                showgrid=False
            ),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.7,
            ),
        )
        self.figures['energy_carbon_intensity'] = fig

    def set_figure_composition(self):
        fig = self.go.Figure()

        fig.add_trace(
            self.go.Pie(
                name='live entsoe',
                values=[],
                labels=[],
            )
        )

        fig.update_layout(
            # margin=dict(l=10, r=50, t=100, b=20),
            paper_bgcolor=colors_figures['paper_bgcolor'],
            plot_bgcolor=colors_figures['paper_bgcolor'],

        )

        self.figures['energy_composition'] = fig

    def set_figure_energy_percentage(self):
        fig = self.go.Figure()

        fig.add_trace(

            self.go.Bar(
                x=[],
                y=[],
                name='forecast statistical',
                hovertemplate=None,
                marker_color=colors_figures['forecast statistical'],
            )

        )

        fig.add_trace(
            self.go.Bar(
                x=[],
                y=[],
                name='live entsoe',
                hovertemplate=None,
                marker_color=colors_figures['live entsoe'],
            )
        )

        fig.update_layout(
            paper_bgcolor=colors_figures['paper_bgcolor'],
            plot_bgcolor=colors_figures['paper_bgcolor'],
            font=dict(
                family=colors_figures['font_type'],
                size=colors_figures['font_size'],
            ),
            xaxis=dict(
                title="",
                tickformat="%H:00",
                showgrid=True,
            ),
            yaxis=dict(
                title="",
                showticklabels=True,
                showgrid=False,
                range=[0, 100]
            ),
            hoverlabel=dict(
                bgcolor=colors_figures["color_hoverlabel"],
                font_size=16,
                # font_family="Rockwell",
            ),
            hovermode='x',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.7,
            ),
        )
        self.figures['energy_percentage'] = fig

    def set_figure_energy_produced(self):
        fig = self.go.Figure()
        # add trace for statistical forecast
        fig.add_trace(
            self.go.Scatter(
                x=[],
                y=[],
                mode='lines+markers',
                name='forecast statistical',
                line_color=colors_figures['forecast statistical']
            )),
        fig.add_trace(
            self.go.Scatter(
                x=[],
                y=[],
                mode='lines+markers',
                name='forecast entsoe',
                line_color=colors_figures['forecast entsoe']
            )),
        fig.add_trace(
            self.go.Scatter(
                x=[],
                y=[],
                mode='lines+markers',
                name='live entsoe',
                line_color=colors_figures['live entsoe']
            )),
        fig.update_layout(
            # margin=dict(l=10, r=50, t=100, b=20),
            paper_bgcolor=colors_figures['paper_bgcolor'],
            plot_bgcolor=colors_figures['paper_bgcolor'],
            font=dict(
                family=colors_figures['font_type'],
                size=colors_figures['font_size'],
                # color="RebeccaPurple"
            ),
            xaxis=dict(
                tickformat="%H:00",
                # tickvals = df.index,
                showgrid=True,
                # range = [df.index[0]-relativedelta(hours=3),df.index[-1]-relativedelta(hours=1)],
            ),
            yaxis=dict(
                title='[MW]',
                showticklabels=False,
                tickformat='%.1f',
                showgrid=False
            ),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.7,
            ),
        )
        self.figures['energy_produced'] = fig

    # define function for model info overlay
    def build_modal_info_overlay(self, id, side, content):
        """
        Build div representing the info overlay for a plot panel
        """
        div = self.html.Div([  # modal div
            self.html.Div([  # content div
                self.html.Div([
                    self.html.H4([
                        "Info",
                        self.html.Img(
                            id=f'close-{id}-modal',
                            src="assets/times-circle-solid.svg",
                            n_clicks=0,
                            className='info-icon',
                            style=dict(margin=0, width='25px', height='25px'),
                        ),
                    ], className="container_title", style={'color': 'white'}),

                    self.dcc.Markdown(
                        content
                    ),
                ])
            ],
                className=f'modal-content {side}',
            ),
            self.html.Div(className='modal')
        ],
            id=f"{id}-modal",
            style={"display": "none"},
        )
        return div

    def get_layout(self):
        return self.layout

    def set_layout(self):
        layout = self.html.Div(
            className='grid-container',
            children=[

                self.build_modal_info_overlay('fig_energy_produced', 'bottom', self.textwrap.dedent("""
                    Chart showing the __**produced electric energy**__ for the selected region. The amount of produced electric energy 
                    is displayed in Mega Watts for every hour of the current day. There are three different lines visible
                    * A statistical forecast, calculated out of the past electric energy generation
                    * A forecast from the [entsoe transparency platform](https://transparency.entsoe.eu/generation/r2/dayAheadAggregatedGeneration/show?name=&defaultValue=false&viewType=TABLE&areaType=CTA&atch=false&datepicker-day-offset-select-dv-date-from_input=D&dateTime.dateTime=13.08.2020+00:00|CET|DAYTIMERANGE&dateTime.endDateTime=13.08.2020+00:00|CET|DAYTIMERANGE&area.values=CTY|10Y1001A1001A83F!CTA|10YDE-VE-------2&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2))
                    * And last but not least the [live energy generation](https://transparency.entsoe.eu/generation/r2/actualGenerationPerProductionType/show?name=&defaultValue=false&viewType=TABLE&areaType=CTA&atch=false&datepicker-day-offset-select-dv-date-from_input=D&dateTime.dateTime=13.08.2020+00:00|CET|DAYTIMERANGE&dateTime.endDateTime=13.08.2020+00:00|CET|DAYTIMERANGE&area.values=CTY|10Y1001A1001A83F!CTA|10YDE-VE-------2&productionType.values=B01&productionType.values=B02&productionType.values=B03&productionType.values=B04&productionType.values=B05&productionType.values=B06&productionType.values=B07&productionType.values=B08&productionType.values=B09&productionType.values=B10&productionType.values=B11&productionType.values=B12&productionType.values=B13&productionType.values=B14&productionType.values=B20&productionType.values=B15&productionType.values=B16&productionType.values=B17&productionType.values=B18&productionType.values=B19&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)). 
                    """)),
                self.build_modal_info_overlay('fig_energy_carbon_intensity', 'bottom', self.textwrap.dedent("""
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
                self.build_modal_info_overlay('fig_energy_percentage', 'bottom', self.textwrap.dedent("""
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
                self.build_modal_info_overlay('fig_energy_composition', 'bottom', self.textwrap.dedent("""
                    Chart showing the __**composition of the generated electric energy**__. Renewable energy components are shown in green and non renewable in brown or grey.
                    """)),

                self.html.Div(
                    className="Area_0",
                    children=[
                        self.html.H1(
                            "Renewable Energy Forecast",
                        ),
                    ]
                ),
                self.html.Div(
                    className="Area_1",
                    children=[
                        self.html.Div(
                            className="Area_1_l",
                            children=[
                                self.html.Div(
                                    className='Area_1_l_top',
                                    children=[
                                        self.html.H4(
                                            'Select your Region',
                                        ),
                                        self.dcc.Dropdown(
                                            className='dropdown_region',
                                            id='Dropdown',
                                            options=[
                                                {'label': 'Germany', 'value': 'DE'},
                                                {'label': '50hertz', 'value': 'DE-50HZ'},
                                                {'label': 'TENNET', 'value': 'DE-TENNET'},
                                                {'label': 'amprion', 'value': 'DE-AMPRION'},
                                                {'label': 'EnBw', 'value': 'DE-TRANSNET'}
                                            ],
                                            value='DE',
                                            placeholder='Select your Region...',
                                        ),
                                        self.html.Img(
                                            className='select-region-image',
                                            src=self.app.get_asset_url('regelzonen.png'),  # os.path.abspath('.png'),
                                            alt='regelzonen_image',
                                        )
                                    ]
                                ),

                            ]
                        ),
                        self.html.Div(
                            className="Area_1_r",
                            id='fig_energy_produced-div',
                            children=[
                                self.html.Div(
                                    className='container_title',
                                    children=[
                                        self.html.H4(
                                            [
                                                "produced energy",
                                                self.html.Img(
                                                    id='show-fig_energy_produced-modal',
                                                    src="assets/question-circle-solid.svg",
                                                    n_clicks=0,
                                                    className='info-icon',
                                                    # style = dict(width='25px',height='25x')
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                self.dcc.Graph(
                                    className='fig_energy_produced',
                                    id='fig_energy_produced',
                                    figure=self.figures['energy_produced'],  # should be fig_energy_carbon_intensity
                                )
                            ]
                        ),
                    ]
                ),
                self.html.Div(
                    className="Area_2",
                    children=[
                        self.html.Div(
                            className="Area_2_l",
                            id='fig_energy_carbon_intensity-div',
                            children=[
                                self.html.Div(
                                    className='container_title',
                                    children=[
                                        self.html.H4(
                                            [
                                                "energy carbon intensity",
                                                self.html.Img(
                                                    id='show-fig_energy_carbon_intensity-modal',
                                                    src="assets/question-circle-solid.svg",
                                                    n_clicks=0,
                                                    className='info-icon',
                                                    # style = dict(width='25px',height='25x')
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                self.dcc.Graph(
                                    className='fig_energy_carbon_intensity',
                                    id='fig_energy_carbon_intensity',
                                    figure=self.figures['energy_carbon_intensity']
                                    # should be fig_energy_carbon_intensity
                                )

                            ]
                        ),
                        self.html.Div(
                            className="Area_2_r",
                            id='fig_energy_percentage-div',
                            children=[
                                self.html.Div(
                                    className='container_title',
                                    children=[
                                        self.html.H4(
                                            [
                                                "percentage of renewable energy",
                                                self.html.Img(
                                                    id='show-fig_energy_percentage-modal',
                                                    src="assets/question-circle-solid.svg",
                                                    n_clicks=0,
                                                    className='info-icon',
                                                    # style = dict(width='25px',height='25x')
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                self.dcc.Graph(
                                    className='fig_energy_percentage',
                                    id='fig_energy_percentage',
                                    figure=self.figures['energy_percentage'],
                                ),

                            ],
                        )
                    ]
                ),
                self.html.Div(
                    className="Area_3",
                    id='fig_energy_composition-div',
                    children=[
                        self.html.Div(
                            className='Area_3_l',
                            children=[
                                self.dcc.RangeSlider(
                                    className='range_slider',
                                    id='range-slider',
                                    vertical=True,
                                    allowCross=False,
                                    count=1,  # number of ranges to handle
                                    min=0,
                                    max=24,
                                    value=[0, 24],
                                    marks={
                                        0: {'label': '00:00',
                                            'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        1: {'label': '01:00',
                                            'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        2: {'label': '02:00',
                                            'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        3: {'label': '03:00',
                                            'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        4: {'label': '04:00',
                                            'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        5: {'label': '05:00',
                                            'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        6: {'label': '06:00',
                                            'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        7: {'label': '07:00',
                                            'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        8: {'label': '08:00',
                                            'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        9: {'label': '09:00',
                                            'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        10: {'label': '10:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        11: {'label': '11:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        12: {'label': '12:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        13: {'label': '13:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        14: {'label': '14:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        15: {'label': '15:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        16: {'label': '16:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        17: {'label': '17:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        18: {'label': '18:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        19: {'label': '19:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        20: {'label': '20:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        21: {'label': '21:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        22: {'label': '22:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        23: {'label': '23:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}},
                                        24: {'label': '24:00',
                                             'style': {'fontFamily': 'Courier New, monospace', 'fontSize': 14}}
                                    },
                                )
                            ]
                        ),
                        self.html.Div(
                            className='Area_3_r',
                            children=[
                                self.html.Div(
                                    className='container_title',
                                    children=[
                                        self.html.H4(
                                            [
                                                "energy composition",
                                                self.html.Img(
                                                    id='show-fig_energy_composition-modal',
                                                    src="assets/question-circle-solid.svg",
                                                    n_clicks=0,
                                                    className='info-icon',
                                                    # style = dict(width='25px',height='25x')
                                                ),
                                            ]
                                        ),
                                        self.dcc.Graph(
                                            className='fig_energy_composition',
                                            id='fig_energy_composition',
                                            figure=self.figures['energy_composition'],
                                        )
                                    ]
                                ),
                            ]
                        )
                    ],
                )
            ]
        )
        return layout

    # figure #1: energy intensity
    def go_figure(self):
        fig = self.go.Figure()
        fig.update_layout(
            paper_bgcolor=colors_figures['paper_bgcolor'],
            plot_bgcolor=colors_figures['paper_bgcolor'],
            font=dict(
                family=colors_figures['font_type'],
                size=colors_figures['font_size'],
            ),
            xaxis=dict(
                tickformat="%H:00",
                showgrid=True,
            ),
            yaxis=dict(
                title='[gC02/kWh]',
                showticklabels=False,
                tickformat='%.1f',
                showgrid=False
            ),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.7,
            ),
        )
        return fig

    def fig_energy_composition(self, df):
        # Declaration:
        #     pie figure of energy composition
        #     INPUT:
        #     requested input: region
        #     possible input: data_type and model
        #     OUTPUT:
        #     figure 
        # input_value = [0,1]
        # df = df.loc[df.index[input_value[0]]:df.index[input_value[1]]]
        df_summ = df.sum()
        fig = self.px.pie(
            df,
            values=df_summ,
            names=df_summ.index,
            color=df_summ.index,
            color_discrete_map={'Fossil Gas': 'brown',
                                'Fossil Brown coal/Lignite': 'brown',
                                'Nuclear': 'brown',
                                'Solar': 'green',
                                'Fossil Hard coal': 'brown',
                                'Wind Onshore': 'green',
                                'Biomass': 'green',
                                'Other': 'grey',
                                'Hydro Run-of-river and poundage': 'green',
                                'Hydro Pumped Storage': 'green',
                                'Other renewable': 'green',
                                'Waste': 'grey',
                                'Geothermal': 'green',
                                'Fossil Oil': 'brown',
                                'Wind Offshore': 'green',
                                'Hydro Water Reservoir': 'green'
                                }
        )
        fig.update_layout(
            # margin=dict(l=10, r=50, t=100, b=20),
            paper_bgcolor=colors_figures['paper_bgcolor'],
            plot_bgcolor=colors_figures['paper_bgcolor'],
        )
        return fig
