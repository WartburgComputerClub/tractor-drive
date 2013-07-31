import GameLogic

def init(cont):
    for obj in GameLogic.getCurrentScene().objects:
        if 'dyn_warp_placer' == obj.name:
            owner = cont.owner
            owner.applyRotation((.1,0,0),True)
