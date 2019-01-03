#!/usr/bin/env python
import rospy
from man_ctrl.msg import WheelRpm
from obj_detect.srv import *
from sensors.msg import Imu
from man_ctrl.srv import *
import subprocess
from std_msgs.msg import Int16
from termcolor import colored

class OBJ() :
	def __init__(self):
		rospy.init_node("obj")
		
		self.pub_drive = rospy.Publisher("drive_inp",WheelRpm,queue_size=10)
		self.pub_cam_turn = rospy.Publisher("cam_turn",Int16,queue_size=10)
		self.pub_drive=rospy.Publisher("drive_inp",WheelRpm,queue_size=10)
		
		rospy.Subscriber("imu",Imu, self.imuCallback)
		
		self.obj_srv = rospy.Service('obj_detect',obj_detect,self.obj_detect_func)
		try:
		    rospy.wait_for_service('rotator')
		    self.drive_rotate_srv = rospy.ServiceProxy('rotator', rotate)
		except Exception,e:
		    print "Service call failed: %s"%e
		    
		self.peri="0.00"
		self.turned = 0.0 
		self.threshold_peri = 350.0
		self.bearing_curr = 0.0
		    
	def start(self):
		rate = rospy.Rate(1)
		while not rospy.is_shutdown():
		    rate.sleep()
	
	def obj_detect_func(self,msg):
		self.peri = "0.0"
		while float(self.peri) < self.threshold_peri:
		
			subprocess.call(["./darknet","detector","demo","cfg/coco.data","cfg/yolov2-tiny.cfg","WEIGHTS/yolov2-tiny.weights","-thresh","0.15","-c","0"]) 
			
			file_path = "/home/anveshak/aurora2019/src/obj_detect/obj_detect.txt"
			try:
				self.peri = open(file_path,'r')
				for l in self.peri:
					r = l.split()
					self.peri = r[0]
					
			except Exception:
				print colored("Object file not found",'red')
				
			if(self.peri == '0.000000'):
				self.pub_cam_turn.publish(30)
				self.turned = self.turned + 30.0
				if self.turned == 360.0:
					sys.exit(0)
			else:	
				turn = float(self.bearing_curr+self.turned)
				if turn>360.0:
					turn = turn-360.0
				result = self.drive_rotate_srv(turn)
				print result
				self.pub_cam_turn.publish(0)
				
				rpm =WheelRpm()
				rpm.vel=2
				rpm.omega=0
				rpm.max_rpm=30
				self.pub_drive.publish(rpm)
				
				rate = rospy.Rate(0.5)
				rate.sleep()
				
				rpm =WheelRpm()
				self.pub_drive.publish(rpm)
				
				
		return obj_detectResponse(10.00)

	def imuCallback(self,msg):
		self.bearing_curr = msg.yaw
            
if __name__ == '__main__':
	obj=OBJ()
	obj.start()
