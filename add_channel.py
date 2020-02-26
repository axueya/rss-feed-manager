import listparser
import requests
from flask_restful.representations import json

result = listparser.parse('feedly.opml')
url = 'http://127.0.0.1:5000/api/v1.0/channels'
for item in result['feeds']:
    print(item)
    res = requests.post(url, json.dumps(item))
    print(res.content)
