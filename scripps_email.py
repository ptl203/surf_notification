import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import noaa_coops as nc
from bouy_class import Bouy
import numpy as np

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
waveheight_text = ('Wave Height is ' + str(waveheight) + " FT")
wavedirection = scripps_trough.data['MWD'][0]
wavedirection_text = ('Wave Direction is ' + str(wavedirection) + " DEG")
period = scripps_pier.data['DPD'][0]
waveperiod_text = ('Wave Period is ' + str(period) + " SEC")
windspeed = scripps_pier.data['WSPD'][0]
windspeed_text = ('Wind Speed is ' + str(windspeed) + " MPH")
winddirection = scripps_pier.data['WDIR'][0]
winddirection_text = ('Wind Direction is ' + str(winddirection) + " DEG")
watertemp = scripps_trough.data['WTMP'][0]
watertemp_text = ('Water Temperature is ' + str(watertemp) + " DEG F")

import smtplib

gmail_user = 'californiaburritowsc@gmail.com'
gmail_password = 'Bllom10!'

sent_from = gmail_user
to = ['californiaburritowsc@gmail.com']
subject = str(date.today()) + " SCRIPPs Current Conditions"
body = waveheight_text + "\n" + wavedirection_text + "\n" + waveperiod_text + "\n" + windspeed_text + "\n" + winddirection_text + "\n" + watertemp_text

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(sent_from, to, email_text)
    smtp_server.close()
    print ("Email sent successfully!")
except Exception as ex:
    print ("Something went wrong….",ex)