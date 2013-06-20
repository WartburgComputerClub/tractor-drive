import bge
import GameLogic
from mathutils import Vector
from random import random
from math import cos,sin,copysign,atan2

from game.types import LandAnimal
from game.environment import Environment
from ram.states import *

class Ram(LandAnimal):

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
        self.runVelocity = 0.07
            
    def setVelocity(self,vel):
        self.act('motion').dLoc = (vel[0],vel[1],0)
        
    def turn(self,angle):
        self.act('motion').dRot = (0,0,angle*-1)
        
    def updateHook(self):
        self.controller.activate(self.act('motion'))
    
from ram.handles import *
