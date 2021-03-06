import GameLogic
from mathutils import Vector
from math import atan2,pi,cos,sin
from random import random

class Environment:

    instance = None
    
    def __init__(self):
        self.r1 = 4
        self.r2 = 6
        self.bigObstacles = []
        self.obstacles = []
        self.fences = []
        for obj in GameLogic.getCurrentScene().objects:
            if obj.name in ['right_side_tree','left_side_tree','small_sphere',
                    'fan_tree','cube','cylinder_tree','chevron_tree']:
                self.obstacles.append(obj.worldPosition.copy())
            elif obj.name in ['water','square_house','Front House','L_house','shed',
                              'large_square_house','front_left_house','asymm_shed','small_house','small_house.001','House','Barn','bridge']:
                self.bigObstacles.append(obj.worldPosition.copy())
            elif obj.name == 'fence_long':
                self.fences.append(obj.worldPosition.copy())   
            elif obj.name.startswith('water'):
                self.obstacles.append(obj.worldPosition.copy())

    @staticmethod
    def getInstance():
        if Environment.instance == None:
            Environment.instance = Environment()
        return Environment.instance
        
    def staticAvoidanceVector(self,playerPos):
        '''find an avoidance vector for static objects in scene

        Parameters:
        playerPos -- the 3D Vector of the player's position
       
        Returns:
        2D Vector describing a way to avoid the static 
        objects in the scene (fences, houses, trees,...)
        '''
        p1 = playerPos.copy()
        p1.z = 0
        result = Vector((0,0,0))
        for v in self.obstacles:
            p2 = v.copy()
            p2.z = 0
            dist = (p1 - p2).magnitude
            angle = atan2(p1.y - p2.y,p1.x - p2.x)
            
            if 0 < dist < 2*self.r1:
                size = 2/dist**2
                result.x = result.x  + size*cos(angle)
                result.y = result.y + size*sin(angle)

        for v in self.bigObstacles:
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

        for v in self.fences:
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
        return Vector((result.x,result.y))
        

