class DateTimeHandler:
    def __init__(self, datetime, pytz, relativedelta, pd):
        self.datetime = datetime
        self.pytz = pytz
        self.relativedelta = relativedelta
        self.pd = pd
        print('DateTimeHandler initiated')

    def get_day_times(self):
        '''
        Declaration: 
        getting datetimes of today for EntsoeClient call
        
        Input: 
        datetime.object
        Output:
        pd.Timestamp,pd.Timestamp
        '''
        germany_tz = self.pytz.timezone("Europe/Berlin")
        start_time = self.datetime.datetime.combine(self.datetime.datetime.now(), self.datetime.datetime.min.time())
        end_time = start_time + self.datetime.timedelta(days=1) - self.datetime.timedelta(
            microseconds=1)
        start_time = germany_tz.localize(start_time)
        end_time = germany_tz.localize(end_time)
        start_time = self.pd.Timestamp(start_time)
        end_time = self.pd.Timestamp(end_time)
        return start_time, end_time

    def get_live_daytimes(self):
        '''
        Declaration: 
        getting datetimes for live EntsoeClient call
        
        Input: 
        datetime.object
        Output:
        pd.Timestamp,pd.Timestamp
        00:00 - (now - 2std.)
        '''
        date = self.datetime.datetime.now()
        germany_tz = self.pytz.timezone("Europe/Berlin")
        start_time = self.datetime.datetime.combine(date, self.datetime.datetime.min.time())
        end_time = start_time + self.relativedelta(hours=date.hour)
        start_time = germany_tz.localize(start_time)
        end_time = germany_tz.localize(end_time)
        start_time = self.pd.Timestamp(start_time)
        end_time = self.pd.Timestamp(end_time)
        
        return start_time,end_time
    
        