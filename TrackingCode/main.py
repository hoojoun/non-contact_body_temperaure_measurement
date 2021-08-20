#five point model with dlib
import cv2
import dlib

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')

cap = cv2.VideoCapture(0) # 'imgs/01.mp4'
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# print('original size: %d, %d' % (width, height))

while cap.isOpened():
    ret, img = cap.read()

    if ret:
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
                if roi_center[1]<cap_center[1]:
                    print('move down')
                elif roi_center[1]>cap_center[1]:
                    print('move up')
                if roi_center[0]<cap_center[0]:
                    print('move right')
                elif roi_center[0]>cap_center[0]:
                    print('move left')
                
            try:
                x1 = face.left()
                y1 = face.top()
                x2 = face.right()
                y2 = face.bottom()

                cv2.rectangle(img, pt1=(x1, y1), pt2=(x2, y2), color=(255, 0, 0), thickness=2)
                print('check')
            except:
                pass
        
        
    if cv2.waitKey(1) == ord('q'):
        break
