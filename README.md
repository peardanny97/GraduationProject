# GraduationProject

무인 점포를 위한 영상내 객체 인식 및 추적용 딥러닝 알고리즘 개발

## Abstract
본 연구는 무인 점포를 위한 영상내 객체 인식 및 추적용 딥러닝 알고리즘 개발을 목표로 한다. 

객체 인식 딥러닝 모델은 YOLOv3를 선택하였으며, framework로는 darknet을 선택하였다. 

본 연구에서는 크게 두 가지 단계로 나뉘어 진행되었는데 train을 위한 dataset을 만드는 Auto-labeling 과정과 단일 카메라로만 진행되는 기존 객체 인식 모델의 한계점을 보완하는 과정으로 진행되었다.

## Auto-labeling

더 빠르고 많은 data를 얻기 위해 컴퓨터 프로그램이 만든 image에 대하여 자동으로 bounding box를 만드는 auto-labeling 방식을 취함(오른쪽)
![image](https://user-images.githubusercontent.com/37990408/229814018-d83c1bf4-1f5f-4173-9b69-8033d73ec92c.png)

## Data augmentation
무인 점포의 환경에 따라 다양하게 변하는 data에 대응하기 위하여 기존 data에 대하여 다양한 data augmentation을 적용하여 data의 다양성을 증가시킴

![image](https://user-images.githubusercontent.com/37990408/229814644-1f24eb1e-a2c1-41ca-9981-13e5f7572002.png)

(a. orginal, b. color change, c. gamma change, d. hsv change, e. size change, f. rotation)

## GP-GAN with content loss
기존 image 합성 방식의 경우 original image의 테두리가 배경과의 괴리를 만드는 문제가 발생, 이를 방지하고자 GP-GAN을 이용한 image 합성을 시도했지만 반대로 background의
content가 foreground image에 반대로 합성되는 문제가 발생. 
이에 대한 해결책으로 content loss를 도입하여 foreground image의 content loss를 최소화하며 이미지를 합성하는 것이 가능함. 
하지만 전체적으로 foreground image가 어두워지고 background 이미지의 경우 그림자가 진 것처럼 변화함.

![image](https://user-images.githubusercontent.com/37990408/229816345-752738da-1780-4dd5-a972-836cb8ca3e13.png)

(순서대로 troublsesome data, GP-GAN data, GP-GAN with content loss data)

Background subtraction

## Single Camera to

Multi Camera

Arduino & Weight Sensor


## Overall View

[졸업 프로젝트 포스터.pdf](https://github.com/peardanny97/GraduationProject/files/11148431/_.pdf)
