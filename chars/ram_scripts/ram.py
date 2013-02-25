# file ram.py
# author: Andrew Reisner <andrew@reisner.co>
# This class makes it easy to control a ram
# by extending the data and methods provided
# by the ram's blender object.

import bge

class Ram(bge.types.KX_GameObject):
    
    def __init__(self,old_owner):
        self.status = None
        self.actmap = {
                       'walk':'ram_walk',
                       'run': 'ram_run',
                       'graze':'ram_graze',
                       'helpless':'ram_helpless',
                       'hit':'hit_ram',
                       'flounder':'ram_flounder',
                       'drown':'ram_drown',
                       'attack':'ram_attack',
                       'motion':'ram_motion'
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
        ram = Ram(cont.owner)
        ram.controller = cont
        ram.walk()
        cont.owner['initialized'] = True
    else:
        cont.owner.update()
        