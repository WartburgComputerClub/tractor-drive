# file: init.py 
# author: Andrew Reisner
# This script initializes a third person eat sheep tractor
# and is called from blender on startup

import bge

from tractor_scripts.tractor import Tractor
from tractor_scripts.wheel import Wheel
from tractor_scripts.cruise_control import CruiseControl

def main(cont):
	if cont.owner['is3P']:
		if cont.owner['isUser']:
			import tractor_scripts.settings.estractor as settings
		else:
			import tractor_scripts.settings.estractor_sentient as settings
	else:
		import tractor_scripts.settings.estractorfp as settings

	cont.activate('set_hud')
	
	trac = Tractor(cont.owner)
	trac.setup(settings)
	# make a handle in the blender object so we can access this
	# instance later
		
	cc = CruiseControl(settings)
	cont.owner['cc'] = cc

	if cont.owner['isUser']:
		wheel = Wheel(settings)
		cont.owner['wheel'] = wheel
