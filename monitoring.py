import time
from enum import Enum
import numpy as np
import cv2

class TrafficColor(Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2
    UNKNOWN = 3

#use param self.currState and self.changeDelta
#maybe want to have the region in the image?
class TrafficLight:
    # change buffer is how many times to soft_change_state need
    # to be called for enough confidence for light to be that color
    def __init__(self, initialState=TrafficColor.UNKNOWN, changeBuffer=5):
        self.currState = initialState
        self.lastChangeTime = time.time()
        self.changeDelta = 0
        self.changeBuffer = changeBuffer
        self.softChangeInfo = (TrafficColor.UNKNOWN, 0)

    def hard_change_state(self, state):
        self.currState = state
        currTime = time.time()
        #just in case lol
        self.changeDelta = currTime - self.lastChangeTime
        self.lastChangeTime = currTime
        self.softChangeInfo = (state, 0)

    def soft_change_state(self, state):
        if self.currState == TrafficColor.UNKNOWN:
            self.hard_change_state(state)
        
        # if the current reading is the same as the current state ignore
        if state == self.currState:
            self.softChangeInfo = (state, 0)
            return
        # if the state has changed from what was expected, set to 0
        if self.softChangeInfo[0] != state:
            self.softChangeInfo = (state, 0)
        if self.softChangeInfo[1] < self.changeBuffer:
            self.softChangeInfo = (self.softChangeInfo[0], self.softChangeInfo[1]+1)
            return
        
        self.hard_change_state(state)

    # in case want region in image
    # def step(self):
        #call soft_change_state on light state

    def time_since_change(self):
        return time.time() - self.lastChangeTime

class TrafficLightExt():
    def __init__(self):
        self.light = TrafficLight()

        self.lowerRed = np.array([170,100,50])
        self.upperRed = np.array([180,255,255])

    def get_masked(self, img):
        hlsFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hlsFrame, self.lowerRed, self.upperRed)
        mask = cv2.dilate(mask, (np.ones((15, 15), 'uint8')))
        
        res_mask = cv2.bitwise_and(img, img, mask=mask)
        return res_mask

    def set_current_light_color(self, frame):
        masked_light = self.get_masked(frame)

        if np.sum(np.mean(masked_light, axis=(0, 1))) < 20:
            self.light.soft_change_state(TrafficColor.GREEN)
        else:
            self.light.soft_change_state(TrafficColor.RED)

class Indicator:
    def __init__(self, topLeftCoords, bottomRightCoords):
        self.trafficLight = TrafficLightExt()

        self.camera = self.get_camera()
        self.crossing = 0
        self.crossingTime = 18

        self.topLeftCoords = topLeftCoords
        self.bottomRightCoords = bottomRightCoords
    
    def get_camera(self):
        for camera_idx in range(10):
            cap = cv2.VideoCapture(camera_idx)
            if cap.isOpened():
                print(camera_idx)
                return cap
    
    def get_crossing_state(self):
        ret, frame = self.camera.read()
        topLeftX, topLeftY = self.topLeftCoords
        botRightX, botRightY = self.bottomRightCoords

        self.trafficLight.set_current_light_color(
            frame[topLeftY:botRightY, 
                  topLeftX:botRightX]
        )

        currTime = time.time()

        if (self.trafficLight.light.currState == TrafficColor.GREEN):
            self.crossing = max(0, self.crossingTime - int(currTime - self.trafficLight.light.lastChangeTime))
        frame = cv2.rectangle(frame, self.topLeftCoords, self.bottomRightCoords, color=(255,0,0), thickness=2)        
        return frame

if __name__ == "__main__":
    crossingIndicator = Indicator(
        (200, 200), (300, 300)
    )

    while(True):
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        if key & 0xFF == ord('r'):
            tlc = (int(input('Enter top left x')), int(input('Enter top left y')))
            brc = (int(input('Enter bottom right x')), int(input('Enter bottom right y')))
            if tlc[0] < brc[0] and tlc[1] < brc[1]:
                crossingIndicator.topLeftCoords = tlc
                crossingIndicator.bottomRightCoords = brc
            else:
                print('INVALID RECTANGLE!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        frame = crossingIndicator.get_crossing_state()
        cv2.imshow('frame', frame)
        print(crossingIndicator.crossing)

# light = TrafficLight(initialState=TrafficColor.RED, changeBuffer=2)
# light.soft_change_state(TrafficColor.GREEN)
# print(light.time_since_change(), light.currState)
# light.soft_change_state(TrafficColor.GREEN)
# print(light.time_since_change(), light.currState)
# light.soft_change_state(TrafficColor.GREEN)
# print(light.time_since_change(), light.currState)