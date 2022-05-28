import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets='1'
classes = ["ball"]

#用于得到归一化的txt标签数据
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

#进行xml2txt转化
def convert_annotation(image_id):
    #xml地址
    in_file = open('./xml/%s.xml'%image_id)
    #输出文件地址
    out_file = open('./txt/%s.txt'%image_id, 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
#进行批量处理

def readname():
    InfilePath = 'xml/'
    with open("names.txt", 'wt') as Outfile:
        Outfile.truncate(0)
        if len(os.listdir(r'{0}'.format(InfilePath))):
            name = os.listdir(r'{0}'.format(InfilePath))
            for i in range(len(name)):
                Outfile.write('{0}\n'.format((name[i].rsplit(".",1))[0]))

for image_set in sets:
    # 读取所有xml文件名称
    readname()
    image_ids = open('./names.txt').read().strip().split()
    for image_id in image_ids:
        convert_annotation(image_id)
    

