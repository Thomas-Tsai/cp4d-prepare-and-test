import requests
import json
import urllib3
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mssql import \
    BIGINT, BINARY, BIT, CHAR, DATE, DATETIME, DATETIME2, \
    DATETIMEOFFSET, DECIMAL, FLOAT, IMAGE, INTEGER, MONEY, \
    NCHAR, NTEXT, NUMERIC, NVARCHAR, REAL, SMALLDATETIME, \
    SMALLINT, SMALLMONEY, SQL_VARIANT, TEXT, TIME, \
    TIMESTAMP, TINYINT, UNIQUEIDENTIFIER, VARBINARY, VARCHAR
from sqlalchemy.schema import Sequence
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

server = '203.145.220.250'
database = 'WebCrawlerData'
#database = 'test2'
username = 'ler1'
password = ''
port='1433'
table = 'weather_data_03_cache'

dbengine = "mssql+pyodbc://{1}:{2}@{0}:{3}/{4}?driver=ODBC+Driver+17+for+SQL+Server".format(server, username, password, port, database)
engine = create_engine(dbengine)

Base = declarative_base()
weatherData_metadata = MetaData()
weatherData_table = Table(table, weatherData_metadata,
        Column('ID', BIGINT, Sequence('article_aid_seq', start=1, increment=1), primary_key=True ),
        Column('obsTime', DATETIME),
        Column('lat', FLOAT),
        Column('lon', FLOAT),
        Column('locationName', NVARCHAR),
        Column('stationId', NVARCHAR),
        Column('ELEV', FLOAT),
        Column('WDIR', FLOAT),
        Column('WDSD', FLOAT),
        Column('TEMP', FLOAT),
        Column('HUMD', FLOAT),
        Column('PRES', FLOAT),
        Column('H_FX', FLOAT),
        Column('H_XD', FLOAT),
        Column('H_FXT', FLOAT),
        Column('H_F10', FLOAT),
        Column('H_10D', FLOAT),
        Column('H_F10T', FLOAT),
        Column('H_UVI', FLOAT),
        Column('D_TX', FLOAT),
        Column('D_TXT', FLOAT),
        Column('D_TN', FLOAT),
        Column('D_TNT', FLOAT),
        Column('D_TS', FLOAT),
        Column('H_VIS', FLOAT),
        Column('H_Weather', NVARCHAR),
        Column('CITY', NVARCHAR),
        Column('CITY_SN', FLOAT),
        Column('TOWN', NVARCHAR),
        Column('TOWN_SN', FLOAT),
        Column('H_24R', FLOAT)
        )

class weatherData(object):
    def __init__(self, obsTime, lat, lon, locationName, stationId, ELEV, WDIR, WDSD, TEMP, HUMD, PRES, H_FX, H_XD, H_FXT, H_F10, H_10D, H_F10T, H_UVI, D_TX, D_TXT, D_TN, D_TNT, D_TS, H_VIS, H_Weather, CITY, CITY_SN, TOWN, TOWN_SN, H_24R):
        self.obsTime = obsTime
        self.lat = lat
        self.lon = lon
        self.locationName = locationName
        self.stationId = stationId
        self.ELEV = ELEV
        self.WDIR = WDIR
        self.WDSD = WDSD
        self.TEMP = TEMP
        self.HUMD = HUMD
        self.PRES = PRES
        self.H_FX = H_FX
        self.H_XD = H_XD
        self.H_FXT = H_FXT
        self.H_F10 = H_F10
        self.H_10D = H_10D
        self.H_F10T = H_F10T
        self.H_UVI = H_UVI
        self.D_TX = D_TX
        self.D_TXT = D_TXT
        self.D_TN = D_TN
        self.D_TNT = D_TNT
        self.D_TS = D_TS
        self.H_VIS = H_VIS
        self.H_Weather = H_Weather
        self.CITY = CITY
        self.CITY_SN = CITY_SN
        self.TOWN = TOWN
        self.TOWN_SN = TOWN_SN
        if H_24R == '':
            H_24R = float(0)
        self.H_24R = H_24R

mapper(weatherData, weatherData_table)

Base.metadata.create_all(engine)


Session = sessionmaker()
Session.configure(bind=engine)
session = Session()



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
            #value=key+" not found"
            value=""
    return value
   
def retrieveParameter(parameterSets, key):
    for parameter in parameterSets:
        if parameter['parameterName'] == key:
            value = parameter['parameterValue']
            return value
        else:
            value=""
    return value
 

weatherStDatasetAPI = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization=rdec-key-123-45678-011121314"
weatherStFile = "weatherSt.json"

weatherStDownload = requests.get(weatherStDatasetAPI, verify=False)

weatherStData = {}
new_weatherData = []

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
    H_FX = retrieveWeatherElement(weatherSt['weatherElement'], "H_FX")
    H_XD = retrieveWeatherElement(weatherSt['weatherElement'], "H_XD")
    H_FXT = retrieveWeatherElement(weatherSt['weatherElement'], "H_FXT")
    H_F10 = retrieveWeatherElement(weatherSt['weatherElement'], "H_F10")
    H_10D = retrieveWeatherElement(weatherSt['weatherElement'], "H_10D")
    H_F10T = retrieveWeatherElement(weatherSt['weatherElement'], "H_F10T")
    H_UVI = retrieveWeatherElement(weatherSt['weatherElement'], "H_UVI")
    D_TX = retrieveWeatherElement(weatherSt['weatherElement'], "D_TX")
    D_TXT = retrieveWeatherElement(weatherSt['weatherElement'], "D_TXT")
    D_TN = retrieveWeatherElement(weatherSt['weatherElement'], "D_TN")
    D_TNT = retrieveWeatherElement(weatherSt['weatherElement'], "D_TNT")
    D_TS = retrieveWeatherElement(weatherSt['weatherElement'], "D_TS")
    H_VIS = retrieveWeatherElement(weatherSt['weatherElement'], "H_VIS")
    H_Weather = retrieveWeatherElement(weatherSt['weatherElement'], "H_Weather")
    CITY = retrieveParameter(weatherSt['parameter'], "CITY")
    CITY_SN = retrieveParameter(weatherSt['parameter'], "CITY_SN")
    TOWN = retrieveParameter(weatherSt['parameter'], "TOWN")
    TOWN_SN = retrieveParameter(weatherSt['parameter'], "TOWN_SN")
    H_24R = retrieveWeatherElement(weatherSt['weatherElement'], "H_24R")

    print(obsTime, lat, lon, locationName, stationId, ELEV, WDIR, WDSD, TEMP, HUMD, PRES, H_FX, H_XD, H_FXT, H_F10, H_10D, H_F10T, H_UVI, D_TX, D_TXT, D_TN, D_TNT, D_TS, H_VIS, H_Weather, CITY, CITY_SN, TOWN, TOWN_SN, H_24R)
    new_weatherData.append(weatherData(obsTime, lat, lon, locationName, stationId, ELEV, WDIR, WDSD, TEMP, HUMD, PRES, H_FX, H_XD, H_FXT, H_F10, H_10D, H_F10T, H_UVI, D_TX, D_TXT, D_TN, D_TNT, D_TS, H_VIS, H_Weather, CITY, CITY_SN, TOWN, TOWN_SN, H_24R))

session.add_all(new_weatherData)
session.commit()

my_test = session.query(weatherData).all()
for test_one in my_test:
    print(test_one.TOWN)
