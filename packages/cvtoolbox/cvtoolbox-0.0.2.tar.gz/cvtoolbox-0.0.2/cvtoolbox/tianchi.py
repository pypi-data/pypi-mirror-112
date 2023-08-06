# -*- coding: utf-8 -*-
import os
import time
import cv2
import os.path as osp
import glob
import json
import numpy as np
import pandas as pd
import random
from tqdm import tqdm
import shutil
import imagesize
import logging
import torch
from mmdet.apis import inference_detector
from .base import bbox_overlaps


def get_img_ann_list(csv_path, data_root):
	df = pd.read_csv(csv_path,header=None)
	# 读取图片路径和原始标注
	img_list = [os.path.join(data_root,_) for _ in df[4]]
	ann_list = [json.loads(_) for _ in df[5]]
	return ann_list,img_list

def save_json(obj_ins,save_path: str = 'result.json') -> None:
    '''
    将内容保存至json文件
    :param obj_ins:
    :return:
    '''
    with open(save_path, 'w') as fp:
        json.dump(obj_ins, fp, indent=4, ensure_ascii=False)
    print("json saved.\n")

def data2coco(csv_path: str, data_root: str, save_json_path: str = 'coco_full.json') -> None:
    '''
    将csv提取出来的列表信息转为coco格式
    param img_list:
    param ann_list:
    param save_json_path:
    return:
    '''
	
    meta={}
    images=[]
    annotations = []
    box_id=0
    ann_list,img_list = get_img_ann_list(csv_path, data_root)
    for idx,img_ann in enumerate(ann_list):
        width, height = imagesize.get(img_list[idx])
        image={}
        image['file_name']=img_list[idx].split('/')[-1]
        image['height']=height
        image['width']=width
        image['id']=idx
        images.append(image)
        for item in img_ann['items']:
            logging.info(f'box_id:{box_id}, idx:{idx}')
            annotation={}
            x1,y1,x2,y2 = item['meta']['geometry']
            w,h = x2-x1,y2-y1
            box = [x1,y1,w,h]
            label = item['labels']['标签'] if item['labels']['标签']!='wrongclothes' \
                else item['labels']['不合规原因'][0]
            try:
                cat_id = CATEGORIES_TO_ID[label]
            except:
                logging.warning(f'Label:{label}')
            # for (cat_id, key) in [(1,'guarder'),(2,'rightdressed'),(3,'wrongdressed')]:
            annotation['image_id'] = idx
            annotation['id'] = box_id
            annotation['category_id'] = cat_id
            annotation['bbox'] = box
            annotation['area'] = w * h
            annotation['segmentation']=[]
            annotation['iscrowd'] = 0
            annotations.append(annotation)
            box_id += 1

    meta['images'] = images
    meta['annotations'] = annotations
    meta['categories'] = CATEGORIES
    save_json(meta,save_json_path)

def create_data_dict(img_list,ann_list):
    img_instance={}
    for idx,img_ann in enumerate(ann_list):
        img_instance[img_list[idx]]={}
        info_temp=[]
        width, height = imagesize.get(img_list[idx])
        for item in img_ann['items']:
            x1,y1,x2,y2 = item['meta']['geometry']
            w,h = x2-x1,y2-y1
            label = item['labels']['标签'] if item['labels']['标签']!='wrongclothes' \
                else item['labels']['不合规原因'][0]
            try:
                cat_id = CATEGORIES_TO_ID[label]
            except:
                logging.warning(f'Label:{label}')
            ins={}
            ins['x1']=x1
            ins['y1']=y1
            ins['w']=w
            ins['h']=h
            ins['category_id']=cat_id
            info_temp.append(ins)

        img_instance[img_list[idx]]['bbox']=info_temp
        img_instance[img_list[idx]]['width'] = width
        img_instance[img_list[idx]]['height'] = height

    return img_instance

def split_train_val(csv_path,data_root,train_json_path,val_json_path,ratio: float = 0.2):
    '''
    设定随机种子，根据比例划分训练集与验证集
    :param json_path:
    :param pic_path:
    :param ratio:
    :return:
    '''
    random.seed(2021)
    ann_list,img_list = get_img_ann_list(csv_path, data_root)
    img_instance = create_data_dict(img_list,ann_list)
    all_images = img_instance.keys()
    print("all imgs: ",len(all_images))
    val_images_split = random.sample(all_images,int(len(all_images)*ratio))
    print("val imgs:",len(val_images_split))
	
    train_imgs = []
    train_annos = []
    val_imgs = []
    val_annos = []
    train_id = 0
    val_id = 0
    train_box_id = 0
    val_box_id = 0

    for img_name in tqdm(img_instance.keys()):
        flag_val = False
        if img_name in val_images_split:
            flag_val = True
            val_id += 1
            if not osp.exists('./data/coco/val2017/'):
                os.makedirs('./data/coco/val2017/')
            shutil.copy(img_name,"./data/coco/val2017/")
        else:
            train_id += 1
            if not osp.exists('./data/coco/train2017/'):
                os.makedirs('./data/coco/train2017/')
            shutil.copy(img_name,"./data/coco/train2017/")
        
        img_anno = {}
        img_anno['filename']=img_name.split("/")[-1]
        img_anno['width'] = img_instance[img_name]['width']
        img_anno['height'] = img_instance[img_name]['height']
        if flag_val:
            img_anno['id'] = val_id
            val_imgs.append(img_anno)
        else:
            img_anno['id'] = train_id
            train_imgs.append(img_anno)
        
        bboxes = img_instance[img_name]['bbox']
        for bbox in bboxes:
            bbox_anno={}
            if flag_val:
                val_box_id += 1
                bbox_anno['id'] = val_box_id
                bbox_anno['image_id'] = val_id
            else:
                train_box_id += 1
                bbox_anno['id'] = train_box_id
                bbox_anno['image_id'] = train_id
            x1 = bbox['x1']
            y1 = bbox['y1']
            w = bbox['w']
            h = bbox['h']
            cat_id = bbox['category_id']
            bbox_anno['bbox'] =[x1,y1,w,h]
            bbox_anno['category_id'] = cat_id
            bbox_anno['area'] = w * h
            bbox_anno['iscrowd'] = 0
            if flag_val:
                val_annos.append(bbox_anno)
            else:
                train_annos.append(bbox_anno)
    train_meta = {'images':train_imgs,'annotations':train_annos,'categories':CATEGORIES}
    val_meta = {'images':val_imgs,'annotations':val_annos,'categories':CATEGORIES}
    if not osp.exists('./data/coco/annotations/'):
        os.makedirs('./data/coco/annotations/')
    save_json(train_meta,train_json_path)
    save_json(val_meta,val_json_path)

def vis_gt(img_list: list, ann_list: list):
    '''
    可视化ground truth
    :param img_list:
    :param ann_list:
    :return:
    '''
    img_instance = create_data_dict(img_list,ann_list)
    print(len(img_instance.keys()))
    for img_name, v in img_instance.items():
        bboxes = v['bbox']
        src = cv2.imread(img_name)
        for bbox in bboxes:
            x1, y1, x2, y2 = int(bbox['x1']), int(bbox['y1']), int(bbox['x1'] + bbox['w']), int(
                bbox['y1'] + bbox['h'])
            label = bbox['category_id']
            cv2.rectangle(src, (x1, y1), (x2, y2), (255, 0, 0), 4)
            cv2.putText(src, '%d' % label,
                        (x2, y2), cv2.FONT_HERSHEY_COMPLEX,
                        0.8,
                        (0, 0, 255), 4)
        print(img_name)
        cv2.imwrite('./visual_results/'+osp.basename(img_name),src)
        input()

def process_results(result, threshold = 0.4):
    """将mmresult转换成天池所需的格式\\
    Args:
        result: mmdet预测结果存储于该list
        threshold: 过滤小于该阈值的结果
    Return:
        processed_result: 格式同result,只有三个类别，分别为'guarder', 'rightdressed', 'wrongdressed'
    """
    result_filtered = [m[np.where(m[:,4]>threshold)] for m in result]
    person_result = torch.FloatTensor(result_filtered[1])
    clothes_result = torch.FloatTensor(result_filtered[2])
    rightdressed = bbox_overlaps(person_result[:,:4], clothes_result[:,:4],mode='siou')
    w1_result = torch.FloatTensor(result_filtered[3])
    w2_result = torch.FloatTensor(result_filtered[4])
    w3_result = torch.FloatTensor(result_filtered[5])
    w_result = torch.cat((w1_result, w2_result, w3_result), 0)
    wrongdressed = bbox_overlaps(person_result[:,:4], w_result[:,:4] ,mode='siou')
    # %% badge result
    badge_result = torch.FloatTensor(result_filtered[0])
    guarder = bbox_overlaps(person_result[:,:4], badge_result[:,:4],mode='siou')
    assert len(rightdressed) == len(guarder) == len(wrongdressed)
    out = [np.empty((0,5)) for i in range(6)]
    for idx, person_box in enumerate(person_result):
        # 有袖章，[有√、无√]无x：guarder
        # 无袖章，有√，无x：rightdressed
        # 否则（无袖章[无√、有√]有x、有袖章有√有x）：wrongdressed
        # print(idx)
        # if wrongdressed[idx].__len__():  # 如果穿错了衣服放进 wrongdressed
        #  person 穿错衣服 或者 没有任何一个穿对衣服的框，那就wrong dressed
        if torch.any(wrongdressed[idx]>0.8) or torch.all(rightdressed[idx]<0.8): 
            out[2] = np.append(out[2],person_box.reshape(1,5),axis=0) 
        else:
            out[1] = np.append(out[1],person_box.reshape(1,5),axis=0)
        # elif guarder[idx].__len__() and wrongdressed[idx].__len__(): #如果带着袖章
        if torch.any(guarder[idx]>0.8):  # 有安全员袖章
            out[0] = np.append(out[0],person_box.reshape(1,5),axis=0)*0.9
            # out[1] = np.append(out[1],person_box.reshape(1,5),axis=0)
    return out[:3]

def mmresult2json(csv_path:str, data_root:str, model, save_json_path: str ='push_result.json', threshold:int=0.4):
    """将mmdet预测的结果转为json格式，用于评分获取\\
    Args:
        csv_path: 测试集的csv文件，只包含测试地址的路径
        data_root:存放测试集文件夹的地址，即测试集的父文件夹
        model: 在 from mmdet.apis import init_detector(config, checkpoint) 之后获得的模型
        save_json_path: 存储地址的地方，默认push_result.json
    Return:
        Null
    """
    box_id=0
    CATEGORIES_RESULT = {'guarder':1, 'rightdressed':2,'wrongdressed':3}
    img_list = pd.read_csv(csv_path,header=None)[0][1:]
    meta = {}
    result_json = []
    block={}
    for idx,img_path in tqdm(enumerate(img_list)):
        # 获取识别结果
        result = inference_detector(model, os.path.join(data_root,img_path))
        # print(f'idx: {idx} img_path: {img_path}')
        results_processed = process_results(result,threshold=threshold)
        print(f'Use threshold : {threshold}')
        for iidx, bboxs  in enumerate(results_processed):
            # if not len(i):continue
            # else:
            for bbox in bboxs:
                block={}
                block['image_id'] = idx
                block['category_id'] = iidx+1 #CATEGORIES_RESULT[iidx]
                block['bbox'] = bbox[:4].tolist()
                block['score'] = bbox[-1].tolist()
                result_json.append(block)
    meta['result_json'] = result_json
    save_json(result_json,save_json_path)

if __name__=='__main__':
    CATEGORIES = [{'id': 1, 'name': 'badge'},  # 监护袖章（只识别红色袖章）
                {'id': 2, 'name': 'person'},  # 图中出现的所有在场人员
                {'id': 3, 'name': 'clothes'},  # 合规工作服
                {'id': 4, 'name': 'wrongbottom'},  # 不合规工作服（含有上衣开襟、挽裤腿、挽袖、不成套等现象）
                {'id': 5,'name':'wrongtop'},
                {'id': 6,'name':'wrongsuit'}
                ] 
    CATEGORIES_TO_ID = {"badge":1, "person":2, "clothes":3, \
        "wrongbottom":4, "wrongtop":5, "wrongsuit":6}

    save_json_path = 'gd2grid_train2017_full_coco.json' 
    train_json_path = './data/coco/annotations/gd2grid_coco_train2017.json'
    val_json_path = './data/coco/annotations/gd2grid_coco_val2017.json'
    csv_path = '2train_rname.csv'
    data_root = '/home/xds/Documents/data'
    #生成所有图像数据的coco格式json
    data2coco(csv_path, data_root,save_json_path)
    #划分train和val，并生成各自coco格式json到对应文件夹
    split_train_val(csv_path,data_root,train_json_path,val_json_path)

