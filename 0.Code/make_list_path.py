import glob
import os
import random

bg_dir = "" #FIX_ME
src_dir = "" #FIX_ME

list_bg =[]
file_train = open('target.csv','w') #name of target txt file, has to be changed to csv

for f_path in glob.iglob(os.path.join(bg_dir, "*.jpg")):
        title, ext = os.path.splitext(os.path.basename(f_path))
        list_bg.append(title)


for f_path in glob.iglob(os.path.join(src_dir, "*.jpg")):
    title, ext = os.path.splitext(os.path.basename(f_path))    
    file_train.write("{0}/{1}.jpg;".format(src_dir.replace('\\','/'),title))
    name = random.choice(list_bg)
    file_train.write("{0}/{1}.jpg;".format(bg_dir.replace('\\','/'),name))
    file_train.write("{0}/{1}_mask.png\n".format(src_dir.replace('\\','/'),title))
    


