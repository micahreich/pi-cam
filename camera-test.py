import numpy as np
import cv2

lower = np.array([170,100,50])
upper = np.array([180,255,255])


def get_masked(img):
    hlsFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hlsFrame, lower, upper)
    mask = cv2.dilate(mask, (np.ones((15, 15), 'uint8')))
    
    res_mask = cv2.bitwise_and(img, img, mask=mask)
    return res_mask

def get_camera():
    for camera_idx in range(10):
        cap = cv2.VideoCapture(camera_idx)
        if cap.isOpened():
            print(camera_idx)
            return cap

cap = get_camera()
while(True):
    ret, frame = cap.read()
    
    if frame is None:
        cap = get_camera()
        continue

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    light = get_masked(frame[340:370, 625:])
    cv2.imshow('frame', light)

    if np.sum(np.mean(light, axis=(0, 1))) == 0:
        print("GREEN")
    else:
        print("RED")
    
cap.release()
cv2.destroyAllWindows()
