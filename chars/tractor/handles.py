import bge

from tractor import Tractor
from tractor.wheel import Wheel
from tractor.cruise_control import CruiseControl

def init(cont):
    if cont.owner['is3P']:
        if cont.owner['isUser']:
            import tractor.settings.estractor as settings
        else:
            import tractor.settings.estractor_sentient as settings
    else:
        import tractor.settings.estractorfp as settings        
        
    cont.activate('set_hud')
    
    trac = Tractor(cont.owner)
    trac.setup(settings)
    
    cont.owner.controller = cont

    cont.owner['initialized'] = True

def update(cont):
    if not cont.owner['initialized']:
        init(cont)
    else:
        cont.owner.update()

def portal(cont):
    # function courtesy of the YoFrankie folks
    own = cont.owner
    
    portal_ob = cont.sensors['portal_touch'].hitObject
    
    if not portal_ob:
        return
    #sce = bge.logic.getCurrentScene()
    #target_name = portal_ob['portal']

    # A bit dodgy, for the first logic tick show the loading text only
    # portal collision must be on pulse so its gets a second tick and runs the portal code below.
    for sce in bge.logic.getSceneList():
        if sce.name == 'hud':
            print('keys:',sce.objects)
            loading_ob = sce.objects['loading']#sce.objects['OBloading']
            if not loading_ob.visible:
                loading_ob.visible = True
                return
            
    
    set_blend_actu = cont.actuators['portal_blend']
    set_blend_actu.fileName = portal_ob['portal_blend']

    cont.activate(set_blend_actu)
