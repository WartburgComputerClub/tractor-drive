# file ram.py
# author: Andrew Reisner <andrew@reisner.co>
# This class makes it easy to control a ram
# by extending the data and methods provided
# by the ram's blender object.

import bge

class Ram(bge.types.KX_GameObject):
    
    def __init__(self,old_owner):
        self.animations = {}
        pass
    
    def registerAnimation(self,name,controller,actuator):
        self.animations[name] = (controller,actuator)
    
    def animate(self,action):
        if action in self.animations.keys():
            self.animations[action][0].activate(self.animations[action][1])
    
def init(cont):
    ram = Ram(cont.owner)
    acts = cont.actuators
    ram.registerAnimation('walk', cont,acts['ram_walk'])
    ram.registerAnimation('run', cont,acts['ram_run'])
    ram.registerAnimation('graze',cont,acts['ram_graze'])
    ram.registerAnimation('helpless',cont,acts['ram_helpless'])
    ram.registerAnimation('hit',cont,acts['hit_ram'])
    ram.registerAnimation('flounder',cont,acts['ram_flounder'])
    ram.registerAnimation('drown',cont,acts['ram_drown'])
    ram.registerAnimation('attack',cont,acts['ram_attack'])
    ram.animate('walk')
