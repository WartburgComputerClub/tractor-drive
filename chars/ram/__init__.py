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
        self.act('motion').dLoc = vel
        
    def tractorAimError(self):
        tractor = GameLogic.getCurrentScene().objects['tractor']
        p1 = self.worldPosition.copy()
        p1.z = 0
        result = Vector((0,0,0))
        p2 = tractor.worldPosition.copy()
        p2.z = 0
        v1 = self.orientation[:][1].copy()
        v2 = p2 - p1
        return abs(v1.angle(v2))
    
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
        angle = self.angleToTractor()
        vec = Vector((0,0,0))
        vec.x += cos(angle)
        vec.y += sin(angle)
        return vec

    def randomDirectionVector(self):
        theta = random() * 2*pi
        temp = Vector((0,0,0))
        temp.x, temp.y, temp.z = cos(theta), sin(theta), 0
        return temp

    def iterTurn(self,target):
        temp = self.orientation[:][1].copy()
        self.turn(self.decideTurn(temp,target))
        
    def decideTurn(self,current,target):
        toTurn = current.angle(target)
        if abs(toTurn) > 2*pi/3:
            return copysign(0.05,toTurn)
        elif abs(toTurn) > pi/2:
            return copysign(0.03,toTurn)
        elif abs(toTurn) == 0:
            return 0
        else:
            return copysign(0.02,toTurn)
        
    def turn(self,angle):
        self.act('motion').dRot = (0,0,angle)
        
    def updateHook(self):
        self.controller.activate(self.act('motion'))
        print(self.act('motion').dLoc)
    
from ram.handles import *
