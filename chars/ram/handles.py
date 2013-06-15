import bge

from ram import Ram

def init(cont):
    cont.owner['controller'] = cont
    ram = Ram(cont.owner)
    cont.owner['initialized'] = True

def update(cont):
    if not cont.owner['initialized']:
        init(cont)
    else:
        cont.owner.update()
