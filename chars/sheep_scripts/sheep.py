# file sheep.py
# author: Andrew Reisner <andrew@reisner.co>
# This class makes it easy to control a sheep
# by extending the data and methods provided
# by the sheep's blender object.

import bge
from random import random, choice

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
        if self.status != None:
            self.controller.deactivate(self.act(self.status))
        self.status = 'walk'
        
        self.controller.activate(self.act('walk'))
        self.act('motion').dLoc = (0,speed,0)

    def run(self,speed=.03):
        if self.status != None:
            self.controller.deactivate(self.act(self.status))
        self.status = 'run'

        self.controller.activate(self.act('run'))
        self.act('motion').dLoc = (0,speed,0)

    def graze(self):
        if self.status != None:
            self.controller.deactivate(self.act(self.status))
        self.status = 'graze'

        self.controller.activate(self.act('graze'))
        self.act('motion').dLoc = (0,0,0)

    def navigate(self):
        x = random()
        print(x)
        if x < 0.015:
            temp = choice(['walk','run','graze'])
            if temp != 'graze':
                self.turn(choice([-0.01, 0, 0.01]))
                if temp == 'walk':
                    self.walk()
                else:
                    self.run()
            else:
                self.turn(0)
                self.graze()
        elif x < 0.05 and self.status != 'graze':
            self.turn(choice([-0.01, 0, 0.01]))
    
    def turn(self,angle):
        self.act('motion').dRot = (0,0,angle)
        
    def update(self):
        self.navigate()
        #self.controller.activate(self.act(self.status))
        self.controller.activate(self.act('motion'))
        print(self.status, "at", self.worldPosition)
        
    
        
def init(cont):
    if not cont.owner['initialized']:
        sheep = Sheep(cont.owner)
        sheep.controller = cont
        sheep.graze()
        cont.owner['initialized'] = True
    else:
        cont.owner.update()
