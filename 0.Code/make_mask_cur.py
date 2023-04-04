import cv2
import os
import argparse
import random
import glob

current_dir = os.getcwd()
cnt = 0

#FIXME
added_prefix = "_mask"

####Process
list = []
for f_path in glob.iglob(os.path.join(current_dir, "*.jpg")):
	title, ext = os.path.splitext(os.path.basename(f_path))
	list.append(title)

while list:
    name = random.choice(list)
    cnt += 1
    if(cnt%100==0):
        print(cnt)
    '''
    parser = argparse.ArgumentParser(description='make_mask')
    parser.add_argument('--src_name', default='', help='name of soure image')
    args = parser.parse_args()
    '''
    src = cv2.imread(name + ".jpg")

    gray_src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_src, 10, 1, cv2.THRESH_BINARY)
    # mask = cv2.adaptiveThreshold(gray_src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)
    # blurred = cv2.GaussianBlur(gray_src, (7,7), 0)
    # _, mask = cv2.threshold(blurred, 3, 1, cv2.THRESH_BINARY)
    
    cv2.imwrite(name+added_prefix + ".png", mask)
    list.remove(name)
    
    '''
    src_name, src_extension = os.path.splitext(args.src_name)
    cv2.imwrite(src_name + '_mask.png', mask)
    '''

'''
cv2.imshow('mask', mask)
cv2.waitKey()
'''