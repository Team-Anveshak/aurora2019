#!/usr/bin/env python
import rospy
#from man_ctrl.msg import Wheel_rpm
from sensor_msgs.msg import Joy
import numpy
import math
import smbus
import time

bus = smbus.SMBus(1)
addf = 0x0f
addm = 0x10
addb = 0x11

class drive():

    def __init__(self):

        rospy.init_node("drive")
        rospy.Subscriber("/joy",Joy,self.joyCallback)

        self.straight = 0
        self.zero_turn = 0
        self.d = 1
        self.rpm = 0
        self.direction = 0
        self.mode

	def spin(self):
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
		    self.main()
        	rate.sleep()
    def loco(self,address):
		
		bus.write_byte(address,self.rpm)
		bus.write_byte(address,self.direction)
		bus.write_byte(address,self.mode)

    def main(self):

		if(abs(self.straight)>0.25):

			self.rpm = abs(self.straight*self.d*30)
			self.mode = 0
			if (self.straight >= 0):
				self.direction = 0
			else:
				self.direction = 1

			self.loco(addf)
			self.loco(addm)
			self.loco(addb)
			

		elif(abs(self.zero_turn)>0.25):

			self.rpm = abs(self.zero_turn*self.d*30)
			self.mode = 1
			if (self.zero_turn >= 0):
				self.direction = 1
			else:
				self.direction = 0

			self.loco(addf)
			self.loco(addm)
			self.loco(addb)
		else:

			self.rpm = 0
			self.mode = 0
			self.direction = 0

			self.loco(addf)
			self.loco(addm)
			self.loco(addb)

    def joyCallback(self,msg):
        
		self.straight  = msg.axes[1]
		self.zero_turn = msg.axes[2]

		if(msg.buttons[5]==1):
			if self.d <6:
				self.d = self.d + 1
			print("Max rpm is {}".format(self.d*30))
		
		elif(msg.buttons[4]==1):
			if self.d >1:
				self.d = self.d - 1
			print("Max rpm is {}".format(self.d*30))


if __name__ == '__main__':
    run = drive()
    run.spin()