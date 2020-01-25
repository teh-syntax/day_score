import requests
import json
r = requests.get('http://127.0.0.1:8080/api/token')
print (r)
r = requests.post('http://127.0.0.1:8080/api/token/', json = {'username':'vagrant', 'password':'temp1234'})
print (r.text)
jsonout = json.loads(r.text)
print (jsonout['access'])

headers = {'Authorization':'Bearer ' + jsonout['access']}

r = requests.get('http://127.0.0.1:8080/hello', headers=headers)
print (r)
print (r.text)