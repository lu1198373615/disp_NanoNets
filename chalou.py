import requests
import os
from multiprocessing.pool import ThreadPool

images_test_path = 'H:\data2\images_testing'
predicts_path = r'H:\data2\predicts'
if not os.path.exists(predicts_path):
    os.mkdir(predicts_path)
images_test = sorted(os.listdir(images_test_path))
predict_list = sorted(os.listdir(predicts_path))

lost_list = []
for file in images_test:
    file_ = file.replace('.jpg','.txt')
    if file_ in predict_list:
        continue
    else:
        lost_list.append(file)

print(len(lost_list))

url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/74de4f54-a7e7-4558-838f-1fbb4e9a43d1/LabelFile/'

def predict_process(cnt,image):
    data = {'file': open(os.path.join(images_test_path, image), 'rb')}
    response = requests.post(url, auth=requests.auth.HTTPBasicAuth('I4UQOdAXBenkRM2lJfMr1waLz7KXxits', ''), files=data)
    boxes = response.json()['result'][0]['prediction']
    with open(os.path.join(predicts_path, str(image).replace('.jpg', '.txt')), 'w') as f:
        for box in boxes:
            li = [box['xmin'], box['ymin'], box['xmax'] - box['xmin'], box['ymax'] - box['ymin'], box['score']]
            f.write(str(li) + '\n')
    print(image, 'is done!','count:',cnt)

tp = ThreadPool(20)
count = 0
for image in lost_list:
    count += 1
    if count<0:
        continue
    # if count>1000:
    #     print('这个model用了360次啦！！！')
    #     break
    tp.apply_async(predict_process, args=(count, image,))

tp.close()
tp.join()
print('over')


