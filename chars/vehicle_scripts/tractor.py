import bge
import GameLogic
from math import atan2, acos, pi, cos, sin
from vehicle_scripts.wheel import Wheel
from vehicle_scripts.cruise_control import CruiseControl
from vehicle_scripts.vehicle import Vehicle

def update(cont):
    if not cont.owner['initialized']:
        if cont.owner['is3P']:
            if cont.owner['isUser']:
                import vehicle_scripts.settings.estractor as settings
            else:
                import vehicle_scripts.settings.estractor_sentient as settings
        else:
            import vehicle_scripts.settings.estractorfp as settings
        
        cont.activate('set_hud')
        trac = Vehicle(cont.owner)
        trac.setup(settings)
        
        trac.cruise_control = CruiseControl(settings)
        
        if cont.owner['isUser']:
            wheel = Wheel(settings)
            cont.owner['wheel'] = wheel
        
        cont.owner['initialized'] = True
    else:
        if cont.owner['isUser']:
            user_update(cont)
        else:
            ai_update(cont)

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
    
def check_dead(cont):
        
    trac = cont.owner
    if trac.flipped():
        cont.activate(cont.actuators['restart_game'])
    elif trac.stuck() and not cont.sensors['d'].positive:
        cont.activate(cont.actuators['restart_game'])
    elif trac.timedOut():
        cont.activate(cont.actuators['restart_game'])
        
def user_update(a):
    check_dead(a)
    trac = a.owner

    wheel = trac['wheel']
    if wheel.connected() and trac.active:
        wheel.update()
        trac.steer(wheel.getSteer())
    # Cruise control calculations
    trac.cruise_control.update(trac.getSpeed())
    if not a.sensors['d'].positive: # disable cruise control
        trac.setPower(trac.cruise_control.getPower())
        
    # should we make active
    if not trac.active:
        if wheel.connected():
            prev = wheel.getSteer()
            wheel.update()
            if abs(prev - wheel.getSteer()) > .01:
                if trac.stuckCount > 2:
                    trac.active = True
                    trac.cruise_control.reset()      # reset cruise control (time drift)
                    trac.stuckCount = 0
                    
                else:
                    trac.stuckCount += 1
        else:
            trac.active = True

def ai_update(cont):
    check_dead(cont)
    cont.owner.setPower(4)
    cont.owner.steer(0)
    user = GameLogic.getCurrentScene().objects['tractor']
    uPos = user.worldPosition
    mePos = cont.owner.worldPosition
    meDir = cont.owner.localLinearVelocity
    uDir = user.localLinearVelocity
    diff = uPos - mePos
    diff.z = 0
    theta = angleBetween(diff, meDir)
    if diff.magnitude < 8:
        # User is close enough to the tractor to be considered
        print("close",end="")
        if theta < pi/2:
            print(", going", end = " ")
            # Tractor is going towards the user, should turn
            temp = mePos.copy()
            temp.x = cos(theta + pi/12)*meDir.magnitude
            temp.y = sin(theta + pi/12)*meDir.magnitude
            temp.z = 0
            temp0 = temp.copy()
            temp0.x = cos(theta - pi/12)*meDir.magnitude
            temp0.y = sin(theta - pi/12)*meDir.magnitude
            temp1 = mePos + temp - uPos - uDir
            temp1.z = 0
            temp2 = mePos + temp0 - uPos - uDir
            temp2.z = 0
            if temp1.magnitude > temp2.magnitude:
                # Turning right is away from the user.
                cont.owner.steer(-0.5)
                print("right.",end="")
            else:
                # Turning left is away from the user.
                cont.owner.steer(0.5)
                print("left.",end="")
        print()
    

def dot(v1,v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

def angleBetween(v1,v2):
    return acos(dot(v1,v2)/v1.magnitude/v2.magnitude)

