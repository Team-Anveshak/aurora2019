#!/usr/bin/env python
import rospy
# from func import *
from sensor_msgs.msg import Joy
from man_ctrl.msg import Wheel_rpm_diff
from termcolor import colored
import thread

rospy.init_node("mux")
n_inputs = 0
inputs = rospy.get_param('/Input_mux')
pub={}
velocity_joy= 1.0
angular_vel_joy= 0.0

def init():
    thread.start_new_thread(user_input,())
    try:
        for nodes in inputs["destination"] :
            a = str(nodes)
            pub[a] = rospy.Publisher(str(inputs["destination"][nodes]["topic_name"]),Wheel_rpm_diff,queue_size=10)
    except Exception,e:
        print e
    try:
        for nodes in inputs["inputs"]:
            topic = inputs["inputs"][nodes]["topic_name"]
            rospy.Subscriber(topic,Joy,globals()[nodes])
    except Exception,e:
        print e

def spin():
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        main()
        rate.sleep()

def user_input():

    print "Usr input takes"
    while not rospy.is_shutdown():
        input = raw_input('Enter device number to change drive input: ')
        if(input=='1'):
            print "drive input joystick\n"
        elif(input=='2'):
            print "drive input gui\n"
        else:
            print "Invalid input\n"

def main():
    global velocity_joy
    vel= Wheel_rpm_diff()
    vel.forward = velocity_joy
    print velocity_joy
    pub["drive"].publish(vel)

def joy_drive(msg):
    global velocity_joy, angular_vel_joy
    velocity_joy=msg.axes[0]
    angular_vel_joy=msg.axes[1]
    # print "hey"

def gui_drive(msg):
    global velocity_joy, angular_vel_joy
    velocity_gui=1
    angular_vel_gui= 2

def joy_arm(msg):
    pass



if __name__ == '__main__':
    init()
    spin()
