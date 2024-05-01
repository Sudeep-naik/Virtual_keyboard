import cv2
import mediapipe
import math
from Modules import HandDetector
from time import sleep
detector= HandDetector(detectionCon=0.8)

cap=cv2.VideoCapture(0)

text=""
def draw(img,buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (223, 125, 68), cv2.FILLED)
        cv2.putText(img, button.text, (x + 8, y +30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    return img
class Button:
    def __init__(self,pos,text,size=[45,45]):
        self.pos=pos
        self.text=text
        self.size=size


# myButton=Button([50,50],"Q")
keys=[["Q","W","E","R","T","Y","U","I","O","P"],
      ["A","S","D","F","G","H","J","K","L"],
      ["Z","X","C","V","B","N","M",",",".","."]]

buttonList=[]
for i in range(len(keys)):
    for j,key in enumerate(keys[i]):
        buttonList.append(Button([50*j+80,60*i+20],key))


while True:
    sucess,img=cap.read()
    hands,img=detector.findHands(img,flipType=False,draw=True)
    img = draw(img, buttonList)
    if hands:
        hand1=hands[0]
        lmList1=hand1["lmList"]
        bbox1=hand1["bbox"]

        #if lmList1:
        for button in buttonList:
            x,y=button.pos
            w,h=button.size

            if x<lmList1[8][0]<x+w and y<lmList1[12][1]<y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (223, 94, 20), cv2.FILLED)
                cv2.putText(img, button.text, (x + 8, y + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                x1, y1 = lmList1[8][0],lmList1[8][1]
                x2, y2 = lmList1[12][0],lmList1[12][1]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                length = math.hypot(x2 - x1, y2 - y1)
                if length<26:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (223, 94, 20), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 8, y + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    text+=button.text
                    sleep(0.25)

    cv2.putText(img,text,(60,425),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),2)


    # cv2.rectangle(img,(50,50),(100,100),(0,255,0),cv2.FILLED)
    # cv2.putText(img,"Q",(65,85),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

    cv2.imshow("Image",img)
    k=cv2.waitKey(1)
    if k==ord('q'):
        break