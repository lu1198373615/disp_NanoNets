import requests
import os
from multiprocessing.pool import ThreadPool
images_path = 'H:\data2\images_training'
jsons_path = 'H:\data2\jsons'
files = sorted(os.listdir(images_path))

uploaded_list = []
with open('上传记录.txt','r') as f:
    line = f.readline()
    while line:
        uploaded_list.append(line.strip())
        line = f.readline()

lost_list = []
for file in files:
    if file in uploaded_list:
        continue
    else:
        lost_list.append(file)

# print(lost_list)
print(len(lost_list))

# model_list = ['24b305fb-ced5-4e67-ab9d-556efa2146d2','314f839f-4e3a-4944-8fb3-cf1e160a7273','75ed5891-9236-4aa8-ad07-d0352317fd1a','8a5679fe-8a8f-45f6-94a0-9fc5329662d1','8922c011-354c-4a71-873a-970b7713ed02']
model_list = ['14fcd528-00fc-4a4b-81be-b50c7afee216']


def send_data(count,file):
    with open(os.path.join(jsons_path, file.replace('.jpg', '.json')),'r') as f:
        labels = f.read()
    for ID in model_list:
        url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/%s/UploadFile/' %(ID)
        data = {'file': open(os.path.join(images_path, file), 'rb'),
                'data': ('', '[{"filename":"%s", "object": %s}]' % (file, labels)),
                'modelId': ('', ID)}
        response = requests.post(url, auth=requests.auth.HTTPBasicAuth('I4UQOdAXBenkRM2lJfMr1waLz7KXxits', ''),
                                 files=data)
    print(file, 'status_code:', response.status_code, 'count:', count)
    with open('上传记录.txt', 'a') as ff:
        ff.write(str(file) + '\n')

count = 0
tp = ThreadPool(15)
for file in lost_list:
    count += 1
    tp.apply_async(send_data,args=(count,file,))

tp.close()
tp.join()
print('over')


