from modules.submodules.DateTimeHandler import DateTimeHandler

class FileHandler(DateTimeHandler):
    def __init__(self,os,datetime,pytz):
        self.os = os
        self.datetime = datetime
        self.pytz = pytz
        print("FileHandler initiated")

    
    # def update_metadata(self,metada = {}):
    # # complete set of metadata required for a data call
    # # possible entries : 
    # #   - start,end = pd.Timestamp
    # #   - region =  'DE-TENNET' 'DE-AMPRION'  'DE-50HZ' 'DE-TRANSNET' 'DE'
    # #   - data_type = 'forecast' / 'historical'
    # #   - forecast_type = 'statistical' 'entsoe' 'deep_learning'
    #     for key,value in metada.items():
    #         if (key == 'start'):
    #             self.set_start(value)
    #             print(self.get_start())
    #         elif (key == 'end'):
    #             self.set_end(value)
    #             print(self.get_start())
    #         elif (key == 'region'):
    #             self.set_region(value)
    #         elif (key == 'data_type'):
    #             self.set_data_type(value)    
    #         elif (key == 'forecast_type'):
    #             self.set_forecast_type(value)    
    #     self.set_FilePath()


    # def set_start(self,start):
    #     self.start = start    

    # def get_start(self):
    #     return self.start

    # def set_end(self,end):
    #     self.end = end    

    # def get_end(self):
    #     return self.end
    
    # def set_region(self,region):
    #     self.region = region    

    # def get_region(self):
    #     return self.region

    # def set_data_type(self,data_type):
    #     self.data_type = data_type    

    # def get_data_type(self):
    #     return self.data_type
    
    # def set_forecast_type(self,forecast):
    #     self.forecast_type = forecast    

    # def get_forecast_type(self):
    #     return self.forecast_type

    # def get_FilePath(self):
    #     return self.FilePath

    def get_FilePath(self,metadata):
        # Declaration:
        # this function is used as a data handler for the storgae system. 
        # It will ask for the data and if it is not existing pull it.

        # file structuring: 
        #                    regions(5 possibilities)      #region
        #                  /                \
        #               forecast            historical     #data_type
        #           /     |        \
        #  statistical   entsoe deep_learning              #forecast_type

        FilePath    = metadata['start'].strftime('%Y-%d-%m') +metadata['region']+ '.csv'
        directory   = self.os.path.abspath("rsc")
        try:
            self.os.stat(directory)
        except:
            self.os.mkdir(directory)       
        directory = self.os.path.join(directory,metadata['region'])
        try:
            self.os.stat(directory)
        except:
            self.os.mkdir(directory)
        directory = self.os.path.join(directory,metadata['data_type'])
        try:
            self.os.stat(directory)
        except:
            self.os.mkdir(directory)
        if metadata['data_type'] == "forecast":
            directory = self.os.path.join(directory,metadata['forecast_type'])
            try:
                self.os.stat(directory)
            except: 
                self.os.mkdir(directory)
        FilePath = self.os.path.join(directory,FilePath)
        FilePath = self.os.path.abspath(FilePath)
        return FilePath

    def test_file_exists(self,FilePath):
        '''
        Declaration : 

        Tests if file under current FilePath exists
        
        '''
        if (self.os.path.exists(FilePath)):
            return True
        else:
            return False