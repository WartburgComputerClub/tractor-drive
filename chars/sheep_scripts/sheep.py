# file sheep.py
# author: Andrew Reisner <andrew@reisner.co>
# This class makes it easy to control a sheep
# by extending the data and methods provided
# by the sheep's blender object.

import bge

class Sheep(bge.types.KX_GameObject):
    
    def __init__(self,old_owner):
        self.animations = {}
        pass
    
    def registerAnimation(self,name,controller,actuator):
        self.animations[name] = (controller,actuator)
    
    def animate(self,action):
        if action in self.animations.keys():
            self.animations[action][0].activate(self.animations[action][1])
    
def init(cont):
    sheep = Sheep(cont.owner)
    acts = cont.actuators
    sheep.registerAnimation('walk', cont,acts['sheep_walk'])
    sheep.registerAnimation('run', cont,acts['sheepcute_run'])
    sheep.registerAnimation('graze',cont,acts['sheep_graze'])
    sheep.registerAnimation('helpless',cont,acts['sheepcute_helpless'])
    sheep.registerAnimation('hit',cont,acts['hit_sheep'])
    sheep.registerAnimation('flounder',cont,acts['sheep_flounder'])
    sheep.registerAnimation('puff',cont,acts['sheep_puff'])
    sheep.registerAnimation('drown',cont,acts['sheep_drown'])
    sheep.animate('walk')
