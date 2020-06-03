import requests

model_list = ['14fcd528-00fc-4a4b-81be-b50c7afee216']
for ID in model_list:
    url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/%s/Train/' %ID
    response = requests.request('POST', url, auth=requests.auth.HTTPBasicAuth('I4UQOdAXBenkRM2lJfMr1waLz7KXxits', ''))

    print(response.text)



