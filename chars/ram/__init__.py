import bge
import GameLogic
from mathutils import Vector
from random import random
from math import cos,sin,copysign,atan2

from game.types import AnimatedGameObject
from game.environment import Environment
from ram.states import *

class Ram(AnimatedGameObject):

    def initHook(self):
        self.registerAnimations([
            ('walk','ram_walk'),
            ('run','ram_run'),
            ('graze','ram_graze'),
            ('helpless','ram_helpless'),
            ('hit','hit_ram'),
            ('flounder','ram_flounder'),
            ('drown','ram_drown'),
            ('attack','ram_attack'),
            ('motion','ram_motion')])
            
    def setVelocity(self,vel):
        self.act('motion').dLoc = (vel[0],vel[1],0)
        
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

    def turn(self,angle):
        self.act('motion').dRot = (0,0,angle*-1)
        
    def updateHook(self):
        self.controller.activate(self.act('motion'))
    
from ram.handles import *
