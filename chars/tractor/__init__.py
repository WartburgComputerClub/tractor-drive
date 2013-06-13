import bge

from tractor.states import *
from tractor.sensors import *
from game.types import GameObject
from game.sensors import Timer

class Tractor(GameObject):
    
    def initHook(self):
        self.wheel = None
        self.cruise_control = None
        self.startPos = self.worldPosition.copy()
        self.startOrientation = self.orientation.copy()
        self.debug = False

        self.flipSensor = FlipSensor(self)
        self.activeSensor = ActiveSensor(self)
        self.stuckSensor = StuckSensor(self)
        self.timer = Timer(self)
        self.timer.connect(self.restart)
        self.timer.activate()
        self.flipSensor.connect(self.reset)
        self.stuckSensor.connect(self.reset)
        self.addSensor(self.flipSensor)
        self.addSensor(self.activeSensor)
        self.addSensor(self.timer)
        self.addSensor(self.stuckSensor)

        self.setState(IdleState(self))
                
    def setup(self,settings):
        
        self.settings = settings
        
        self.initPhysics()
        self.initTires()
        self.addTires()
        self.initSusp()

        self.cruise_control = CruiseControl(settings)
        
        wheel = Wheel(settings)
        if wheel.connected():
            self.wheel = wheel

        self.timer.timeout = self.settings.TIMEOUT

    def initSusp(self):
        settings = self.settings
        for i in range(4):
            self.vid.setTyreFriction(settings.TIRE_GRIP[i],i)
            self.vid.setSuspensionCompression(settings.TIRE_SUSP['compression'][i],i)
            self.vid.setSuspensionDamping(settings.TIRE_SUSP['damping'][i],i)
            self.vid.setSuspensionStiffness(settings.TIRE_SUSP['stiffness'][i],i)
            self.vid.setRollInfluence(settings.ROLL_INFLUENCE[i],i)
        
    def initPhysics(self):
        phid = self.getPhysicsId()
        constraint = bge.constraints.createConstraint(phid,0,11)
        cid = constraint.getConstraintId()
        self.vid = bge.constraints.getVehicleConstraint(cid)
        self['vehicleID'] = self.vid
        
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
            
    def getSpeed(self):
        return -1*self.getLinearVelocity(True)[1]
            
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
                
    def reset(self):
        self.worldPosition = self.startPos
        self.orientation = self.startOrientation
        self.localLinearVelocity = Vector((0,0,0))
        self.localAngularVelocity = Vector((0,0,0))
        self.setState(IdleState(self))

    def updateHook(self):
        if self.controller.sensors['d'].positive:
            self.debug = True
            self.currState.message('')
        elif self.controller.sensors['f'].positive:
            self.debug = False
            self.currState.message('')

    def restart(self):
            self.controller.activate(self.actuators['restart_game'])

from tractor.handles import *
