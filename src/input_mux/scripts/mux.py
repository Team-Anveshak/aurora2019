#!/usr/bin/env python
import rospy
# from func import *
from sensor_msgs.msg import Joy
from man_ctrl.msg import WheelRpm
from termcolor import colored
import thread

rospy.init_node("mux")
n_inputs = 0
inputs = rospy.get_param('/Input_mux')
pub={}
velocity= 0.0
angular_vel= 0.0
active_input = '1'

def init():
    thread.start_new_thread(user_input,())
    try:
        for nodes in inputs["destination"] :
            a = str(nodes)
            pub[a] = rospy.Publisher(str(inputs["destination"][nodes]["topic_name"]),WheelRpm,queue_size=10)
    except Exception,e:
        print e
    try:
        for nodes in inputs["inputs"]:
            topic = inputs["inputs"][nodes]["topic_name"]
            rospy.Subscriber(topic,WheelRpm,globals()[nodes])
    except Exception,e:
        print e

def spin():
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        main()
        rate.sleep()

def user_input():
    global active_input 

    print "Usr input takes"
    while not rospy.is_shutdown():
        active_input= raw_input('Enter device number to change drive input: ')
        if(active_input=='1'):
            print "drive input joystick\n"
        elif(active_input=='2'):
            print "drive input gui\n"
        else:
            print "Invalid input\n"

def main():
    global velocity_joy
    vel=WheelRpm()
    vel.vel = velocity
    vel.omega = angular_vel
    # print velocity_joy
    pub["drive"].publish(vel)

def joy_drive(msg):
    global velocity, angular_vel,active_input 
    if active_input == '1':
        velocity=msg.vel
        angular_vel=msg.omega
    # print "hey"

def planner_drive(msg):
    global velocity, angular_vel,active_input 
    if active_input == '2':
        velocity=msg.vel
        angular_vel=msg.omega
        # velocity=1
        # angular_vel= 2

def joy_arm(msg):
    pass



if __name__ == '__main__':
    init()
    spin()
