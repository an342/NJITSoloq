import sys
import os
import codecs
import threading
import urllib3
import certifi
import json
conn=urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(),timeout=2.0)
r=conn.request('GET',"https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/vayler?api_key=RGAPI-78b4cb9f-d610-40b3-9525-26ca52c3f64e")
d=json.loads(r.data.decode('utf-8'))
for i in d:
    print(i)