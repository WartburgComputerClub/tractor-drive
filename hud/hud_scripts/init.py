# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


# This sucks a bit, it updates both players life meters rather then just 1

import Rasterizer
import GameLogic

def main(cont):
	own= cont.owner
	#cont.activate("end_p2")
	
	for actu in cont.actuators:
		actu_own = actu.owner
		if actu_own.name.startswith('OBitem_'):
			actu_own.setVisible(False, True) # recursive, sets text invisible also
	
	'''
	print(dir(own))
	# set crap in a 
	point_p1 = [0.0,0.0,0.0]
	
	while own.pointInsideFrustum(point_p1):
		point_p1[2] += 0.02
	
	point_p1[2] -= 0.02
	
	while own.pointInsideFrustum(point_p1):
		point_p1[0] += 0.02
	
	point_p1[0] -= 0.02
	
		
	# own.perspective = 0
	cont.actuators["end_p2"].owner.localPosition = point_p1
	
	Rasterizer.setMaterialMode(0)
	
	'''
	cont.activate("hud_monitor_state")

