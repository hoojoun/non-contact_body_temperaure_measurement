# 마스크 검출 예제

import cvlib as cv
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array   # PIL -> Numpy
from PIL import ImageFont, ImageDraw, Image
import time

try:
    model_path = 'TestDetector/testmodel.h5'
    model = load_model(model_path)
    model.summary() # 모델 구조 요약해서 출력
except OSError as e:
    print(f'{e}\nmodel이 없습니다.')
    exit()

recognition_flag = 0 # 마스크 인식 확인용 flag (임시)

cam = cv2.VideoCapture(0)
after_time = time.time() # 초기값 (구동 시간)

# 평균 시간 계산식
cnt = 0 # counter
sum_term_time = 0
sum_lead_time = 0

if not cam.isOpened():
    print("실행 가능한 카메라가 없습니다.")
    exit()

while cam.isOpened():
    status, frame = cam.read()  # ret, img
    
    if not status:  # ret==false
        print("다음 프레임을 읽을 수 없습니다.")
        exit()
 
    start_time = time.time() # 처음 시작시 시간 저장용
    # opencv 내장 얼굴인식 함수
    face, confidence = cv.detect_face(frame)   
 
    # 얼굴인식
    for idx, pos in enumerate(face):    # number, position_tmp
        start_time = time.time() # 처음 시작시 시간 저장용
        (startX, startY) = pos[0], pos[1]
        (endX, endY) = pos[2], pos[3]
        roi_center = (pos[1]+pos[3])/2  # y좌표만 보유 (액추에이터는 상하운동만 가능)
        
        # start, end 좌표가 img(0~max_img) 안에 있는지 
        if 0 <= startX <= frame.shape[1] and 0 <= endX <= frame.shape[1] and\
           0 <= startY <= frame.shape[0] and 0 <= endY <= frame.shape[0]:
            
            face_region_origin = frame[startY:endY, startX:endX]
            # 보간법 지정; 영상 축소시 효과적인 보간법
            face_region = cv2.resize(face_region_origin, (224, 224), interpolation = cv2.INTER_AREA)
            
            x = img_to_array(face_region)   # PIL -> Numpy
            x = np.expand_dims(x, axis=0)   # 차원 추가
            x = preprocess_input(x) # 전처리
            
            prediction = model.predict(x)   # 모델 불러와서 예측
            print(f'실행 시간 : {time.time()-start_time}')  # 현재 시각 - 얼굴 인식할 때 시간
 
            if prediction > 0.5: # 마스크 착용
                cv2.rectangle(frame, (startX,startY), (endX,endY), (0,255,0), 2)
                Y = startY - 10 if startY - 10 > 10 else startY + 10    # 범위 조정, 없어도 괜찮음
                text = "Mask ({:.2f}%)".format(prediction[0][0]*100)
                cv2.putText(frame, text, (startX,Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                
                if roi_center<frame.shape[0]/2:
                    print('move down')
                    recognition_flag = 1
                elif roi_center>frame.shape[0]/2:
                    print('move up')
                    recognition_flag = 1

            else: # 마스크 미착용
                cv2.rectangle(frame, (startX,startY), (endX,endY), (0,0,255), 2)
                Y = startY - 10 if startY - 10 > 10 else startY + 10    # 범위 조정, 없어도 괜찮음
                text = "No Mask ({:.2f}%)".format((1 - prediction[0][0])*100)
                cv2.putText(frame, text, (startX,Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                
                if roi_center<frame.shape[0]/2:
                    print('move down')
                    recognition_flag = 1
                elif roi_center>frame.shape[0]/2:
                    print('move up')
                    recognition_flag = 1
            
            term_time = time.time()-after_time
            print(f'term : {term_time}')  # 다음 얼굴 인식까지 걸리는 시간
            sum_term_time += term_time
            lead_time = time.time()-start_time  # 현재 시각 - 얼굴 인식할 때 시간 = 얼굴 인식할 때 걸리는 시간

            print(f'time : {lead_time}\n')
            sum_lead_time += lead_time
            after_time = time.time() # 얼굴 인식 끝나고 시간 저장
            cnt += 1
    if recognition_flag == 0:
        print('invalid recognition')
    recognition_flag = 0
                
                
    # 결과 출력
    cv2.imshow("mask classify", frame)
    if cv2.waitKey(1) == ord('q'):
        print(f'평균 인식 시간 : {sum_term_time/cnt}, 평균 인식 간격 : {sum_lead_time/cnt}')
        break
    
# 카메라 사용 종료
cam.release()
cv2.destroyAllWindows()