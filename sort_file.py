import os


images_path = 'H:\data2\images_training'
jsons_path = 'H:\data2\jsons'
files = sorted(os.listdir(images_path))
cnt = 0
for file in files:
    oldname = os.path.join(images_path, file)
    newname = os.path.join(images_path, str(cnt)+'.jpg')
    os.rename(oldname,newname)
    oldname = os.path.join(jsons_path, str(file).replace('.jpg','.json'))
    newname = os.path.join(jsons_path, str(cnt) + '.json')
    os.rename(oldname, newname)
    cnt += 1
