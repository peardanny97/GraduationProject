import pandas as pd
import glob
import os
import random

# BG_DIR = "C:\Workspace\python_project\project\bg\"
# INPUT_DIR = "C:\Workspace\python_project\project"

# read_file = pd.read_csv(INPUT_DIR)
# read_file.to_csv('test.csv')
bg_dir = "C:\Workspace\python_project\project\bg" #FIX_ME
#current_dir = os.getcwd()
src_dir = "C:\Workspace\python_project\project" #FIX_ME

list_1 = []
list_2 =[]
list_3 = []
list_bg =[]
list =[]

list_bg = []
for f_path in glob.iglob(os.path.join(bg_dir, "*.jpg")):
        title, ext = os.path.splitext(os.path.basename(f_path))
        list_bg.append(title)


print (list_bg)
for f_path in glob.iglob(os.path.join(src_dir, "*.jpg")):
    title, ext = os.path.splitext(os.path.basename(f_path))
    list_1.append("{0}/{1}.jpg\n".format(src_dir.replace('\\','/'),title))
    list_2.append("{0}/{1}_mask.png\n".format(src_dir.replace('\\','/'),title))   
    name = random.choice(list_bg)
    list_3.append("{0}/{1}.jpg\n".format(bg_dir.replace('\\','/'),name))
    
list = [list_1,list_2,list_3]    
dataframe = pd.DataFrame(list)
dataframe = dataframe.transpose()
dataframe.to_csv('test.csv',header=False,index=False)

