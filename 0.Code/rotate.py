import os
import random
import glob
import cv2
import numpy as np

current_dir = os.getcwd()
cnt = 0
cnt1 = 0

###FIXME
added_prefix = "_rotate"
# from 0 to 255, choose appropriate value for finding contour(depends on the color of the object)
threshold_value = 15

####Process
list = []
for f_path in glob.iglob(os.path.join(current_dir, "*.jpg")):
	title, ext = os.path.splitext(os.path.basename(f_path))
	list.append(title)

print("Total %d images" %len(list))

while list:
	name = random.choice(list)
	cnt1 += 1
	if(cnt1%100==0):
		print(cnt1)
	src = cv2.imread(name+".jpg", cv2.IMREAD_COLOR)
	
	theta = random.randint(0,359)
	height, width, channel = src.shape
	
	shift_x, shift_y = 0,9
	f = open(name+".txt", "r")
	txtfile = f.readlines()
	for line in txtfile:
		contents = line.split()
		shift_x = int((0.5-float(contents[1]))*width)
		shift_y = int((0.5-float(contents[2]))*height)
	f.close()
	
	matrix_shift = np.float32([[1,0,shift_x],[0,1,shift_y]])
	shift = cv2.warpAffine(src, matrix_shift, (width, height))

	matrix_rotate = cv2.getRotationMatrix2D((width/2, height/2), theta, 1)
	dst = cv2.warpAffine(shift, matrix_rotate, (width, height))
	
	gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
	gray = cv2.erode(gray, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
	gray = cv2.dilate(gray, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
	gray = cv2.dilate(gray, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
	gray = cv2.erode(gray, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
	ret, binary = cv2.threshold(gray,threshold_value,255,cv2.THRESH_BINARY)
	NULL, contours, hierachy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	if(len(contours) == 0):
		cnt += 1
		print(name)
		list.remove(name)
		continue
	
	#sel = binary == 0
	#dst = cv2.drawContours(dst,contours, 0, (0,0,255), 1)
	err_flag = 0
	for point in contours[0]:
		a = point[0][0]
		b = point[0][1]
		binary[b][a] = 0
		if(b == 0 or b == height-1 or a == 0 or a == width-1):
			err_flag = 1
			break
	if(err_flag == 1):
		print(name)
		list.remove(name)
		continue
		
	for point in contours[0]:
		a = point[0][0]
		b = point[0][1]
		if(binary[b-1][a] == 255):
			dst[b][a] = dst[b-1][a]
		elif(binary[b+1][a] == 255):
			dst[b][a] = dst[b+1][a]
		elif(binary[b][a+1] == 255):
			dst[b][a] = dst[b][a+1]
		elif(binary[b][a-1] == 255):
			dst[b][a] = dst[b][a-1]

	cv2.imwrite(name+added_prefix+".jpg", dst)
	
	x,y,w,h = cv2.boundingRect(contours[0])
	x_new = (x+w/2)/width
	y_new = (y+h/2)/height
	w_new = w/width
	h_new = h/height

	f = open(name+".txt", "r")
	txtfile = f.readlines()
	
	g = open(name+added_prefix+".txt", "w")
	for line in txtfile:
		contents = line.split()
		new_content = contents[0]+" "+str(x_new)+" "+str(y_new)+" "+str(w_new)+" "+str(h_new)+"\n";
		g.write(new_content)
	f.close()
	g.close()

	'''
	white = dst.copy()
	white[sel] = (255,255,255)
	cv2.rectangle(dst, (x,y), (x+w,y+h), (0,255,0), 2)
	cv2.imshow("src",src)
	cv2.moveWindow("src",0,0)
	cv2.imshow("white",white)
	cv2.moveWindow("white",640,0)
	cv2.imshow("dst",dst)
	cv2.moveWindow("dst",0,500)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	'''

	list.remove(name)

print("%d images undetected" %cnt)
input("Press Enter to exit...")
