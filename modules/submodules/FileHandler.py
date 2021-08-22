from modules.submodules.DateTimeHandler import DateTimeHandler

class FileHandler(DateTimeHandler):
    def __init__(self,os,datetime,pytz):
        self.os = os
        self.datetime = datetime
        self.pytz = pytz
        print("FileHandler initiated")

    

    def get_FilePath(self,metadata):
        # Declaration:
        # this function is used as a data handler for the storgae system. 
        # It will ask for the data and if it is not existing pull it.

        # file structuring: 
        #                    regions(5 possibilities)           #region
        #                  /                \           \
        #               forecast            historical   live   #data_type
        #           /     |        \
        #  statistical   entsoe deep_learning                   #forecast_type

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
            #print('I am here, with dtype = '+metadata['data_type'] +' and Directory = '+directory)
            directory = self.os.path.join(directory,metadata['forecast_type'])
            try:
                self.os.stat(directory)
                #print(directory)
            except: 
                self.os.mkdir(directory)
                #print(directory)
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