import mediapipe as mp
import cv2
import pyautogui
import time
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
mpHands = mp.solutions.hands
hands = mpHands.Hands(False,1,1,0.5,0.5)
mpDraw = mp.solutions.drawing_utils
pTime =0
cTime =0
fps=10.0
prev_pos = "neutral"
x = 500
y = 500
while True:
    lmList =[]
    success,img =vid.read()
    img = cv2.flip(img,1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
    if len(lmList)!=0:
        x,y = lmList[9][1],lmList[9][2]
        cv2.circle(img, (x,y), 12, (0,255,0),cv2.FILLED)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.line(img, (450,250), (450,470),(255,0,0),3)
    cv2.line(img, (830,250), (830,470),(255,0,0),3)
    cv2.line(img, (450,250), (830,250),(255,0,0),3)
    cv2.line(img, (450,470), (830,470),(255,0,0),3)
    cv2.putText(img, str(int(fps)),(10,70), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),2,cv2.LINE_AA)
    
    if x < 450:
        curr_pos = "left"
    elif x > 830:
        curr_pos = "right"
    elif y < 250 and x > 450 and x < 830:
        curr_pos = "up"
    elif y > 470 and x > 450 and x < 830:
        curr_pos = "down"
    else:
        curr_pos = "neutral"
    if curr_pos!=prev_pos:
        if curr_pos != "neutral":
          prev_pos = curr_pos
    print(curr_pos)
    pyautogui.press(curr_pos)
    cv2.imshow("Frame",img)
    q = cv2.waitKey(1)
    if q ==ord(' ') or q==27:
       break
vid.release()
cv2.destroyAllWindows()