import cv2
from misc import is_cv2_img, cv2pil

def save_gif(images, save_path, duration_msec=100):
    """ cv2 or PILの画像リストを受け取り、gifアニメとして保存 """

    if is_cv2_img(images[0]): 
        images = [cv2pil(img) for img in images]

    images[0].save(save_path,
                   format='GIF',
                   append_images=images[1:],
                   duration=duration_msec,
                   quality=95,
                   loop=0, #ずっと繰り返す
                   optimize=False,
                   save_all=True)

def save_gif_2(images, save_path, duration_msec=100):
    """ cv2の画像リストを受け取り、gifアニメとして保存 (moviepy使用)"""
    from moviepy.editor import ImageSequenceClip

    images = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in images]

    fps = 1000 / duration_msec
    clip = ImageSequenceClip(images, fps=fps)
    clip.write_gif(save_path)

