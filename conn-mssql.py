import pymssql

server = '203.145.220.250'
#database = 'WebCrawlerData'
database = 'test2'
username = ''
password = ''

# pymssql
conn = pymssql.connect(server, username, password, database)
cursor = conn.cursor(as_dict=True)

cursor.execute("SELECT * from dbo.Table_1;")
for row in cursor:
    print("%s, %s, %s" % (row['tblc1'], row['tblc2'], row['tblc3']))

# dbo.air_data_cache, source, 
# source,gps_num,app,s_d1,fmt_opt,s_d2,s_d0,gps_alt,s_h0,SiteName,gps_fix,ver_app,gps_lat,s_t0,timestamp,gps_lon,date,tick,device_id,s_1,20,s_0,21,s_3,22,s_2,23,ver_format,time
cursor.executemany(

  "INSERT INTO dbo.air_data_cache VALUES (%s, %f, %s, %f, %s, %f, %f, %f, %f, %s, %f, %s, %f, %f, %s, %f, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
  [('1', 'John Smith', 'John Doe'),
   ('3', 'Mike T.', 'Sarah H.')])
conn.commit()

cursor.execute("SELECT * from dbo.Table_1;")
for row in cursor:
    print("%s, %s, %s" % (row['tblc1'], row['tblc2'], row['tblc3']))


