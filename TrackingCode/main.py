#five point model with dlib
import cv2
import dlib

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('models/shape_predictor_5_face_landmarks.dat')

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, img = cap.read()

    if ret:
        dets = detector(img)
        for det in dets:
            shape = predictor(img, det) # 랜드마크 저장, point; (전체 이미지 프레임, 얼굴 영역 좌표)
            
            # 점의 순서를 알아내기 위함; enumerate를 for문에서 사용할 경우 순서와 값을 동시에 출력함
            for i, point in enumerate(shape.parts()):
                cv2.circle(img, center=(point.x, point.y), radius=2, color=(0, 0, 255), thickness=-1)   # 점 그리기
                cv2.putText(img, text=str(i+1), org=(point.x, point.y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(255, 255, 255), thickness=2)

            try:
                x1 = det.left()
                y1 = det.top()
                x2 = det.right()
                y2 = det.bottom()

                cv2.rectangle(img, pt1=(x1, y1), pt2=(x2, y2), color=(255, 0, 0), thickness=2)
            except:
                pass
        cv2.imshow('result', img)
        
    if cv2.waitKey(1) == ord('q'):
        break
