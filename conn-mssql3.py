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
username = 'lassuser1'
password = ''
port='1433'
table = 'air_data_cache'

dbengine = "mssql+pyodbc://{1}:{2}@{0}:{3}/{4}?driver=ODBC+Driver+17+for+SQL+Server".format(server, username, password, port, database)

#engine = create_engine('mssql+pyodbc://DemoUsername:DemoPassword@DESKTOP-T40QFVL/Demo?driver=SQL+Server+Native+Client+11.0')
engine = create_engine(dbengine)

#print(list(engine.execute('sp_who')))
#print(engine.table_names())

#result = engine.execute("select * from Table_1")
#for row in result:
#    print (row)
#result.close()

Base = declarative_base()
airData_metadata = MetaData()
airData_table = Table(table, airData_metadata,
        Column('ID', BIGINT, Sequence('article_aid_seq', start=1, increment=1), primary_key=True ),
        Column('source',NVARCHAR),
        Column('gps_num',FLOAT),
        Column('app', NVARCHAR),
        Column('s_d1',FLOAT),
        Column('fmt_opt',NVARCHAR),
        Column('s_d2',FLOAT),
        Column('s_d0',FLOAT),
        Column('gps_alt',FLOAT),
        Column('s_h0',FLOAT),
        Column('SiteName',NVARCHAR),
        Column('gps_fix',FLOAT),
        Column('ver_app',NVARCHAR),
        Column('gps_lat',FLOAT),
        Column('s_t0',FLOAT),
        Column('timestamp',NVARCHAR),
        Column('gps_lon',FLOAT),
        Column('date',DATE),
        Column('tick',NVARCHAR),
        Column('device_id',NVARCHAR),
        Column('s_1',NVARCHAR),
        Column('s_0',NVARCHAR),
        Column('s_3',NVARCHAR),
        Column('s_2',NVARCHAR),
        Column('ver_format',NVARCHAR),
        Column('time', TIME)
        )

class airData(object):
    def __init__(self, source, gps_num, app, s_d1, fmt_opt, s_d2, s_d0, gps_alt, s_h0, SiteName, gps_fix, ver_app, gps_lat, s_t0, timestamp, gps_lon, date, tick, device_id, s_1, s_0, s_3, s_2, ver_format, time):
        self.source = source
        self.gps_num = gps_num
        self.app = app
        self.s_d1 = s_d1
        self.fmt_opt = fmt_opt
        self.s_d2 = s_d2
        self.s_d0 = s_d0
        self.gps_alt = gps_alt
        self.s_h0 = s_h0
        self.SiteName = SiteName
        self.gps_fix = gps_fix
        self.ver_app = ver_app
        self.gps_lat = gps_lat
        self.s_t0 = s_t0
        self.timestamp = timestamp
        self.gps_lon = gps_lon
        self.date = date
        self.tick = tick
        self.device_id = device_id
        self.s_1 = s_1
        self.s_0 = s_0
        self.s_3 = s_3
        self.s_2 = s_2
        self.ver_format = ver_format
        self.time = time

mapper(airData, airData_table)

Base.metadata.create_all(engine)


Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

new_airData = airData("last-all-airbox by IIS-NRL", 9.0, "AirBox", 0.0, "", 0.0, 21.0, 2.0, 81.0, "taiwan.tciot.epa.6865912633", 1.0, "", 24.63264, 7.87, "2020-04-12T13:51:00Z", 121.81306, "2020-04-12", "", "taiwan.tciot.epa.6865912633", "", "", "", "", "", "13:51:00")
session.add_all([new_airData])
session.commit()

my_test = session.query(airData).all()
for test_one in my_test:
    print(test_one.SiteName)

