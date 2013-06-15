from math import pi

from game.types import GameObjectState
from game.environment import Environment

class WanderState(GameObjectState):
    
    r1 = 4
    r2 = 8
    
    def enter(self):
        self.owner.setAnimation('walk')
        self.owner.setVelocity((0, 0.02, 0))

    def update(self):
        owner = self.owner
        print("wander")
        print(Environment.getInstance().staticAvoidanceVector(owner))
        #if owner.distanceToTractor() <= self.r2:
        #    owner.setState(AttackState(owner))
        #owner.iterTurn(5*owner.environment.staticAvoidanceVector(owner) + owner.randomDirectionVector())
        
class AttackState(GameObjectState):
    
    r1 = 4
    r2 = 8
    
    def enter(self):
        self.owner.setAnimation('run')
        self.owner.setVelocity((0, .07, 0))
        
    def update(self):
        owner = self.owner
        print('aggressive')
        dist = owner.distanceToTractor()
        print(owner.vectorToTractor())
        if self.r2/2 < dist < self.r2:
            if owner.tractorAimError() > pi/6:
                owner.setAnimation('walk')
                owner.setVelocity((0, 0.02, 0))
                owner.iterTurn(5*Environment.getInstance.staticAvoidanceVector(owner) + owner.randomDirectionVector() + 10*owner.vectorToTractor())
            else:
                owner.setAnimation('attack')
                owner.setVelocity((0, 0, 0))
                owner.turn(0)
        elif self.r1 < dist <= self.r2/2:
            owner.setAnimation('run')
            owner.setVelocity((0, 0.07, 0))
            owner.iterTurn(5*Environment.getInstance.staticAvoidanceVector(owner) + owner.randomDirectionVector() + 10* owner.vectorToTractor())
        elif 0 < dist <= self.r1:
            owner.setAnimation('attack')
            owner.setVelocity((0, 0.07, 0))
            owner.turn(0)
        
        
    
    
