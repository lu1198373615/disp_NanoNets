import cv2
import os


color = (5,12,255)
image_path = 'H:\data2\images_testing\set06V000I00029.jpg'

font = cv2.FONT_HERSHEY_SIMPLEX
image = cv2.imread(image_path, 1)
boxes = [{'xmax':200,'xmin':100,'ymax':200,'ymin':100,'score':0.6}]
count = len(boxes)
for box in boxes:
    xmax, xmin, ymax, ymin, score = box['xmax'], box['xmin'], box['ymax'], box['ymin'], box['score']
    # cv2.rectangle(image, (xmin, ymin-10), (xmin+75, ymin), color, -1)
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 3)
    # cv2.putText(image, 'pedestrian: %d%%'%(score * 100), (xmin, ymin), font, fontScale=0.3, color=(0,0,0), thickness=1, lineType=cv2.LINE_AA)
cv2.imwrite('xxx.jpg', image)
