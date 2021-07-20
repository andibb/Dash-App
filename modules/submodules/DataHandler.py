from modules.submodules.FileHandler import FileHandler
from modules.submodules.CalcEngine import CalcEngine
class DataHandler(FileHandler):

    def __init__(self,pd,relativedelta,os,pytz,datetime,API_KEY,EntsoePandasClient):
        self.datetime = datetime
        self.pytz = pytz
        self.os = os
        self.pd = pd
        self.relativedelta = relativedelta
        self.API_KEY = API_KEY
        self.CalcEngine = CalcEngine(pd,relativedelta)
        self.entsoe = EntsoePandasClient(api_key = self.API_KEY)

        print("DataHandler initiated")

    def get_data(self,metadata):
        '''
        Input-strukture : 
        metadata = {
            'region' : 'DE-50HZ',
            'start' : start,
            'end'    : end,
            'data_type' : 'historical',
        }
        
        '''
        FilePath = self.get_FilePath(metadata)
        if (self.test_file_exists(FilePath)):
            print('read file from db : '+ FilePath)
            df = self.pd.read_csv(FilePath,index_col=0)
            df.index = df.index.map(lambda x: self.pd.Timestamp(x,tz='Europe/Berlin',freq='H'))
            return df
        else:
            print('no data @db -> generate new data')
            return self.set_data(metadata)

    def set_data(self,metadata):
        '''
        This function is to load/create data. In case the upper class : FileHandler has found a non existing file it will call 
        datahandler to load/create the file.
        
        It does not check if there is allready data existing. It will directly load it.
        '''
        #print('write to db file:',FilePath)
        FilePath = self.get_FilePath(metadata)

        if metadata["data_type"] == 'live':
            if metadata['region'] =='DE':   
                df = self.entsoe.query_generation(start=metadata['start'],end=metadata['end']+self.relativedelta(hours=1),country_code=metadata['region'])
                df = df.resample('1H').mean()
            else:
                df = self.entsoe.query_generation(start=start,end=metadata['end']+self.relativedelta(hours=1),country_code=metadata['region'],lookup_bzones=True)
                df = df.resample('1H').mean()
            df.to_csv(FilePath)

        if metadata["data_type"] == "forecast":
            '''
            #Data : 
            forecast := all "created" forecasts

            timegrid :  for a whole day, (00 - 23) based on hours.

            data per timeslot : MW, all energy-parts together! 

            '''
            if metadata["forecast_type"] == "statistical":
                print('call calc engine for statistical forecast')
                df = self.get_statistical_forecast(metadata)
                df.to_csv(FilePath)
                return df

            if metadata["forecast_type"] == "deep_learning":
                df=self.calc_deep_learning()
                df.to_csv(FilePath)
                return df

            if metadata["forecast_type"] == "entsoe":
                df = self.entsoe.query_generation_forecast(metadata['region'],start=metadata['start'],end=metadata['end'])
                df.to_csv(FilePath,header="0")
                #df['0']=df
                return df

            if metadata["forecast_type"] == 'entsoe_wind_and_solar':
                if (metadata["region"]== 'DE'):
                    df = self.entsoe.query_wind_and_solar_forecast(metadata['region'],start=metadata['start'],end=metadata['end'])
                    df.to_csv(FilePath)
                    #df['0']=df
                else:
                    df = self.entsoe.query_wind_and_solar_forecast(metadata['region'],start=metadata['start'],end=metadata['end'],lookup_bzones = True)
                    df.to_csv(FilePath)
                    #df['0']=df
                return df
                
        if metadata["data_type"] == "historical":
            '''
            #Data : 
            historical := past days

            timegrid :  for a whole day, (00 - 23) based on hours.

            data per timeslot : MW, all energy-parts! (10 entries)
            '''
            if metadata["region"] =='DE':
                df = self.entsoe.query_generation(start=metadata['start'],end=metadata['end']+self.relativedelta(hours=1),country_code=metadata['region'])
                df = df.resample('1H').mean()
                df.to_csv(FilePath)
            else:
                df = self.entsoe.query_generation(start=metadata['start'],end=metadata['end']+self.relativedelta(hours=1),country_code=metadata['region'],lookup_bzones=True)
                df = df.resample('1H').mean()
                df.to_csv(FilePath)        
            return df

    def get_data_container(
        self,
        metadata_grp_call):

        # this function performs db queries for whole data-sets.it reads out metadata_grp_call and pulls sets of data

        data_metadata_dummy = {
            'region' : '',
            'start' : '',
            'end'    : '',
            'data_type' : '',
            'forecast_type' : ''
        }

        for region in metadata_grp_call:
            data_metadata_dummy['region'] = region
            for data_type in metadata_grp_call[region]:
                data_metadata_dummy['data_type'] = data_type
                if data_type == "historical":
                    for i,timestamps in enumerate(metadata_grp_call[region][data_type]):
                        data_metadata_dummy['start'] = timestamps[0]
                        data_metadata_dummy['end'] = timestamps[1]
                        metadata_grp_call[region][data_type][i] = self.get_data(data_metadata_dummy)
                    metadata_grp_call[region][data_type] = self.pd.concat(metadata_grp_call[region][data_type])
                else:
                    for forecast_type in metadata_grp_call[region][data_type]:
                        data_metadata_dummy['start'] = metadata_grp_call[region][data_type][forecast_type][0]
                        data_metadata_dummy['end'] = metadata_grp_call[region][data_type][forecast_type][1]
                        data_metadata_dummy['forecast_type'] = forecast_type
                        metadata_grp_call[region][data_type][forecast_type] = self.get_data(data_metadata_dummy)
        return metadata_grp_call

# calls to calc Engine


    def get_statistical_forecast(self,metadata):
        # this function pulls the data and passes it to the CalcEngine. CalcEngine calculates the forecast and returns it
        dates = [[metadata['start']-self.relativedelta(weeks = i),metadata['end'] - self.relativedelta(weeks = i)] for i in range(4)]

        metadata_grp_call = {
            metadata['region'] :{
                "historical" : dates,
                "forecast" : {
                    'entsoe_wind_and_solar' : [metadata['start'],metadata['end']]
                }
            }
        }
        
        df = self.CalcEngine.calc_statistical(self.get_data_container(metadata_grp_call))
        return df

    def get_percentage(self,metadata):
        return self.CalcEngine.calc_percentage(self.get_data(metadata))

    def get_gC02(self,metadata):
        return self.CalcEngine.calc_gC02(self.get_data(metadata))