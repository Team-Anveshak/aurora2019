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
        rospy.Subscriber("drive_inp",WheelRpm,self.driveCallback)

        #rospy.Subscriber("diag/wheel_vel",Diag_wheel,self.Callback)

        #insert subscriber to drive control

        self.vel = 0
        self.omega = 0
        self.d = 1
        self.max_rpm=30.0

    def spin(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.main()
            rate.sleep()

    '''def rotateClient(self):
        rospy.wait_for_service('rotator')
        rotateFunc = rospy.ServiceProxy('rotator',rotate)

        goal = rotateFunc(self.theta)'''

    def main(self):

        rpm = WheelRpm()
	rpm.max_rpm= self.max_rpm


        if(abs(self.vel)>0 or abs(self.omega)>0):

            rpm.vel = self.vel
            rpm.omega = self.omega

        else:

            rpm.vel = 0
            rpm.omega = 0


        self.pub_motor.publish(rpm)

    def driveCallback(self,msg):
        self.vel=msg.vel
        self.max_rpm=msg.max_rpm
        self.omega=msg.omega



if __name__ == '__main__':
    run = drive()
    run.spin()
