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
username = ''
password = ''
port='1433'
table = 'weather_data_02_cache'

dbengine = "mssql+pyodbc://{1}:{2}@{0}:{3}/{4}?driver=ODBC+Driver+17+for+SQL+Server".format(server, username, password, port, database)
engine = create_engine(dbengine)

Base = declarative_base()
rainStData_metadata = MetaData()
rainStData_table = Table(table, rainStData_metadata,
        Column('ID', BIGINT, Sequence('article_aid_seq', start=1, increment=1), primary_key=True ),
        Column('obsTime', DATETIME),
        Column('lat', FLOAT),
        Column('lon', FLOAT),
        Column('locationName', NVARCHAR),
        Column('stationId', NVARCHAR),
        Column('ELEV', FLOAT),
        Column('RAIN', FLOAT),
        Column('MIN_10', FLOAT),
        Column('HOUR_3', FLOAT),
        Column('HOUR_6', FLOAT),
        Column('HOUR_12', FLOAT),
        Column('HOUR_24', FLOAT),
        Column('NOW', FLOAT),
        Column('latest_2days', FLOAT),
        Column('latest_3days', FLOAT),
        Column('CITY', NVARCHAR),
        Column('CITY_SN', FLOAT),
        Column('TOWN', NVARCHAR),
        Column('TOWN_SN', FLOAT),
        Column('ATTRIBUTE', NVARCHAR)
        )

class rainStData(object):
    def __init__(self, obsTime, lat, lon, locationName, stationId, ELEV, RAIN, MIN_10, HOUR_3, HOUR_6, HOUR_12, HOUR_24, NOW, latest_2days, latest_3days, CITY, CITY_SN, TOWN, TOWN_SN, ATTRIBUTE):
        self.obsTime = obsTime
        self.lat = lat
        self.lon = lon
        self.locationName = locationName
        self.stationId = stationId
        self.ELEV = ELEV
        self.RAIN = RAIN
        self.MIN_10 = MIN_10
        self.HOUR_3 = HOUR_3
        self.HOUR_6 = HOUR_6
        self.HOUR_12 = HOUR_12
        self.HOUR_24 = HOUR_24
        self.NOW = NOW
        self.latest_2days = latest_2days
        self.latest_3days = latest_3days
        self.CITY = CITY
        self.CITY_SN = CITY_SN
        self.TOWN = TOWN
        self.TOWN_SN = TOWN_SN
        self.ATTRIBUTE = ATTRIBUTE

mapper(rainStData, rainStData_table)

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
            value = ""
    return value
   
def retrieveParameter(parameterSets, key):
    for parameter in parameterSets:
        if parameter['parameterName'] == key:
            value = parameter['parameterValue']
            return value
        else:
            value = ""
    return value
 

rainStDatasetAPI = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0002-001?Authorization=rdec-key-123-45678-011121314"
rainStFile = "rainSt.json"

rainStDownload = requests.get(rainStDatasetAPI, verify=False)

rainStRawData = {}
new_rainStData = []

open(rainStFile, 'wb').write(rainStDownload.content)

with open(rainStFile, 'rb') as f:
    file_content = f.read()
    #print(file_content)
    rainStRawData = json.loads(file_content)

#print(json.dumps(rainStData))
rainStRecordsLocation = rainStRawData['records']
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
    ATTRIBUTE = retrieveParameter(rainSt['parameter'], "ATTRIBUTE")

    print(obsTime, lat, lon, locationName, stationId, ELEV, RAIN, MIN_10, HOUR_3, HOUR_6, HOUR_12, HOUR_24, NOW, latest_2days, latest_3days, CITY, CITY_SN, TOWN, TOWN_SN, ATTRIBUTE)
    new_rainStData.append(rainStData(obsTime, lat, lon, locationName, stationId, ELEV, RAIN, MIN_10, HOUR_3, HOUR_6, HOUR_12, HOUR_24, NOW, latest_2days, latest_3days, CITY, CITY_SN, TOWN, TOWN_SN, ATTRIBUTE))

session.add_all(new_rainStData)
session.commit()

my_test = session.query(rainStData).all()
for test_one in my_test:
    print(test_one.TOWN)
