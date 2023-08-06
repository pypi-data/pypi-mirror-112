# -*- coding: utf-8 -*-
# @Time : 2021/7/9 上午11:17
# @Author : Jianglin Zhang
# @File : testing.py

import xml.etree.ElementTree as ET
import os


class Voc2Yolo:

    def __init__(self, defaultImgWidth=1920, defaultImgHeight=1080):
        self.defaultImgWidth = defaultImgWidth
        self.defaultImgHeight = defaultImgHeight

    @staticmethod
    def transfer_coordinate(size, box):

        x_center = (box[0] + box[1]) / 2.0
        y_center = (box[2] + box[3]) / 2.0
        x = x_center / size[0]
        y = y_center / size[1]
        w = (box[1] - box[0]) / size[0]
        h = (box[3] - box[2]) / size[1]
        return x, y, w, h

    def convert_annotation(self, xml_files_path, save_txt_files_path, need_deal_class_list):
        xml_files = os.listdir(xml_files_path)
        for xml_name in xml_files:
            # print(xml_name)
            if str(xml_name).find(".xml") < 0:
                continue
            xml_file = os.path.join(xml_files_path, xml_name)
            out_txt_path = os.path.join(save_txt_files_path, xml_name.split('.')[0] + '.txt')
            out_txt_f = open(out_txt_path, 'w')
            tree = ET.parse(xml_file)
            root = tree.getroot()
            size = root.find('size')
            w = int(size.find('width').text)
            h = int(size.find('height').text)
            if w is None or w == 0:
                w = self.defaultImgWidth
            if h is None or h == 0:
                h = self.defaultImgHeight

            for obj in root.iter('object'):
                difficult = obj.find('difficult').text
                cls = obj.find('name').text
                if cls not in need_deal_class_list or int(difficult) == 1:
                    continue
                cls_id = need_deal_class_list.index(cls)
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text))
                # b=(xmin, xmax, ymin, ymax)
                # print(w, h, b)
                bb = self.transfer_coordinate((w, h), b)
                out_txt_f.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


if __name__ == "__main__":
    # 把forklift_pallet的voc的xml标签文件转化为yolo的txt标签文件
    # 1、需要转化的类别
    need_deal_class_list = ['allcar', 'truck', 'car', 'authorize', 'human', 'tail', 'authorize_squat', 'authorize_sit',
                            'chacar',
                            'highcar', 'vest_squat', 'authorize_recline', 'vest', 'helmet', 'human_squat', 'helmet_sit']
    # 2、voc格式的xml标签文件路径
    xml_files_path = r'/home/wwl/mypython/myworkspace/vialearning/mwdstesting'
    # 3、转化为yolo格式的txt标签文件存储路径
    save_txt_files_path = r'/home/wwl/mypython/myworkspace/vialearning/mwdstesting'

    voc2Yolo = Voc2Yolo()
    voc2Yolo.convert_annotation(xml_files_path, save_txt_files_path, need_deal_class_list)
