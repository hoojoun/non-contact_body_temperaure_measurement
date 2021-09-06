# 마스크 검출 예제

import cvlib as cv
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array   # PIL -> Numpy
from PIL import ImageFont, ImageDraw, Image

model = load_model('TestDetector/testmodel.h5')
model.summary() # 모델 구조 요약해서 출력

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("실행 가능한 카메라가 없습니다.")
    exit()

while cam.isOpened():
    status, frame = cam.read()  # ret, img
    
    if not status:  # ret==false
        print("다음 프레임을 읽을 수 없습니다.")
        exit()
 
    # opencv 내장 얼굴인식 함수
    face, confidence = cv.detect_face(frame)   
 
    # 얼굴인식
    for idx, pos in enumerate(face):    # number, position_tmp
        
        (startX, startY) = pos[0], pos[1]
        (endX, endY) = pos[2], pos[3]
        
        # start, end 좌표가 img(0~max_img) 안에 있는지 
        if 0 <= startX <= frame.shape[1] and 0 <= endX <= frame.shape[1] and 0 <= startY <= frame.shape[0] and 0 <= endY <= frame.shape[0]:
            
            face_region_origin = frame[startY:endY, startX:endX]
            # 보간법 지정; 영상 축소시 효과적인 보간법
            face_region = cv2.resize(face_region_origin, (224, 224), interpolation = cv2.INTER_AREA)
            
            x = img_to_array(face_region)   # PIL -> Numpy
            x = np.expand_dims(x, axis=0)   # 차원 추가
            x = preprocess_input(x) # 전처리
            
            prediction = model.predict(x)   # 모델 불러와서 예측
 
            if prediction < 0.5: # 마스크 미착용/
                cv2.rectangle(frame, (startX,startY), (endX,endY), (0,0,255), 2)
                Y = startY - 10 if startY - 10 > 10 else startY + 10    # 범위 조정, 없어도 괜찮음
                text = "No Mask ({:.2f}%)".format((1 - prediction[0][0])*100)
                cv2.putText(frame, text, (startX,Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                
            else: # 마스크 착용
                cv2.rectangle(frame, (startX,startY), (endX,endY), (0,255,0), 2)
                Y = startY - 10 if startY - 10 > 10 else startY + 10    # 범위 조정, 없어도 괜찮음
                text = "Mask ({:.2f}%)".format(prediction[0][0]*100)
                cv2.putText(frame, text, (startX,Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                
    # 결과 출력
    cv2.imshow("mask classify", frame)
    if cv2.waitKey(1) == ord('q'):
        break
    
# 카메라 사용 종료
cam.release()
cv2.destroyAllWindows() 