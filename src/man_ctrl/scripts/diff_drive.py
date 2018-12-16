#!/usr/bin/env python
import rospy
from man_ctrl.msg import Wheel_rpm_diff
from sensor_msgs.msg import Joy
import numpy
import math

class drive():

    def __init__(self):

        rospy.init_node("drive")

        self.pub_motor = rospy.Publisher("loco/wheel_rpm",Wheel_rpm_diff,queue_size=10)

        #rospy.Subscriber("diag/wheel_vel",Diag_wheel,self.Callback)
        rospy.Subscriber("/joy",Joy,self.joyCallback)
        self.straight = 0
        self.zero_turn = 0
        self.d = 1

    def spin(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.main()
            rate.sleep()

    def main(self):

        rpm = Wheel_rpm_diff()
		
        rpm.max_rpm = self.d*30
        
        if(abs(self.straight)>0.1 or abs(self.zero_turn)>0.1):
            
            rpm.forward = self.straight*self.d*30
            rpm.rotate = self.zero_turn*self.d*30

        else:

            rpm.forward = 0
            rpm.rotate = 0


        self.pub_motor.publish(rpm)
    def joyCallback(self,msg):
        
        self.straight  = -msg.axes[1]
        self.zero_turn = msg.axes[2]

        if(msg.buttons[5]==1):
            if self.d <5:
                self.d = self.d + 1
                print("Max rpm is {}".format(self.d*30))
        
        elif(msg.buttons[4]==1):
            if self.d >1:
                self.d = self.d - 1
                print("Max rpm is {}".format(self.d*30))

if __name__ == '__main__':
    run = drive()
    run.spin()