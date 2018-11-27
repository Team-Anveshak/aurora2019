#!/usr/bin/env python

import sys
import rospy
from navigation.srv import plan_state

def srv_test():
    rospy.wait_for_service('Planner_state_ctrl')
    try:
        add_two_ints = rospy.ServiceProxy('Planner_state_ctrl', plan_state)
        resp1 = add_two_ints(1,0)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    srv_test()
