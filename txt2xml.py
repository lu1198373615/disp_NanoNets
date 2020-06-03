import os


indent = lambda x,y: ''.join(['  ' for _ in range(y)]) + x
annotations_path = r'H:\homework_data\annotations'
xml_path = r'H:\homework_data\xmls'
width, height = 640, 480
if not os.path.exists(xml_path):
    os.mkdir(xml_path)
txtlist = os.listdir(annotations_path)

for txtFile in txtlist:
    if int(txtFile[3:5])>5:
        continue
    with open(os.path.join(annotations_path, txtFile),'r') as f:
        line = f.readline()
        rect_list = []
        while line:
            if line.startswith('person'):
                content_list = line.split(' ')
                rect_list.append([int(content_list[1]),int(content_list[2]),int(content_list[3]),int(content_list[4])])
            line = f.readline()
        with open(os.path.join(xml_path, str(txtFile).replace('.txt','.xml')), 'w') as fx:
            fx.write('<annotation>\n')
            fx.write(indent('<filename>' + str(txtFile).replace('.txt','.jpg') + '</filename>\n', 1))
            fx.write(indent('<size>\n', 1))
            fx.write(indent('<width>' + str(width) + '</width>\n', 2))
            fx.write(indent('<height>' + str(height) + '</height>\n', 2))
            fx.write(indent('<depth>3</depth>\n', 2))
            fx.write(indent('</size>\n', 1))

            for point in rect_list:
                xmin = point[0]
                ymin = point[1]
                xmax = xmin + point[2]
                ymax = ymin + point[3]
                if ((ymax < height) & (xmax < width) & (xmin > 0) & (ymin > 0)):
                    fx.write(indent('<object>\n', 1))
                    fx.write(indent('<name>' + 'pedestrian' + '</name>\n', 2))
                    fx.write(indent('<bndbox>\n', 2))
                    fx.write(indent('<xmin>' + str(xmin) + '</xmin>\n', 3))
                    fx.write(indent('<ymin>' + str(ymin) + '</ymin>\n', 3))
                    fx.write(indent('<xmax>' + str(xmax) + '</xmax>\n', 3))
                    fx.write(indent('<ymax>' + str(ymax) + '</ymax>\n', 3))
                    fx.write(indent('</bndbox>\n', 2))
                    fx.write(indent('</object>\n', 1))

            fx.write('</annotation>\n')

