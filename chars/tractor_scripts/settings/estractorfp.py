# file: estractorfp.py
# author: Andrew Reisner
# Settings for the first person eat sheep tractor

from math import pi
import configparser
from os.path import dirname,realpath
from os import name as osname

if osname == 'nt': # stupid windows...
    deli = '\\'
else:
    deli = '/'

cfg_file = dirname(realpath(__file__))
for i in range(3):
    cfg_file = cfg_file[0:cfg_file.rfind(deli)]
cfg_file += '/global.cfg'

gc = configparser.ConfigParser()
gc.read(cfg_file)


# location of wheel
WHEEL = gc.get('wheel','port')

# Positions for tires in blender model (blender units)
TIRE_POS = ((.371,  -.539, -.3425), # front driver's tire
            (-.371, -.539, -.3425), # front passenger's tire
            (.34,   .276,  -.3425),      # rear driver's tire
            (-.34,  .276,  -.3425))      # rear passenger's tire
# the positions of the tires identified in the previous tuple will
# remain consistent throughout this file, (FD,FP,RD,RP).

TIRE_RADIUS = (.3, .3, .3, .3)

TIRE_SUSP = {
             'height': (0.02166666, 0.02166666, 0.0499999999, 0.0499999999),
             'angle': ((0.0,0,-1),
                       (0.0,0,-1),
                       (0.0,0,-1),
                       (0.0,0,-1)),
             'compression': (gc.getfloat('suspension','compression_FD'),
                             gc.getfloat('suspension','compression_FP'),
                             gc.getfloat('suspension','compression_RD'),
                             gc.getfloat('suspension','compression_RP')),
             'damping': (gc.getfloat('suspension','damping_FD'),
                         gc.getfloat('suspension','damping_FP'),
                         gc.getfloat('suspension','damping_RD'),
                         gc.getfloat('suspension','damping_RP')),
             'stiffness': (gc.getfloat('suspension','stiffness_FD'),
                           gc.getfloat('suspension','stiffness_FP'),
                           gc.getfloat('suspension','stiffness_RD'),
                           gc.getfloat('suspension','stiffness_RP')),
             }

TIRE_AXIS = ((-1.0,0.0,0.0),
             (-1.0,0.0,0.0),
             (-1.0,0.0,0.0),
             (-1.0,0.0,0.0))

TIRE_STEER = (gc.getboolean('tire','steerable_FD'),
              gc.getboolean('tire','steerable_FP'),
              gc.getboolean('tire','steerable_RD'),
              gc.getboolean('tire','steerable_RP'))

# name of tire objects in blender
TIRE_OBJS = ('TireFD', 'TireFP','TireRD', 'TireRP')

TIRE_GRIP = (gc.getfloat('tire','grip_FD'),
             gc.getfloat('tire','grip_FP'),
             gc.getfloat('tire','grip_RD'),
             gc.getfloat('tire','grip_RP'))

ROLL_INFLUENCE = (gc.getfloat('tire','rollInfluence_FD'),
                  gc.getfloat('tire','rollInfluence_FP'),
                  gc.getfloat('tire','rollInfluence_RD'),
                  gc.getfloat('tire','rollInfluence_RP'),)

FORWARD_POWER = 60.0

BACKWARD_POWER = 30.0

# flip threshold
FLIP_THRESH = gc.getfloat('game','flipThreshold')

CRUISE_CONTROL = {
                  'kp': gc.getfloat('cruise_control','kp'),
                  'ki': gc.getfloat('cruise_control','ki'),
                  'kd': gc.getfloat('cruise_control','kd'),
                  'SP': gc.getfloat('cruise_control','SP'),
                  }
CALIBRATION = {
    'left_max' : gc.getfloat('wheel','left_max'),
    'midpoint' : gc.getfloat('wheel','midpoint'),
    'right_max': gc.getfloat('wheel','right_max'),
    }
