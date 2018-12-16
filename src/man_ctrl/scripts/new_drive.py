#!/usr/bin/env python
import rospy
from man_ctrl.msg import Wheel_rpm
#from rover_msgs.msg import Diag_wheel
from sensor_msgs.msg import Joy
import numpy
import math

class drive():

    def __init__(self):

        rospy.init_node("drive")

        self.pub_motor = rospy.Publisher("loco/wheel_rpm",Wheel_rpm,queue_size=10)

        #rospy.Subscriber("diag/wheel_vel",Diag_wheel,self.Callback)
        rospy.Subscriber("/joy",Joy,self.joyCallback)
        #self.mode = 1
        self.straight = 0
        self.zero_turn = 0
        self.d = 1
        # self.mode = 1

    def spin(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.main()
            rate.sleep()

    def main(self):

		rpm = Wheel_rpm()
		
		if(abs(self.straight)>0.1):
		    
			rpm.rpm = abs(self.straight*self.d*30)
			rpm.mod = 0
			if (self.straight>=0):
				rpm.dir = 0
			else :
				rpm.dir = 1


		elif(abs(self.zero_turn)>0.1):

			rpm.rpm = abs(self.zero_turn*self.d*30)
			rpm.mod = 1
			if (self.zero_turn>=0):
				rpm.dir = 0
			else :
				rpm.dir = 1
		else:

			rpm.rpm = 0
			rpm.dir = 0
			rpm.mod = 0


		self.pub_motor.publish(rpm)
    def joyCallback(self,msg):
        
		self.straight  = msg.axes[1]
		self.zero_turn = msg.axes[3]

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