from __future__ import division

import os
import torch
from src.config import opt
from src.head_detector_vgg16 import Head_Detector_VGG16
from trainer import Head_Detector_Trainer
from PIL import Image
import numpy as np
from data.dataset import preprocess
import matplotlib.pyplot as plt
import src.array_tool as at
from src.vis_tool import visdom_bbox
import argparse
import src.utils as utils
from src.config import opt
import time
import cv2
import torchvision.transforms as transforms
from interface import write_sensor_occupant
import initial_nano

SAVE_FLAG = 0
THRESH = 0.05
IM_RESIZE = False


def read_img(path,flag=0):
    if flag==1:
        f=path
    else:
        f = Image.open(path)
    if IM_RESIZE:
        f = f.resize((640,480), Image.ANTIALIAS)

    f=f.convert('RGB')
    img_raw=f.copy()
    # img_raw = np.asarray(f, dtype=np.uint8)
    # img_raw_final = img_raw.copy()
    img = np.asarray(f, dtype=np.float32)
    _, H, W = img.shape
    img = img.transpose((2,0,1))
    img = preprocess(img)
    _, o_H, o_W = img.shape
    scale = o_H / H
    img_raw=img_raw.resize((o_W,o_H),Image.ANTIALIAS)
    return img, img_raw, scale


def detect_video(video_path,model_path):
    transform = transforms.Compose([transforms.Resize((32, 32)), transforms.ToTensor()])
    head_detector = Head_Detector_VGG16(ratios=[1], anchor_scales=[2, 4])
    trainer = Head_Detector_Trainer(head_detector).cuda()
    trainer.load(model_path)

       # second
    dif_frame=0
    num_frame=0

    cap=cv2.VideoCapture(video_path)
    cap.set(3,1080)
    cap.set(4,1920)
    cv2.namedWindow('number',0)
    while(1):
        ret,frame=cap.read()
        if ret==True:
            dif_frame=dif_frame+1
            if dif_frame==5:
                dif_frame=0
            else:
                continue
            img=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            #img=img.transpose(Image.ROTATE_180)
            img, img_raw, scale=read_img(img,flag=1)

            img = at.totensor(img)
            img = img[None, :, :, :]
            img = img.cuda().float()
            st = time.time()
            pred_bboxes_, final_score = head_detector.predict(img, scale, mode='evaluate', thresh=THRESH)
            et = time.time()
            tt = et - st
            print("[INFO] Head detection over. Time taken: {:.4f} s".format(tt))

            #try:write_sensor_occupant(IP =initial_nano.GetPiIP('./binding.csv'), occupant_num =pred_bboxes_.shape[0])
            except:print('cannot connect mysql')

            for i in range(pred_bboxes_.shape[0]):
                ymin, xmin, ymax, xmax = pred_bboxes_[i, :]
                utils.draw_bounding_box_on_image(img_raw, ymin, xmin, ymax, xmax)

            opimg=cv2.cvtColor(np.array(img_raw),cv2.COLOR_RGB2BGR)
            opimg=cv2.putText(opimg,str(pred_bboxes_.shape[0]),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,255,0),2)
            #cv2.imwrite('iave111.jpg',opimg)
            cv2.imshow('number',opimg)      
            cv2.waitKey(40)

            # plt.axis('off')
            # plt.imshow(img_raw)
            # plt.show()

            num_frame=num_frame+1
            string=str(num_frame)+' '+str(len(final_score))+' '+str(final_score)+'\n'
            print(string)
            #time.sleep(abs(60-int(tt)))

        else:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path", type=str, help="test image path",default='19.jpg')
    parser.add_argument("--model_path", type=str, default='./checkpoints/head_detector_final')
    args = parser.parse_args()
    detect_video(0, args.model_path)
    # detect(args.img_path, args.model_path)
    # model_path = './checkpoints/sess:2/head_detector08120858_0.682282441835'

    # test_data_list_path = os.path.join(opt.data_root_path, 'brainwash_test.idl')
    # test_data_list = utils.get_phase_data_list(test_data_list_path)
    # data_list = []
    # save_idx = 0
    # with open(test_data_list_path, 'rb') as fp:
    #     for line in fp.readlines():
    #         if ":" not in line:
    #             img_path, _ = line.split(";")
    #         else:
    #             img_path, _ = line.split(":")

    #         src_path = os.path.join(opt.data_root_path, img_path.replace('"',''))
    #         detect(src_path, model_path, save_idx)
    #         save_idx += 1


