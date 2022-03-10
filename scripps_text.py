import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import noaa_coops as nc
from bouy_class import Bouy
import numpy as np
import SMS
import schedule
import time

def job():
    scripps_pier = Bouy('scripps_pier', 'LJPC1')
    scripps_trough = Bouy('scripps_trough', '46254')

    scripps_pier.get_data()
    scripps_trough.get_data()

    scripps_pier.clean_data()
    scripps_trough.clean_data()

    #print tail
    print(scripps_pier.data.head())
    print(scripps_trough.data.head())

    #Make Email
    waveheight = scripps_pier.data['WVHT'][0]
    waveheight_text = ('Wave Height is ' + "{:.2f}".format(waveheight) + " FT")
    wavedirection = scripps_trough.data['MWD'][0]
    wavedirection_text = ('Wave Direction is ' + "{:.0f}".format(wavedirection) + " DEG")
    period = scripps_pier.data['DPD'][0]
    waveperiod_text = ('Wave Period is ' + "{:.0f}".format(period) + " SEC")
    windspeed = scripps_pier.data['WSPD'][0]
    windspeed_text = ('Wind Speed is ' + "{:.0f}".format(windspeed) + " MPH")
    winddirection = scripps_pier.data['WDIR'][0]
    winddirection_text = ('Wind Direction is ' + "{:.0f}".format(winddirection) + " DEG")
    watertemp = scripps_trough.data['WTMP'][0]
    watertemp_text = ('Water Temperature is ' + "{:.1f}".format(watertemp) + " DEG F")

    body = waveheight_text + "\n" + wavedirection_text + "\n" + waveperiod_text + "\n" + windspeed_text + "\n" + winddirection_text + "\n" + watertemp_text

    SMS.send(body)

schedule.every().day.at("05:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
    "Slept"
