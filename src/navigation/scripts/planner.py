#!/usr/bin/env python

#add service to reload params

import rospy
from navigation.srv import *
from std_msgs.msg import String
from navigation.msg import Goal,Planner_state
from sensors.msg import Imu
import math
import thread


class Planner():

    def __init__ (self):
        rospy.init_node("Planner")

        #threads
        thread.start_new_thread( self.obs_scanner,())

        #subscribers
        try:
            rospy.Subscriber("imu",Imu, self.imuCallback)
            rospy.Subscriber("goal",Goal,self.goalCallback)
            rospy.Subscriber("pos",Pos,self.posCallback)
        except Exception,e:
            print e
        #publishers
        # self.pub_drive=rospy.Publisher("drive_msg",Drive,queue_size=10)
        self.pub_planner_state=rospy.Publisher("planner_state",Planner_state,queue_size=2)


        #service server
        self.state_ser=rospy.Service('Planner_state_ctrl',plan_state,self.state_ctrl) #state service
        #service clients
        # try:
        #     self.cli_drive_state = rospy.ServiceProxy('Drive_state_ctrl', drive_state)
        # except rospy.ServiceException, e:
        #     print "Service call failed: %s"%e


        #variables
        self.state="pause"  # states are 'run','pause','stop'
        self.distance_to_dest=0;
        self.distance_travelled=0;#this is the distance that is travelled along the destination so need to convert it from the distance value from the distance calculator
        # reset it when new goal is recieved
        self.bearing_dest=

        #param variables
        self.load_params()


    def spin(self):
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            #main func
            self.main()
            rate.sleep()

    def main(self):

        if(self.state=="run"):
            if(self.distance_to_dest>self.dist_tolerance):
                if(self.distance_travelled<(self.distance_to_dest-self.dist_tolerance)):



                pass
            else:
                #already reached

        elif(self.state=="pause"):
            self.drive_pub(0,0)
            pass
        elif(self.state=="stop"):
            self.reset()
            pass

        # print(self.dist_tolerance)
        # pass

    def state_ctrl(self,srv_msg):

        if (srv_msg.pause==1 and srv_msg.contin==0 ) :
            self.state = "pause"
        elif (srv_msg.contin==1 and srv_msg.pause==0):
            self.state = "run"
        elif (srv_msg.rst==1):
            pass
        else:
            rospy.loginfo("Error in changing planner state")
        print(srv_msg.contin)
        return plan_stateResponse(self.state)



    def obs_scanner(self):
        # rate2= rospy.Rate(1)
        # while not rospy.is_shutdown():
        #     print("hey")
        #     #main func
        #     rate2.sleep()
        pass

    def load_params(self):
        self.dist_tolerance    = float(rospy.get_param('~dist_tolerance', 5))
        self.bearing_tolerance = float(rospy.get_param('~bearing_tolerance', 10))
        self.forward           = float(rospy.get_param('~forward', 40))
        self.turn_min          = float(rospy.get_param('~turn_min', 20))
    def imuCallback(self,msg):
        pass
    def goalCallback(self,msg):# each time i am getting a new goal i have to reset the distance calculator node
        self.distance_to_dest = msg.distance
        pass
    def posCallback(self,msg): #getting the position of the bot from the pos calculator
        pass
    def reset(self,msg): #for resetting all variables to start position, sending the distance calculator to reset etc
        pass
    def drive_pub(self,vel,omega,theta=1000): #used to send the drive node the info, the value of theta taken is 0 to 359 if any other value is given the service won't be called.

        pass

if __name__ == '__main__':
    run = Planner()
    run.spin()
