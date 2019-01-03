#!/usr/bin/env python
import rospy
from science.msg import Science
from sensor_msgs.msg import Joy
import numpy
import math
import time

class Test():

    def __init__(self):

        rospy.init_node("JoyScience")
        self.pub_motor = rospy.Publisher("Science_data",Science,queue_size=10)

        #rospy.Subscriber("diag/wheel_vel",Diag_wheel,self.Callback)
        rospy.Subscriber("/joy",Joy,self.joyCallback)
        self.direction = 0
        self.S1 = 0
        self.S2 = 0
        self.NW = 0
        self.Servo = 0
        self.x = 0
        self.y = 0
        self.z = 0
    def spin(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            if(self.direction!=0):
                self.main(1,self.direction)
                self.main(0,self.direction)
            else:
                self.main(0,0)
        rospy.spin()

    def main(self,period,dirn):
        step = Science()  
		
        step.steps = dirn
        step.spd = 0.005
        #z=step.spd
        step.period = period
        step.sol1 = self.S1
        step.sol2 = self.S2
        step.nwire = self.NW
        step.servo = self.Servo
        self.pub_motor.publish(step)
        time.sleep(0.005)
        #print "hgk"

    def joyCallback(self,msg):
        self.direction  = msg.axes[5]
        if(msg.buttons[0]==1 and self.x==0):
            self.x=1
            self.S1 = 1
        elif(msg.buttons[0]==1 and self.x==1):
            self.x=0
            self.S1=0
        if(msg.buttons[2]==1 and self.z==0):
            self.z=1
            self.S2 = 1
        elif(msg.buttons[2]==1 and self.z==1):
            self.z=0
            self.S2=0
        if(msg.buttons[3]==1 and self.y==0):
            self.y=1
            self.NW = 1
        elif(msg.buttons[3]==1 and self.y==1):
            self.y=0
            self.NW=0
        if(msg.buttons[1]==1):
            self.Servo=msg.buttons[1]
            time.sleep(5)
            self.Servo=0

        
if __name__ == '__main__':
    run = Test()
    run.spin()
