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
        acts = self.controller.actuators
        self.registerAnimations([
            ('walk',acts['ram_walk']),
            ('run',acts['ram_run']),
            ('graze',acts['ram_graze']),
            ('helpless',acts['ram_helpless']),
            ('hit',acts['hit_ram']),
            ('flounder',acts['ram_flounder']),
            ('drown',acts['ram_drown']),
            ('attack',acts['ram_attack'])])
        self.motion = acts['ram_motion']
        self.runVelocity = 0.07
            
from ram.handles import *
