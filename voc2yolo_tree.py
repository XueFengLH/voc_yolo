import os
import numpy as np
import xml.etree.ElementTree as ET
import random
from tqdm import tqdm

classes_new = ['person_model']

random.seed(42)
np.random.seed(42)

error_box_num_x = 0
error_box_num_y = 0
def convert(size, box):
    '''
    Invoked by **voc2yolo**

    :param size:
    :param box:
    :return: 4 values in a tuple representing the bbox in the format of (x, y, w, h)
    '''
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    if w >= 1:
        w = 0.99
    if h >= 1:
        h = 0.99
    return (x, y, w, h)

def voc2yolo(rootpath, xmlname, classes):
    '''
    标注文件转换 xml转txt （VOC to YOLO）
    目录组织格式如下：
        rootpath-|
                 |-annotations-|
                 |             |-123.xml
                 |             |-124.xml
                 |             |-125.xml
                 |             |...
                 |
                 |-Cyolo-------|
                 |             |-123.txt
                 |             |-124.txt
                 |             |-125.txt
                 |             |...
                 |
                 |........
        其中, annotations是预先准备好的数据标签, Cyolo是自动创建的输出目录

    转换完毕后需人工写一个.yaml文件, eg:
        test.yaml:
            # train and val data as 1) directory: path/images/,
                                    2) file: path/images.txt, or
                                    3) list: [path1/images/, path2/images/]
            train: ../coco128/images/train2017/
            val: ../coco128/images/val2017/

            # number of classes
            nc: 4

            # class names
            names: ['person', 'escalator', 'dog', 'bus']

    :param rootpath: str
    :param xmlname: str
    :param classes: list, a classes list containing classes that you want to have in output coco annotations
            使用方法 eg: classes = ['person', 'escalator', 'dog', 'bus']

            如果classes = ['person', 'escalator', 'dog', 'bus'],
                则输出的class标签对应的为 [0, 1, 2, 3]
    :return: None
    '''

    base_path, basename = os.path.split(xmlname)
    dst_path = base_path.replace('annotation', 'labels')
    #dst_path = base_path.replace('tmp_val', 'tmp_labels_val')
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    with open(xmlname, "r", encoding='UTF-8') as in_file:
        txtname = basename[:-4] + '.txt'
        txtfile = os.path.join(dst_path, txtname)
        with open(txtfile, "w+", encoding='UTF-8') as out_file:
            tree = ET.parse(in_file)
            root = tree.getroot()
            size = root.find('size')
            if "all_usc_data" in rootpath or "all_iccv_data" in rootpath:
                h = int(size.find('width').text)
                w = int(size.find('height').text)
            else:
                w = int(size.find('width').text)
                h = int(size.find('height').text)
            if w==0 and h==0:
                w=640
                h=400
            out_file.truncate()
            for obj in root.iter('object'):
                cls = obj.find('name').text
                if cls not in classes and not cls in classes_new:
                    continue
                if cls in classes_new:
                    cls_id = classes.index('person')
                    # print("person_model", classes.index('person'))
                else:
                    cls_id = classes.index(cls)
                xmlbox = obj.find('bndbox')
                box = [float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text)]


                if box[0] > box[1]:
                    global error_box_num_x
                    tmp = box[0]
                    box[0] = box[1]
                    box[1] = tmp
                    print("error box 0", xmlname)
                    error_box_num_x += 1
                if box[2] > box[3]:
                    global error_box_num_y
                    tmp = box[2]
                    box[2] = box[3]
                    box[3] = tmp
                    print("error box 1")
                    error_box_num_y += 1
                b = (box[0], box[1], box[2], box[3])

                bb = convert((w, h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

# test example

def read_xml_list(file):
    file_list = []
    with open(file, 'r') as file_r:
        lines = file_r.readlines()
        for line in lines:
            value = line.strip()
            # value = os.path.join("/media/xin/data1/data/rubby/20220913/label/all",value)
            file_list.append(value)
    return file_list

def voc2yolox(lables_path,classes,rootPath=''):



    xml_list = read_xml_list(lables_path)
    for file in tqdm(xml_list):
        voc2yolo(rootPath, file, classes)
    print(error_box_num_x, error_box_num_y)

# if __name__ == "__main__":
#     # classes = ['person', 'escalator', 'person_model', 'person_dummy', 'fake_escalator']
#     # rootPath = "D:/00_indemind_lyk/ICE_I26R_I18R/ICEDataSets/data_filter/batch2&batch3_Lit/"
#     # rootPath = "D:/00_indemind_lyk/ICE_I26R_I18R/ICEDataSets/data_filter/902_domain/"
#     # rootPath = "D:/00_indemind_lyk/ICE_I26R_I18R/ICEDataSets/902_model/i18Rperson_model_dummy/"
#     # rootPath = "D:/00_indemind_lyk/ICE_I26R_I18R/ICEDataSets/902_20210705/record_3/"
#     # rootPath = "D:/00_indemind_lyk/ICE_I26R_I18R/ICEDataSets/openData/all_usc_data/"
#     # rootPath = "D:/00_indemind_lyk/ICE_I26R_I18R/ICEDataSets/openData/all_iccv_data/"
#
#     # classes = ['escalator', 'escalator_handrails']
#     # classes = ['person', 'escalator', 'escalator_handrails', 'person_dummy', 'escalator_model', 'escalator_handrails_model', 'difficult']
#     classes = ['dirtyliquid']
#     # classes = ['person', 'escalator_handrails', 'person_dummy', 'escalator_model', 'escalator_handrails_model']
#     classes_new = ['person_model']
#
#     # rootPath = "D:/00_indemind_lyk/ICE_I26R_I18R/ICEDataSets/escalator_20210716/"
#     # rootPath = 'D:/00_indemind_lyk/ICE_I26R_I18R/ICEDataSets/escalator_new_standard/escalator_20210721/7.21/all/'
#     # rootPath = 'D:/00_indemind_lyk/ICE_I26R_I18R/ICEDataSets/902_0712/all/xmls/train/'
#     # rootPath = 'D:/00_indemind_lyk/ICE_I26R_I18R/ICEDataSets/902_20210705_i18R/dataset/plan2/'
#     # rootPath = 'D:/00_indemind_lyk/ICE_I26R_I18R/ICEDataSets/selfCollection/collection/'
#     # rootPath = 'D:/00_indemind_lyk/ICE_I26R_I18R/ICEDataSets/902_new_rules/escalator_cover/902/collection'
#     # rootPath = 'D:/00_indemind_lyk/ICE_I26R_I18R/ICEDataSets/902_bug_20210826/collection'
#     # filePath = os.path.join(rootPath, "xml")
#     # xml_list = read_xml_list('D:/00_indemind_lyk/tinyDataSet/tiny_rgb_data/new_list.txt')
#
#     rootPath = '/media/xin/data1/data/dirty_data/ALL/voc'
#     # xml_list = read_xml_list('D:/00_indemind_lyk/tinyDataSet/5000PLUS/data/xml_list.txt')
#     # xml_list = read_xml_list('D:/00_indemind_lyk/tinyDataSet/shunyi_test_1w2/anno/test.txt')
#     # xml_list = read_xml_list('E:/dataset/ANNOTATION/TEST/ICE.txt')
#     # xml_list = read_xml_list('E:/dataset/ANNOTATION/TEST/ICE2000.txt')
#     # xml_list = read_xml_list('D:/00_indemind_lyk/DATASET_INDEM/ANNOTATIONS/V104_nococo_notest.txt')
#     # xml_list = read_xml_list('/media/xin/data1/data/dirty_data/ALL/labels.txt')
#     xml_list = read_xml_list('/media/spring/948058230E04CFC6/20240416/ALL/label.txt')
#
#
#
#
#
#     # files = os.listdir(filePath)
#     for file in tqdm(xml_list):
#         voc2yolo(rootPath, file, classes)
#     print(error_box_num_x, error_box_num_y)


