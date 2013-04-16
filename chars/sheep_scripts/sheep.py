# file sheep.py
# author: Andrew Reisner <andrew@reisner.co>
# This class makes it easy to control a sheep
# by extending the data and methods provided
# by the sheep's blender object.

import bge
import GameLogic
from random import random, choice
from math import atan2, pi, cos, sin
from time import sleep,time

global obstacles
global bigObstacles
global fences
global grass
global rams

obstacles = []
bigObstacles = []
fences = []
grass = []

for obj in GameLogic.getCurrentScene().objects:
    if obj.name in ['right_side_tree','left_side_tree','small_sphere',
                    'fan_tree','cube','cylinder_tree','chevron_tree']:
        obstacles.append(obj.worldPosition.copy())
    elif obj.name in ['water','square_house','Front House','L_house','shed',
                    'large_square_house','House','front_left_house','asymm_shed']:
        bigObstacles.append(obj.worldPosition.copy())
    elif obj.name == 'fence_long':
        fences.append(obj.worldPosition.copy())
    elif obj.name == 'grass_002':
        grass.append(obj.worldPosition.copy())
        
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


        self.flock = [ob for ob in GameLogic.getCurrentScene().objects if 'initialized' in ob]

        n = len(self.flock)
        self.savedAngle = None
        self.lastPosition = self.worldPosition.copy()

        self.blank = self.lastPosition
        self.blank.x = 0
        self.blank.y = 0
        self.blank.z = 0
        
        self.hunger = random()*40
        self.hungerGrowth = 1
        self.lastTime = time()

        self.hitTime = time()

        self.r1 = 4
        self.r2 = 32

        #self.obstacles = []

        self.leader = False
        
    def act(self,name):
        return self.controller.actuators[self.actmap[name]]
    
    def walk(self,speed=.02): #0.02 normal
        if self.status != None:
            self.controller.deactivate(self.act(self.status))
        self.status = 'walk'
        
        self.controller.activate(self.act('walk'))
        self.act('motion').dLoc = (0,speed,0)

    def run(self,speed=.05): #0.05 normal
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

    def hit(self):
        print("HI!")
        if self.status != None:
            self.controller.deactivate(self.act(self.status))
        self.status = 'hit'
        
        self.controller.activate(self.act('hit'))
        self.act('motion').dLoc = -self.act('motion').dLoc

    def flounder(self,speed =.035): #0.035 normal
        if self.status != None:
            self.controller.deactivate(self.act(self.status))
        self.status = 'flounder'
        
        self.controller.activate(self.act('flounder'))
        self.act('motion').dLoc = (0,speed,0)

    def navigate(self):
        x = random()
        if self.status == 'hit' and time() - self.hitTime < 0.5:
            self.hit()
        elif self.canGraze() and self.isSafeToGraze(): #and self.status != 'graze' 
            self.graze()
            self.turn(0)
            self.grazeTime = time()
            self.hungerGrowth = -8
            #print("GRAZING!!!", time(), self.hunger)
##        elif time() - self.grazeTime > self.hunger or self.status != 'graze':
##            target = self.avoid()*10 + 4 * self.center() + 6 * self.match() + self.vary()
##            temp = self.orientation[:][1].copy()
##            self.turn(self.decideTurn(temp,target))
##            self.hunger = 0
##        elif self.isSafeToGraze():
##            self.graze()
##            self.turn(0)
        else:
            target = self.avoid()*10 + 4 * self.center() + 4 * self.match() + max(0,min(8,(self.hunger-30)/3)) * self.forage() + self.unite() + self.vary() 
            temp = self.orientation[:][1].copy()
            self.turn(self.decideTurn(temp,target))
            self.hungerGrowth = 1
            #print("Not")

    def canGraze(self):
        return 0 < self.closestGrass()[0] < 1 and self.hunger > 0

    def hungry(self):
        return self.hunger > 30

    def hungryFollowers(self):
        if not self.leader:
            return False
        p1 = self.worldPosition.copy()
        p1.z = 0
        for sheep in self.flock:
            p2 = sheep.worldPosition.copy()
            p2.z = 0
            dist = (p1 - p2).magnitude
            
            if dist < self.r2:
                if sheep.hungry():
                    return True
        return False
    
    def closestGrass(self):
        # Closest untaken grass
        p1 = self.worldPosition.copy()
        p1.z = 0
        least = 0
        closest = grass[0]
        for g in grass:
            #print("a")
            p2 = g.copy()
            p2.z = 0
            dist = (p1 - p2).magnitude
            if not least or dist < least:
                taken = False
                for sheep in self.flock:
                    try:
                        p3 = sheep.worldPosition.copy()
                        p3.z = 0
                        dist2 = (p2 - p3).magnitude
                        if dist2 < dist and dist2 < sheep.r2 and sheep.hungry():
                            taken = True
                    except:
                        pass
                #print(taken)
                if not taken:
                    least = dist
                    closest = g
        return least, closest

    def isSafeToGraze(self):
        p1 = self.worldPosition.copy()
        p1.z = 0
        tractor = GameLogic.getCurrentScene().objects['tractor']
        p2 = tractor.worldPosition.copy()
        p2.z = 0
        dist = (p1 - p2).magnitude
        return dist > 3*self.r1
        

    def avoid(self):
        p1 = self.worldPosition.copy()
        p1.z = 0
        result = self.blank.copy()
        for sheep in self.flock:
            p2 = sheep.worldPosition.copy()
            p2.z = 0
            dist = (p1 - p2).magnitude
            angle = atan2(p1.y - p2.y,p1.x - p2.x)
            
            if 0 < dist < self.r1:
                size = 1/dist**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)

        try: #Will fail if there is no ram.
            ram = GameLogic.getCurrentScene().objects['ram']
            p2 = ram.worldPosition.copy()
            p2.z = 0
            dist = (p1 - p2).magnitude
            angle = atan2(p1.y - p2.y,p1.x - p2.x)
            
            if 0 < dist < 1.5*self.r1:
                size = 1.5/dist**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)
        except:
            pass

        result = result + self.avoidStatic()
        tractor = GameLogic.getCurrentScene().objects['tractor']
        p2 = tractor.worldPosition.copy()
        p2.z = 0
        dist = (p1 - p2).magnitude
        angle = atan2(p1.y - p2.y,p1.x - p2.x)
        
        if 0 < dist < 3*self.r1:
            size = 5/dist**2
            result.x = result.x  + size*cos(angle)
            result.y = result.y + size*sin(angle)
            if result.magnitude > 0.05:
                self.run()
                result.normalize()
                return result

        if result.magnitude > 0.04:
            self.flounder()
        else:
            self.walk()
        result.normalize()
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
            
            if self.r1 < dist < 2*self.r1:
                size = 2/dist**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)
            if dist <= self.r1:
                size = 4/dist**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)

        for v in bigObstacles:
            p2 = v.copy()
            p2.z = 0
            dist = (p1 - p2).magnitude
            angle = atan2(p1.y - p2.y,p1.x - p2.x)
            
            if 4*self.r1 < dist < 7*self.r1:
                size = 3.5/(dist-3.5*self.r1)**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)
            elif 0 < dist <= 4*self.r1:
                size = 4/dist**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)

        for v in fences:
            p2 = v.copy()
            p2.z = 0
            dist = (p1 - p2).magnitude
            angle = atan2(p1.y - p2.y,p1.x - p2.x)
            
            if 2*self.r1 < dist < 3*self.r1:
                size = 2/dist**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)
            elif 0 < dist <= 2*self.r1:
                size = 10/dist**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)
        return result
            
    
    def center(self):
        p1 = self.worldPosition.copy()
        p1.z = 0
        result = self.blank.copy()
        close = 0
        for sheep in self.flock:
            p2 = sheep.worldPosition.copy()
            p2.z = 0
            dist = (p1 - p2).magnitude
            
            if dist < self.r2:
                result.x = result.x  + p2.x
                result.y = result.y + p2.y
                close = close + 1
                try:
                    if sheep.leader:
                        for i in range(2):
                            result.x = result.x  + p2.x
                            result.y = result.y + p2.y
                            close = close + 1
                except:
                    pass
        result = result/close

        toCenterVector = result - p1
        toCenterVector.normalize()
        return toCenterVector

    def closestLeader(self):
        # Closest leader to a sheep
        p1 = self.worldPosition.copy()
        p1.z = 0
        least = 0
        closest = None
        for sheep in self.flock:
            #print("a")
            p2 = sheep.worldPosition.copy()
            p2.z = 0
            dist = (p1 - p2).magnitude
            if not least or dist < least:
                if dist != 0:
                    least = dist
                    closest = p2
        return least, closest
    
    def match(self):
        p1 = self.worldPosition.copy()
        p1.z = 0
        result = self.blank.copy()
        close = 0
        for sheep in self.flock:
            p2 = sheep.worldPosition.copy()
            p2.z = 0
            dist = (p1 - p2).magnitude
            
            if dist < self.r2:
                temp = sheep.orientation[:][1].copy()
                result.x = result.x  + temp.x
                result.y = result.y + temp.y
                close = close + 1
                try:
                    if sheep.leader:
                        for i in range(2):
                            result.x = result.x  + temp.x
                            result.y = result.y + temp.y
                            close = close + 1
                except:
                    pass
        result = result/close
        result.normalize()

        return result
    
    def vary(self):
        theta = random() * 2*pi
        temp = self.blank.copy()
        temp.x, temp.y, temp.z = cos(theta), sin(theta), 0
        return temp

    def forage(self):
        if not self.hungry() and not self.hungryFollowers():
            return self.blank.copy()
        
        p1 = self.worldPosition.copy()
        p1.z = 0
        result = self.blank.copy()
        p2 = self.closestGrass()[1]
        p2.z = 0
        dist = (p1 - p2).magnitude
        if (self.hungry() and (self.leader or dist < self.r2)) or (self.leader and self.hungryFollowers() and dist > self.r1):
            # Move yourself to food or get closer to it for your followers
            angle = atan2(p2.y - p1.y,p2.x - p1.x)
            result.x = result.x  + cos(angle)
            result.y = result.y + sin(angle)
        if not self.hungry() and self.leader and self.hungryFollowers() and dist < self.r1:
            # Make room for hungry followers
            angle = atan2(p1.y - p2.y,p1.x - p2.x)
            result.x = result.x  + cos(angle)
            result.y = result.y + sin(angle)
        
        result.normalize()
        return result

    def unite(self):
        if not self.leader:
            return self.blank.copy()
        size, target = self.closestLeader()
        result = target - self.worldPosition.copy()
        result.normalize()
        if size/self.r2 > 4:
            return result
        if size/self.r2 > 2:
            return result * 2
        if size/self.r2 > 1:
            return result * 3
        return result * 4    
    

    def decideTurn(self,current,target):
        toTurn = angleFromVectors(current,target)
        if abs(toTurn) > 2*pi/3:
            return sign(toTurn)*0.03
        elif abs(toTurn) > pi/2:
            return sign(toTurn)*0.02
        elif abs(toTurn) == 0:
            return 0
        else:
            return sign(toTurn)*0.01
            
    def turn(self,angle):
        self.act('motion').dRot = (0,0,angle)

    def needsToBeLeader(self):
        p1 = self.worldPosition.copy()
        p1.z = 0
        for sheep in self.flock:
            p2 = sheep.worldPosition.copy()
            p2.z = 0
            dist = (p1 - p2).magnitude
            if 0 < dist < self.r2:
                try:
                    if sheep.leader:
                        #if self.leader:
                            #print("I'll follow now!")
                        return False
                except:
                    print("oops!")
                    pass
        #if self.leader:
            #print("I'm stil gonna lead!")
        
        return True

    def updateHunger(self):
        self.hunger = self.hunger + (time() - self.lastTime) * self.hungerGrowth
        self.lastTime = time()
        
        
    def update(self):
        #self.fallCheck()
        self.flock = [ob for ob in GameLogic.getCurrentScene().objects if ob.name == "sheep_cute"]

        self.leader = self.needsToBeLeader()
        if self.leader:
            self.scaling = (5,5,5)
        else:
            self.scaling = (3/2,3/2,3/2)
                
            
        self.navigate()
        self.updateHunger()
        #self.controller.activate(self.act(self.status))
        self.controller.activate(self.act('motion'))
        #print(self.status, "at", self.worldPosition)
        #print(self.leader, self.hungry())

    def fallCheck(self):
        # This doesn't work yet. I was looking at respawning them if they fall off the edge.
        if self.worldPosition.z < -10:
            self.worldPosition = (0,0,1)
        
def init(cont):
    if not cont.owner['initialized']:
        print(cont.owner.name)
        sheep = Sheep(cont.owner)
        sheep.controller = cont
        sheep.run()
        #sheep.controller.activate(sheep.act('helpless'))
        cont.owner['initialized'] = True
    else:
        cont.owner.update()

def seeObstacle(cont):
    pass
##    flock = [ob for ob in GameLogic.getCurrentScene().objects if 'initialized' in ob]
##    for sheep in flock:
##        if sheep.worldPosition == cont.owner.worldPosition:
##            print("found one!")
##            obstacle = cont.owner.worldPosition.copy()
##            obstacle.y = obstacle.y + 4
##            if not tooClose(obstacle,sheep.obstacles):
##                sheep.obstacles.append(obstacle)
##        sheep.obstacles = tooFar(sheep.worldPosition,sheep.obstacles)
##
##def tooClose(pos,vectorList):
##    for v in vectorList:
##        dist = (pos - v).magnitude
##        if dist < 2:
##            return True
##    return False
##
##def tooFar(pos,vectorList):
##    new = []
##    for v in vectorList:
##        dist = (pos-v).magnitude
##        if dist < 25:
##            new.append(v)
##    return new
    
    

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

def wasHit(cont):
##    flock = [ob for ob in GameLogic.getCurrentScene().objects if 'initialized' in ob]
##    for sheep in flock:
##        if sheep.worldPosition == cont.owner.worldPosition:
##            sheep.hit()
##            sheep.hitTime = time()
    cont.owner.hit()
    cont.owner.hitTime = time()

def sign(num):
    if num >= 0:
        return 1
    return -1
