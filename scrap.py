import pandas as pd
import time
import matplotlib.pyplot as plt
import noaa_coops as nc

class Bouy:
    def __init__(self, name, bouy_id):
        print('Setting Bouy ID')
        self.id = bouy_id
        self.name = name
    def get_data(self):
        url = "https://www.ndbc.noaa.gov/data/realtime2/" + self.id + '.txt'
        self.data = pd.read_csv(url,delim_whitespace=True)
        
    def clean_data(self):
        #Delete First Row First
        self.data = self.data.drop([0])
        #Delete other bad values; This drops the whole row so could be better
        bad_values = ["MM"] 
        for (columnName, columnData) in self.data.iteritems():
            self.data = self.data[~self.data[columnName].isin(bad_values)]
        #Clean Bouy DataTypes
        self.data['#YY'] = self.data['#YY'].astype(str)
        self.data['MM'] = self.data['MM'].astype(str)
        self.data['DD'] = self.data['DD'].astype(str)
        self.data['hh'] = self.data['hh'].astype(str)
        self.data['mm'] = self.data['mm'].astype(str)
        self.data['WDIR'] = pd.to_numeric(self.data['WDIR'])
        self.data['WSPD'] = pd.to_numeric(self.data['WSPD'])
        self.data['GST'] = pd.to_numeric(self.data['GST'])
        self.data['WVHT'] = pd.to_numeric(self.data['WVHT'])
        self.data['DPD'] = pd.to_numeric(self.data['DPD'])
        self.data['APD'] = pd.to_numeric(self.data['APD'])
        self.data['MWD'] = pd.to_numeric(self.data['MWD'])
        self.data['PRES'] = pd.to_numeric(self.data['PRES'])
        self.data['ATMP'] = pd.to_numeric(self.data['ATMP'])
        self.data['WTMP'] = pd.to_numeric(self.data['WTMP'])
        self.data['DEWP'] = pd.to_numeric(self.data['DEWP'])
        self.data['VIS'] = pd.to_numeric(self.data['VIS'])
        self.data['PTDY'] = pd.to_numeric(self.data['PTDY'])
        self.data['TIDE'] = pd.to_numeric(self.data['TIDE'])
        print(self.data.head())
        #Delete Columns that don't exist
        for (columnName, columnData) in self.data.iteritems():
            if self.data[columnName][1] == "MM":
                self.data = self.data.drop(columnName, axis=1)
        #Rename Columns and convert to datetime
        self.data = self.data.rename(columns={"#YY": "year", "MM": "month", "DD": "day", "hh": "hours", "mm": "minutes",})
        self.data['datetime'] = pd.to_datetime(self.data[['year', 'month', 'day', 'hours', 'minutes']])
        datetime_temp = self.data['datetime']
        self.data.drop(labels=['datetime'], axis=1,inplace = True)
        self.data.insert(0, 'datetime', datetime_temp)
        self.data.drop(labels=['year', 'month', 'day', 'hours', 'minutes'], axis=1,inplace = True)
        self.data = self.data.set_index('datetime')
        print(self.data.head()) # Lets prove its actually there

scripps_pier = Bouy('scripps_pier', 'LJPC1') #46254 is off the scripps pier, LJPC1 is on the pier, 46258 is in the trough, 46225 is in Scripps Canyon
scripps_trough = Bouy('scripps_trough', '46254')

scripps_pier.get_data()
scripps_trough.get_data()

scripps_pier.clean_data()
scripps_trough.clean_data()

scripps_pier.data.plot(subplots=True, figsize=(20, 20))
scripps_trough.data.plot(subplots=True, figsize=(20, 20))