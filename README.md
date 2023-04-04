# GraduationProject

무인 점포를 위한 영상내 객체 인식 및 추적용 딥러닝 알고리즘 개발

## Abstract
본 연구는 무인 점포를 위한 영상내 객체 인식 및 추적용 딥러닝 알고리즘 개발을 목표로 한다. 

객체 인식 딥러닝 모델은 YOLOv3를 선택하였으며, framework로는 darknet을 선택하였다. 

본 연구에서는 크게 두 가지 단계로 나뉘어 진행되었는데 train을 위한 dataset을 만드는 Auto-labeling 과정과 

단일 카메라로만 진행되는 기존 객체 인식 모델의 한계점을 보완하는 과정으로 진행되었다.

## Auto-labeling

더 빠르고 많은 data를 얻기 위해 컴퓨터 프로그램이 만든 image에 대하여 자동으로 bounding box를 만드는 auto-labeling 방식을 사용했다(오른쪽)

![image](https://user-images.githubusercontent.com/37990408/229814018-d83c1bf4-1f5f-4173-9b69-8033d73ec92c.png)

## Data augmentation
무인 점포의 환경에 따라 다양하게 변하는 data에 대응하기 위하여 기존 data에 대하여 다양한 data augmentation을 적용하여 data의 다양성을 증가시켰다

![image](https://user-images.githubusercontent.com/37990408/229814644-1f24eb1e-a2c1-41ca-9981-13e5f7572002.png)

(a. orginal, b. color change, c. gamma change, d. hsv change, e. size change, f. rotation)

## GP-GAN with content loss
기존 image 합성 방식의 경우 original image의 테두리가 배경과의 괴리를 만드는 문제가 발생, 이를 방지하고자 GP-GAN을 이용한 image 합성을 시도했지만 

반대로 background의 content가 foreground image에 반대로 합성되는 문제가 발생. 

이에 대한 해결책으로 content loss를 도입하여 foreground image의 content loss를 최소화하며 이미지를 합성하는 것이 가능함. 

하지만 전체적으로 foreground image가 어두워지고 background 이미지의 경우 그림자가 진 것처럼 변화함.

![image](https://user-images.githubusercontent.com/37990408/229816345-752738da-1780-4dd5-a972-836cb8ca3e13.png)

(순서대로 troublsesome data, GP-GAN data, GP-GAN with content loss data)

GP-GAN 이외에도 cut-and-paste에서 생기는 문제를 해결하기 위하여 기존 image를 투명도 alpha channel을 사용하기 위하여 png 파일로 변환한 뒤에 

변환한 png 파일을 python library를 사용하여 깔끔하게 background를 제거한 뒤 cut-and-paste하는 방식 또한 사용하였다.


## Single Camera

Unified dataset을 사용하여 학습시킨 모델을 single camera 환경에서 객체 인식 실험을 진행하였고 single camera의 몇가지 문제점을 확인할 수 있었다.

첫째로 single camera는 시점이 한 방향으로 고정되어 있어 물체가 뒤에 가려질 경우 해당 물체가 일부 또는 전체가 사라진 것으로 인식한다.

둘째로 특정 물체의 뒷면은 특징이 약하기 때문에 학습한 모델이 잘 인식하지 못하는 경우가 발생한다.

마지막으로 몇가지 물체의 경우 서로 비슷하여 특정 각도나 빛에 따라 모델이 오인식하는 경우가 발생한다.

![image](https://user-images.githubusercontent.com/37990408/229845666-56135c11-0d49-4f97-b08c-75d0c8e901a9.png)

( a,b. 물체의 방향에 따라 인식이 어려운 경우, c. 서로 비슷하여 구별이 어려운 경우, d,e. 카메라의 사각에 의해 가려진 경우)

이러한 single camera의 문제점을 해결하기 위하여 아래와 같은 두가지 method를 사용하였다.

## Weight sensor and Arduino

물체의 오인식과 미인식을 방지하기 위하여 실제 한국의 무인 점포인 언커몬 스토어에서도 사용하고 있는 weight sensor를 사용하기로 하였다. 

Arduino에 연결된 4개의 weight sensor를 상품 진열대의 아래에 배치하여 실시간으로 물체의 무게를 확인할 수 있게 하였다. 

우선은 각각의 물체의 무게를 측정한 뒤에 해당 물체의 오차 범위 10g 이내의 물체들의 후보를 Arduino의 프로그램에 입력하였다. 

이를 통해 weight sensor가 빠져나가거나 추가된 무게를 인식하여 현재 빠져나가거나 들어온 물체의 후보를 출력하는 것이 가능하게 되었다. 

이는 비슷하게 생겼으나 무게가 다른 물체를 구분하거나, 새로운 물체가 들어와 기존 물체를 가려 

물체가 빠져나가는 것으로 오인식하는 것을 방지할 수 있게 만들어 주었다.

## Multi Camera

Weight sensor에 더불어 기존 single camera의 한계를 보완하기 위하여 다양한 각도에서 상품을 탐색할 수 있는 multi camera 방식을 도입하였다. 

Multi camera 방식을 도입함에 따라 기존 single camera의 사각에 숨겨진 물체를 인식하거나, 

물체의 뒷면이나 옆면만으로 인식이 어려운 물체에 대한 인식이 가능하게 됨을 확인할 수 있었다.

실험 환경에서는 판매대의 정면 카메라에 더불어 판매대의 왼쪽과 오른쪽에 카메라를 설치하여 기존 카메라의 사각지대를 보완하였다.

![image](https://user-images.githubusercontent.com/37990408/229846746-72838479-54b2-4b9e-bc32-865a2107bfd7.png)


## Result

### Dataset의 인식률 비교

총 6가지의 dataset의 인식률을 비교하기 위하여 YOLOv3의 darknet에서 mAP(mean Average Precision)을 측정하였다.

|Dataset|mAP|
|------|---|
|Human-labeled dataset|82.68%|
|Cut-and-Paste auto-labeled dataset|42.30%|
|Data augmented dataset|49.26%|
|GP-GAN with content loss dataset|55.78%|
|Background subtraction by PNG dataset|62.77%|
|Unified dataset|86.92%|

### 이벤트 측정에 의한 실제 인식률 비

 Single camera model과 weight sensor, multi camera model의 인식률을 측정하기 위하여 실제 판매대에서 실험을 진행하였다.
 
물체가 빠져나가거나 들어오는 것을 하나의 event로 가정하여 각각의 event에 대해서 물체를 오인식 혹은 미인식하는 경우를 확인하였다. 

Weight sensor의 경우 물체가 빠져나가거나 들어왔을 때에 카메라가 인식한 물체가 weight sensor가 인식한 물체들의 후보에 있을 경우 

해당 물체를 제대로 인식한 event라 가정하였다. 

또한 multi camera의 경우 3개의 카메라에 대하여 weighted parameter와 threshold를 정하지 못했기에 

모든 카메라에서 오인식 혹은 미인식한 경우만 틀린 event라고 가정하였다. 

같은 동영상으로 같은 event에 대해 single camera, weight sensor, multi-camera, multi-camera with weight sensor로 테스트한 인식률은 다음과 같다.

|Method|accuracy|
|------|---|
|Single camera|73.61%|
|Weight Sensor with single camera|91.67%|
|Multi camera|83.33%|
|Weight Sensor with multi camera|95.83%|


### 결과 분석

Dataset의 인식률을 분석한 결과 unified dataset의 mAP가 86.92%로 가장 높았으며 

그 다음으로는 human-labeled dataset가 82.68%로 높은 것을 확인할 수 있다.

auto-labeled data만으로 구성된 dataset은 모두 human-labeled dataset보다는 mAP가 떨어진다. 

이는 이번 연구에서 사용한 방법만으로 만든 auto-labeled dataset은 human-labeled dataset을 대체할 수 있는 수준은 아니라는 것을 알 수 있다. 

그러나 이렇게 만든 auto-labeled dataset과 human-labeled dataset을 합친 unified dataset은 mAP가 증가하는 것을 확인할 수 있기에, 

auto-labeled dataset은 기존 양이 부족한 human-labeled dataset을 보조하는 데에 유의미한 효과를 만들 수 있다는 것을 알 수 있다.

Single camera의 단점을 보완한 multi-camera와 weight sensor의 경우 더 높은 인식률을 보이는 것을 확인할 수 있었으나 

multi camera, weight sensor 모두 객관적인 program을 통한 측정이 아닌 실험자에 의한 측정이 이뤄졌기에 

실험자의 주관이 들어갈 수 있다는 문제점이 아직 남아 있다.

하지만 이번 실험 결과를 통해 single camera의 문제점인 사각지대, 물체의 미인식과 오인식 등에 

두가지 방법 모두 인식률을 높이는 데에 유의미한 도움을 준다는 것을 알 수 있다.

## Overall View

[졸업 프로젝트 포스터.pdf](https://github.com/peardanny97/GraduationProject/files/11148431/_.pdf)
