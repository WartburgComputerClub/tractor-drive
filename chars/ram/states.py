from math import pi

from game.types import GameObjectState
from game.environment import Environment

class WanderState(GameObjectState):
    
    r1 = 4
    r2 = 20
    
    def enter(self):
        self.owner.setAnimation('walk')
        self.owner.setVelocity((0, 0.02))

    def update(self):
        owner = self.owner
        print("wander")
        if owner.distanceToTractor() <= self.r2:
            owner.setState(AttackState(owner))
        avoidance = Environment.getInstance().staticAvoidanceVector(owner.worldPosition)
        randomness = owner.randomDirectionVector()
        owner.iterTurn(5*avoidance + randomness)
        
class AttackState(GameObjectState):
    
    r1 = 4
    r2 = 20
    
    def enter(self):
        self.owner.setAnimation('run')
        self.owner.setVelocity((0, .07))
        
    def update(self):
        owner = self.owner
        dist = owner.distanceToTractor()
        if self.r2/2 < dist < self.r2:
            if owner.tractorAimError() > pi/6:
                owner.setAnimation('walk')
                owner.setVelocity((0, 0.02))
                owner.iterTurn(5*Environment.getInstance().staticAvoidanceVector(owner.worldPosition) + owner.randomDirectionVector() + 10*owner.vectorToTractor())
            else:
                owner.setAnimation('attack')
                owner.setVelocity((0, 0))
                owner.turn(0)
        elif self.r1 < dist <= self.r2/2:
            owner.setAnimation('run')
            owner.setVelocity((0, 0.07, 0))
            owner.iterTurn(5*Environment.getInstance().staticAvoidanceVector(owner.worldPosition) + owner.randomDirectionVector() + 10* owner.vectorToTractor())
        elif 0 < dist <= self.r1:
            owner.setAnimation('attack')
            owner.setVelocity((0, 0.07))
            owner.turn(0)
