import bge

class GameObject(bge.types.KX_GameObject):
    
    def __init__(self,old_owner):
        self.currState = None
    
    def setState(self,newstate):
        if self.currState != None:
            self.currState.leave()
        self.currState = newstate
        self.currState.enter()
        
    def update(self):
        self.currState.update()
        
    def message(self,msg):
        self.currState.message()
        
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
