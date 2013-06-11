from game.types import GameObjectSensor
from time import time

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
        
