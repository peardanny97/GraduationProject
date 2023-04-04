import os
import random
import glob
import cv2
import shutil
import numpy as np

current_dir = os.getcwd()
cnt = 0

#FIXME
added_prefix = "_gamma"
alpha = 1.3 # Enter the alpha value [1.0-3.0]
beta = 0  # Enter the beta value [0-100]

####Process
list = []
for f_path in glob.iglob(os.path.join(current_dir, "*.jpg")):
	title, ext = os.path.splitext(os.path.basename(f_path))
	list.append(title)

print("Total %d images" %len(list))

while list:
	name = random.choice(list)
	cnt += 1
	if(cnt%100==0):
		print(cnt)

	src = cv2.imread(name+".jpg", cv2.IMREAD_COLOR)
	height, width, channel = src.shape
	dst = np.zeros(src.shape, src.dtype)
	
	'''
	hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
	h,s,v = cv2.split(hsv)
	v[v>50] -= 50
	dst_hsv = cv2.merge((h,s,v))
	dst = cv2.cvtColor(dst_hsv, cv2.COLOR_HSV2BGR)
	'''

	img = np.int16(src)	
	img = np.clip(alpha*img+beta, 0, 255)
	dst = np.uint8(img)

	#cv2.imwrite(name+added_prefix+".jpg", dst)
	#shutil.copyfile(name+".txt", name+added_prefix+".txt")

	#'''	
	cv2.imshow("src",src)
	cv2.moveWindow("src",0,0)
	cv2.imshow("dst",dst)
	cv2.moveWindow("dst",0,500)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	#'''	

	
	list.remove(name)

input("Press Enter to exit...")
