# five point model with dlib
# 마스크를 쓴 상태에선 인식 안됨
# 분기 만들어서 재사용할지 현재 고민중

import cv2
import dlib
import time

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('models/shape_predictor_5_face_landmarks.dat')

cap = cv2.VideoCapture(0)
after_time = time.time() # 초기값 (구동 시간)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# print('original size: %d, %d' % (width, height))

# 계산식
cnt = 0 # counter
sum_term_time = 0
sum_lead_time = 0

while cap.isOpened():
    ret, img = cap.read()

    if ret:
        start_time = time.time() # 처음 시작시 시간 저장용
        faces = detector(img)
        for face in faces:  # 얼굴 감지
            shape = predictor(img, face) # 랜드마크 저장 (전체 이미지 프레임, 얼굴 영역 좌표)
            
            # 점의 순서를 알아내기 위함; enumerate를 for문에서 사용할 경우 순서와 값을 동시에 출력함
            for i in shape.parts():
                cv2.circle(img, center=(i.x, i.y), radius=2, color=(0, 0, 255), thickness=-1)   # 점 그리기, BGR
                y_start = (shape.part(3).y+shape.part(1).y)/2-(shape.part(0).x-shape.part(1).x-shape.part(2).x+shape.part(3).x)/2   #3.x~1.x - 평균 눈크기
                y_end = (shape.part(3).y+shape.part(1).y)/2+(shape.part(0).x-shape.part(1).x-shape.part(2).x+shape.part(3).x)/2     #3.x~1.x + 평균 눈크기
                cv2.rectangle(img, (shape.part(3).x,int(y_start)), (shape.part(1).x,int(y_end)), color=(255, 255, 255), thickness=1)
                roi_center = ((shape.part(3).x+shape.part(1).x)/2,(shape.part(3).y+shape.part(1).y)/2)
                cap_center = (width/2, height/2)
                # print(shape.part(1), shape.part(1).x, shape.part(1).y, roi_center, cap_center)
                """
                if roi_center[1]<cap_center[1]:
                    print('move down')
                elif roi_center[1]>cap_center[1]:
                    print('move up')
                if roi_center[0]<cap_center[0]:
                    print('move right')
                elif roi_center[0]>cap_center[0]:
                    print('move left')
                """
            try:
                x1 = face.left()
                y1 = face.top()
                x2 = face.right()
                y2 = face.bottom()

                cv2.rectangle(img, pt1=(x1, y1), pt2=(x2, y2), color=(255, 0, 0), thickness=2)

                term_time = time.time()-after_time
                print(f'term : {term_time}')  # 다음 얼굴 인식까지 걸리는 시간
                sum_term_time += term_time
                lead_time = time.time()-start_time  # 현재 시각 - 얼굴 인식할 때 시간 = 얼굴 인식할 때 걸리는 시간

                print(f'time : {lead_time}\n')
                sum_lead_time += lead_time
                after_time = time.time() # 얼굴 인식 끝나고 시간 저장
                cnt += 1
            except:
                pass
        cv2.imshow('result', img)
        
    if cv2.waitKey(1) == ord('q'):
        print(f'평균 인식 시간 : {sum_term_time/cnt}, 평균 인식 간격 : {sum_lead_time/cnt}')
        break