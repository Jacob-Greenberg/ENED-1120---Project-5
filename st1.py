#!/usr/bin/env python3

from final import *

fubar = False

X = 27
Y = 18


"""
Definitely a more elegant way to do this, but I'm not sure how to do it
"""
if(not fubar):
    #Go to the given coordinate
    fubar = coordinateMove(X-6,Y+6)

if(not fubar):
    #Sleep for 5 seconds
    time.sleep(5)

if(not fubar):
    #Go to home B
    coordinateMove(Y+6,96-X)