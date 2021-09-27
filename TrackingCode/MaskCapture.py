# 얼굴 이미지를 입력받아 마스크 착용 여부 검출, 촬영하는 프로그램
# 10프레임마다 촬영함
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os

# readNet으로 모델 읽기 -> 하나의 Net 객체 반환
facenet = cv2.dnn.readNet('models/deploy.prototxt', 'models/res10_300x300_ssd_iter_140000.caffemodel')
model = load_model('models/mask_detector.model')

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("카메라를 실행할 수 없습니다.")
    exit()


path_mask = './TestDetector/mask/'
path_nomask = './TestDetector/nomask/'
# TestDetector를 제거할 일이 잦아서 추가한 코드, 정식 릴리즈시엔 제거해도 상관 없음
if not os.path.exists(path_mask):
    print('mask 폴더가 없습니다.')
    os.makedirs(path_mask)
    print(f'\'{path_mask}\' 위치에 mask 폴더를 생성했습니다.')
if not os.path.exists(path_nomask):
    print('nomask 폴더가 없습니다.')
    os.makedirs(path_nomask)
    print(f'\'{path_nomask}\' 위치에 nomask 폴더를 생성했습니다.')

cam_cnt = 0 # 프레임 가산
pic_num = 0 # 사진 파일 이름

while True:
    ret, img = cam.read()

    if ret == False:    
        break

    h, w, c = img.shape
    # 이미지 전처리하기
    # blobFromImage; 이미지를 가지고 4차원의 blob 만들기, resize 포함
    blob = cv2.dnn.blobFromImage(img, size=(300, 300), mean=(104., 177., 123.))

    # 얼굴 영역 탐지 모델로 추론하기
    # blob를 신경망에 추가, setInput으로 입력받기
    # forward() 통해 신경망이 학습데이터 입력받은 후 forward propagation 진행
    facenet.setInput(blob)
    dets = facenet.forward()

    # 각 얼굴에 대해서 반복문 돌기
    for i in range(dets.shape[2]):
        confidence = dets[0, 0, i, 2]

        if confidence < 0.5:    # min_confidence
            continue

        # 사각형 꼭지점 찾기
        # 아래는 x1 = int(dets[0, 0, i, 3] * w) 형식을 수정한 것
        box = dets[0,0,i,3:7]*np.array([w, h, w, h])
        (x1,y1,x2,y2) = box.astype('int')

        face = img[y1:y2, x1:x2]

        # <전처리>
        # resizing, BGR->RGB, 전처리 연산, 차원 변형
        face_input = cv2.resize(face, dsize=(224, 224))
        face_input = cv2.cvtColor(face_input, cv2.COLOR_BGR2RGB)
        face_input = preprocess_input(face_input)
        face_input = np.expand_dims(face_input, axis=0)

        mask, nomask = model.predict(face_input).squeeze()
        cam_cnt += 1

        if mask > nomask:
            if cam_cnt % 10 == 0:
                pic_num += 1
                face_slice = img[y1:y2, x1:x2, :]
                cv2.imwrite('./TestDetector/mask/mask'+str(pic_num)+'.jpg', face_slice)
            
            color = (0, 255, 0)
            cv2.putText(img, text='%.2f'%mask, org=(x1, y1), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=color)
        else:
            if cam_cnt % 10 == 0:
                pic_num += 1
                face_slice = img[y1:y2, x1:x2, :]
                cv2.imwrite('./TestDetector/nomask/nomask'+str(pic_num)+'.jpg', face_slice)
            color = (0, 0, 255)
            cv2.putText(img, text='%.2f'%mask, org=(x1, y1), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=color)
            
        # 사각형 그리기
        cv2.rectangle(img, pt1=(x1, y1), pt2=(x2, y2), thickness=2, color=color)

    cv2.imshow('result', img)
    if cv2.waitKey(1) == ord('q'):
        break