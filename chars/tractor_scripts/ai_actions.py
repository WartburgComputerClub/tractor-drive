import bge
import GameLogic
from math import atan2, acos, pi, cos, sin
    
def update(cont):
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
