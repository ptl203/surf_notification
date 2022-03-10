from datetime import date

today = date.today()
print(today +)

#Get 24 Hours and then plot
scripps_pier_24 = scripps_pier.data[:20]
print(scripps_pier_24.head())

scripps_pier_24['WVHT'].plot(figsize=(20, 20))
plt.title("Scripps Pier Wave Height")
plt.ylabel("FEET")
plt.show()

scripps_pier_24['WSPD'].plot(figsize=(20, 20))
plt.title("Scripps Pier Wind Speed")
plt.ylabel("MPH")
plt.show()

scripps_pier_24['DPD'].plot(figsize=(20, 20))
plt.title("Scripps Pier Period")
plt.ylabel("SECONDS")
plt.show()