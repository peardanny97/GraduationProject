import sys
import os
import glob
import random
import numpy as np
from os import getcwd
from pathlib import Path
from PIL import Image
import xml.etree.ElementTree as Et
from xml.etree.ElementTree import Element, ElementTree
import collections
import cv2
import csv



number_of_objects = {
#    'person': 5447, 
    'car': 1644, 
    'chair': 1432, 
    'bottle': 634, 
    'pottedplant': 625, 
    'bird': 599, 
    'dog': 538, 
    'sofa': 425, 
    'bicycle': 418, 
    'horse': 406, 
    'boat': 398, 
    'cat': 389, 
    'motorbike': 390, 
    'tvmonitor': 367, 
    'cow': 356, 
    'sheep': 353, 
    'aeroplane': 331, 
    'train': 328, 
    'diningtable': 310, 
    'bus': 272
} 

object_list = []

def read_xml_save_mask(xml_path, img_path, path_dir_mask):
    #print("XML parsing Start\n")
    xml = open(xml_path, "r")
    tree = Et.parse(xml)
    root = tree.getroot()

    size = root.find("size")

    width = size.find("width").text
    height = size.find("height").text
    channels = size.find("depth").text

    objects = root.findall("object")
    
    for _object in objects:
        name = _object.find("name").text
        number_of_objects[str(name)] += 1
        bndbox = _object.find("bndbox")
        xmin = bndbox.find("xmin").text
        ymin = bndbox.find("ymin").text
        xmax = bndbox.find("xmax").text
        ymax = bndbox.find("ymax").text
        annot = xmin, ymin, xmax, ymax, name

        print("class : {}\nxmin : {}\nymin : {}\nxmax : {}\nymax : {}\n".format(name, xmin, ymin, xmax, ymax))
        
        img = cv2.imread(img_path)
        mask = np.zeros(img.shape[:2], dtype="uint8")
        cv2.rectangle(mask, (int(xmin), int(ymin)), (int(xmax), int(ymax)), 255, -1)
        masked = cv2.bitwise_and(img, img, mask=mask)
        class_dir = path_dir_mask + "/" + name
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)
        save_mask = class_dir +  "/" + name + "_" + str(number_of_objects[str(name)]) + ".jpg"
        print(save_mask)
        #cv2.imshow('image', masked)
        cv2.imwrite(save_mask, masked)
        create_xml(save_mask, annot)
        #cv2.waitKey(1)

    #print("XML parsing END")

def create_xml(path_name, annot):
    image_path = Path(path_name)
    img = np.array(Image.open(image_path).convert('RGB'))

    annotation = Et.Element('annotation')
    Et.SubElement(annotation, 'folder').text = 'VOC2007'
    Et.SubElement(annotation, 'filename').text = str(image_path.name)
    #Et.SubElement(annotation, 'path').text = str(image_path)

    size = Et.SubElement(annotation, 'size')
    Et.SubElement(size, 'width').text = str (img.shape[1])
    Et.SubElement(size, 'height').text = str(img.shape[0])
    Et.SubElement(size, 'depth').text = str(img.shape[2])

    Et.SubElement(annotation, 'segmented').text = '0'

    xmin, ymin, xmax, ymax, label = annot[0], annot[1], annot[2], annot[3], annot[4]

    object = Et.SubElement(annotation, 'object')
    Et.SubElement(object, 'name').text = label
    Et.SubElement(object, 'pose').text = 'Unspecified'
    Et.SubElement(object, 'truncated').text = '0'
    Et.SubElement(object, 'difficult').text = '0'

    bndbox = Et.SubElement(object, 'bndbox')
    Et.SubElement(bndbox, 'xmin').text = str(xmin)
    Et.SubElement(bndbox, 'ymin').text = str(ymin)
    Et.SubElement(bndbox, 'xmax').text = str(xmax)
    Et.SubElement(bndbox, 'ymax').text = str(ymax)

    tree = Et.ElementTree(annotation)
    xml_file_name = image_path.parent / (image_path.name.split('.')[0]+'.xml')
    tree.write(xml_file_name, method='xml')


def rand_aug(path_dir, rand, bg_path, save_path):
    xml_path = path_dir + '/' + rand + ".xml"
    img_path = path_dir + '/' + rand + ".jpg"

    xml = open(xml_path, "r")
    tree = Et.parse(xml)
    root = tree.getroot()

    size = root.find("size")
    width = size.find("width").text
    height = size.find("height").text
    channels = size.find("depth").text
    objects = root.findall("object")
    
    for _object in objects:
        name = _object.find("name").text
        number_of_objects[str(name)] += 1
        bndbox = _object.find("bndbox")
        xmin = bndbox.find("xmin").text
        ymin = bndbox.find("ymin").text
        xmax = bndbox.find("xmax").text
        ymax = bndbox.find("ymax").text
        annot = xmin, ymin, xmax, ymax, name

        img = cv2.imread(img_path)
        imH, imW, _ = img.shape
        bg_img = cv2.imread(bg_path)
        gen_img = cv2.resize(bg_img, dsize=(imW, imH), interpolation=cv2.INTER_AREA)
        mask = np.zeros(img.shape[:2], dtype="uint8")
        cv2.rectangle(mask, (int(xmin), int(ymin)), (int(xmax), int(ymax)), 255, -1)
        cv2.copyTo(img, mask, gen_img)
        #cv2.imshow('bg_img', gen_img)
        #cv2.waitKey(1) 

        class_dir = save_path + "/" + name
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)
        object_name = name + "_" + str(number_of_objects[str(name)])
        object_list.append(object_name)
        save_name = class_dir +  "/" + object_name + ".jpg"
        print(save_name)

        cv2.imwrite(save_name, gen_img)
        create_xml(save_name, annot)
 

def gen_aug_images():
    path_dir = sys.argv[1]
    path_dir_xml = path_dir + "/Annotations/"
    path_dir_img = path_dir + "/JPEGImages/"
    path_dir_mask = path_dir + "/MaskImages/"
    path_dir_aug = path_dir + "/AugImages/"
    if not os.path.exists(path_dir_mask):
        os.makedirs(path_dir_mask)
    if not os.path.exists(path_dir_aug):
        os.makedirs(path_dir_aug)
    bg_path_dir = "/home/vidzrox/data/VOCdevkit/EtraData/2.random_bg_image/"
    filename = "/home/vidzrox/data/VOCdevkit/VOC2007/ImageSets/Main/trainval.txt"
    save_class_csv = "./number_of_objects.csv"
    MAX_objects = 6000
    
    # Read trainset 
    list = []
    with open(filename) as file:
        for title in file:
            line = title.rstrip()
            list.append(line)

    while list:
        rand = random.choice(list) 
        xml_path = path_dir_xml + '/' + rand + ".xml"
        img_path = path_dir_img + '/' + rand + ".jpg"
        read_xml_save_mask(xml_path, img_path, path_dir_mask)
        list.remove(rand)
    
    print(number_of_objects)

    with open("./number_of_objects.csv", 'w') as f:
        w = csv.writer(f)
        w.writerow(number_of_objects.keys())
        w.writerow(number_of_objects.values())



    bg_list = []
    for f_path in glob.iglob(os.path.join(bg_path_dir, "*.jpg")):
        bg_list.append(f_path)

    for key in number_of_objects:
        count = MAX_objects - number_of_objects[key]
        print(key, ":" , str(count))
        mask_img_dir = path_dir_mask + "/" + key

        img_list = []
        for f_path in glob.iglob(os.path.join(mask_img_dir, "*.xml")):
            title, ext = os.path.splitext(os.path.basename(f_path))
            img_list.append(title)

        while (count > 0 ):
            rand = random.choice(img_list) 
            bg_rand = random.choice(bg_list) 
            bg_path = bg_rand
            rand_aug(mask_img_dir, rand, bg_path, path_dir_aug)
            print(count)
            count = count-1


    with open('aug_images.txt', 'w') as f:
        for item in object_list:
            f.write("%s\n" % item)

    cv2.destroyAllWindows()

def combine_dataset():
    filename = "/home/vidzrox/data/VOCdevkit/VOC2007/ImageSets/Main/trainval.txt"
    aug_images = "/home/vidzrox/data/VOCdevkit/aug_images.txt"
    gan_images = "/home/vidzrox/data/VOCdevkit/gan_images_new.txt"
    save_dataset = "/home/vidzrox/data/VOCdevkit/VOC2007/ImageSets/Main/trainval_aug.txt"
    save_dataset_gan = "/home/vidzrox/data/VOCdevkit/VOC2007/ImageSets/Main/trainval_gan_new.txt"

    list_1 = []
    with open(filename) as file:
        for title in file:
            line = title.rstrip()
            list_1.append(line)
    
    list_2 = []
    with open(aug_images) as file:
        for title in file:
            line = title.rstrip()
            list_2.append(line)

    list_3 = []
    with open(gan_images) as file:
        for title in file:
            line = title.rstrip()
            list_3.append(line)

    combine_list = list_1 + list_2
    random.shuffle(combine_list)
    
    with open(save_dataset, 'w') as f:
        for item in combine_list:
            f.write("%s\n" % item)

    combine_list1 = list_1 + list_3
    random.shuffle(combine_list1)
    
    with open(save_dataset_gan, 'w') as f:
        for item in combine_list1:
            f.write("%s\n" % item)

def run_gpgan(path_dir, rand, bg_rand, save_path):
    gpgan_run_dir = "/home/vidzrox/1.Projects/1.ActiveLearning/Tensorflow_GP-GAN/"
    model_checkpoint_path = '/home/vidzrox/1.Projects/1.ActiveLearning/Tensorflow_GP-GAN/save_folder/train1201/GP-GAN_2021-12-01-10-08-58.ckpt-5168595004'
    gpgan_python = "/home/vidzrox/.conda/envs/gpgan/bin/python"

    xml_path = path_dir + '/' + rand + '.xml'
    img_path = path_dir + '/' + rand + '.jpg'

    xml = open(xml_path, "r")
    tree = Et.parse(xml)
    root = tree.getroot()

    size = root.find("size")
    width = size.find("width").text
    height = size.find("height").text
    channels = size.find("depth").text
    objects = root.findall("object")
    
    for _object in objects:
        name = _object.find("name").text
        number_of_objects[str(name)] += 1
        bndbox = _object.find("bndbox")
        xmin = bndbox.find("xmin").text
        ymin = bndbox.find("ymin").text
        xmax = bndbox.find("xmax").text
        ymax = bndbox.find("ymax").text
        annot = xmin, ymin, xmax, ymax, name
        if ((int(xmax) - int(xmin)) > 64 and (int(ymax) - int(ymin)) > 64):
            print(annot)
            img = cv2.imread(img_path)
            cv2.imwrite('src_image.jpg', img)
            cv2.waitKey(0)
            imH, imW, _ = img.shape
            bg_img = cv2.imread(bg_rand)
            bg_img = cv2.resize(bg_img, dsize=(imW, imH), interpolation=cv2.INTER_AREA)
            mask = np.zeros(img.shape[:2], dtype="uint8")
            #cv2.rectangle(mask, (int(xmin), int(ymin)), (int(xmax), int(ymax)), 1, -1)
            x_min = int(xmin)
            x_max = int(xmax)
            y_min = int(ymin)
            y_max = int(ymax)
            center = (int(x_min + (x_max - x_min)/2), int(y_min + (y_max - y_min)/2))
            c_xr = (x_max - x_min)/2
            c_yr = (y_max - y_min)/2
            print(center, c_xr, c_yr)
            axes = (int(c_xr), int(c_yr))
            cv2.ellipse(mask, center, axes , 0, 0, 360, 1, -1)
     
            src_image = img_path
            dst_image = bg_img
            mask_image = mask
            object_list.append(rand)
            class_dir = save_path + "/" + name
            if not os.path.exists(class_dir):
                os.makedirs(class_dir)
            object_name = name + '_' + str(number_of_objects[str(name)])
            blended_image = class_dir + '/' + object_name + '.jpg'
            print(blended_image)
        

        
            cv2.imwrite('dst_image.jpg', dst_image)
            cv2.imwrite('GPMaskImage.jpg', mask_image)


            os.system(gpgan_python + ' ' + os.path.join(gpgan_run_dir, 'run_gp_gan.py') + \
                        ' --src_imag src_image.jpg' + \
                        ' --dst_image dst_image.jpg' + \
                        ' --mask_image GPMaskImage.jpg' + \
                        ' --blended_image ' + blended_image + \
                        ' --generator_path ' + model_checkpoint_path )

            create_xml(blended_image, annot)

def gen_gpgan_image():
    path_dir = sys.argv[1]
    path_dir_mask = path_dir + "/MaskImages/"
    MAX_objects = 2000

    bg_path_dir = "/home/vidzrox/data/VOCdevkit/EtraData/2.random_bg_image/"
    filename = "/home/vidzrox/data/VOCdevkit/VOC2007/ImageSets/Main/trainval.txt"
    save_path = path_dir + "/GPGANImages_1"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    bg_list = []
    for f_path in glob.iglob(os.path.join(bg_path_dir, "*.jpg")):
        bg_list.append(f_path)

    for key in number_of_objects:
        count = MAX_objects - number_of_objects[key]
        #print(key, ":" , str(count))
        mask_img_dir = path_dir_mask + "/" + key

        img_list = []
        for f_path in glob.iglob(os.path.join(mask_img_dir, "*.xml")):
            title, ext = os.path.splitext(os.path.basename(f_path))
            img_list.append(title)
        
        while (count > 0 ):
            rand = random.choice(img_list) 
            bg_rand = random.choice(bg_list) 
            run_gpgan(mask_img_dir, rand, bg_rand, save_path)
            print(count)
            count = count-1

    with open('gan_images_1.txt', 'w') as f:
        for item in object_list:
            f.write("%s\n" % item)
    

if __name__ == "__main__":
    #gen_aug_images()
    gen_gpgan_image()
    #combine_dataset()
    
"""

'person': 5447, 
'car': 1644, 
'chair': 1432, 
'bottle': 634, 
'pottedplant': 625, 
'bird': 599, 
'dog': 538, 
'sofa': 425, 
'bicycle': 418, 
'horse': 406, 
'boat': 398, 
'cat': 389, 
'motorbike': 390, 
'tvmonitor': 367, 
'cow': 356, 
'sheep': 353, 
'aeroplane': 331, 
'train': 328, 
'diningtable': 310, 
'bus': 272


"""