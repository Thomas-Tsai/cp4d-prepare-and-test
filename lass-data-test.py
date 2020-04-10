import gzip
import requests
import json

#lassDatasetAPI = "https://lass.nchc.org.tw/data/last-all-lass.json.gz"
#lassDatasetAPI = "https://lass.nchc.org.tw/data/last-all-airbox.json.gz"
lassDatasetAPI = ""

lassFile = "last-all-lass.json.gz"

lassDownload = requests.get(lassDatasetAPI, verify=False)

lassData = {}

open(lassFile, 'wb').write(lassDownload.content)

with gzip.open(lassFile, 'rb') as f:
    file_content = f.read()
    #print(file_content)
    lassData = json.loads(file_content)

print(json.dumps(lassData))
