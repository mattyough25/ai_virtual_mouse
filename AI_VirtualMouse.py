import cv2
import numpy as np
import time
import HandTrackingModule as htm
import autopy

wCam, hCam = 640,480
frameR = 100
smoothening = 5

plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
while True:
    # Find Hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Check which fingers are up
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR),(wCam-frameR, hCam-frameR),
                          (255,0,255),2)
        # Only Index Finger - in moving mode
        if fingers[1] == 1 and fingers[2] == 0:
            # Convert Coordinates
            
            x3 = np.interp(x1, (frameR, wCam-frameR), (0,wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0,hScr))

            # Smoothen Values
            clocX = plocX + (x3-plocX)/smoothening
            clocY = plocY + (y3-plocY)/smoothening

            # Move Mouse
            autopy.mouse.move(wScr-clocX, clocY)
            cv2.circle(img, (x1, y1),15,(255,0,255),cv2.FILLED)
            plocX, plocY = clocX, clocY
        # Both Index and Middle Fingers are Up - clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            # Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
             # Click mouse if distance is short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),15,(0,255,0),cv2.FILLED)  
                autopy.mouse.click()
                    
        

       

    # Display
    cv2.imshow("Image", img)

    # Enter key 'q' to break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

