#!/usr/bin/env python3

#Initializations
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B

#Initializations
dist = UltrasonicSensor(INPUT_2)
rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_B)

#This speed is arbitrary, but it seems to work well
motorSpeed = 40

#calibrateVelocity
#
#Quick and dirty calibration of the robot's velocity
#uses the ultrasonic sensor to take the difference in distance from a fixed wall
#
#Input: Seconds to run motors for
#Output: Difference in distance / input seconds (velocity)

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


print(calibrateVelocity(2)