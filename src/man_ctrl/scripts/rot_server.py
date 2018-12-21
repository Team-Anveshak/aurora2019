#!/usr/bin/env python
import rospy
<<<<<<< HEAD
from man_ctrl.srv import rotate
from man_ctrl.msg import WheelRpm
=======
from man_ctrl.srv import *
from man_ctrl.msg import Wheel_rpm
>>>>>>> fce4ce80006a84f99a09d7936249edc9c43d3977
from sensors.msg import Imu
import numpy
import time

<<<<<<< HEAD
class rotateService():
	
	def __init__(self):
		rospy.init_node('rot_server')
=======
curr_bear=0.0
bearing_tolerance = rospy.get_param('~bearing_tolerance',0.1)
rpm = rospy.get_param('~rpm',10)
def rotator(final_bear):
>>>>>>> fce4ce80006a84f99a09d7936249edc9c43d3977

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

<<<<<<< HEAD
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
=======
def imuCallback(msg):
	curr_bear=-msg.yaw


>>>>>>> fce4ce80006a84f99a09d7936249edc9c43d3977

			
			self.last_time = time.time()
			self.last_bear = self.curr_bear


<<<<<<< HEAD
	# def pControl(self):
	# 	self.setOmega = omegaManager(self.remainAngle)
	# 	self.actualOmega = (self.curr_bear - self.last_bear)/(time.time()-self.last_time)
	# 	self.omega = self.omega + self.kp*(self.actualOmega - self.setOmega)
=======
pub_serv = rospy.Publisher("loco/wheel_rpm",Wheel_rpm,queue_size = 10)
rospy.Subscriber("imu", Imu, imuCallback)
>>>>>>> fce4ce80006a84f99a09d7936249edc9c43d3977

		
	def omegaManager(self,angle):
		precOmega = 10 + angle/12				#units in rpm giving a min of 10rpm
		reqOmega = precOmega - (precOmega%5)
		return reqOmega

<<<<<<< HEAD

	def spin(self):
		rate = rospy.Rate(5)
		while not rospy.is_shutdown():
			rate.sleep()


	def imuCallback(self,msg):
		self.curr_bear=-msg.yaw 


if __name__ == '__main__':
	run = rotateService()
	run.spin()
=======
rospy.spin()
>>>>>>> fce4ce80006a84f99a09d7936249edc9c43d3977
