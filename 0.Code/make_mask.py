import cv2
import os
import argparse


parser = argparse.ArgumentParser(description='make_mask')
parser.add_argument('--src_name', default='', help='name of soure image')
args = parser.parse_args()

src = cv2.imread(args.src_name)

gray_src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(gray_src, 10, 1, cv2.THRESH_BINARY)

src_name, src_extension = os.path.splitext(args.src_name)
cv2.imwrite(src_name + '_mask.png', mask)
'''
cv2.imshow('mask', mask)
cv2.waitKey()
'''