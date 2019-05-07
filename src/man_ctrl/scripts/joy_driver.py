#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from man_ctrl.msg import WheelRpm

forward_vel=0.0
omega=0.0
m=1
    
def main():
    rospy.init_node("Joy_driver")
    print "Joy_driver node started"
    #############################################
    global forward_vel, omega ,m
    vel = WheelRpm()
    #############################################
    try:
        pub = rospy.Publisher('joy_drive',WheelRpm,queue_size=10)
    except Exception as e:
         print "couldn't publish -error : {}".format(e)

    try:
        rospy.Subscriber('joy',Joy,joyCallback)
    except Exception as e:
        print "couldn't subscribe - error : {}".format(e)

    #############################################
    rate = rospy.Rate(5)
    #############################################
    while not rospy.is_shutdown():
    
        if(abs(forward_vel)>0.1 or abs(omega)>0.1):
            vel.vel = forward_vel*30*m
            vel.omega = omega*10*m
            vel.max_rpm = m*30
        else:
            vel.vel = 0
            vel.omega = 0
    #############################################
        pub.publish(vel)
    #############################################
        rate.sleep()
###################################################################################

def joyCallback(msg):
    global forward_vel, omega, m

    forward_vel = msg.axes[1]
    omega = msg.axes[2]


    if(msg.buttons[5]==1):
        if m <5:
            m = m + 1
            print("Max rpm is {}".format(m*30))
    
    elif(msg.buttons[4]==1):
        if m >1:
            m = m - 1
            print("Max rpm is {}".format(m*30))

######################################################################################
if __name__=='__main__':
    main()