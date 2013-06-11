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
        self.setup()

    def setup(self):
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
