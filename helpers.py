#standard python library
import os

#third party packages
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import datetime
import pytz
import plotly.express as px
import plotly.graph_objects as go


# local packages
from entsoe.entsoe import EntsoePandasClient



colors_figures = {
    'text' : '#7FDBFF',   #cian = 02edd6
    'background' : '#111111', #white = FFFFFF ; black  = 111111
    'plot_bgcolor' : '#ffffff',
    'background_h1' : '#FFFFFF',
    'paper_bgcolor' : "#ffffff",
    'line_energy_production_statistical' :'#7FDBFF',
    'line_energy_production_entsoe' :'#4da6ff',
    'line_energy_production_live' :'#0073e6',
    'energy_intensity_forecast':'#7FDBFF',
    'energy_intensity_live': '#0073e6',
    'color_hoverlabel':'#0073e6',
    'font_size':15,
    'font_type':"Courier New, monospace",
    'color_percentage_renewable' : 1
    }



def get_day_times(date):
    '''
    Declaration: 
    getting datetimes for EntsoeClient call
    
    Input: 
    datetime.object
    Output:
    pd.Timestamp,pd.Timestamp
    '''
    germany_tz = pytz.timezone("Europe/Berlin")
    start_time = datetime.datetime.combine(date, datetime.datetime.min.time())
    end_time = start_time + datetime.timedelta(days=1) - datetime.timedelta(
        microseconds=1)
    start_time = germany_tz.localize(start_time)
    end_time = germany_tz.localize(end_time)
    start_time = pd.Timestamp(start_time)
    end_time = pd.Timestamp(end_time)
    return start_time, end_time   

def get_live_daytimes():
    date = datetime.datetime.now()
    germany_tz = pytz.timezone("Europe/Berlin")
    start_time = datetime.datetime.combine(date, datetime.datetime.min.time())
    end_time = start_time + relativedelta(hours=date.hour)
    start_time = germany_tz.localize(start_time)
    end_time = germany_tz.localize(end_time)
    start_time = pd.Timestamp(start_time)
    end_time = pd.Timestamp(end_time)

    return start_time,end_time


def get_filename(
    date = datetime.datetime.now(),
    region = "DE-50HZ",
    data_type = "forecast", #"historical",#live
    forecast_type = "statistical",#"deep_learning","entsoe"
                ):
    # Declaration:
    # this function is used as a data handler for the storgae system. 
    # It will ask for the data and if it is not existing pull it.

    # file structuring: 
    #                    regions(5 possibilities)
    #                  /         \
    #            forecast     statistical
    #           /        \
    #  statistical    deep_learning
    start,end   = get_day_times(date)  
    filename    = start.strftime('%Y-%d-%m') +region+ '.csv'
    directory   = os.path.abspath("rsc")
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)       
    directory = os.path.join(directory,region)
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    directory = os.path.join(directory,data_type)
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    if data_type == "forecast":
        directory = os.path.join(directory,forecast_type)
        try:
            os.stat(directory)
        except: 
            os.mkdir(directory)
    filename = os.path.join(directory,filename)
    filename = os.path.abspath(filename)
    return filename


def get_forecast(region="DE-50HZ",date= datetime.datetime.now(),model = "statistical"):

    models = ["statistical","deep_learning","entsoe"]
    
    if model in models:
        filename = get_filename(data_type="forecast",forecast_type=model,region=region,)
        #print("model is supported.")
        try:
            df_forecast = pd.read_csv(filename,index_col=0)
            df_forecast.index = df_forecast.index.map(lambda x : pd.Timestamp(x,tz='Europe/Berlin',freq='H'))
            return df_forecast
        except FileNotFoundError:
            if model == "statistical":
                df_forecast = calc_statistical(region=region,date=date)
                df_forecast.to_csv(filename)
                return df_forecast
            if model == "deep_learning":
                df_forecast = calc_deep_learning(region=region,date=date)
                df_forecast.to_csv(filename)
            if model == 'entsoe':
                df_forecast = calc_entsoe(region=region,date=date)
                df_forecast['0'] = df_forecast
                return df_forecast
            
def get_historical(region ='DE',date=datetime.datetime.now()):
    # Declaration: this function returns the total energy generation of a PAST! day.
    # The function checks the storage, if there is an existing file it loads it. If there is no existing it
    # makes the entso-E call and safes the data.
    '''
    Input: region [str] (see possibilities below); date [datetime.object]
    Return : pd.Dataframe
    '''
    # 'DE-TENNET' #'DE-AMPRION'  'DE-50HZ' 'DE-TRANSNET' 
    filename      = get_filename(date = date,data_type="historical",region=region)
    try: 
        df_generation = pd.read_csv(filename,index_col=0)
        df_generation.index = df_generation.index.map(lambda x : pd.Timestamp(x,tz='Europe/Berlin',freq='H'))
    except FileNotFoundError:
        start,end     = get_day_times(date)
        api_key = 'd3f5632f-b0be-4a39-a6e8-fe25ff95368c'
        object = EntsoePandasClient(api_key=api_key)
        if region =='DE':
            df_generation = object.query_generation(start=start,end=end+relativedelta(hours=1),country_code=region)
            df_generation = df_generation.resample('1H').mean()
            df_generation.to_csv(filename)
        else:
            df_generation = object.query_generation(start=start,end=end+relativedelta(hours=1),country_code=region,lookup_bzones=True)
            df_generation = df_generation.resample('1H').mean()
            df_generation.to_csv(filename)        
    return df_generation


#ziehe life daten des Tages
def get_live_data(region = "DE-AMPRION"):
    '''
    Declaration
    -----------------
    funktion zieht die Daten des heute erzeugten Stromes. 
    Hierbei wird zunächst auf dem lokalen Speicher gesucht. Sind keine Daten vorhanden, oder 
    ind die Daten älter als zwei Stunden, werden neue Daten von der Entsoe-Platform gezogen.
    -----------------
    Input: region
    -----------------
    output: pd.Dataframe() + to_csv
    '''
    filename = get_filename(region=region,data_type='live')
    try:
        df_live_generation = pd.read_csv(filename,index_col=0)
        df_live_generation.index = df_live_generation.index.map(lambda x: pd.Timestamp(x,tz='Europe/Berlin',freq='H'))
        germany_tz = pytz.timezone('Europe/Berlin')
        now = germany_tz.localize(datetime.datetime.now())
        if now - df_live_generation.index[-1] > pd.Timedelta(hours=2):
            start,end = get_live_daytimes()
            api_key = 'd3f5632f-b0be-4a39-a6e8-fe25ff95368c'
            object = EntsoePandasClient(api_key=api_key)
            if region =='DE':
                df_live_generation = object.query_generation(start=start,end=end+relativedelta(hours=1),country_code=region)
                df_live_generation = df_live_generation.resample('1H').mean()
            else:
                df_live_generation = object.query_generation(start=start,end=end+relativedelta(hours=1),country_code=region,lookup_bzones=True)
                df_live_generation = df_live_generation.resample('1H').mean()
            df_live_generation.to_csv(filename)
    except FileNotFoundError:
        start,end = get_live_daytimes()
        api_key = 'd3f5632f-b0be-4a39-a6e8-fe25ff95368c'
        object = EntsoePandasClient(api_key=api_key)
        if region =='DE':
            df_live_generation = object.query_generation(start=start,end=end+relativedelta(hours=1),country_code=region)
            df_live_generation = df_live_generation.resample('1H').mean()
        else:
            df_live_generation = object.query_generation(start=start,end=end+relativedelta(hours=1),country_code=region,lookup_bzones=True)
            df_live_generation = df_live_generation.resample('1H').mean()
        df_live_generation.to_csv(filename)
    return df_live_generation


# percentage renewable 
# therefore I define the following energy forms as renewable:
# Biomass,Geothermal, Hydro Pumped Storage, Hydro Run-of-river and poundage, Other renewable, Solar, Wind (Onshore + Offshore)
# 
#funktion um prozent der erneuerbaren energieträger zu errechnen
#Der Funktion werden ein pd.Dataframe und eine liste an Energieträgern übergeben
#als return erhält man den prozentualen Anteil der übergebenen Energieträger.
#input: pd.Dataframe, list
#output: pd.Dataframe
def get_data(region,data_type,model='statistical',date=datetime.datetime.now()):
    if data_type == 'live':
        return get_live_data(region)
    elif data_type == 'forecast':
        return get_forecast(region=region,model=model,date=date)

    elif data_type == 'historical':
        return get_historical(region=region,date=date)
    else:
        print('Something went wrong! data_type or model not supported.')
#funktion um gC02/kWh (intensität) des Stroms zu errechnen, hierzu brauchte ich die Daten für den jeweiligen energie-konstituente
# Quelle: https://www.wegatech.de/ratgeber/photovoltaik/grundlagen/co2-bilanz-photovoltaik/
# PV: 50, Braunkohle 1075, Steinkohle 830, Erdgas 500, Wasserkraft 23, Windkraft 18
# alle Angaben sind in gC02/KWh 


def get_percentage(region,
        data_type,
        date= datetime.datetime.now(),
        model= "statistical",
        renewable_energies= ["Biomass","Geothermal","Hydro Pumped Storage","Hydro Run-of-river and poundage","Other renewable","Solar","Wind Onshore","Wind Offshore"]
        ):
    df = get_data(region,data_type,model=model,date=date)
    try:
        df = round(df.loc[:,df.columns.intersection(renewable_energies)].sum(axis=1)/df.sum(axis=1),3)
        return df*100
    except KeyError as e:
        try :
            renewable_energies.remove(e.args[0][2:15]) 
            df = df.loc[:,lambda df: renewable_energies].sum(axis=1)//df.sum(axis=1)
            return df*100
        except ValueError:
            print("Bitte wählen Sie einen gültigen Energieträger")
            return 0


def get_summ_gC02_per_kWh(region,data_type,date=datetime.datetime.now(),model='statistical'):
	df = get_data(region,data_type,model=model,date=date)
	lookup_c02_intesities = {'Biomass':50,'Fossil Brown coal/Lignite':1075,'Fossil Gas':500,'Fossil Hard coal':830,'Fossil Oil':900,'Geothermal':0,'Hydro Water Reservoir':23,'Hydro Pumped Storage':23,'Hydro Run-of-river and poundage':23,'Nuclear':10,'Other':500,'Other renewable':100,'Solar':50,'Waste':50,'Wind Onshore':18,'Wind Offshore':18}   
	summ_gC02_per_KWh = np.zeros(len(df))
	for el in df.columns:
		summ_gC02_per_KWh += get_percentage(region,data_type,renewable_energies=[el])/100*lookup_c02_intesities[el]
	return summ_gC02_per_KWh



def calc_statistical(region = "DE-50HZ",date=datetime.datetime.now(),days_to_average_over = 7):
	start,end = get_day_times(date)
	filename = get_filename(date,region,data_type = "forecast",forecast_type = "statistical")
	# historical data for last x week days:
	df_historical = get_historical(date=datetime.datetime.now()-relativedelta(days=days_to_average_over),region=region)
	for i in range(days_to_average_over-1):
	    df_historical = pd.concat([get_historical(date=datetime.datetime.now()-relativedelta(days=7*(i+2)),region=region),df_historical])
	df_historical = df_historical.groupby(df_historical.index.hour).mean()

	# get forecast for: wind, solar and (total) generation from EntsoE
	object = EntsoePandasClient(api_key = 'd3f5632f-b0be-4a39-a6e8-fe25ff95368c')
	if region=='DE':
	    df_wind_and_solar       = object.query_wind_and_solar_forecast(region,start = start, end = end)
	    df_generation_forecast  = object.query_generation_forecast(region,start = start, end = end)
	else:
	    df_wind_and_solar       = object.query_wind_and_solar_forecast(region,start = start, end = end, lookup_bzones=True)
	    df_generation_forecast  = object.query_generation_forecast(region,start = start, end = end)

	df_wind_and_solar = pd.DataFrame(df_wind_and_solar)
	df_wind_and_solar = df_wind_and_solar.groupby(df_wind_and_solar.index.hour).mean()
	df_wind_and_solar['Wind and Solar'] = df_wind_and_solar.sum(axis=1)

	df_generation_forecast  = pd.DataFrame(df_generation_forecast)
	df_generation_forecast  = df_generation_forecast.groupby(df_generation_forecast.index.hour).mean()
	df_generation_forecast.index = df_generation_forecast.index.map(lambda x: start + relativedelta(hours = x))

	# alle gemittelten daten der letzten wochen, bis auf die Vorhersage für wind und solar
	df_forecast = df_historical
	try:
	    df_forecast["Wind Onshore"] = df_wind_and_solar["Wind Onshore"]
	    df_forecast["Wind Offshore"] = df_wind_and_solar["Wind Offshore"]
	except KeyError:
	    print("No Wind Offshore")

	df_forecast.index = df_forecast.index.map(lambda x: start + relativedelta(hours = x))
	df_forecast.to_csv(filename)
	return df_forecast

	


def calc_entsoe(region='DE',date = datetime.datetime.now()):
	start,end = get_day_times(date)
	filename  = get_filename(date,region,data_type = "forecast",forecast_type = "entsoe")
	object    = EntsoePandasClient(api_key = 'd3f5632f-b0be-4a39-a6e8-fe25ff95368c')
	df_generation_forecast = object.query_generation_forecast(country_code=region,start=start,end=end)
	df_generation_forecast.to_csv(filename,header="0")
	return df_generation_forecast


# figure #1: energy production
def fig_energy_produced(region,component='total_composition',date=datetime.datetime.now()):
    
    df_statistical_forecast     = get_forecast(region=region,model='statistical',date=date)
    df_live_generation          = get_live_data(region=region)
    df_entsoe                   = get_forecast(region=region,model='entsoe',date=date)

    
    fig    = go.Figure()
    '''title={
                                    'text': "produced energy",
                                    'y':0.9,
                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top',
                                },'''
    fig.update_layout(
        #margin=dict(l=10, r=50, t=100, b=20),
        paper_bgcolor = colors_figures['paper_bgcolor'],
        plot_bgcolor   = colors_figures['paper_bgcolor'],
        font=dict(
            family=colors_figures['font_type'],
            size=colors_figures['font_size'],
            #color="RebeccaPurple"
        ), 
        xaxis = dict(
            tickformat  = "%H:00",
            #tickvals = df.index,
            showgrid = True,
            #range = [df.index[0]-relativedelta(hours=3),df.index[-1]-relativedelta(hours=1)],
        ),
        yaxis = dict(
            title = '[MW]',
            showticklabels = False,
            tickformat = '%.1f',
            showgrid = False
            ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.7,
        ),
    )
    if component == "total_composition":
        fig.add_trace (
            go.Scatter(
                x=df_statistical_forecast.index,
                y=df_statistical_forecast.sum(axis=1),
                mode = 'lines+markers',
                name = 'statistical forecast',
                line_color = colors_figures['line_energy_production_statistical']
                ))
        fig.add_trace(
            go.Scatter(
                x = df_live_generation.index,
                y = df_live_generation.sum(axis=1),
                mode = 'lines+markers',
                name = 'live generation',
                line_color = colors_figures['line_energy_production_live']
                #marker = ''
                ))
        fig.add_trace(
            go.Scatter(
                x=df_entsoe.index,
                y=df_entsoe['0'],
                mode = 'lines+markers',
                name = 'entsoe forecast',
                line_color = colors_figures['line_energy_production_entsoe']
                ))
    else:
        fig.add_trace (
            go.Scatter(
                x=df_statistical_forecast.index,
                y=df_statistical_forecast[component],
                mode = 'lines+markers',
                name = 'statistical forecast',
                line_color = colors_figures['line_energy_production_statistical']
                ))
        fig.add_trace(
            go.Scatter(
                x = df_live_generation.index,
                y = df_live_generation[component],
                mode = 'lines+markers',
                name = 'live generation',
                line_color = colors_figures['line_energy_production_live']
                ))
    return fig



# figure #1: energy intensity
def fig_energy_intensity(region):

    df_summ_C02 = pd.DataFrame()
    df_summ_C02["statistical forecast"] = get_summ_gC02_per_kWh(region,'forecast')
    df_summ_C02["live generation"] = get_summ_gC02_per_kWh(region,'live')
    fig    = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_summ_C02.index,
            y=np.round(df_summ_C02["statistical forecast"],1),
            mode = 'lines+markers',
            name = 'statistical forecast',
            line_color = colors_figures['energy_intensity_forecast']
        )
    )


    fig.add_trace(
        go.Scatter(
            x=df_summ_C02.index,
            y=np.round(df_summ_C02["live generation"],1),
            mode = 'lines+markers',
            name = 'live generation',
            line_color = colors_figures['energy_intensity_live']
        )
    )
    fig.update_layout(
        #margin=dict(l=10, r=50, t=100, b=20),
        paper_bgcolor = colors_figures['paper_bgcolor'],
        plot_bgcolor   = colors_figures['paper_bgcolor'],
        font=dict(
            family=colors_figures['font_type'],
            size=colors_figures['font_size'],
            #color="RebeccaPurple"
        ), 
        xaxis = dict(
            tickformat  = "%H:00",
            #tickvals = df.index,
            showgrid = True,
            #range = [df.index[0]-relativedelta(hours=3),df.index[-1]-relativedelta(hours=1)],
        ),
        yaxis = dict(
            title = '[gC02/kWh]',
            showticklabels = False,
            tickformat = '%.1f',
            showgrid = False
            ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.7,
        ),
    )
    return fig

def fig_energy_percentage(region):
    df_percentage_renewable = get_percentage(region,data_type='forecast')
    fig = px.bar(
        x=df_percentage_renewable.index,
        y=np.round(df_percentage_renewable,1),
        #color = colors_figures['color_percentage_renewable'],
    
    )
    fig.update_traces(
        hovertemplate=None,
        marker_color = 'blue',
    )
    '''        title={
            'text': "percentage renewable energy",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            },'''
    fig.update_layout(
        #margin=dict(l=10, r=50, t=100, b=20),
        paper_bgcolor = colors_figures['paper_bgcolor'],
        plot_bgcolor   = colors_figures['paper_bgcolor'],
        font=dict(
            family=colors_figures['font_type'],
            size=colors_figures['font_size'],
            #color="RebeccaPurple"
        ),
        xaxis = dict(
        	title = "",
            tickformat  = "%H:00",
            #tickvals = df.index,
            showgrid = True,
            #range = [df.index[0]-relativedelta(hours=3),df.index[-1]-relativedelta(hours=1)],
        ),
        yaxis = dict(
        	title = "",
            showticklabels = True,
            #tickformat = '%d',
            showgrid = False,
            range = [0,100]
            ),
        hoverlabel=dict(
            bgcolor=colors_figures["color_hoverlabel"], 
            font_size=16, 
            #font_family="Rockwell",
        ),
        hovermode='x'
    )
    return fig


def fig_energy_composition(
    input_value = [0,1],


    region = 'DE-AMPRION',
    data_type='forecast',

    model='statistical',
    date=datetime.datetime.now()): 
    #print(input_value)
    '''Declaration:
        pie figure of energy composition
        INPUT:
        requested input: region
        possible input: data_type and model
        OUTPUT:
        figure'''
    df = get_data(region,data_type,model=model,date=date)
    df = df.loc[df.index[input_value[0]]:df.index[input_value[1]]]
    df_summ = df.sum()
    fig = px.pie(
        df,
        values = df_summ,
        names = df_summ.index,
        color = df_summ.index,
        color_discrete_map={'Fossil Gas':'brown',
                            'Fossil Brown coal/Lignite':'brown',
                            'Nuclear':'brown',
                            'Solar':'green',
                            'Fossil Hard coal' : 'brown',
                            'Wind Onshore' : 'green',
                            'Biomass' : 'green',
                            'Other' : 'grey',
                            'Hydro Run-of-river and poundage' : 'green',
                            'Hydro Pumped Storage' : 'green',
                            'Other renewable' : 'green',
                            'Waste' : 'grey',
                            'Geothermal' : 'green',
                            'Fossil Oil' : 'brown',
                            'Wind Offshore' : 'green',
                            'Hydro Water Reservoir' : 'green'
                            }
    )

    fig.update_layout(
        #margin=dict(l=10, r=50, t=100, b=20),
        paper_bgcolor = colors_figures['paper_bgcolor'],
        plot_bgcolor   = colors_figures['paper_bgcolor'],

    )
    return fig