import bge
from random import random
import mathutils

def bird(cont):
    print('here')
    scene = bge.logic.getCurrentScene()
    fences = [ob for ob in scene.objects if 'fence' in ob]
    spawner = cont.actuators['bird_spawn']
    for fence in fences:
        if random() < .50:
            print(fence.orientation)
            spawner.instantAddObject()
            new_bird = spawner.objectLastCreated
            new_bird.worldPosition = fence.worldPosition
            new_bird.scaling = [5,5,5]
            ident = mathutils.Matrix.Identity(3)
            ident[0][0] = -1
            new_bird.orientation = fence.orientation
            for i in range(3):
                new_bird.orientation[i][1] = fence.orientation[i][2]
                new_bird.orientation[i][2] = fence.orientation[i][1]
            


