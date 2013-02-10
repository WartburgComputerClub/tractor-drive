import bge
import GameLogic
from math import atan2
    
def update(cont):
    cont.owner.setPower(4)
    cont.owner.steer(0.5)
    user = GameLogic.getCurrentScene().objects['tractor']
    uPos = user.worldPosition
    mePos = cont.owner.worldPosition
    diff = uPos - mePos
    print(diff)

