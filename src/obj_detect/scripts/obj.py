#!/usr/bin/env python
import rospy
import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
from man_ctrl.msg import WheelRpm
from obj_detect.srv import *
from sensors.msg import Imu
from man_ctrl.srv import *



class OBJ() :
    def __init__(self):
        rospy.init_node("obj")
        '''self.obj_srv=rospy.Service('obj_detect',obj_detect,self.obj_detect_func)
        self.pub_drive=rospy.Publisher("drive_inp",WheelRpm,queue_size=10)
        #rospy.Subscriber("imu",Imu, self.imuCallback)
        try:
            rospy.wait_for_service('rotator')
            # self.cli_drive_state = rospy.ServiceProxy('Drive_state_ctrl', drive_state)
            self.drive_rotate_srv = rospy.ServiceProxy('rotator', rotate)
        except Exception,e:
            print "Service call failed: %s"%e'''
        self.video_width = 480
        self.video_height = 200
        self.bearing_curr = 0.0
        self.bearing_offset = 30.0
        self.time_delay =  10.0
        self.label = ["a","a","a"]

    def start(self):
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            rate.sleep()

    def obj_detect_func(self,msg):
	self.label = ["a","a","a"]
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH,self.video_width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_height)
        t = True
        n=0
        rect_per=0
        stime = time.time()


        while not rospy.is_shutdown() and t:
            if (abs(time.time() - stime)>self.time_delay):
                stime = time.time()
                if((n*self.bearing_offset)>360):
                    rect_per=0
                    t=False
                    n=0
                else:
                    #result = self.drive_rotate_srv(float(self.bearing_curr+self.bearing_offset))
		    print result
                    n = n + 1

            ret, frame = capture.read()
	    if ret:
		for i in range(3):
			results = tfnet_arr[i].return_predict(frame)
		        print(results)
			print i
		        for result in results:
		            tl = (result['topleft']['x'], result['topleft']['y'])
		            br = (result['bottomright']['x'], result['bottomright']['y'])
		            self.label[i] = result['label']
		            print self.label[i]
		            #confidence = result['confidence']
		            rect_per=2*(abs(tl[0]-br[0])+abs(tl[1]-br[1]))
		        if(len(results)!=0):
		            pass
		            #t=False
			    #break
	    if (abs(time.time() - stime)>self.time_delay):
	    	t=False
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
	result  = self.label[0]+','+self.label[1]+','+self.label[2]
        capture.release()
        cv2.destroyAllWindows()
        return obj_detectResponse(result)

    def imuCallback(self,msg):
        self.bearing_curr = msg.yaw

if __name__ == '__main__':

    disc = {
        'model': 'cfg/yolov2-tiny.cfg',
        'load': 'bin/yolov2-tiny.weights',
        'threshold': 0.1,
        'labels':'labels2.txt'
    }
    box = {
        'model': 'cfg/yolov2-tiny-1c-box.cfg',
        'load': 6875,
        'threshold': 0.3,
        'labels':'labels_box.txt'
    }
    bottle = {
        'model': 'cfg/yolov2-tiny.cfg',
        'load': 'bin/yolov2-tiny.weights',
        'threshold': 0.3,
        'labels':'labels1.txt'
    }

    tfnet_disc = TFNet(disc)
    tfnet_box = TFNet(box)
    tfnet_bottle = TFNet(bottle)
    tfnet_arr = [tfnet_disc,tfnet_box,tfnet_bottle]

    obj=OBJ()
    obj.start()
    # obj.obj_detect_func()
