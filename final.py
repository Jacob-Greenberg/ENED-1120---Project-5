#!/usr/bin/env python3

"""
This file contains all subroutines that are used to perform the final demo.
Each function is labeled with the name of the task it performs.
"""

import time
#Initializations
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, ColorSensor
from ev3dev2.sensor import INPUT_1,INPUT_2,INPUT_3,INPUT_4
from ev3dev2.motor import LargeMotor, MediumMotor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_D

#Initializations
#Motors
rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_B)
liftMotor = MediumMotor(OUTPUT_D)
#Sensors
gyro = GyroSensor(INPUT_1)
dist = UltrasonicSensor(INPUT_2)
color = ColorSensor(INPUT_4)
#Calibrating the gyroscope
gyro.calibrate()
gyro.reset()

#Arbitrary global variables
global motorSpeed
global leftSpeed
global rightSpeed
global velocity

motorSpeed = 40
leftSpeed = 40
rightSpeed = 40
velocity = 6.25 #in/s

#Offsets for the homes
#homeA = [6,-6]#in
#homeB = [102,-6]#in

"""
calibrateVelocity

Quick and dirty calibration of the robot's velocity
uses the ultrasonic sensor to take the difference in distance from a fixed wall

Input: Seconds to run motors for
Output: Difference in distance / input seconds (velocity)
"""
def calibrateVelocity(seconds):
    #Take a reading of the distance away from fixed object
    initialDistance = dist.distance_inches

    #Move for X seconds
    rightMotor.on_for_seconds(speed=motorSpeed, seconds=seconds, brake = True, block = False)
    leftMotor.on_for_seconds(speed=motorSpeed, seconds=seconds, brake = True, block = True)

    #See how close we are now
    finalDistance = dist.distance_inches

    #Return the difference in distances
    difference = initialDistance - finalDistance

    #Return the difference the Velocity
    return difference/seconds

"""
moveDistance

Moves a set distance in inches
Uses the global velocity value, so make sure it's set properly

Input: Inches to move
Output: Moves the robot forward for the specified distance
"""
def moveDistance(distance):
    startTime = time.time()
    moveTime = abs(distance)/velocity
    while time.time() - startTime < moveTime and distance is not 0:
    #Obstacle detection
        if(dist.distance_centimeters < 10):
            rightMotor.off()
            leftMotor.off()
            print("Obstacle detected")
            break

        # Erroring left
        #if(gyro.angle < 0):
            #leftSpeed = 42
        #else:
            #leftSpeed = 40

        # Erroring right
        #if(gyro.angle > 0):
            #rightSpeed = 42
        #else:
            #rightSpeed = 40

        rightMotor.on(speed=rightSpeed, block= False)
        leftMotor.on(speed=leftSpeed, block= False)
    rightMotor.off()
    leftMotor.off()

"""
turnDegrees

Turns the robot a set number of degrees
Resets the gyroscope to zero after turning
**Note: This isn't super precise and tends to overshoot the desired angle i.e. 90 degree turn should be 88 degrees

Input: Degrees to turn
Output: Robot turns the specified number of degrees
"""
def turnDegrees(degrees):
    gyro.reset()
    if(degrees > 0):#Clockwise right
        while(gyro.angle <= degrees):
            #print(gyro.angle)
            rightMotor.on(speed=-40, block= False)
            leftMotor.on(speed=40, block= False)
    else:#Counterclockwise left
        while(abs(gyro.angle) <= abs(degrees)):
            #print(gyro.angle)
            rightMotor.on(speed=40, block= False)
            leftMotor.on(speed=-40, block= False)
    gyro.reset()

"""
coordinateMove

Moves a set distance in inches vertically then turns and moves laterally

Input: Lateral magnitude, Vertical magnitude
Output: Moves the robot forward for the specified distance in each direction
"""
def coordinateMove(x,y, ignoreObstacle = False):
    obstacle = False
    
    rightMotor.off()
    leftMotor.off()
    while(dist.distance_centimeters > 10):
        #Move vertically
        if(y != 0):
            moveDistance(y)

        #Turn and move laterally
        if(x > 0 and dist.distance_centimeters > 10):
            turnDegrees(88)
            moveDistance(x)
        elif (x < 0 and dist.distance_centimeters > 10):
            turnDegrees(-88)
            moveDistance(x)
        break

    if(dist.distance_centimeters < 10):
        obstacle = True
    #Turn off motors
    rightMotor.off()
    leftMotor.off()

    if(not ignoreObstacle):
        return obstacle


"""
barcode

Scans the barcode and returns the type of box read
**Note: Assumes the robot facing th box

Input: n/a
Output: The box type in integer form (1,2,3,4) and -1 if an invalid code was read
"""
def barcode():
    rightMotor.off()
    leftMotor.off()
    liftMotor.off()

    #Helper variables
    colorList = []
    white = 0

    #Move types (read from bottom to top)
    type1and3 = [1,0]
    type2 = [1,0,1,0]
    type4 = [1,0,1]

    #Move forward toward the box
    startTime = time.time()
    while(dist.distance_centimeters > 5):
        rightMotor.on(speed=10, block= False)
        leftMotor.on(speed=10, block= False)
    endTime = time.time()
    difference = endTime - startTime
    rightMotor.off()
    leftMotor.off()

    #Read the barcode
    start = time.time()
    while(len(colorList) < 4 and (time.time() - start < 10)):
        liftMotor.on(speed=10,block=False, brake=False)
        if(color.reflected_light_intensity > 50):
            white = white + 1
            if(len(colorList) == 0 or colorList[len(colorList)-1] != 1):
                colorList.append(1)
        elif (color.reflected_light_intensity < 20 and color.reflected_light_intensity > 5):
            if(len(colorList) == 0 or colorList[len(colorList)-1] != 0):
                colorList.append(0)

    rightMotor.off()
    leftMotor.off()
    liftMotor.off()

    #return to track
    rightMotor.on_for_seconds(speed=-10, seconds=difference, brake = True, block = False)
    leftMotor.on_for_seconds(speed=-10, seconds=difference, brake = True, block = True)



    start = time.time()
    while(time.time()-start < 5):
        liftMotor.on(speed=-10,block=False, brake=False)

    print(colorList)
    rightMotor.off()
    leftMotor.off()
    if(colorList == type1and3):
        if(white > 7):#If read in more than 7 we can be pretty confident we're on box one
            return 1
        else:#Anything less and we can be pretty sure we're in box 3
            return 3
    elif(colorList == type2):#Box #2
        return 2
    elif(colorList == type4):#Box #4
        return 4
    else:#Error
        return -1

"""
pickup

Moves forward until the box is in front of the robot and picks it up
**Note: Assumes the robot is facing th box
"""
def pickup():
    #Make sure all motors are off
    rightMotor.off()
    leftMotor.off()
    startTime = time.time()
    #Move forward until we're close enough to the box
    while(dist.distance_centimeters > 4 and time.time() - startTime < 5):
        rightMotor.on(speed=10, block= False)
        leftMotor.on(speed=10, block= False)
    endTime = time.time()
    difference = endTime - startTime
    rightMotor.off()
    leftMotor.off()

    start=time.time()
    #Move the lift up until either the touch sensor is triggered or we've run for 5 seconds and timeout
    while(time.time() - start < 5):
        liftMotor.on(speed=15, block= False)


    #return to track
    rightMotor.on_for_seconds(speed=-10, seconds=difference, brake = True, block = False)
    leftMotor.on_for_seconds(speed=-10, seconds=difference, brake = True, block = True)
    rightMotor.off()
    leftMotor.off()

    #cd "ENED 1120 - Final Demo"



def moveBack(distance):
    startTime = time.time()
    moveTime = abs(distance)/velocity
    while time.time() - startTime < moveTime and distance is not 0:
    #Obstacle detection
        if(dist.distance_centimeters < 10):
            rightMotor.off()
            leftMotor.off()
            print("Obstacle detected")
            break

        # Erroring left
        #if(gyro.angle < 0):
            #leftSpeed = 42
        #else:
            #leftSpeed = 40

        # Erroring right
        #if(gyro.angle > 0):
            #rightSpeed = 42
        #else:
            #rightSpeed = 40

        rightMotor.on(speed=-10, block= False)
        leftMotor.on(speed=-10, block= False)
    rightMotor.off()
    leftMotor.off()