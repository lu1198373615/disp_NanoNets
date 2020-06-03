import os
import json

predicts_path = 'H:\data2\predicts'
res_path = r'H:\data2\res'
if not os.path.exists(res_path):
    os.mkdir(res_path)

pre_list = sorted(os.listdir(predicts_path))
for file in pre_list:
    set_name = file[0:5]
    v_name = file[5:9]
    i_name = file[10:15]
    data = ''
    with open(os.path.join(predicts_path,file)) as f:
        line = f.readline()
        while line:
            line = json.loads(line)
            data += str(int(i_name)+1) + ' ' + str(line[0]) + ' ' + str(line[1]) + ' ' + str(line[2]) + ' ' + str(line[3]) + ' ' + str(line[4]) + '\n'
            line = f.readline()
    with open(os.path.join(os.path.join(res_path, set_name), v_name + '.txt'), 'a') as fa:
        fa.write(data)
