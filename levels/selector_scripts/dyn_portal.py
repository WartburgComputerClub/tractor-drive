
import GameLogic
from bge import texture,logic 
from mathutils import Vector, Matrix
from math import sin,cos,pi

def main(cont):
    # only proceed if we are warping
    if not cont.sensors['trigger_warp_script'].positive:
        return

    own = cont.owner
    own_pos = Vector(own.worldPosition)

    sce = GameLogic.getCurrentScene()

    blendFiles = GameLogic.getBlendFileList('//')
    blendFiles += GameLogic.getBlendFileList('//levels')
    
    blendFiles = dict([(b, None) for b in blendFiles]).keys()
    blendFiles = list(blendFiles) # py3 has its own dict_keys type
    
    blendFiles.sort()

    for b in blendFiles[:]:
        # get rid of this file
        if 'portal_world' in b:
            blendFiles.remove(b)
        if 'library' in b:
            blendFiles.remove(b)
            
    print(blendFiles)
    totFiles = len(blendFiles)

    if not totFiles:
        print('No levels found!')
        return
    # radius for paintings to be displayed in exhibit
    r = 11
    theta = 0 # starting angle for first painting
    totFiles = float(totFiles)
    logic.texture = len(blendFiles)*[2]
    pos_xy = [0,0,0]
    for i,f in enumerate(blendFiles):
        theta = 2*pi* (i/totFiles)
        pos_xy[2] = 1.8
        pos_xy[0] = r*cos(theta)
        pos_xy[1] = r*sin(theta)

        # dynamically change texture
        actu_add_object = cont.actuators['add_dyn_portal.00'+str(i+1)]
        actu_add_object.instantAddObject()
        new_portal = actu_add_object.objectLastCreated
        ID = texture.materialID(new_portal,'MAMyMaterial.00' +str(i+1))
        object_texture = texture.Texture(new_portal,ID)
        url = logic.expandPath('//' + f[0:-6] + '.jpg')
        new_source = texture.ImageFFmpeg(url)
        logic.texture.append(object_texture)
        object_texture.source = new_source
        object_texture.refresh(False)
        
        new_portal.worldPosition = pos_xy

        d,new_vect,local = new_portal.getVectTo((0,0,1))
        new_portal.alignAxisToVect(new_vect,0)
        new_portal.alignAxisToVect(new_vect,1)
        new_portal.alignAxisToVect(new_vect,2)

        new_portal['portal_blend'] = '//' + f
            
        own.endObject() # may as well distroy, wont use anymore
