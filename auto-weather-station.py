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
 

weatherStDatasetAPI = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=rdec-key-123-45678-011121314"
weatherStFile = "autoWeatherSt.json"

weatherStDownload = requests.get(weatherStDatasetAPI, verify=False)

weatherStData = {}

open(weatherStFile, 'wb').write(weatherStDownload.content)

with open(weatherStFile, 'rb') as f:
    file_content = f.read()
    #print(file_content)
    weatherStData = json.loads(file_content)

#print(json.dumps(weatherStData))
weatherStRecordsLocation = weatherStData['records']
for stLocation in weatherStRecordsLocation['location']:
    weatherSt = stLocation
    #print(weatherSt)
    obsTime = weatherSt['time']['obsTime']
    lat = weatherSt['lat']
    lon = weatherSt['lon']
    locationName = weatherSt['locationName']
    stationId = weatherSt['stationId']
    ELEV = retrieveWeatherElement(weatherSt['weatherElement'], "ELEV")
    WDIR = retrieveWeatherElement(weatherSt['weatherElement'], "WDIR")
    WDSD = retrieveWeatherElement(weatherSt['weatherElement'], "WDSD")
    TEMP = retrieveWeatherElement(weatherSt['weatherElement'], "TEMP")
    HUMD = retrieveWeatherElement(weatherSt['weatherElement'], "HUMD")
    PRES = retrieveWeatherElement(weatherSt['weatherElement'], "PRES")
    SUN =  retrieveWeatherElement(weatherSt['weatherElement'], "SUN")
    H_24R = retrieveWeatherElement(weatherSt['weatherElement'], "H_24R")
    H_FX = retrieveWeatherElement(weatherSt['weatherElement'], "H_FX")
    H_XD = retrieveWeatherElement(weatherSt['weatherElement'], "H_XD")
    H_FXT = retrieveWeatherElement(weatherSt['weatherElement'], "H_FXT")
    D_TX = retrieveWeatherElement(weatherSt['weatherElement'], "D_TX")
    D_TXT = retrieveWeatherElement(weatherSt['weatherElement'], "D_TXT")
    D_TN = retrieveWeatherElement(weatherSt['weatherElement'], "D_TN")
    D_TNT = retrieveWeatherElement(weatherSt['weatherElement'], "D_TNT")
    CITY = retrieveParameter(weatherSt['parameter'], "CITY")
    CITY_SN = retrieveParameter(weatherSt['parameter'], "CITY_SN")
    TOWN = retrieveParameter(weatherSt['parameter'], "TOWN")
    TOWN_SN = retrieveParameter(weatherSt['parameter'], "TOWN_SN")
    print(obsTime, lat, lon, locationName, stationId, ELEV, WDIR, WDSD, TEMP, HUMD, PRES, SUN, H_24R, H_FX, H_XD, H_FXT, D_TX, D_TXT, D_TN, D_TNT, CITY, CITY_SN, TOWN, TOWN_SN)
