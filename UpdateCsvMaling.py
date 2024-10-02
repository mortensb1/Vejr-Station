import requests
import csv
import os

token = os.environ.get("API_SECRECT")

# Request the data
response = requests.get(f"https://api.weather.com/v2/pws/observations/all/1day?stationId=IRISSK13&format=json&units=m&apiKey={token}")

# Read the response as json data
dataJson = response.json()

currentReads = []
with open('maalinger.csv', mode='r', newline='') as csvFile:
    csvRead = csv.DictReader(csvFile)
    for lines in csvRead:
        currentReads.append(lines["obsTimeLocal"])

# Write to csv
with open('maalinger.csv', mode='a', newline='') as csvFile:
    # Define the colonnes
    fieldnames = ["stationID", "tz", "obsTimeUtc", "obsTimeLocal", "epoch", "lat", "lon", "solarRadiationHigh", "uvHigh", "winddirAvg", "humidityHigh", "humidityLow", "humidityAvg", "qcStatus", "tempHigh", "tempLow", "tempAvg", "windspeedHigh", "windspeedLow", "windspeedAvg", "windgustHigh", "windgustLow", "windgustAvg", "dewptHigh", "dewptLow", "dewptAvg", "windchillHigh", "windchillLow", "windchillAvg", "heatindexHigh", "heatindexLow", "heatindexAvg", "pressureMax", "pressureMin", "pressureTrend", "precipRate", "precipTotal"]
    csvWrite = csv.DictWriter(csvFile, fieldnames=fieldnames)

    # Add the data
    data = dataJson['observations']
    for malinger in data:
        if malinger["obsTimeLocal"] in currentReads:
            continue
        
        # Save the metric data
        metric = malinger["metric"]

        # Remove the metric data from the from the målinger as it is a dict in the dict
        del malinger["metric"]
        # Add the metric data again but as singulair colonnes
        malinger.update(metric)
        csvWrite.writerow(malinger)