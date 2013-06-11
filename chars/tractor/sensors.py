from time import time
from math import acos

from game.types import GameObjectSensor

# triggers when the steering wheel has been moved slightly
class ActiveSensor(GameObjectSensor):
    
    def setup(self):
        self.activeCount = 0
        self.waitFlag = False
        self.prevTime = time()*2

    def update(self):
        owner = self.owner
        if time() - self.prevTime > .01:
            self.waitFlag = True
            
        if not self.waitFlag:
            self.prevVal = owner.wheel.getSteer()
            self.prevTime = time()
        else:
            curr = owner.wheel.getSteer()
                
        if self.waitFlag and abs(self.prevVal - curr) > .01:
            if self.activeCount > 2:
                self.trigger()
            else:
                self.activeCount += 1
            self.waitFlag = False
        
class FlipSensor(GameObjectSensor):

    def update(self):
        owner = self.owner
        # get angle between global and local z value
        val = owner.getAxisVect((0,0,1)) 
        cos_val = val[2]/(val[0]**2 + val[1]**2 + val[2]**2)**(.5)
        theta = acos(cos_val)
        if theta > owner.settings.FLIP_THRESH:
            self.trigger()
