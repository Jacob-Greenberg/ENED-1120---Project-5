#!/usr/bin/env python3

from final import *

"""
Make some way to disable object avoidance since it'll get tripped up when lifting the box
"""

"""
IMPORTANT!!!!!!
This program assumes the robot is directly in front of the box
Normally pickup() resets the position but since we start in front of the box it wont reset
"""

pickup()

location = 12


#moveBack(6)
turnDegrees(-90)
moveDistance(location - 24)