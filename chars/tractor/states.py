from game.types import GameObjectState
from time import time

class IdleState(GameObjectState):

    def enter(self):
        self.activeCount = 0

    def update(self):
        owner = self.owner
        if owner.wheel == None:
            owner.setState(KeyboardState(owner))
        else:
            prev = wheel.getSteer()
            curr = wheel.getSteer()
            if abs(prev - curr) > .01:
                if self.activeCount > 2:
                    owner.setState(WheelState(owner))
                else:
                    self.activeCount += 1

    def leave(self):
        if self.owner.startTime == 0:
            self.owner.startTime = time()

class WheelState(GameObjectState):
    
    def update(self):
        owner = self.owner
        #check dead or stuck
        wheel = self.owner.wheel
        owner.steer(wheel.getSteer())
        owner.cruise_control.update(owner.getSpeed())
        owner.setPower(owner.cruise_control.getPower())

class KeyboardState(GameObjectState):

    def update(self):
        owner = self.owner

        steerLeft = owner.controller.sensors['left']
        steerRight = owner.controller.sensors['right']
        if steerRight.positive:
            turn = -.3
        elif steerLeft.positive:
            turn = .3
        else:
            turn = 0.0
        
        owner.steer(turn)
        
        if owner.controller.sensors['gas'].positive:
            owner.forward()
        elif owner.controller.sensors['reverse'].positive:
            owner.backward()
        else:
            owner.setPower(0)
            
            
