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
        self.obj_srv=rospy.Service('obj_detect',obj_detect,self.obj_detect_func)
        self.pub_drive=rospy.Publisher("drive_inp",WheelRpm,queue_size=10)
        rospy.Subscriber("imu",Imu, self.imuCallback)
        try:
            rospy.wait_for_service('rotator')
            # self.cli_drive_state = rospy.ServiceProxy('Drive_state_ctrl', drive_state)
            self.drive_rotate_srv = rospy.ServiceProxy('rotator', rotate)
        except Exception,e:
            print "Service call failed: %s"%e
        self.video_width = 480
        self.video_height = 200
        self.bearing_curr = 0.0
        self.bearing_offset = 30.0
        self.time_delay =  60.0
        
    def start(self):
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            rate.sleep()

    def obj_detect_func(self,msg):
        
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
                    result = self.drive_rotate_srv(float(self.bearing_curr+self.bearing_offset))
                    n = n + 1

            ret, frame = capture.read()
            if ret:
                results = tfnet.return_predict(frame)
                print(results)
                for result in results:
                    tl = (result['topleft']['x'], result['topleft']['y'])
                    br = (result['bottomright']['x'], result['bottomright']['y'])
                    label = result['label']
                    print label
                    # confidence = result['confidence']
                    rect_per=2*(abs(tl[0]-br[0])+abs(tl[1]-br[1]))
                if(len(results)!=0):
                    t=False

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()
        return obj_detectResponse(rect_per)
        
    def imuCallback(self,msg):
        self.bearing_curr = msg.yaw

if __name__ == '__main__':

    options = {
        'model': 'cfg/yolov2-tiny.cfg',
        'load': 'bin/yolov2-tiny.weights',
        'threshold': 0.15
    }

    tfnet = TFNet(options)

    obj=OBJ()
    obj.start()
    # obj.obj_detect_func()
