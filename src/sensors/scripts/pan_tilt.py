#!/usr/bin/env python

from sensors.msg import PanTilt
from sensor_msgs.msg import Joy
import rospy
import time
class Servo():

	def __init__(self):
		rospy.init_node("servoCtrl")
		rospy.Subscriber('/joy',Joy,self.joyCallback)
		self.servo_pub = rospy.Publisher('pan_tilt_ctrl',PanTilt, queue_size=10)
		self.panCtrl = 0
		self.tiltCtrl = 0
		self.panAngle = 90
		self.tiltAngle = 150
		self.relay = False
		self.lastTime = time.time()

	def joyCallback(self,msg):

		self.panCtrl = msg.axes[4]
		self.tiltCtrl = msg.axes[5]
		if msg.buttons[9]==1:
			self.relay = True
		elif msg.buttons[8] == 1:
			self.relay = False

	def main(self):
		servo_msg = PanTilt()
		servo_msg.rel = self.relay
		if time.time() - self.lastTime>0.1:
			if(self.panAngle>0 and self.panAngle<253):
				self.panAngle = self.panAngle + 2*self.panCtrl
			else:
				if self.panAngle<=0:
					self.panAngle = 1
				if self.panAngle>=253:
					self.panAngle = 252

			if(self.tiltAngle>0 and self.tiltAngle<253):
				self.tiltAngle = self.tiltAngle - 2*self.tiltCtrl
			else:
				if self.tiltAngle<=0:
					self.tiltAngle = 1
				if self.tiltAngle>=253:
					self.tiltAngle = 252

			servo_msg.pan = 3276.8 + self.panAngle*18.2044444
			servo_msg.tilt = 3276.8 + self.tiltAngle*18.2044444
			self.servo_pub.publish(servo_msg)
			self.lastTime = time.time()

	def spin(self):
		rate = rospy.Rate(1)
		while not rospy.is_shutdown():
				self.main()
		rate.sleep()

if __name__ == '__main__':
	servo = Servo()
	servo.spin()
