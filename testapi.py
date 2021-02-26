import requests
import json
import time
import uuid

with open('testcsv.json') as json_file: # reads a json file containing requests
    data = json.load(json_file)
    for p in data:
        p.update({'id': str(uuid.uuid4())}) # creates a uuid and appends it to json
        print(p['id'])
        response = requests.post("http://127.0.0.1:5000/predict", json=p) # sends request to flaskapi
        print(json.loads(response.content))
        time.sleep(1)
