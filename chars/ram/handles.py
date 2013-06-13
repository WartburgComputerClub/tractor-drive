import bge
from ram import Ram

def init(cont):
    ram = Ram(cont.owner)
    cont.owner.controller = cont
    cont.owner['initialized'] = True

def update(cont):
    if not cont.owner['initialized']:
        init(cont)
    else:
        cont.owner.update()
