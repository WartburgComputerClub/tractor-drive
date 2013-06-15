import bge

class GameObject(bge.types.KX_GameObject):
    
    def __init__(self,old_owner):
        self.currState = None
        self.senses = []
        self.initHook()

    def initHook(self):
        pass

    def setState(self,newstate):
        if self.currState != None:
            self.currState.leave()
        self.currState = newstate
        self.currState.enter()
        
    def update(self):
        self.updateHook()

        for sensor in self.senses:
            if sensor.active:
                sensor.update()

        self.currState.update()
        
    def updateHook(self):
        pass

    def message(self,msg):
        self.currState.message()

    def addSensor(self,sensor):
        self.senses.append(sensor)

class AnimatedGameObject(GameObject):

    def __init__(self,old_owner):
        self.currState = None
        self.currAnimation = None
        self.actmap = {}
        self.senses = []
        self.initHook()

    def registerAnimation(self,name,actuatorName):
        self.actmap[name] = actuatorName

    def registerAnimations(self,mappedTuples):
        for mapping in mappedTuples:
            self.registerAnimation(mapping[0],mapping[1])

    def setAnimation(self,newAnim):
        if self.currAnimation != None:    
            self['controller'].deactivate(self.act(self.currAnimation))
        self.currAnimation = newAnim
        self['controller'].activate(self.act(newAnim))
        
    def act(self,name):
        return self['controller'].actuators[self.actmap[name]]
    
        
class GameObjectState:
    
    def __init__(self,owner):
        self.owner = owner
    
    def enter(self):
        pass
    
    def leave(self):
        pass
    
    def update(self):
        pass
    
    def message(self,msg):
        pass

class GameObjectSensor:
    
    def __init__(self,owner):
        self.owner = owner
        self.callbacks = []
        self.active = False
        self.initHook()

    def initHook(self):
        pass

    def update(self):
        pass

    def connect(self,callback):
        self.callbacks.append(callback)

    def trigger(self):
        for callback in self.callbacks:
            callback()

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def clear(self):
        del self.callbacks
        self.callbacks = []
