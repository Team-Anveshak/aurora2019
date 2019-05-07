#!/bin/bash
. devel/setup.bash
export ROS_MASTER_URI='http://192.168.1.11:11311' 
export ROS_IP='192.168.1.11'
rosparam load config/ports.yaml
