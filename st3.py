#!/usr/bin/env python3

from final import *
import os

#Switch to the ev3 to display print statements
os.system('setfont Lat15-TerminusBold14')

Y = 15

goalBox = 1
readAttempts = 0

#Go to the given coordinate
coordinateMove(0,Y)

#Turn to face box
turnDegrees(90)

#Determine box type and display it

reading = barcode()
if(reading == 1):
    print("Box type: 1")
elif(reading  == 2):
    print("Box type: 2")
elif(reading  == 3):
    print("Box type: 3")
elif(reading == 4):
    print("Box type: 4")
else:
    print("Box 1")

if(reading == goalBox):
    print("Correct box")

time.sleep(5)

#Super cool code that would retry the barcode - but the since the lift doesn't reset it doesn't work
"""
#Read & Display barcode, if invalid, try again
while(barcode == -1 and readAttempts < 5):
    if(barcode() == 1):
        print("Box type: 1")
        break
    elif(barcode() == 2):
        print("Box type: 2")
        break
    elif(barcode() == 3):
        print("Box type: 3")
        break
    elif(barcode() == 4):
        print("Box type: 4")
        break
    #readAttempts = readAttempts + 1

if(readAttempts <= 5):
    print("Error reading barcode")
"""