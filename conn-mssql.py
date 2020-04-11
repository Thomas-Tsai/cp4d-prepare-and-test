import pyodbc
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = '203.145.220.250'
database = 'WebCrawlerData'
username = ''
password = ''
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
#conn = pyodbc.connect('DRIVER={FreeTDS};SERVER=203.145.220.250;PORT=1433;DATABASE=WebCrawlerData;UID=thomas;PWD=okok7480;TDS_VERSION=7.2')
cursor = cnxn.cursor()

cursor.execute("SELECT @@version;")
row = cursor.fetchone()
while row:
    print(row[0])
    row = cursor.fetchone()
