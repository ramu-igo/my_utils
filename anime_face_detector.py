#-*- coding: utf-8 -*-
import cv2
import os.path as osp

#lbpcascade_animeface: https://github.com/nagadomi/lbpcascade_animeface

class AnimeFaceDetector:
    def __init__(self, face_len_min=0):
        abs_dir = osp.dirname(osp.abspath(__file__))
        xml = osp.join(abs_dir, 'lbpcascade_animeface.xml')
        self.detector = cv2.CascadeClassifier(xml)
        self.face_len_min = face_len_min #最小検出サイズ

    def detect_faces(self, cv2img):
        im_h, im_w, _ = cv2img.shape
        det = self.detector.detectMultiScale(cv2img)

        faces = []
        for x_, y_, w_, h_ in det:
        
            # 生の検出結果だと顔部分だけなので、頭部まで入るように広げる
            x = int(max(x_ - w_ / 8, 0))
            rx = int(min(x_ + w_ * 9 / 8, im_w))
            y = int(max(y_ - h_ / 4, 0))
            by = int(y_ + h_)
            w = rx - x
            h = by - y
   
            if w < self.face_len_min or h < self.face_len_min:
                continue
 
            area = [x, y, w, h]
            faces.append(area)

        return faces
