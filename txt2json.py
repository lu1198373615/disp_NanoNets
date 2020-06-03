import os
annotations_path = r'H:\homework_data\annotations'
json_path = r'H:\homework_data\jsons'
width, height = 640, 480
if not os.path.exists(json_path):
    os.mkdir(json_path)
txtlist = os.listdir(annotations_path)
with open('douhao','r') as f:
    danyinhao = f.readline()[0]
    shuangyinhao = f.readline()[0]
    print(danyinhao)
    print(shuangyinhao)
for txtFile in txtlist:
    if int(txtFile[3:5])>5:
        continue
    rect_list = []
    with open(os.path.join(annotations_path, txtFile),'r') as f:
        line = f.readline()
        line = f.readline()
        while line:
            content_list = line.split(' ')
            rect_dict = {}
            rect_dict["xmin"] = int(content_list[1])
            rect_dict["ymin"] = int(content_list[2])
            rect_dict["xmax"] = int(content_list[1])+int(content_list[3])
            rect_dict["ymax"] = int(content_list[2])+int(content_list[4])
            object_dict = {}
            object_dict["name"] = "pedestrian"
            object_dict["bndbox"] = rect_dict
            rect_list.append(object_dict)
            line = f.readline()
    with open(os.path.join(json_path, txtFile.replace('txt','json')), 'w') as f:
        f.write(str(rect_list).replace(danyinhao,shuangyinhao))
