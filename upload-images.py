import requests
import os

images_path = 'H:\homework_data\images_training'
jsons_path = 'H:\homework_data\jsons'
files = os.listdir(images_path)
count = 0
for file in files:
    count += 1
    if count>60:
        break
    with open(os.path.join(jsons_path,file.replace('.jpg','.json'))) as f:
        labels = f.read()
    url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/5bfff0de-ea41-418d-b548-d8b2c5e4d692/UploadFile/'

    data = {'file': open(os.path.join(images_path,file), 'rb'), 'data': ('', '[{"filename":"%s", "object": %s}]'%(file,labels))}

    requests.post(url, auth=requests.auth.HTTPBasicAuth('I4UQOdAXBenkRM2lJfMr1waLz7KXxits', ''), files=data)

    print(file,'count:',count)

