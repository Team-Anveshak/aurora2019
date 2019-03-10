#!/usr/bin/env python
import rospy
from science.msg import Science
from sensor_msgs.msg import Joy
import math
import time

class Test():

    def __init__(self):

        rospy.init_node("JoyScience")
        self.pub_motor = rospy.Publisher("Science_data",Science,queue_size=10)

        #rospy.Subscriber("diag/wheel_vel",Diag_wheel,self.Callback)
        rospy.Subscriber("/joy",Joy,self.joyCallback)
        self.direction1 = 0
        self.direction2 = 0
        self.S1 = 0
        self.S2 = 0
        self.NW = 0
        self.Servo = 0
        self.x = 0
        self.y = 0
        self.z = 0
    def spin(self):
        #rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            if(self.direction1!=0):
                self.main(1,0,self.direction1,self.direction2)
                self.main(0,0,self.direction1,self.direction2)
            elif(self.direction2!=0):
                self.main(0,1,self.direction1,self.direction2)
                self.main(0,0,self.direction1,self.direction2)
            elif(self.direction1!=0 and self.direction2!=0):
                self.main(1,1,self.direction1,self.direction2)
                self.main(0,0,self.direction1,self.direction2)
            else:
                self.main(0,0,0,0)
        rospy.spin()

    def main(self,period1,period2,dirn1,dirn2):
        step = Science()  
        #rate = rospy.Rate(200)

        step.steps1 = dirn1
        step.steps2 = dirn2
        step.period1 = period1
        step.period2 = period2

        step.sol1 = self.S1
        step.sol2 = self.S2
        self.pub_motor.publish(step)
        #rate.sleep()
        time.sleep(0.0005)
        #print "hgk"

    def joyCallback(self,msg):
        self.direction1  = msg.axes[5]
        self.direction2  = msg.axes[4]
        if(msg.buttons[0]==1 and self.x==0):
            self.x=1
            self.S1 = (1.0 + 30/180.0)*3276.8
        elif(msg.buttons[0]==1 and self.x==1):
            self.x=0
            self.S1= (1.0 + 200/180.0)*3276.8
        if(msg.buttons[2]==1 and self.z==0):
            self.z=1
            self.S2 = (1.0 + 120/180.0)*3276.8
        elif(msg.buttons[2]==1 and self.z==1):
            self.z=0
            self.S2= (1.0 + 170/180.0)*3276.8
        
if __name__ == '__main__':
    run = Test()
    run.spin()

    #pwm = (1.0 + pos/180.0)*3276.8;