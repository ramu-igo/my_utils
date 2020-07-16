import os
import shutil
import numpy as np
import cv2
from PIL import Image

# 画像について、特に記載なければcv2画像(np.ndarray)の前提

def reset_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)

def is_cv2_img(img):
    return True if isinstance(img, np.ndarray) else False

def pil2cv(image):
    """ PIL型 -> OpenCV型 """
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2: # グレースケール
        pass
    elif new_image.shape[2] == 3: # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4: # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

def cv2pil(image):
    """ OpenCV型 -> PIL型 """
    new_image = image.copy()
    if new_image.ndim == 2: # グレースケール
        pass
    elif new_image.shape[2] == 3: # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4: # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image

def crop_img(img, area):
    """ crop cv2 image """
    x, y, w, h = area
    cropped = img[y:y+h, x:x+w, :]
    return cropped

def rotate_img(img, angle, bg_color=(255, 255, 255)):
    """ 回転 (はみ出る部分が切れないようにする) """
    
    h, w = img.shape[:2]
    angle_rad = angle/180.0*np.pi
    
    # 回転後の画像サイズを計算
    w_rot = int(np.round(h*np.absolute(np.sin(angle_rad))+w*np.absolute(np.cos(angle_rad))))
    h_rot = int(np.round(h*np.absolute(np.cos(angle_rad))+w*np.absolute(np.sin(angle_rad))))
    size_rot = (w_rot, h_rot)
    
    # 元画像の中心を軸に回転する
    center = (w/2, h/2)
    scale = 1.0
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
    
    # 平行移動を加える (rotation + translation)
    affine_matrix = rotation_matrix.copy()
    affine_matrix[0][2] = affine_matrix[0][2] -w/2 + w_rot/2
    affine_matrix[1][2] = affine_matrix[1][2] -h/2 + h_rot/2
    
    img_rot = cv2.warpAffine(img, affine_matrix, size_rot, flags=cv2.INTER_CUBIC, borderValue=bg_color)
    return img_rot

def alpha_to_white(src):
    """ 透過pngの透過部分を白にする """
    H, W = src.shape[:2]
    dst = np.ones([H, W, 3]) * 255 #白背景

    mask = src[:,:,3]
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    mask = mask / 255.0
    src = src[:,:,:3]

    dst[...] *= 1 - mask
    dst[...] += src * mask 

    return dst

def make_image_grid(img_list, num_H=4, num_W=4):
    """ グリッド状に並べて1枚にする

        num_H, num_Wで縦横に並べる個数を指定(違ってもOK)
    """
    num_images = num_H * num_W #listがこれより多くても、ここまでをgridにする
    H, W = img_list[0].shape[:2] #画像1枚のサイズ (list内は全て同じサイズの前提)

    canvas = np.zeros((H*num_H,W*num_W,3),dtype=np.uint8)
    for i,p in enumerate(img_list[:num_images]):
        h,w = i//num_W, i%num_W
        canvas[H*h:H*-~h,W*w:W*-~w,:] = p
    return canvas

