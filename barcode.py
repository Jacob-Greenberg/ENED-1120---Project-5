#!/usr/bin/env python3
from ev3dev2.sensor import INPUT_4, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, TouchSensor
from ev3dev2.motor import MediumMotor, OUTPUT_D

#Initializations
ts = TouchSensor(INPUT_3)#Just for testing to end the loop
color = ColorSensor(INPUT_4)
liftMotor = MediumMotor(OUTPUT_D)
colorList = []
white = 0

type1and3 = [1,0]
type2 = [1,0,1,0]
type4 = [1,0,0,1]


#Codes are read left -> right | top -> bottom

#Rather than reading the code outright we detect the changes in color
#This simplifies everything but comes with a few caveats
#Mainly, if the barcode has fewer than then maximum number of bars we need another way to tell the robot to stop reading
#In my case this is done with a touch sensor placed at the top of the lift but it can also be done with a timer or other methods

#The main loop checks if the list has reached its maximum size or if the touch sensor is pressed
while(len(colorList) < 4 and not ts.is_pressed):
    #Since neither of those things are true we can continue to read the barcode
    #We start slowly moving the lift upwards
    liftMotor.on(speed=10,block=False, brake=False)

    #Here we check the % of light being reflected
    if(color.reflected_light_intensity > 50):# Generally, white reflects more than 50%
        print("White")
        #This is super scuffed but we used a counter to compare the number of times we see the same color
        #This is only used when we are looking for box types 1 and 3 since they have the same color change
        #We're essentially timing how long we remain on white
        white = white + 1
        #We need to make sure the color is different from the last one, we also need to make sure the list isn't empty
        if(len(colorList) == 0 or colorList[len(colorList)-1] != 1):
            colorList.append(1)
    #Rinse and repeat for black
    elif (color.reflected_light_intensity < 20 and color.reflected_light_intensity > 5):#Generally, black reflects less than 20%
        print("Black")
        if(len(colorList) == 0 or colorList[len(colorList)-1] != 0):
            colorList.append(0)
    #for the reflected light between 20 and 50 percent we don't really care
    else:
        print("No color")
#We print the list for now
print(colorList)
print(white)

#And we make sure to turn the motor off
liftMotor.off()

#We check the list to see if it is a valid barcode
if(colorList == type1and3):
    #Here's where the scuffed timing things comes in
    if(white > 7):#If read in more than 7 we can be pretty confident we're on box one
        print("Box type 1")
    else:#Anything less and we can be pretty sure we're in box 3
        print("Box type 3")
elif(colorList == type2):
    print("Box type 2")
elif(colorList == type4):
    print("Box type 4")
else:
    print("Error invalid or unknown barcode")
    print(colorList)
