import pyautogui
#pyautogui.screenshot("ftem.png",region=(380,770,100,25))

try:
    import Image

except ImportError:
    from PIL import Image

import pytesseract

tem=pytesseract.image_to_string(Image.open("ftem.png"))
tem=tem.split("°")
print(tem[0])
