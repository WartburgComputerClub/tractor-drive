import bge
import GameLogic

from game.types import LandAnimal
from sheep.states import *

class Sheep(LandAnimal):
    
    def initHook(self):
        self.registerAnimations([
            ('walk','sheep_walk'),
            ('run','sheepcute_run'),
            ('graze','sheep_graze'),
            ('helpless','sheepcute_helpless'),
            ('hit','hit_sheep'),
            ('flounder', 'sheep_flounder'),
            ('puff','sheep_puff'),
            ('drown','sheep_drown'),
            ('motion','sheep_motion')])

    def setVelocity(self,vel):
        self.act('motion').dLoc = (vel[0],vel[1],0)

    def updateHook(self):
        self.controller.activate(self.act('motion'))

from sheep.handles import *
