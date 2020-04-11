import gzip
import requests
import json

#lassDatasetAPI = "https://lass.nchc.org.tw/data/last-all-lass.json.gz"
#lassDatasetAPI = "https://lass.nchc.org.tw/data/last-all-airbox.json.gz"
lassDatasetAPI = "https://lass.nchc.org.tw/data/last-all-airbox.json.gz"
lassFile = "last-all-airbox.json.gz"

lassDownload = requests.get(lassDatasetAPI, verify=False)

lassData = {}

open(lassFile, 'wb').write(lassDownload.content)

with gzip.open(lassFile, 'rb') as f:
    file_content = f.read()
    #print(file_content)
    lassData = json.loads(file_content)

#print(json.dumps(lassData))
lassFeess = lassData['feeds']
for lass in lassFeess:
    source = lassData['source']
    gps_num = lass['gps_num']
    app = lass['app']
    s_d1 = lass['s_d1']
    #fmt_opt = lass['fmt_opt']
    s_d2 = lass['s_d2']
    s_d0 = lass['s_d0']
    gps_alt = lass['gps_alt']
    s_h0 = lass['s_h0']
    SiteName = lass['SiteName']
    gps_fix = lass['gps_fix']
    #ver_app = lass['ver_app']
    gps_lat = lass['gps_lat']
    s_t0 = lass['s_t0']
    timestamp = lass['timestamp']
    gps_lon = lass['gps_lon']
    date = lass['date']
    #tick = lass['tick']
    device_id = lass['device_id']
    #s_1 = lass['s_1']
    #s_0 = lass['s_0']
    #s_3 = lass['s_3']
    #s_2 = lass['s_2']
    #ver_format = lass['ver_format']
    time = lass['time']
    #print(source, gps_num, app, s_d1, fmt_opt, s_d2, s_d0, gps_alt, s_h0, SiteName, gps_fix, ver_app, gps_lat, s_t0, timestamp, gps_lon, date, tick, device_id, s_1, s_0, s_3, s_2, ver_format, time)
    print(source, gps_num, app, s_d1, s_d2, s_d0, gps_alt, s_h0, SiteName, gps_fix, gps_lat, s_t0, timestamp, gps_lon, date, device_id, time)
