from game.types import GameObjectState
from game.environment import Environment

class WanderState(GameObjectState):
    
    def enter(self):
        self.owner.setAnimation('walk')
        self.owner.setVelocity((0,0.02))
        
    def update(self):
        owner = self.owner
    
