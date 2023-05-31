import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from easyocr import Reader
import cv2

car = cv2.imread("car1.jpg")
car = cv2.resize(car , (800, 600))

gray = cv2.cvtColor(car, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (5,5), 0)

edged = cv2.Canny (blur , 10, 200)

cont , _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cont = sorted(cont ,key =cv2.contourArea, reverse= True )

for c in cont : 
    arc = cv2.arcLength(c , True)
    approx = cv2.approxPolyDP(c, 0.02 * arc , True)
    if len(approx) == 4 :
        plate_cnt = approx 
        break
(x, y , w, h ) = cv2.boundingRect(plate_cnt)
plate = gray [y : y + h , x : x + w ]
    
reader = Reader (['en'] , gpu = False , verbose = False)
detection = reader.readtext(plate)


print(detection)

if len(detection) == 0 :
    text = 'Impossible to read the text from the license plate'
    cv2.putText(car, text, (20,40), cv2.FONT_HERESHY_SIMPLEX , 0.75 , (0,0,255), 3)
    cv2.imshow("image", car)
    cv2.waitKey(0)
    
else :
    cv2.drawContours(car , [plate_cnt], -1 , (0,255,0), 3)    
    text = f'{detection[0][1]} {detection[0][2] * 100 : .2f}%'
    cv2.putText(car, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    
    cv2.imshow('image', car)
    cv2.waitKey(0)