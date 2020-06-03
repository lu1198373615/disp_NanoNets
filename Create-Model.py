import requests

url = "https://app.nanonets.com/api/v2/ObjectDetection/Model/"

payload = "{\"categories\" : [\"pedestrian\"]}"
headers = {
    'Content-Type': "application/json",
}

# 六月2日
# da122b32-200e-4fa0-85f8-3b8db986529c  "accuracy":48.56435//1000ci
# 2fc403f5-1d95-46f6-bbf7-f4174c6d9ce2  "accuracy":47.084373//1000ci
# 4537923c-c811-446d-85b0-5885ef01e11a  "accuracy":43.182243
# 29d3040d-14bf-4574-bdf7-e140c6e7aa62  "accuracy":47.44199//1000ci
# 48a013aa-3489-4813-8909-a5aecf57421d  "accuracy":43.412098

# da07a71e-3972-4d03-a056-acbb22494105  "accuracy":42.674248
# 74de4f54-a7e7-4558-838f-1fbb4e9a43d1  "accuracy":45.359264//接近1000
# 68c0df22-1f67-40f1-bbe4-f3e79211e859  "accuracy":44.683067
# 14fcd528-00fc-4a4b-81be-b50c7afee216  "accuracy":44.914616
response = requests.request("POST", url, headers=headers, auth=requests.auth.HTTPBasicAuth('I4UQOdAXBenkRM2lJfMr1waLz7KXxits', ''), data=payload)

print(response.text)
