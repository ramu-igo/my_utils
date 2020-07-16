#-*- coding: utf-8 -*-
import os
import os.path as osp
import cv2

class ImageDataLoader:
    def __init__(self, src_path):

        if osp.isdir(src_path):
            self.is_video = False
            self.img_dir = src_path
            self.file_list = sorted(os.listdir(src_path))
            self.img_idx = 0
        else:
            self.is_video = True
            self.cap = cv2.VideoCapture(src_path)
            self.frame_idx = 0

    def __iter__(self):
        return self

    def __len__(self):
        if self.is_video:
            return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        else:
            return len(self.file_list)

    def __next__(self):

        if self.is_video:
            if not self.cap.isOpened():
                raise StopIteration
            ret, img = self.cap.read()
            if ret == False:
                self.cap.release()
                raise StopIteration

            info = {
                'frame_no' : self.frame_idx
            }
            self.frame_idx += 1
            return img, info

        else:
            if self.img_idx == len(self.file_list):
                raise StopIteration

            img_path = osp.join(self.img_dir, self.file_list[self.img_idx])
            img = cv2.imread(img_path)

            info = {
                'img_path' : img_path
            }
            self.img_idx += 1
            return img, info

