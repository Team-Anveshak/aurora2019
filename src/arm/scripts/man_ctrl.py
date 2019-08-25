#!/usr/bin/env python
import rospy
from arm.msg import *
from sensor_msgs.msg import Joy
import sys

class Arm:
	def __init__ (self):
		rospy.init_node("Arm_publisher")
		self.pub = rospy.Publisher("set",Pwm,queue_size=5)
		self.allen_pub = rospy.Publisher("turn",Allen,queue_size=5)
		rospy.Subscriber("joy_arm", Joy, self.joyCallback) 
		self.set = Pwm()
		self.turn_msg = Allen()

	def main(self):
		r = rospy.Rate(4)
		while not rospy.is_shutdown():
			self.pub.publish(self.set)
			self.allen_pub.publish(self.turn_msg)
			print self.set 
			print '\n ------- \n'
			r.sleep() 
#base = shoulder; shoulder = base
#pitch-grip	
	def joyCallback(self,msg):

		if(abs(msg.axes[2]) > 0.15):
			if msg.axes[2] < 0 :
				self.set.shoulder = -int(160.0*msg.axes[2])
			else:
				self.set.shoulder = -int(160.0* msg.axes[2])
		else:
			self.set.shoulder =0
			
		if(abs(msg.axes[0]) > 0.2):
			self.set.roll = -int(250.0*msg.axes[0])
		else:
			self.set.roll  =0
		
	
		if(abs(msg.axes[3]) > 0.2):
			if msg.axes[3] > 0:
				self.set.base = int(150.0*msg.axes[3])
			else:
				self.set.base = int(250.0*msg.axes[3])
		else:
			self.set.base =0
		
		
		if(abs(msg.axes[1]) > 0.2):
			self.set.grip = -int(150.0*msg.axes[1])
		else:
			self.set.grip =0
		
		self.set.pitch = -250*( msg.buttons[5]-msg.buttons[7]) 
		
		self.set.elbow = 250*( msg.buttons[6]-msg.buttons[4])

		if msg.buttons[9]==1:
			self.turn_msg.ina = True; self.turn_msg.inb = False
		elif msg.buttons[8] == 1:
			self.turn_msg.inb = True; self.turn_msg.ina = False
		else:
			self.turn_msg.inb = False; self.turn_msg.ina = False 
			
if __name__ == '__main__':
	x = Arm()
	
	
	#rospy.Timer(rospy.Duration(0.1),x.main) 
	x.main()
	rospy.spin()

