# import PIL module
from PIL import Image
import cv2 
import os
import glob
import random

src_dir = "/home/ssai4/8.GPgan_datset/5.Mereged_data_bgrm"  # FIX ME
bg_dir = "/home/ssai4/Tensorflow_GP-GAN/background"  # FIX ME
save_dir = "/home/ssai4/8.GPgan_datset/6.Merged_dataset"  #FIX ME

list_bg = []

for f_path in glob.iglob(os.path.join(bg_dir, "*.jpg")):
        title, ext = os.path.splitext(os.path.basename(f_path))
        list_bg.append(title)


cnt = 0

for f_path in glob.iglob(os.path.join(src_dir, "*.png")):
    
    cnt += 1
    if((cnt%100)==0): print(cnt)
    title, ext = os.path.splitext(os.path.basename(f_path))
          
    frontImage = Image.open(src_dir + "/" + title + ".png")
    name = random.choice(list_bg)
    
    background = Image.open(bg_dir + "/" + name + ".jpg")
    
    frontImage = frontImage.convert("RGBA")
    background = background.convert("RGBA")

    width = (background.width - frontImage.width) // 2

    height = (background.height - frontImage.height) // 2
    
    width_list = [width//2, width, width + width//2 ]
    height_list = [height//2, height, height + height//2]

    background.paste(frontImage, (random.choice(width_list), random.choice(height_list)), frontImage)
    save_img = background.convert('RGB')
    save_img.save(save_dir + "/" + title + ".jpg", format = "JPEG")
  
