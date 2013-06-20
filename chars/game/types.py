import bge
import GameLogic
from mathutils import Vector
from random import random
from math import cos,sin,copysign,atan2,pi

class GameObject(bge.types.KX_GameObject):
    
    def __init__(self,old_owner):
        self.currState = None
        self.senses = []
        self.initHook()

    def initHook(self):
        pass

    def setState(self,newstate):
        if self.currState != None:
            self.currState.leave()
        self.currState = newstate
        self.currState.enter()
        
    def update(self):
        self.updateHook()

        for sensor in self.senses:
            if sensor.active:
                sensor.update()

        self.currState.update()
        
    def updateHook(self):
        pass

    def message(self,msg):
        self.currState.message()

    def addSensor(self,sensor):
        self.senses.append(sensor)

        

class AnimatedGameObject(GameObject):

    def __init__(self,old_owner):
        self.currAnimation = None
        self.actmap = {}
        super().__init__(old_owner)

    def registerAnimation(self,name,actuatorName):
        self.actmap[name] = actuatorName

    def registerAnimations(self,mappedTuples):
        for mapping in mappedTuples:
            self.registerAnimation(mapping[0],mapping[1])

    def setAnimation(self,newAnim):
        if self.currAnimation != None:    
            self.controller.deactivate(self.act(self.currAnimation))
        self.currAnimation = newAnim
        self.controller.activate(self.act(newAnim))
        
    def act(self,name):
        return self.controller.actuators[self.actmap[name]]
    
        
class GameObjectState:
    
    def __init__(self,owner):
        self.owner = owner
    
    def enter(self):
        pass
    
    def leave(self):
        pass
    
    def update(self):
        pass
    
    def message(self,msg):
        pass

class GameObjectSensor:
    
    def __init__(self,owner):
        self.owner = owner
        self.callbacks = []
        self.active = False
        self.initHook()

    def initHook(self):
        pass

    def update(self):
        pass

    def connect(self,callback):
        self.callbacks.append(callback)

    def trigger(self):
        for callback in self.callbacks:
            callback()

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def clear(self):
        del self.callbacks
        self.callbacks = []

class LandAnimal(AnimatedGameObject):

    def __init__(self,old_owner):
        self.walkVelocity = 0.02
        self.runVelocity = 0.04
        super().__init__(old_owner)

    def tractorAimError(self):
        tractor = GameLogic.getCurrentScene().objects['tractor']
        p1 = self.worldPosition.copy()
        p1 = Vector((p1.x,p1.y))
        p2 = tractor.worldPosition.copy()
        p2 = Vector((p2.x,p2.y))
        v1 = self.orientation[:][1].copy()
        v1 = Vector((v1.x,v1.y))
        v2 = p2 - p1
        return abs(v1.angle_signed(v2))
    
    def angleToTractor(self):
        tractor = GameLogic.getCurrentScene().objects['tractor']
        p1 = self.worldPosition.copy()
        p2 = tractor.worldPosition.copy()
        return atan2(p2.y - p1.y, p2.x - p1.x)
    
    def distanceToTractor(self):
        tractor = GameLogic.getCurrentScene().objects['tractor']
        p1 = self.worldPosition.copy()
        p1.z = 0
        result = Vector((0,0,0))
        p2 = tractor.worldPosition.copy()
        p2.z = 0
        dist = (p1-p2).magnitude
        return dist
    
    def vectorToTractor(self):
        tractor = GameLogic.getCurrentScene().objects['tractor']
        p1 = self.worldPosition.copy()
        p2 = tractor.worldPosition.copy()
        vec = Vector((p2.x - p1.x,p2.y - p1.y))
        return vec

    def randomDirectionVector(self):
        theta = random() * 2*pi
        temp = Vector((cos(theta),sin(theta)))
        return temp

    def iterTurn(self,target):
        temp = self.orientation[:][1].copy()
        temp = Vector((temp.x,-1*temp.y))
        self.turn(self.decideTurn(temp,target))
        
    def decideTurn(self,current,target):
        toTurn = current.angle_signed(target)
        print(toTurn*180/pi)
        if abs(toTurn) > 2*pi/3:
            return copysign(0.05,toTurn)
        elif abs(toTurn) > pi/2:
            return copysign(0.03,toTurn)
        elif abs(toTurn) == 0:
            return 0
        else:
            return copysign(0.02,toTurn)

    def walk(self,velocity=None):
        if velocity == None:
            velocity = self.walkVelocity
        self.setAnimation('walk')
        self.setVelocity((0,velocity))

    def run(self,velocity=None):
        if velocity == None:
            velocity = self.runVelocity
        self.setAnimation('run')
        self.setVelocity((0,velocity))
