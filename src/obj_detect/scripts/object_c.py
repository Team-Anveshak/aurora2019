#!/usr/bin/env python
import rospy
from man_ctrl.msg import WheelRpm
from obj_detect.srv import *
from sensors.msg import Imu
from man_ctrl.srv import *
import subprocess
from std_msgs.msg import Empty

class OBJ() :
	def __init__(self):
		rospy.init_node("obj")
		
		self.pub_drive = rospy.Publisher("drive_inp",WheelRpm,queue_size=10)
		self.pub_cam_turn = rospy.Publisher("cam_turn",Empty,queue_size=10)
		self.pub_drive=rospy.Publisher("drive_inp",WheelRpm,queue_size=10)
		
		rospy.Subscriber("imu",Imu, self.imuCallback)
		
		self.obj_srv = rospy.Service('obj_detect',obj_detect,self.obj_detect_func)
		try:
		    rospy.wait_for_service('rotator')
		    self.drive_rotate_srv = rospy.ServiceProxy('rotator', rotate)
		except Exception,e:
		    print "Service call failed: %s"%e
		    
		self.peri=" "
		self.turned = 0.0 
		self.threshold_peri = 350.0
		    
	def start(self):
		rate = rospy.Rate(1)
		while not rospy.is_shutdown():
		    rate.sleep()
	
	def obj_detect_func(self,msg):
	
		while float(self.peri) < self.threshold_peri:
		
			subprocess.call(["./home/anveshak/aurora2019/CNN/darknet","detector","demo","cfg/coco.names","cfg/yolov2-tiny.cfg","WEIGHTS/yolov2-tiny.weights","-thresh","0.15","-c","0"]) 
			
			file_path = "/home/anveshak/aurora2019/src/obj_detect/obj_detect.txt"
			try:
				self.peri = open(file_path,'r')
			except Exception:
				print colored("Object file not found",'red')
				
			if(self.peri == 'none'):
				self.pub_cam_turn.publish()
				self.turned = self.turned + 30.0
				if self.turned == 360.0
					sys.exit(0)
			else:	
				turn = float(self.bearing_curr+self.turned)
				if turn>360.0:
					turn = turn-360.0
				result = self.drive_rotate_srv(turn)
				print result
				
				rpm =WheelRpm()
				rpm.vel=2
				rpm.omega=0
				rpm.max_rpm=30
				self.pub_drive.publish(rpm)
				
				rate = rospyRate(0.5)
				rate.sleep()
				
				rpm =WheelRpm()
				self.pub_drive.publish(rpm)
			
	def imuCallback(self,msg):
		self.bearing_curr = msg.yaw
            
if __name__ == '__main__':
	obj=OBJ()
	obj.start()
