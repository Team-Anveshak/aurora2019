#!/usr/bin/env python
import rospy
from man_ctrl.msg import WheelRpm
from man_ctrl.srv import rotate
#import control signal from multiplexer here
import numpy
import math

class drive():

    def __init__(self):

        rospy.init_node("drive")

        self.pub_motor = rospy.Publisher("motion",WheelRpm,queue_size=10)

        #rospy.Subscriber("diag/wheel_vel",Diag_wheel,self.Callback)

        #insert subscriber to drive control

        self.straight = 0
        self.zero_turn = 0
        self.d = 1

    def spin(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.main()
            rate.sleep()

    def rotateClient(self):
        rospy.wait_for_service('rotator')
        rotateFunc = rospy.ServiceProxy('rotator',rotate)

        goal = rotateFunc(self.theta)

    def main(self):

        rpm = WheelRpm()
		
        rpm.max_rpm = self.d*30

        if(abs(self.straight)>0 or abs(self.zero_turn)>0):
            
            rpm.vel = self.straight*self.d*30
            rpm.omega = self.zero_turn*self.d*10

        else:

            rpm.vel = 0
            rpm.omega = 0


        self.pub_motor.publish(rpm)

    def controlCallback(self):
        pass
        #   whatever control stuff comes in, should be interpreted here
        #   vel and omega values passed onto main() and theta to client



if __name__ == '__main__':
    run = drive()
    run.spin()