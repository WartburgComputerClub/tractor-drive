# file: init.py 
# author: Andrew Reisner
# This script initializes a third person eat sheep tractor
# and is called from blender on startup

import bge

from tractor_scripts.tractor import Tractor
from tractor_scripts.wheel import Wheel
from tractor_scripts.cruise_control import CruiseControl
import tractor_scripts.settings.estractor as settings

def main(cont):
	cont.activate('set_hud')
	
	trac = Tractor(cont.owner,settings)
	# make a handle in the blender object so we can access this
	# instance later
	cont.owner['handle'] = trac
	
	cc = CruiseControl(cont.owner,settings)
	cont.owner['cc'] = cc
	
	wheel = Wheel(settings)
	cont.owner['wheel'] = wheel
