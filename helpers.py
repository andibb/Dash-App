import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import pytz
import os
from lib.entsoe import EntsoePandasClient


file_names = {
    "2015-2017" : 'Realisierte_Erzeugung_201501010000_201612312345_1.csv',
    "2017-2019" : 'Realisierte_Erzeugung_201701010000_201812312345_1.csv',
    "2019" : 'Realisierte_Erzeugung_201901010000_201912312345_1.csv'
}

def get_filename(filename,region = '50Hertz'):
    '''
    Explanation:
    returns the complete filename of the stored data from SMARD. 
    Where filename is element of file_names and region is:
    50Hertz,Amprion,Tennet,Transnet or Germany
    -----------------------------
    Input : str,str
    -----------------------------
    Return : os.file (str)
    -----------------------------
    '''
    folder   = "DatenSMARD"
    subfolder = "Realisierte_Erzeugung_"+region
    filename = os.path.join(subfolder,filename)
    filename = os.path.join(folder,filename)
    filename = os.path.abspath(filename)
    return filename

def process_df(df):
    datum_uhrzeit = df[df.columns[0:2]]
    df = df.drop(df.columns[0:2],axis=1)
    df = df.applymap(lambda x: str(x.replace('.','')))
    df = df.applymap(lambda x: str(x.replace(',','.')))
    df = df.applymap(lambda x: str(x.replace("-","0")))
    df = df.astype(float)
    df.index = df.index.map(lambda x : pd.Timestamp(datum_uhrzeit["Datum"][x]+' '+datum_uhrzeit["Uhrzeit"][x]))
    germany_tz = pytz.timezone("Europe/Berlin") 
    df.index = df.index.map(lambda x : germany_tz.localize(x))
    #df = df.resample('1H').sum()
    return df

def floating_mean(df,date=pd.Timestamp(2020, 5, 19, 0, 0),num_aver=7):
    if num_aver <1:
        print('Number of Days to average over has to be more then one')
        return df
    else:
        start    = date - relativedelta(years=1) - relativedelta(days = round(num_aver/2+.5))
        end      = start + relativedelta(days = num_aver,hours=-1)
        df       = df.loc[start:end]
        overlapp = num_aver - len(df)//24
        #print("overlapp = %d, num_aver =%d" %(overlapp,num_aver))
        if overlapp<num_aver:
            df       = df.loc[start-relativedelta(days=overlapp):end-relativedelta(days=overlapp)]
        df       = df.groupby(df.index.hour).sum()
        df.index = df.index.map(lambda x:date + relativedelta(hours=x))
        return df

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



def get_data_frame(region = "DE-50HZ", deltaDays = 0):
    #awaylable regions : DE-50HZ, DE-AMPRION, DE-TENNET, DE-TRANSNET
    '''
        Declaration : 
        catching data from Entso-E (if no local data exists) and process
        --------
        Input: 
        str,int

        Output:
        pd.Dataframe
    '''

    start,end = get_day_times(datetime.datetime.now() - datetime.timedelta(days=deltaDays))  

    filename = start.strftime('%Y-%d-%m') +region+ '.csv'
    folder   = "DataEntsoE"
    filename = os.path.join(folder,filename)
    filename = os.path.abspath(filename)

    try: 
        df_result = pd.read_csv(filename,index_col = 0)
        df_result.index = pd.to_datetime(df_result.index)
    except FileNotFoundError:
        api_key = 'd3f5632f-b0be-4a39-a6e8-fe25ff95368c';
        object = EntsoePandasClient(api_key=api_key)
        
        if region=='DE':
            df_wind_and_solar = object.query_wind_and_solar_forecast(region,start = start, end = end)
            df_total_energie  = object.query_generation_forecast(region,start = start, end = end)
        else:
            df_wind_and_solar = object.query_wind_and_solar_forecast(region,start = start, end = end, lookup_bzones=True)
            df_total_energie  = object.query_generation_forecast(region,start = start, end = end)

        df_wind_and_solar = pd.DataFrame(df_wind_and_solar)
        df_wind_and_solar = df_wind_and_solar.groupby(df_wind_and_solar.index.hour).mean()
        df_wind_and_solar['Wind and Solar'] = df_wind_and_solar.sum(axis=1)

        df_total_energie  = pd.DataFrame(df_total_energie)
        df_total_energie = df_total_energie.groupby(df_total_energie.index.hour).mean()

        df_total_energie["Percentage Renewable"] = df_wind_and_solar["Wind and Solar"].div(df_total_energie[0],axis = 'index')*100
        df_total_energie["Percentage Renewable"] = df_total_energie["Percentage Renewable"].round(0)
        df_result = pd.merge(df_wind_and_solar,df_total_energie, how='inner', left_index=True, right_index=True)
        df_result = df_result.rename(columns={0 : 'Total Energy'})
        df_result.to_csv(filename)
    return df_result
