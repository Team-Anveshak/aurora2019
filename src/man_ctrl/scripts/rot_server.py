#!/usr/bin/env python

import rospy
from man_ctrl.srv import rotate
from man_ctrl.msg import WheelRpm
from sensors.msg import Imu
import numpy
import time

class rotateService():
	
	def __init__(self):
		rospy.init_node('rot_server')
		service = rospy.Service('rotator',rotate,self.rotator)

		self.pub_serv = rospy.Publisher("motion",WheelRpm,queue_size = 10)
		rospy.Subscriber("imu", Imu, self.imuCallback)



		self.bearing_tolerance = 1#rospy.get_param('~bearing_tolerance',0.1)
		self.kp = 0.05
		self.curr_bear = 0.0

	def rotator(self, request):

		Rpm = WheelRpm()
		self.final_bear = request.angle
		self.initial_bear = self.curr_bear
		self.remainAngle = self.final_bear - self.curr_bear
		self.omega = self.omegaManager(self.remainAngle)
		

		self.last_time = time.time()
		self.last_bear = self.curr_bear
		
		Rpm.max_rpm = 100
		Rpm.theta = 0

		while (abs(self.remainAngle) > self.bearing_tolerance):
						
			Rpm.vel = 0
			if self.remainAngle<0:
				Rpm.omega = int(-self.omega)
			else:
				Rpm.omega = int(self.omega)

			self.pub_serv.publish(Rpm)

			#self.pControl()
			self.setOmega = self.omegaManager(self.remainAngle)
			self.actualOmega = (self.curr_bear - self.last_bear)/(time.time()-self.last_time)
			self.omega = self.omega + self.kp*(self.actualOmega - self.setOmega)

			self.last_time = time.time()
			self.last_bear = self.curr_bear


	# def pControl(self):
	# 	self.setOmega = omegaManager(self.remainAngle)
	# 	self.actualOmega = (self.curr_bear - self.last_bear)/(time.time()-self.last_time)
	# 	self.omega = self.omega + self.kp*(self.actualOmega - self.setOmega)

	def omegaManager(self,angle):
		precOmega = 10 + angle/12				#units in rpm giving a min of 10rpm
		reqOmega = precOmega - (precOmega%5)
		return reqOmega


	def spin(self):
		rate = rospy.Rate(5)
		while not rospy.is_shutdown():
			rate.sleep()
			#rospy.spin()



	def imuCallback(self,msg):
		self.curr_bear=-msg.yaw 


if __name__ == '__main__':
	run = rotateService()
	run.spin()
