#!/usr/bin/env python

from sensors.msg import PanTilt
from sensor_msgs.msg import Joy
import rospy

def joyCallback(msg):
	servo_msg = PanTilt()
	while msg.axes[4]!=0 or msg.axes[5]!=0:
		servo_msg.pan = msg.axes[4]
		servo_msg.tilt = msg.axes[5]

		servo_pub.publish(servo_msg)


rospy.init_node("servoCtrl")
rospy.Subscriber('/joy',Joy,joyCallback)
servo_pub = rospy.Publisher('pan_tilt_ctrl',PanTilt, queue_size=10)
panCtrl = 0
tiltCtrl = 0
rospy.spin()