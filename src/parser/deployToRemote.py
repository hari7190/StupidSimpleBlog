# author: Hari MS
#
# 

import json, urllib.request

with open('../../config.json') as data_file:
    data = json.load(data_file)

jobURL = data["deploy"]["jobURL"]



#Deploy
urllib.request.urlopen(jobURL).read()