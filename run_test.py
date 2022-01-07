import subprocess
from HW import thermalSensor
from HW import crollingThermal
from gtts import gTTS
import pygame
from HW import saveData
import time
import pyautogui
import os
import sys

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
from HW import movingMotor

def mainfun():
    # information
    try:
        exec(open("HW/qrCode.py").read())
    except SystemExit:
        pass
    f=open("qrbarcode_data.txt",'r')
    line=f.readline()
    line=line.split(" ")
    code=line[0]
    name=line[1]

    print("code="+code)
    print("name="+name)

    mlx,lepton=crollingThermal.calibratedTemperature()
    wrist=thermalSensor.checkWristTemperature()
    wrist=float(wrist)+float(mlx)
    wrist=round(wrist,2)
    print("wrist="+str(wrist))

    #if (float(wrist)>35.0 and float(wrist)<37.5):
    if(1==2):
        text=str(wrist)+"도 입니다. 정상입니다."
        tts=gTTS(text=text,lang='ko')
        tts.save("sound1.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("sound1.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy()==True:
            continue
        saveData.saveFireBase1(code,name,wrist)
    else:
        text=str(wrist)+"도 입니다. 비정상입니다. 얼굴로 재측정 하겠습니다."
        time.sleep(1)
        tts=gTTS(text=text,lang='ko')
        tts.save("sound2.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("sound2.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy()==True:
            continue
        movingMotor.upCamera()   
        try:
            exec(open("TrackingCode/landmark_5point.py").read())    
        except SystemExit:
            pass
        pyautogui.screenshot("ftem.png",region=(380,770,100,25))
        tem=pytesseract.image_to_string(Image.open("ftem.png")) 
        tem=tem.split("°")
        face=float(tem[0])+float(lepton)
        face=round(face,2)
        print("face="+str(face))

        #if (float(face)>35.0 and float(face)<37.5):
        if(1==2):
            text=str(face)+"도 입니다. 정상입니다."
            tts=gTTS(text=text,lang='ko')
            tts.save("sound3.mp3")
            pygame.mixer.init()
            pygame.mixer.music.load("sound3.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy()==True:
                continue
            saveData.saveFireBase1(code,name,wrist,face)
        else:
            text=str(face)+"도 입니다. 비정상입니다."
            tts=gTTS(text=text,lang='ko')
            tts.save("sound4.mp3")
            pygame.mixer.init()
            pygame.mixer.music.load("sound4.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy()==True:
                continue
            saveData.saveFireBase2(code,name,wrist,face)
            movingMotor.downCamera()
if __name__ == '__main__':
    mainfun()
    os.execv(__file__, sys.argv)

