import requests
import json
import urllib3

# ssl issue
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

def retrieveWeatherElement(weatherElementSets, key):
    for weatherElement in weatherElementSets:
        if weatherElement['elementName'] == key:
            value = weatherElement['elementValue']
            return value
        else:
            value=key+" not found"
    return value
   
def retrieveParameter(parameterSets, key):
    for parameter in parameterSets:
        if parameter['parameterName'] == key:
            value = parameter['parameterValue']
            return value
        else:
            value=key+" not found"
    return value
 

rainStDatasetAPI = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0002-001?Authorization=rdec-key-123-45678-011121314"
rainStFile = "rainSt.json"

rainStDownload = requests.get(rainStDatasetAPI, verify=False)

rainStData = {}

open(rainStFile, 'wb').write(rainStDownload.content)

with open(rainStFile, 'rb') as f:
    file_content = f.read()
    #print(file_content)
    rainStData = json.loads(file_content)

#print(json.dumps(rainStData))
rainStRecordsLocation = rainStData['records']
for stLocation in rainStRecordsLocation['location']:
    rainSt = stLocation
    #print(rainSt)
    obsTime = rainSt['time']['obsTime']
    lat = rainSt['lat']
    lon = rainSt['lon']
    locationName = rainSt['locationName']
    stationId = rainSt['stationId']
    ELEV = retrieveWeatherElement(rainSt['weatherElement'], "ELEV")
    RAIN = retrieveWeatherElement(rainSt['weatherElement'], "RAIN")
    MIN_10 = retrieveWeatherElement(rainSt['weatherElement'], "MIN_10")
    HOUR_3 = retrieveWeatherElement(rainSt['weatherElement'], "HOUR_3")
    HOUR_6 = retrieveWeatherElement(rainSt['weatherElement'], "HOUR_6")
    HOUR_12 = retrieveWeatherElement(rainSt['weatherElement'], "HOUR_12")
    HOUR_24 = retrieveWeatherElement(rainSt['weatherElement'], "HOUR_24")
    NOW = retrieveWeatherElement(rainSt['weatherElement'], "NOW")
    latest_2days = retrieveWeatherElement(rainSt['weatherElement'], "latest_2days")
    latest_3days = retrieveWeatherElement(rainSt['weatherElement'], "latest_3days")
    CITY = retrieveParameter(rainSt['parameter'], "CITY")
    CITY_SN = retrieveParameter(rainSt['parameter'], "CITY_SN")
    TOWN = retrieveParameter(rainSt['parameter'], "TOWN")
    TOWN_SN = retrieveParameter(rainSt['parameter'], "TOWN_SN")

    print(obsTime, lat, lon, locationName, stationId, ELEV, RAIN, MIN_10, HOUR_3, HOUR_6, HOUR_12, HOUR_24, NOW, latest_2days, latest_3days, CITY, CITY_SN, TOWN, TOWN_SN)
