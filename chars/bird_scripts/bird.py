import bge

class Bird(bge.types.KX_GameObject):
    
    def __init__(self,old_owner):
        self.actmap = {
            'fly':'flying'
            }
        pass
    
    def act(self,name):
        return self.controller.actuators[self.actmap[name]]

    def fly(self):
        self.controller.activate(self.act('fly'))
        self.status = 'fly'
    
    def idle(self):
        self.controller.deactivate(self.act(self.status))
        
    def update(self):
        pass
    
def init(cont):
    if cont.owner['initialized']:
        cont.owner.update()
    else:
        bird = Bird(cont.owner)
        bird.controller = cont
        bird.fly()
        bird['initialized'] = True

