#!/usr/bin/env python3

from final import *

"""
Make some way to disable object avoidance since it'll get tripped up when lifting the box
"""

X = 27
Y = 18

fubar = False
goalBox = 1
rightBox = False

if(not fubar):
    #Go to the given coordinate
    fubar = coordinateMove(X-6,Y+6)

#Robot will backup here after reading the barcode
if(not fubar):
    turnDegrees(90)
    barcode()
    
    pickup()

turnDegrees(-90)
coordinateMove(Y+6,96-X)