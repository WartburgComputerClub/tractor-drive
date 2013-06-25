import bge

from ram import Ram
from ram.states import WanderState

def init(cont):
    ram = Ram(cont.owner)
    ram.setState(WanderState(ram))
    cont.owner['initialized'] = True

def update(cont):
    if not cont.owner['initialized']:
        init(cont)
    else:
        cont.owner.update()
