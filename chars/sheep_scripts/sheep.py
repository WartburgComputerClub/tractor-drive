# file sheep.py
# author: Andrew Reisner <andrew@reisner.co>
# This class makes it easy to control a sheep
# by extending the data and methods provided
# by the sheep's blender object.

import bge

class Sheep(bge.types.KX_GameObject):
    
    def __init__(self,old_owner):
        self.status = None
        self.actmap = {
                       'walk':'sheep_walk',
                       'run':'sheepcute_run',
                       'graze':'sheep_graze',
                       'helpless':'sheepcute_helpless',
                       'hit':'hit_sheep',
                       'flounder': 'sheep_flounder',
                       'puff':'sheep_puff',
                       'drown':'sheep_drown',
                       'motion':'sheep_motion'
                       }
        
    def act(self,name):
        return self.controller.actuators[self.actmap[name]]
    
    def walk(self,speed=.01):
        speed *= -1
        if self.status != None:
            self.controller.deactivate(self.act(self.status))
        self.status = 'walk'
        
        self.controller.activate(self.act('walk'))
        self.act('motion').dLoc = (0,speed,0)
    
    def turn(self,angle):
        self.act('motion').dRot = (0,0,angle)
        
    def update(self):
        self.controller.activate(self.act('motion'))
        print(self.worldPosition)
        
    
        
def init(cont):
    if not cont.owner['initialized']:
        sheep = Sheep(cont.owner)
        sheep.controller = cont
        sheep.walk()
        cont.owner['initialized'] = True
    else:
        cont.owner.update()
