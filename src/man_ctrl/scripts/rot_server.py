#!/usr/bin/env python
import rospy
from man_ctrl.srv import *
from man_ctrl.msg import Wheel_rpm
from sensors.msg import Imu
import numpy

curr_bear=0.0
bearing_tolerance = rospy.get_param('~bearing_tolerance',0.1)
rpm = rospy.get_param('~rpm',10)
def rotator(final_bear):

	Rpm = Wheel_rpm()
	initial_bear = curr_bear
	final_bear = initial_bear + angle

	while (abs(curr_bear - final_bear) > bearing_tolerance):
		Rpm.forward = 0

		if curr_bear>final_bear:
			Rpm.rotate = -rpm
		else:
			Rpm.rotate = rpm

		pub_serv.publish(Rpm)

	return ("final bearing achieved")


def imuCallback(msg):
	curr_bear=-msg.yaw



rospy.init_node('rot_server')

service = rospy.Service('rotator',rotate,rotator)

pub_serv = rospy.Publisher("loco/wheel_rpm",Wheel_rpm,queue_size = 10)
rospy.Subscriber("imu", Imu, imuCallback)


rospy.spin()
