#!/usr/bin/env python3
from ev3dev2.motor import SpeedRPM,LargeMotor, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import UltrasonicSensor

#Initializations
rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_B)
distSensor = UltrasonicSensor(INPUT_2)
speed = SpeedRPM(40)
distanceThreshold = 10
X = float(input("Enter the X coordinate: "))
Y = float(input("Enter the Y coordinate: "))


def distToRPM(distance):#Convert X distance to Y RPM via an arbitrary ratio
    return distance/7

def degToRPM(degrees):#Convert X degrees to Y RPM via an arbitrary ratio
    return degrees/7

def moveForDist(distance):#Move the robot straight forward for X centimeters
    rightMotor.on_for_rotations(speed=speed, rotations=distToRPM(distance), brake= False, block= False)
    leftMotor.on_for_rotations(speed=speed, rotations=distToRPM(distance), brake= False, block= True)

def turnForDeg(degrees):#Turn the robot on a dime (centered about the wheels) for X degrees
    rightMotor.on_for_rotations(speed=speed, rotations=degToRPM(degrees), brake= False, block= False)
    leftMotor.on_for_rotations(speed=-speed, rotations=degToRPM(degrees), brake= False, block= True)


while(True):
    if(distSensor.distance_centimeters < distanceThreshold):
        moveForDist(-10)
        turnForDeg(90)
    else:
        rightMotor.on_for_rotations(speed=speed, rotations=distToRPM(1), brake= False, block= False)
        leftMotor.on_for_rotations(speed=speed, rotations=distToRPM(1), brake= False, block= True)
    
