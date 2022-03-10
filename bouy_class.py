import pandas as pd
import time
import matplotlib.pyplot as plt
import noaa_coops as nc
import numpy as np

class Bouy:
    def __init__(self, name, bouy_id):
        self.id = bouy_id
        self.name = name
    def get_data(self):
        url = "https://www.ndbc.noaa.gov/data/realtime2/" + self.id + '.txt'
        self.data = pd.read_csv(url,delim_whitespace=True)
        
    def clean_data(self):
        #Delete First Row First
        self.data = self.data.drop([0])
        #Delete other bad values; This drops the whole row so could be better
        #Replace MM with NaN
        self.data = self.data.replace('MM', np.nan)
        #Delete Columns that don't exist
        self.data = self.data.dropna(axis=1, how='all')
        #Clean Bouy DataTypes
        self.data['#YY'] = self.data['#YY'].astype(str)
        self.data['MM'] = self.data['MM'].astype(str)
        self.data['DD'] = self.data['DD'].astype(str)
        self.data['hh'] = self.data['hh'].astype(str)
        self.data['mm'] = self.data['mm'].astype(str)
        for (columnName, columnData) in self.data.iteritems():
            if columnName not in ('#YY', 'MM', 'DD', 'hh', 'mm'):
                self.data[columnName] = pd.to_numeric(self.data[columnName])
        #Rename Columns and convert to datetime
        self.data = self.data.rename(columns={"#YY": "year", "MM": "month", "DD": "day", "hh": "hours", "mm": "minutes",})
        self.data['datetime'] = pd.to_datetime(self.data[['year', 'month', 'day', 'hours', 'minutes']])
        datetime_temp = self.data['datetime']
        self.data.drop(labels=['datetime'], axis=1,inplace = True)
        self.data.insert(0, 'datetime', datetime_temp)
        self.data.drop(labels=['year', 'month', 'day', 'hours', 'minutes'], axis=1,inplace = True)
        self.data = self.data.set_index('datetime')
        #set to local time
        self.data=self.data.tz_localize('UTC')
        self.data = self.data.tz_convert('America/Los_Angeles')
        #Change WSPD to MPH, WVHT to Feet, WTMP to Celcius
        if 'WVHT' in self.data.columns:
            self.data['WVHT'] = self.data['WVHT'] * 3.28084
        if 'WSPD' in self.data.columns:
            self.data['WSPD'] = self.data['WSPD'] * 2.23694
        if 'WTMP' in self.data.columns:
            self.data['WTMP'] = self.data['WTMP'] * (9/5) +32.0
