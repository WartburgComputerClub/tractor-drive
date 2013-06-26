from math import pi,cos,sin,atan2
from mathutils import Vector
from random import random

from game.types import GameObjectState
from game.environment import Environment

class WanderState(GameObjectState):

    def enter(self):
        self.owner.walk()


class FlockState(GameObjectState):
    
    r1 = 4
    r2 = 32

    def enter(self):
        self.owner.walk()
        
    def update(self):
        owner = self.owner
        self.direction = Vector((0,0))

        self.avoid()
        #self.center()
        #self.match()
        self.vary()

        owner.iterTurn(self.direction)

    def center(self):
        owner = self.owner
        centering = Vector((0,0))
        p1 = Vector((owner.worldPosition.x,owner.worldPosition.y))
        close = 0
        for sheep in owner.flock:
            p2 = Vector((owner.worldPosition.x,owner.worldPosition.y))
            dist = (p1 - p2).magnitude

            if dist < self.r2:
                centering +=  p2
                close += 1
        centering /= close
        toCenter = centering - p1
        toCenter.normalize()
        self.direction += 4 * centering

    def avoid(self):
        owner = self.owner
        avoidance = Vector((0,0))
        
        for sheep in owner.flock:
            p1 = Vector((owner.worldPosition.x,owner.worldPosition.y))
            p2 = Vector((sheep.worldPosition.x,sheep.worldPosition.y))
            dist = (p1 - p2).magnitude
            theta = atan2(p1.y - p2.y,p1.x - p2.x)
            if 0 < dist < self.r1:
                size = 1/dist**2
                avoidance.x += size*cos(theta)
                avoidance.y += size*sin(theta)
            
        env = Environment.getInstance()
        avoidance += env.staticAvoidanceVector(owner.worldPosition)
        
        try:
            ramAvoidance = owner.avoidanceVector('ram')
            ramDist = owner.distance('ram')
            if 0 < ramDist < 1.5*self.r1:
                ramAvoidance *= 1.5/ramDist**2
                avoidance += ramAvoidance
        except:
            pass

        tractorDist = owner.distance('tractor')
        if 0 < tractorDist < 3*self.r1:
            avoidance += owner.avoidanceVector('tractor')*(5/tractorDist**2)
            if avoidance.magnitude > 0.05:
                owner.run()
        if avoidance.magnitude > 0.04:
            owner.flounder()
        else:
            owner.walk()

        avoidance.normalize()
        self.direction += avoidance*10
        
    def match(self):
        owner = self.owner
        p1 = Vector((owner.worldPosition.x, owner.worldPosition.y))
        matching = Vector((0,0))
        close = 0
    
        for sheep in owner.flock:
            p2 = Vector((sheep.worldPosition.x, sheep.worldPosition.y))
            dist = (p1 - p2).magnitude
            
            if dist < self.r2:
                sheepFace = sheep.orientation[:][1]
                sheepFace = Vector((sheepFace.x,sheepFace.y))
                matching += sheepFace
                close += 1
        matching /= close
        matching.normalize()
        self.direction += 4 * matching

    def vary(self):
        theta = random() * 2*pi
        self.direction += Vector((cos(theta),sin(theta)))

class LeadState(GameObjectState):

    def enter(self):
        self.owner.walk()

    def update(self):
        pass
