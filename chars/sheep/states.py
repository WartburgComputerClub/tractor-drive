from game.types import GameObjectState
from game.environment import Environment

class WanderState(GameObjectState):
    
    def enter(self):
        self.owner.walk()
        
    def update(self):
        owner = self.owner
    
