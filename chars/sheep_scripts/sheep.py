# file sheep.py
# author: Andrew Reisner <andrew@reisner.co>
# This class makes it easy to control a sheep
# by extending the data and methods provided
# by the sheep's blender object.

import bge
import GameLogic
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
        
        self.flock = []
        for obj in GameLogic.getCurrentScene().objects:
            if obj.name == 'sheep_cute':
                self.flock.append(obj)
        print(len(self.flock),"sheep in the flock.")
        self.savedVelo = self.worldVelocity()

        self.r1 = 5
        self.r2 = 20
        
    def act(self,name):
        return self.controller.actuators[self.actmap[name]]
    
    def walk(self,speed=.01): #0.01 normal
        if self.status != None:
            self.controller.deactivate(self.act(self.status))
        self.status = 'walk'
        
        self.controller.activate(self.act('walk'))
        self.act('motion').dLoc = (0,speed,0)

    def run(self,speed=.03): #0.03 normal
        if self.status == None:
            self.controller.activate(self.act('run'))
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
        if x < 0.005:
            options = ['walk','run','graze']
            if self.status:
                options.remove(self.status)
            temp = choice(options)
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
            self.avoid()

    def avoid(self):
        for sheep in self.flock:
            dist = (self.worldPosition - sheep.worldPosition).magnitude
            print(dist)
    
    def center(self):
        pass
    
    def match(self):
        pass
    
    def vary(self):
        pass

    def avoidEdgeBegin(self):
        
            
    
    def turn(self,angle):
        self.act('motion').dRot = (0,0,angle)
        
    def update(self):
        self.navigate()
        #self.controller.activate(self.act(self.status))
        self.controller.activate(self.act('motion'))
        #print(self.status, "at", self.worldPosition)
    
        
def init(cont):
    if not cont.owner['initialized']:
        sheep = Sheep(cont.owner)
        sheep.controller = cont
        sheep.run()
        cont.owner['initialized'] = True
    else:
        cont.owner.update()
