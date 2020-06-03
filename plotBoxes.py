import tkinter
from tkinter import filedialog
import cv2
import json
from PIL import Image, ImageTk
import requests
import os


class Data(object):
    def __init__(self):
        self.image_path = tkinter.StringVar()
        self.annotation_path = tkinter.StringVar()
        self.scall_gate = None
        self.text_annotation = None
        self.label_image = None


def display_welcome(data):
    img = Image.open('welcome.jpg')
    photo = ImageTk.PhotoImage(img)
    data.label_image.config(image=photo)
    data.label_image.image = photo


def get_image_path(data):
    image_path = filedialog.askopenfilename()
    data.image_path.set(image_path)
    if image_path:
        data.annotation_path.set('')
        display_original_image(data)
    else:
        display_welcome(data)


def get_annotation_path(data):
    data.text_annotation.delete('1.0','end')
    annotation_path = filedialog.askopenfilename()
    data.annotation_path.set(annotation_path)
    if annotation_path:
        data.text_annotation.insert(tkinter.END, '这次选择的注释是进行本次展示前，使用NanoNets模型获得，并存放在本地的注释\n')
        data.text_annotation.insert(tkinter.END, '也可以点击“从NanoNets注释”按钮从NanoNets服务器获得，但次数有限请省点用\n')
        with open(annotation_path, 'r') as f:
            line = f.readline()
            while line:
                data.text_annotation.insert(tkinter.END, line)
                line = f.readline()
        display_result_image(data)
    else:
        display_original_image(data)


def gene_image_from_local(data):
    data.text_annotation.delete('1.0', 'end')
    data.text_annotation.insert(tkinter.END, '此时正在展示依据注释文件，使用OpenCV-python在视频帧图片上标注的结果\n')
    if not data.image_path.get():
        data.text_annotation.insert(tkinter.END, '请先选择图片\n')
    elif not data.annotation_path.get():
        data.text_annotation.insert(tkinter.END, '请先选择注释\n')
    else:
        image = cv2.imread(data.image_path.get(), 1)
        with open(data.annotation_path.get(), 'r') as f:
            line = f.readline()
            while line:
                data.text_annotation.insert(tkinter.END, line)
                line = json.loads(line)
                xmin, ymin, xmax, ymax, score = line[0], line[1], line[0] + line[2], line[1] + line[3], line[4]
                if score * 100 > int(data.scall_gate.get()):
                    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 36, 36), 3)
                    cv2.putText(image, '%d%%' % (score * 100), (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                                color=(36, 36, 255), thickness=1, lineType=cv2.LINE_AA)
                line = f.readline()
        cv2.imwrite('temp.jpg', image)


def display_result_image(data):
    gene_image_from_local(data)
    if not data.image_path.get():
        data.text_annotation.delete('1.0', 'end')
        data.text_annotation.insert(tkinter.END, '请先选择图片\n')
    elif not data.annotation_path.get():
        data.text_annotation.delete('1.0', 'end')
        data.text_annotation.insert(tkinter.END, '请先选择注释\n')
    else:
        img = Image.open('temp.jpg')
        photo = ImageTk.PhotoImage(img)
        data.label_image.config(image=photo)
        data.label_image.image = photo
        scall_gate.set('0')


def display_original_image(data):
    data.text_annotation.delete('1.0', 'end')
    if data.image_path.get():
        img = Image.open(data.image_path.get())
        photo = ImageTk.PhotoImage(img)
        data.label_image.config(image=photo)
        data.label_image.image = photo
    else:
        data.text_annotation.insert(tkinter.END,'请先选择图片\n')


def display_gt_image(data):
    data.text_annotation.delete('1.0', 'end')
    data.text_annotation.insert(tkinter.END, '“真实情况”按钮获得的图片是使用从Caltech官网获得的注释，并使用OpenCV-python在视频帧上作图得到\n')
    data.text_annotation.insert(tkinter.END, '可以看出，使用NanoNets模型做的预测相对于“真实情况”略有出入\n')
    if data.image_path.get():
        gt_path = data.image_path.get().replace('images_testing', 'groundtruth').replace('.jpg', '.txt')
        if os.path.exists(gt_path):
            image = cv2.imread(data.image_path.get(), 1)
            with open(gt_path, 'r') as f:
                line = f.readline()
                line = f.readline()
                while line:
                    content_list = line.split(' ')
                    xmin, ymin, xmax, ymax = int(content_list[1]), int(content_list[2]), int(content_list[1]) \
                                             + int(content_list[3]), int(content_list[2]) + int(content_list[4])
                    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (36, 255, 36), 3)
                    cv2.putText(image, 'person', (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                                color=(36, 255, 36), thickness=1, lineType=cv2.LINE_AA)
                    data.text_annotation.insert(tkinter.END,
                                                content_list[1] + content_list[2] + content_list[3] + content_list[
                                                    4] + '\n')
                    if content_list[5] == '1':
                        xmin, ymin, xmax, ymax = int(content_list[6]), int(content_list[7]), int(content_list[6]) \
                                                 + int(content_list[8]), int(content_list[7]) + int(content_list[9])
                        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 255), 3)
                    line = f.readline()
            cv2.imwrite('temp.jpg', image)
            img = Image.open('temp.jpg')
            photo = ImageTk.PhotoImage(img)
            data.label_image.config(image=photo)
            data.label_image.image = photo
            scall_gate.set('0')
        else:
            data.text_annotation.insert(tkinter.END, '警告：此图片的groundtruth未找到！！！\n')
    else:
        data.text_annotation.delete('1.0', 'end')
        data.text_annotation.insert(tkinter.END,'请先选择图片\n')


def call_scall(text):
    gene_image_from_local(data)
    if not data.image_path.get():
        data.text_annotation.delete('1.0', 'end')
        data.text_annotation.insert(tkinter.END, '请先选择图片\n')
    elif not data.annotation_path.get():
        data.text_annotation.delete('1.0', 'end')
        data.text_annotation.insert(tkinter.END, '请先选择注释\n')
    else:
        img = Image.open('temp.jpg')
        photo = ImageTk.PhotoImage(img)
        data.label_image.config(image=photo)
        data.label_image.image = photo


def get_NanoNets(data):
    if data.image_path.get():
        data.text_annotation.delete('1.0', 'end')
        save_path = os.path.join(os.getcwd(), os.path.basename(data.image_path.get()).replace('.jpg', '.txt'))
        if os.path.exists(save_path):
            data.text_annotation.insert(tkinter.END, '本地已经有注释啦，它在：' + save_path + '\n')
            with open(save_path, 'r') as f:
                line = f.readline()
                while line:
                    data.text_annotation.insert(tkinter.END, line)
                    line = f.readline()
        else:
            data.text_annotation.insert(tkinter.END, '这是从NanoNets获得的注释哦，次数有限请省点用\n')
            url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/14fcd528-00fc-4a4b-81be-b50c7afee216/LabelFile/'
            file_data = {'file': open(data.image_path.get(), 'rb')}
            response = requests.post(url, auth=requests.auth.HTTPBasicAuth('I4UQOdAXBenkRM2lJfMr1waLz7KXxits', ''),
                                     files=file_data)
            boxes = response.json()['result'][0]['prediction']
            data.text_annotation.insert(tkinter.END, '为了节约次数，我已经将注释文件保存在：' + save_path + '\n')
            with open(save_path, 'w') as f:
                for box in boxes:
                    li = [box['xmin'], box['ymin'], box['xmax'] - box['xmin'], box['ymax'] - box['ymin'], box['score']]
                    f.write(str(li) + '\n')
                    data.text_annotation.insert(tkinter.END, str(li) + '\n')
        data.annotation_path.set(save_path)
        display_result_image(data)
    else:
        data.text_annotation.delete('1.0', 'end')
        data.text_annotation.insert(tkinter.END,'请先选择图片\n')



root = tkinter.Tk()
root.title('《机器学习》作业展示(Powered by Python.tkinter)')
root.geometry('700x650')

data = Data()

entry_image_path = tkinter.Entry(root, textvariable=data.image_path, width=40)
entry_image_path.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, x=-200, y=-305)

button_ask_image_path = tkinter.Button(root, text="图片路径", command=lambda: get_image_path(data))
button_ask_image_path.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, x=0, y=-305)

entry_annotation_path = tkinter.Entry(root, textvariable=data.annotation_path, width=40)
entry_annotation_path.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, x=-200, y=-275)

button_ask_annotation_path = tkinter.Button(root, text="注释路径", command=lambda: get_annotation_path(data))
button_ask_annotation_path.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, x=0, y=-275)

button_NanoNets = tkinter.Button(root, text="从NanoNets注释", command=lambda: get_NanoNets(data))
button_NanoNets.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, x=100, y=-275)

button_original_image = tkinter.Button(root, text="原始图片", command=lambda: display_original_image(data))
button_original_image.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, x=100, y=-305)

button_predict_image = tkinter.Button(root, text='预测图片', command=lambda: display_result_image(data))
button_predict_image.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, x=200, y=-305)

button_gt_image = tkinter.Button(root, text='真实情况', command=lambda: display_gt_image(data))
button_gt_image.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, x=300, y=-305)

label_gate = tkinter.Label(root, text='判决门限：')
label_gate.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, x=200, y=-265)

scall_gate = tkinter.Scale(root, from_=0, to=100.0, resolution=1.0, orient=tkinter.HORIZONTAL, command=call_scall)
scall_gate.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, x=280, y=-270)
data.scall_gate = scall_gate

label_annotation = tkinter.Label(root, text='获得的注释内容：')
label_annotation.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, x=-296, y=-220)

scroll_annotation = tkinter.Scrollbar(root, borderwidth=4)
text_annotation = tkinter.Text(root, width=80, height=4)
scroll_annotation.config(command=text_annotation.yview)
text_annotation.config(yscrollcommand=scroll_annotation.set)
text_annotation.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, x=30, y=-220)
# scroll_annotation.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, x=320, y=-221)
scroll_annotation.pack(side=tkinter.RIGHT, fill=tkinter.Y)
data.text_annotation = text_annotation

label_image = tkinter.Label(root)
label_image.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER, x=-15, y=65)
data.label_image = label_image
display_welcome(data)

root.mainloop()




