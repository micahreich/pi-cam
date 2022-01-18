import time
from enum import Enum

class TrafficColor(Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2
    UNKNOWN = 3

#use param self.currState and self.changeDelta
#maybe want to have the region in the image?
class TrafficLight:

    #change buffer is how many times to soft_change_state need
    #to be called for enough confidence for light to be that color
    def __init__(self, initialState=TrafficColor.UNKNOWN, changeBuffer=0):
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
        #if the current reading is the same as the current state ignore
        if state == self.currState:
            self.softChangeInfo = (state, 0)
            return
        #if the state has changed from what was expected, set to 0
        if self.softChangeInfo[0] != state:
            self.softChangeInfo = (state, 0)
        if self.softChangeInfo[1] < self.changeBuffer:
            self.softChangeInfo = (self.softChangeInfo[0], self.softChangeInfo[1]+1)
            return
        self.hard_change_state(state)

    #in case want region in image
    #def step(self):
        #call soft_change_state on light state

    def time_since_change(self):
        return time.time() - self.lastChangeTime

light = TrafficLight(initialState=TrafficColor.RED, changeBuffer=2)
light.soft_change_state(TrafficColor.GREEN)
print(light.time_since_change(), light.currState)
light.soft_change_state(TrafficColor.GREEN)
print(light.time_since_change(), light.currState)
light.soft_change_state(TrafficColor.GREEN)
print(light.time_since_change(), light.currState)