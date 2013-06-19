import bge

from sheep import Sheep
from sheep.states import WanderState

def init(cont):
    sheep = Sheep(cont.owner)
    cont.owner.controller = cont
    sheep.setState(WanderState(sheep))
    cont.owner['initialized'] = True

def update(cont):
    if not cont.owner['initialized']:
        init(cont)
    else:
        cont.owner.update()
