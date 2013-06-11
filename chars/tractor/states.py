from game.types import GameObjectState
from mathutils import Vector
from time import time

class IdleState(GameObjectState):

    def activate(self):
        self.owner.activeSensor.clear()
        self.owner.activeSensor.deactivate()
        self.owner.setState(WheelState(self.owner))

    def update(self):
        owner = self.owner
        if owner.wheel == None:
            if owner.debug:
                owner.setState(DebugState(owner))
            else:
                owner.setState(KeyboardState(owner))
        else:
            if not owner.activeSensor.active:
                owner.activeSensor.connect(self.activate)
                owner.activeSensor.activate()

    def leave(self):
        if self.owner.timer.elapsed == 0:
            self.owner.timer.start()

class WheelState(GameObjectState):
    
    def enter(self):
        self.owner.cruise_control.reset()
        self.owner.flipSensor.activate()

    def update(self):
        owner = self.owner
        wheel = self.owner.wheel
        owner.steer(wheel.getSteer())
        owner.cruise_control.update(owner.getSpeed())
        owner.setPower(owner.cruise_control.getPower())

    def leave(self):
        self.owner.flipSensor.deactivate()

class KeyboardState(GameObjectState):

    def enter(self):
        self.owner.flipSensor.activate()

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
    
    def message(self,msg):
        if self.owner.debug:
            self.owner.setState(DebugState(self.owner))

    def leave(self):
        self.owner.flipSensor.deactivate()

class DebugState(GameObjectState):

    def enter(self):
        self.owner.cruise_control.reset()
        self.owner.flipSensor.activate()
    
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
        
        owner.cruise_control.update(owner.getSpeed())
        owner.setPower(owner.cruise_control.getPower())

    def message(self,msg):
        if not self.owner.debug:
            self.owner.setState(KeyboardState(self.owner))

    def leave(self):
        self.flipSensor.deactivate()
