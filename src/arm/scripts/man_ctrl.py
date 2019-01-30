#!/usr/bin/env python
import rospy
from arm.msg import Pwm
from sensor_msgs.msg import Joy
import sys

class Arm:
	def __init__ (self):
		rospy.init_node("Arm_publisher")
		self.pub = rospy.Publisher("set",Pwm,queue_size=5)
		self.rate = rospy
		rospy.Subscriber("joy_arm", Joy, self.joyCallback) 
		self.set = Pwm()

	def main(self):
		r = rospy.Rate(4)
		while not rospy.is_shutdown():
			self.pub.publish(self.set)
			print self.set 
			print '\n ------- \n'
			r.sleep() 
		
	def joyCallback(self,msg):
		if(abs(msg.axes[2]) > 0.15):
			if msg.axes[2] < 0 or msg.axes[2] is 0:
				self.set.base = -int(90.0*msg.axes[2])
			else:
				self.set.base = -int(90.0* msg.axes[2])
		else:
			self.set.base =0
			
		if(abs(msg.axes[0]) > 0.2):
			self.set.roll = int(250.0*msg.axes[0])
		else:
			self.set.roll  =0
		
	
		if(abs(msg.axes[3]) > 0.2):
			if msg.axes[3] > 0:
				self.set.shoulder = -int(150.0*msg.axes[3])
			else:
				self.set.shoulder = -int(100.0*msg.axes[3])
		else:
			self.set.shoulder =0
		
		
		if(abs(msg.axes[1]) > 0.2):
			self.set.elbow = int(150.0*msg.axes[1])
		else:
			self.set.elbow =0
		
		self.set.pitch = -250*( msg.buttons[5]-msg.buttons[7]) 
		
		self.set.grip = 250*( msg.buttons[6]-msg.buttons[4]) 
			
if __name__ == '__main__':
	x = Arm()
	y = raw_input("Do you want to start? (y/n) ")
	
	if(y == 'y'):
		#rospy.Timer(rospy.Duration(0.1),x.main) 
		x.main()
		rospy.spin()
	else:
		print 'Exiting....'
		sys.exit()
