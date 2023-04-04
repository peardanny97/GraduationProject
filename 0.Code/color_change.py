import os
import random
import glob
import cv2
import shutil
import numpy as np

current_dir = os.getcwd()
cnt = 0

#FIXME
added_prefix = "_color"

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

	hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

	lower_range = np.array([0,0,200])
	upper_range = np.array([255,255,255])

	mask = cv2.inRange(hsv, lower_range, upper_range)
	dst = cv2.bitwise_and(src, src, mask=mask)
	mask_inv = cv2.bitwise_not(mask)
	dst_inv = cv2.bitwise_and(src, src, mask=mask_inv)
	new_src = src.copy()
	a = np.zeros((height, width), dtype=np.uint32)

	i,j = (mask != 0).nonzero()
	#k =((new_src[i,j,2] > 235) != 0).nonzero()
	#print(i[k],j[k])
	a[i,j] = (np.uint32(new_src[i,j,0])+np.uint32(new_src[i,j,1])+np.uint32(new_src[i,j,2]))/3
	new_src[i,j] = np.tile(a[i,j],(3,1)).T

	cv2.imwrite(name+added_prefix+".jpg", new_src)
	shutil.copyfile(name+".txt", name+added_prefix+".txt")

	'''
	cv2.imshow("src",src)
	cv2.moveWindow("src",0,0)
	cv2.imshow("dst_inv",dst_inv)
	cv2.moveWindow("dst_inv",640,0)
	cv2.imshow("dst",dst)
	cv2.moveWindow("dst",640,500)
	cv2.imshow("new_src",new_src)
	cv2.moveWindow("new_src",0,500)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	'''
	list.remove(name)

input("Press Enter to exit...")
