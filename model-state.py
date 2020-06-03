import requests, os, json

model_id = '14fcd528-00fc-4a4b-81be-b50c7afee216'
api_key = 'I4UQOdAXBenkRM2lJfMr1waLz7KXxits'

url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/' + model_id

response = requests.request('GET', url, auth=requests.auth.HTTPBasicAuth(api_key, ''))
print(response.text)