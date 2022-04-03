#!/usr/bin/env python3
import time
from ev3dev2.motor import SpeedRPM,LargeMotor, OUTPUT_A, OUTPUT_B

#Initializations
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor

#Move for a set distance in centimeters, negative for backwards, positive for forwards
def moveDistance(distance):
    startTime = time.time()
    moveTime = distance/velocity
    while time.time() - startTime < moveTime:
    #Obstacle detection
        if(dist.distance_centimeters < 10):
            rightMotor.off()
            leftMotor.off()
            print("Obstacle detected")
            break
        # Erroring left
        if(gyro.angle < 0):
            leftSpeed = 42
        else:
            leftSpeed = 40

        # Erroring right
        if(gyro.angle > 0):
            rightSpeed = 42
        else:
            rightSpeed = 40
        rightMotor.on(speed=rightSpeed, block= False)
        leftMotor.on(speed=leftSpeed, block= False)


#Turn for a set number of degrees, negative for left, positive for right
def turnDegrees(degrees):
    if(degrees > 0):#Clockwise right
        while(gyro.angle <= degrees):
            print(gyro.angle)
            rightMotor.on(speed=-10, block= False)
            leftMotor.on(speed=10, block= False)
    else:#Counterclockwise left
        while(gyro.angle <= -degrees):
            print(gyro.angle)
            rightMotor.on(speed=10, block= False)
            leftMotor.on(speed=-10, block= False)
    gyro.reset()

dist = UltrasonicSensor(INPUT_2)
gyro = GyroSensor(INPUT_1)
rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_B)
gyro.calibrate()
gyro.reset()
leftSpeed = 40
rightSpeed = 40
velocity = 11.25 #cm/s

x = float(input("Enter the X coordinate: "))
y = float(input("Enter the Y coordinate: "))

rightMotor.off()
leftMotor.off()
while(True):
    #Obstacle detection
    if(dist.distance_centimeters < 10):
        rightMotor.off()
        leftMotor.off()
        print("Obstacle detected")
        break

    #Movement
    moveDistance(y)
    if(x > 0):
        turnDegrees(90)
    else:
        turnDegrees(-90)
    moveDistance(x)
    break
rightMotor.off()
leftMotor.off()

#1 ft = 30.48 cm
#2 ft = 60.96 cm