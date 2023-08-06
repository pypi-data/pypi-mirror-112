# -*- coding: utf-8 -*-
# @Time : 2021/7/9 上午11:17
# @Author : Jianglin Zhang
# @File : testing.py

import xml.dom.minidom as xmldom
import os


class VocTools:
    def __init__(self, annotation_file_path):
        self.annotation_file_path = annotation_file_path
        pass

    def get_class_dict(self):
        annotation_names = [os.path.join(self.annotation_file_path, i) for i in os.listdir(self.annotation_file_path)]
        labels = dict()
        for names in annotation_names:
            xmlfilepath = names
            if str(xmlfilepath).find(".xml") < 0:
                continue
            domobj = xmldom.parse(xmlfilepath)
            # 得到元素对象
            elementobj = domobj.documentElement
            # 获得子标签
            subElementObj = elementobj.getElementsByTagName("object")
            for s in subElementObj:
                label = s.getElementsByTagName("name")[0].firstChild.data
                if None is labels.get(label):
                    labels[label] = 1
                else:
                    labels[label] = int(labels.get(label)) + 1
        d_order = sorted(labels.items(), key=lambda x: x[1], reverse=True)
        return d_order

"""
if __name__ == '__main__':
    annotation_file_path = "/home/wwl/mypython/myworkspace/vialearning/jianglinzhangdatasets/mawanpedestrianandcar"
    vocTools = VocTools(annotation_file_path)
    print(vocTools.get_class_dict())
"""