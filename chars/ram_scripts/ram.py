# file ram.py
# author: Andrew Reisner <andrew@reisner.co>
# This class makes it easy to control a ram
# by extending the data and methods provided
# by the ram's blender object.

import bge
import GameLogic
from random import random, choice
from math import atan2, pi, cos, sin
from time import sleep,time

global obstacles
global bigObstacles
global fences

obstacles = []
bigObstacles = []
fences = []

for obj in GameLogic.getCurrentScene().objects:
    if obj.name in ['right_side_tree','left_side_tree','small_sphere',
                    'fan_tree','cube','cylinder_tree','chevron_tree']:
        obstacles.append(obj.worldPosition.copy())
    elif obj.name in ['water','square_house','Front House','L_house','shed',
                    'large_square_house','front_left_house','asymm_shed']:
        bigObstacles.append(obj.worldPosition.copy())
    elif obj.name == 'fence_long':
        fences.append(obj.worldPosition.copy())

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

        self.grazeTime = time()
        self.hunger = 0

        self.chargeTime = time()

        self.blank = self.worldPosition.copy()
        self.blank.x = 0
        self.blank.y = 0
        self.blank.z = 0

        self.r1 = 4
        self.r2 = 36
        
    def act(self,name):
        return self.controller.actuators[self.actmap[name]]

    def puff(self):
        tractor = GameLogic.getCurrentScene().objects['tractor']
        p1 = self.worldPosition.copy()
        p1.z = 0
        result = self.blank.copy()
        p2 = tractor.worldPosition.copy()
        p2.z = 0
        v1 = self.orientation[:][1].copy()
        v2 = p2 - p1
        angle = angleFromVectors(v1,v2)
        otherAngle = angleFromVectors(v1,self.blank)
        if abs(angle - otherAngle) > pi/6:
            self.walk()
        else:
            if self.status != None:
                self.controller.deactivate(self.act(self.status))
            self.status = 'attack'

            self.controller.activate(self.act('attack'))
            self.act('motion').dLoc = (0,0,0)
            
    
    def walk(self,speed=.02): #0.02 normal
        if self.status != None:
            self.controller.deactivate(self.act(self.status))
        self.status = 'walk'
        
        self.controller.activate(self.act('walk'))
        self.act('motion').dLoc = (0,speed,0)

    def run(self,speed=.07): #0.07 normal
        if self.status == None:
            self.controller.activate(self.act('run'))
        if self.status != None:
            self.controller.deactivate(self.act(self.status))
        self.status = 'run'
        
        self.controller.activate(self.act('run'))
        self.act('motion').dLoc = (0,speed,0)

    def attack(self,speed = .07): #0.07 normal
        if time() - self.chargeTime >= 3:
            self.chargeTime = time()
        if self.status == None:
            self.controller.activate(self.act('attack'))
        if self.status != None:
            self.controller.deactivate(self.act(self.status))
        self.status = 'attack'
        
        self.controller.activate(self.act('attack'))
        self.act('motion').dLoc = (0,speed,0)

    def graze(self):
        if self.status != None:
            self.controller.deactivate(self.act(self.status))
        self.status = 'graze'

        self.controller.activate(self.act('graze'))
        self.act('motion').dLoc = (0,0,0)

    def navigate(self):
        target = self.avoidStatic()*5 + self.vary() + 10*self.aggression()
        temp = self.orientation[:][1].copy()
        if self.status not in ['attack']:
            self.turn(self.decideTurn(temp,target))
        else:
            self.turn(0)
##        x = random()
##        if x < 0.0001 and self.state == 'run':
##            self.walk()
##        elif x < 0.1 and self.state == 'walk':
##            self.run()

    def aggression(self):
        tractor = GameLogic.getCurrentScene().objects['tractor']
        p1 = self.worldPosition.copy()
        p1.z = 0
        result = self.blank.copy()
        p2 = tractor.worldPosition.copy()
        p2.z = 0
        dist = (p1-p2).magnitude
        angle = atan2(p2.y - p1.y,p2.x - p1.x)
        if self.r2/2 < dist < self.r2:
            self.puff()
            result.x = result.x  + cos(angle)
            result.y = result.y + sin(angle)            
        elif self.r1 < dist <= self.r2/2:
            self.run()
            result.x = result.x  + cos(angle)
            result.y = result.y + sin(angle)
        elif 0 < dist <= self.r1:
            self.attack()
            result.x = result.x  + cos(angle)
            result.y = result.y + sin(angle)
        return result

    def avoidStatic(self):
        p1 = self.worldPosition.copy()
        p1.z = 0
        result = self.blank.copy()
        for v in obstacles:
            p2 = v.copy()
            p2.z = 0
            dist = (p1 - p2).magnitude
            angle = atan2(p1.y - p2.y,p1.x - p2.x)
            
            if 0 < dist < 2*self.r1:
                size = 2/dist**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)

        for v in bigObstacles:
            p2 = v.copy()
            p2.z = 0
            dist = (p1 - p2).magnitude
            angle = atan2(p1.y - p2.y,p1.x - p2.x)
            
            if 3*self.r1 < dist < 6*self.r1:
                size = 2/(dist-2*self.r1)**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)
            elif self.r1 < dist <= 3*self.r1:
                size = 2/dist**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)
            elif dist < self.r1:
                size = 10/dist**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)

        for v in fences:
            p2 = v.copy()
            p2.z = 0
            dist = (p1 - p2).magnitude
            angle = atan2(p1.y - p2.y,p1.x - p2.x)
            
            if self.r1 < dist < 3*self.r1:
                size = 2/dist**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)
            elif 0 < dist <= self.r1:
                size = 10/dist**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)
        return result

    def vary(self):
        theta = random() * 2*pi
        temp = self.blank.copy()
        temp.x, temp.y, temp.z = cos(theta), sin(theta), 0
        return temp

    def decideTurn(self,current,target):
        toTurn = angleFromVectors(current,target)
        if abs(toTurn) > 2*pi/3:
            return sign(toTurn)*0.05
        elif abs(toTurn) > pi/2:
            return sign(toTurn)*0.03
        elif abs(toTurn) == 0:
            return 0
        else:
            return sign(toTurn)*0.02
        
    def turn(self,angle):
        self.act('motion').dRot = (0,0,angle)
        
    def update(self):
        self.navigate()
        self.controller.activate(self.act('motion'))
        #print(self.status, "at", self.worldPosition)
    
def init(cont):
    if not cont.owner['initialized']:
        ram = Ram(cont.owner)
        ram.controller = cont
        ram.walk()
        cont.owner['initialized'] = True
    else:
        cont.owner.update()

def angleFromVectors(v1,v2):
    v1 = v1.copy()
    v1.y = -v1.y
    v1.normalize()
    v2 = v2.copy()
    v2.normalize()
    crossProd = v1.cross(v2)
    angle = atan2(crossProd.magnitude, v1.dot(v2))
    up = v1.copy()
    up.x, up.y, up.z = 0,0,1
    if (up.dot(crossProd) < 0):
        angle = -angle
    return angle

def sign(num):
    if num >= 0:
        return 1
    return -1
