import bge


def update(cont):
    trac = cont.owner['handle']
    trac.setPower(2)
    trac.steer(0.5)

