import bge
import GameLogic

from game.types import LandAnimal
from sheep.states import *

class Sheep(LandAnimal):
    
    def initHook(self):
        acts = self.controller.actuators
        self.registerAnimations([
            ('walk',acts['sheep_walk']),
            ('run',acts['sheepcute_run']),
            ('graze',acts['sheep_graze']),
            ('helpless',acts['sheepcute_helpless']),
            ('hit',acts['hit_sheep']),
            ('flounder', acts['sheep_flounder']),
            ('puff',acts['sheep_puff']),
            ('drown',acts['sheep_drown'])])
        self.motion = acts['sheep_motion']

    def flounder(self,velocity=0.035):
        self.setAnimation('flounder')
        self.setVelocity((0,velocity))

    def updateHook(self):
        self.flock = [ob for ob in GameLogic.getCurrentScene().objects if ob.name == 'sheep_cute']
    
from sheep.handles import *
