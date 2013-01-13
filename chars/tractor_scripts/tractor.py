# file tractor.py
# author: Andrew Reisner <andrew.reisner@gmail.com>
# This class makes it easy to interact with the 
# bullet vehicle physics
import bge
from math import acos
import mathutils

class Tractor:
    
    def __init__(self,obj,settings):
        self.active = False
        self.simFlag = False
        self.simOver = False
                
        self.stuckCount = 0
        self.vel = []
        # blender object
        self.obj = obj
        
        self.settings = settings
        
        self.initPhysics()
        
        self.initTires()
        
        self.addTires()
        
        self.initSusp()
        
    def simFinished(self):
        # add time limit
        return self.simOver
        
    def setSim(self):
        self.simFlag = True
        self.active = True
        self.simFile = open('sim.data','w')
        
    def initSusp(self):
        settings = self.settings
        for i in range(4):
            self.vid.setTyreFriction(settings.TIRE_GRIP[i],i)
            self.vid.setSuspensionCompression(settings.TIRE_SUSP['compression'][i],i)
            self.vid.setSuspensionDamping(settings.TIRE_SUSP['damping'][i],i)
            self.vid.setSuspensionStiffness(settings.TIRE_SUSP['stiffness'][i],i)
            self.vid.setRollInfluence(settings.ROLL_INFLUENCE[i],i)
        
    def initPhysics(self):
        phid = self.obj.getPhysicsId()
        constraint = bge.constraints.createConstraint(phid,0,11)
        cid = constraint.getConstraintId()
        self.vid = bge.constraints.getVehicleConstraint(cid)
        self.obj['vehicleID'] = self.vid
        
    def initTires(self):
        settings = self.settings
        scene = bge.logic.getCurrentScene()
        objs = scene.objects
        self.tires = (objs[settings.TIRE_OBJS[0]],
                      objs[settings.TIRE_OBJS[1]],
                      objs[settings.TIRE_OBJS[2]],
                      objs[settings.TIRE_OBJS[3]])

    def addTires(self):
        settings = self.settings
        for i in range(4):
            self.vid.addWheel(self.tires[i],
                              settings.TIRE_POS[i],
                              settings.TIRE_SUSP['angle'][i],
                              settings.TIRE_AXIS[i],
                              settings.TIRE_SUSP['height'][i],
                              settings.TIRE_RADIUS[i],
                              settings.TIRE_STEER[i])
    
    def setPower(self,power):
        for i in range(4):
            self.vid.applyEngineForce(power,i)
            
    def forward(self):
        self.setPower(self.settings.FORWARD_POWER)
    
    def backward(self):
        self.setPower(-1*self.settings.BACKWARD_POWER)
        
    def steer(self,value):
        #print("Steer:",value)
        settings = self.settings
        for i in range(4):
            if (settings.TIRE_STEER[i]):
                self.vid.setSteeringValue(value,i)
                
    def flipped(self):
        '''
        returns true if we detect that the tractor
        flipped beyond a given threshold and false
        otherwise
        '''
        tractor = self.obj
        # get angle between global and local z value
        val = tractor.getAxisVect((0,0,1)) 
        cos_val = val[2]/(val[0]**2 + val[1]**2 + val[2]**2)**(.5)
        theta = acos(cos_val)
        if theta > self.settings.FLIP_THRESH:
            return True
        else:
            return False
        
    def stuck(self):
        '''
        returns true if we detect hat the tractor
        is stuck on an object. (happens when using
        the steering wheel)
        '''
        car = self.obj
        wheel = car['wheel']
        if (wheel.connected() and self.active):
            resolution = 300
            threshold = .5
            if (self.stuckCount == resolution):
                average = sum(self.vel)/len(self.vel)
                if (average) < threshold:
                    return True
                self.stuckCount = 0
                self.vel = []
            else:
                self.stuckCount += 1
                self.vel.append(self.obj.getLinearVelocity().magnitude)
            return False
        else:
            return False
    
