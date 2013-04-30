from game.types import GameObjectState
from mathutils import Vector
from time import time

class IdleState(GameObjectState):

    def enter(self):
        self.activeCount = 0

    def update(self):
        owner = self.owner
        if owner.wheel == None:
            if owner.debug:
                owner.setState(DebugState(owner))
            else:
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
    
    def enter(self):
        self.owner.cruise_control.reset()

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
        if owner.flipped():
            owner.reset()

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
    
    def message(self,msg):
        if self.owner.debug:
            self.owner.setState(DebugState(self.owner))
            
class DebugState(GameObjectState):

    def enter(self):
        self.owner.cruise_control.reset()
    
    def update(self):
        owner = self.owner
        if owner.flipped():
            owner.reset()
            
        steerLeft = owner.controller.sensors['left']
        steerRight = owner.controller.sensors['right']
        if steerRight.positive:
            turn = -.3
        elif steerLeft.positive:
            turn = .3
        else:
            turn = 0.0
        
        owner.steer(turn)
        
        owner.cruise_control.update(owner.getSpeed())
        owner.setPower(owner.cruise_control.getPower())

    def message(self,msg):
        if not self.owner.debug:
            self.owner.setState(KeyboardState(self.owner))
            
