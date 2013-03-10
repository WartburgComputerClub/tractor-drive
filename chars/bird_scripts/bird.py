import bge
from mathutils import *

class Bird(bge.types.KX_GameObject):
    
    def __init__(self,old_owner):
        self.actmap = {
            'fly':'flying',
            'motion':'bird_motion',
            }
        self.r1 = 4
        self.r2 = 40
        self.vel  = Vector((0,.01,.04))
        self.alpha = .01
        self.beta = .01
        self.gamma = .01
        self.delta = .01
    
    def act(self,name):
        return self.controller.actuators[self.actmap[name]]

    def fly(self):
        self.controller.activate(self.act('fly'))

        self.status = 'fly'
    
    def idle(self):
        self.controller.deactivate(self.act(self.status))
        
    def update(self):

        r1 = []
        r2 = []
        scene = bge.logic.getCurrentScene()
        flock = [ob for ob in scene.objects if 'bird' in ob and ob.worldPosition != self.worldPosition]
        for i in range(len(flock)):
            if (flock[i].worldPosition - self.worldPosition).magnitude < self.r1:
                r1.append(i)
            elif (flock[i].worldPosition - self.worldPosition).magnitude < self.r2:
                r2.append(i)
        
        # SEPARATION
        f1 = self.worldPosition
        sigma = Vector((0,0,0))
        for s in r1:
            f2 = flock[s].worldPosition
            part = (( (f1-f2).normalized())/(f1-f2).magnitude)
            sigma += part
        v1 = sigma
        
        # ALIGNMENT
        v2 = Vector((0,0,0))
        for f in r2:
            v2 += flock[f].vel
        if len(r2) > 0:
            v2 = v2/len(r2)
        
        # COHESION
        sigma = Vector((0,0,0))
        for f in r2:
            sigma += flock[f].worldPosition
        if len(r2) > 0:
            v3 = sigma / len(r2) - f1
        else:
            v3 = Vector((0,0,0))

        self.vel = self.alpha*self.vel.normalized() + self.beta * v1.normalized() + self.gamma * v2.normalized() + self.delta * v3.normalized()

        self.alignAxisToVect(self.vel.normalized(),2,1)
        # need to align the wings too
        self.parent.children[0].alignAxisToVect(self.vel.normalized(),2,1)

        self.act('motion').dLoc = self.vel
        self.controller.activate(self.act('motion'))
        
def init(cont):
    if cont.owner['initialized']:
        cont.owner.update()
    else:
        bird = Bird(cont.owner)
        bird.controller = cont
        bird.fly()
        bird['initialized'] = True

