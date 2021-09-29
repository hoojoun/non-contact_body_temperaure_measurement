# 테스트용 하르 분류기
# 시간 체크용, commit에서 제거해도 무방함

import cv2
import time

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
after_time = time.time() # 초기값 (구동 시간)

# 계산식
cnt = 0 # counter
sum_term_time = 0
sum_lead_time = 0

while cap.isOpened():    
    ret, img = cap.read()
    if ret:
        start_time = time.time() # 처음 시작시 시간 저장용
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 얼굴 검출
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(80,80))
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255,0),2)
            roi = gray[y:y+h, x:x+w]
            # 눈 검출
            eyes = eye_cascade.detectMultiScale(roi)
            for i, (ex, ey, ew, eh) in enumerate(eyes):
                if i >= 2:
                    break
                cv2.rectangle(img[y:y+h, x:x+w], (ex,ey), (ex+ew, ey+eh), (255,0,0),2)

                term_time = time.time()-after_time
                print(f'term : {term_time}')  # 다음 얼굴 인식까지 걸리는 시간
                sum_term_time += term_time
                lead_time = time.time()-start_time  # 현재 시각 - 얼굴 인식할 때 시간 = 얼굴 인식할 때 걸리는 시간

                print(f'time : {lead_time}\n')
                sum_lead_time += lead_time
                after_time = time.time() # 얼굴 인식 끝나고 시간 저장
                cnt += 1
        cv2.imshow('face detect', img)
    else:
        break
    if cv2.waitKey(1) == ord('q'):
        print(f'평균 인식 시간 : {sum_term_time/cnt}, 평균 인식 간격 : {sum_lead_time/cnt}')
        break
cv2.destroyAllWindows()