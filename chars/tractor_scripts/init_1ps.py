# file: init_1ps.py 
# author: Andrew Reisner <andrew.reisner@gmail.com>
# This script initializes a first person eat sheep tractor
# and is called from blender on startup

import bge

from tractor_scripts.tractor import Tractor
from tractor_scripts.wheel import Wheel
from tractor_scripts.cruise_control import CruiseControl
import tractor_scripts.settings.estractorfp as settings

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
