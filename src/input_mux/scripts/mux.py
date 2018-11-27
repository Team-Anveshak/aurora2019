#!/usr/bin/env python
import rospy
from func import *
from sensor_msgs.msg import Joy

rospy.init_node("mux")
n_inputs = 0
inputs = rospy.get_param('/Input_mux')
pub={}

def spin():
    for nodes in inputs["destination"] :
        a = str(nodes)
        pub[a] = rospy.Publisher(str(inputs["destination"][nodes]["topic_name"]),Joy,queue_size=10)
    for nodes in inputs["inputs"]:
        topic = inputs["inputs"][nodes]["topic_name"]
        rospy.Subscriber(topic,Joy,globals()[nodes])
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        main()
        rate.sleep()

def main():
    vel = Joy()
    # self.pub["drive"].publish(vel)
    pass

if __name__ == '__main__':
    spin()
