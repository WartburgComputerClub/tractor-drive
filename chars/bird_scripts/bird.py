import bge

class Bird(bge.types.KX_GameObject):
    
    def __init__(self,old_owner):
        self.animations = {}
        pass
    
    def registerAnimation(self,name,controller,actuator):
        self.animations[name] = (controller,actuator)
    
    def animate(self,action):
        if action in self.animations.keys():
            self.animations[action][0].activate(self.animations[action][1])
    
def init(cont):
    bird = Bird(cont.owner)
    acts = cont.actuators
    bird.registerAnimation('fly', cont,acts['flying'])
    bird.animate('fly')
