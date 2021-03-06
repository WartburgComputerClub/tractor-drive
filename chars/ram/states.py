from math import pi

from game.types import GameObjectState
from game.environment import Environment

class WanderState(GameObjectState):
    
    r1 = 4
    r2 = 20
    
    def enter(self):
        self.owner.walk()

    def update(self):
        owner = self.owner
        if owner.distanceToTractor() <= self.r2:
            owner.setState(AttackState(owner))
        avoidance = Environment.getInstance().staticAvoidanceVector(owner.worldPosition)
        randomness = owner.randomDirectionVector()
        owner.iterTurn(5*avoidance + randomness)
        
class AttackState(GameObjectState):
    
    r1 = 4
    r2 = 20
    
    def enter(self):
        self.owner.run()
        
    def update(self):
        owner = self.owner
        dist = owner.distanceToTractor()
        if self.r2/2 < dist < self.r2:
            if owner.tractorAimError() > pi/6:
                owner.walk()
                owner.iterTurn(5*Environment.getInstance().staticAvoidanceVector(owner.worldPosition) + owner.randomDirectionVector() + 10*owner.vectorToTractor())
            else:
                owner.setAnimation('attack')
                owner.setVelocity((0, 0))
                owner.turn(0)
        elif self.r1 < dist <= self.r2/2:
            owner.run()
            owner.iterTurn(5*Environment.getInstance().staticAvoidanceVector(owner.worldPosition) + owner.randomDirectionVector() + 10* owner.vectorToTractor())
        elif 0 < dist <= self.r1:
            owner.setAnimation('attack')
            owner.setVelocity((0, 0.07))
            owner.turn(0)
        else:
            owner.setState(WanderState(owner))
