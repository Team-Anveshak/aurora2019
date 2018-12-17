#!/usr/bin/env python
#add service to reload params
import rospy
from navigation.srv import *
from std_msgs.msg import String
from navigation.msg import Goal,Planner_state
from sensors.msg import Imu
from man_ctrl.srv import *
from man_ctrl.msg import WheelRpm
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
        self.pub_drive=rospy.Publisher("drive_inp",WheelRpm,queue_size=10)
        self.pub_planner_state=rospy.Publisher("planner_state",Planner_state,queue_size=2)

        #service server
        self.state_ser=rospy.Service('Planner_state_ctrl',plan_state,self.state_ctrl) #state service

        #service clients
        try:
            # self.cli_drive_state = rospy.ServiceProxy('Drive_state_ctrl', drive_state)
            self.drive_rotate_srv = rospy.ServiceProxy('rotator', rotate)
        except Exception,e:
            print "Service call failed: %s"%e

        self.load_vars() #variables
        self.load_params() #param variables

    def spin(self):
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            self.main() #main func
            rate.sleep()

    def main(self):
        if(self.state=="run"):
            if(self.distance_to_dest_init>self.dist_tolerance):
                if(self.distance_travelled<(self.distance_to_dest_init-self.dist_tolerance)): # replace with distacetodest > tolerance
                    if(abs(self.bearing_dest-self.bearing_curr)<self.bearing_tolerance):
                        mult = (self.distance_to_dest/self.distance_to_dest_init)*self.forward_mult
                        forward_vel = self.forward_vel_cal(self.forward_min,self.forward_max,mult)
                        self.drive_pub(forward_vel,0,self.forward_max)  #setup a primitive pid w.r.t to diatnce to be travelled.
                    else:
                        try:
                			result = self.drive_rotate_srv(float(self.bearing_dest))
                            print result
                            # while resul
                        except rospy.ServiceException,e :
                            print "Service call failed: %s"%e
                        #send service call to drive node to turn to self.bearing destination
                else:
                    rospy.loginfo("destination reached")
            else:
                rospy.loginfo("destination reached")


        elif(self.state=="pause"):
            self.drive_pub(0.0,0.0)
            pass
        elif(self.state=="stop"):
            self.reset()
            pass

    def obs_scanner(self):
        # rate2= rospy.Rate(1)
        # while not rospy.is_shutdown():
        #     print("hey")
        #     #main func
        #     rate2.sleep()
        pass

    def state_ctrl(self,srv_msg):

        if (srv_msg.pause==1 and srv_msg.contin==0 ) :
            self.state = "pause"
        elif (srv_msg.contin==1 and srv_msg.pause==0):
            self.state = "run"
        elif (srv_msg.rst==1):
            self.state = "stop"
        else:
            rospy.loginfo("Error in changing planner state")
        # print(srv_msg.contin)
        return plan_stateResponse(self.state)

    def load_params(self):
        self.dist_tolerance     = float(rospy.get_param('~dist_tolerance', 5.0))        #in metres ; default 5 metre
        self.bearing_tolerance  = float(rospy.get_param('~bearing_tolerance', 10.0))    #in degrees ; default 10 degrees
        self.forward_max        = float(rospy.get_param('~forward_max', 40.0))          #in terms of pwm now
        self.forward_min        = float(rospy.get_param('~forward_min', 20.0))          #in terms of pwm now
        self.turn_vel_max       = float(rospy.get_param('~turn_max', 20.0))             #in terms of pwm value
        self.forward_mult       = float(rospy.get_param('~forward_mult', 1.0))

    def load_vars(self):
        self.state                  = "pause"  # states are 'run','pause','stop'
        self.distance_to_dest_init  = 0.0
        self.distance_to_dest       = 0.0
        self.distance_travelled     = 0.0   #this is the distance that is travelled along the destination so need to convert it from the distance value from the distance calculator reset it when new goal is recieved
        self.bearing_dest           = 0.0
        self.bearing_curr           = 0.0   #current bearing of the rover

    def imuCallback(self,msg):
        self.bearing_curr = msg.yaw

    def goalCallback(self,msg):# each time i am getting a new goal i have to reset the distance calculator node
        self.distance_to_dest = msg.distance
        self.bearing_dest = msg.bearing

    def posCallback(self,msg): #getting the position of the bot from the pos calculator
        pass

    def reset(self): #for resetting all variables to start position, sending the distance calculator to reset etc
        self.load_vars()
        self.load_params()
        #need to reset distance calculator

    def drive_pub(self,vel,omega,max_vel,theta=1000): #used to send the drive node the info, the value of theta taken is 0 to 359 if any other value is given the service won't be called.
        vel =WheelRpm()
        vel.vel=vel
        vel.omega=omega
        self.pub_drive.publish(vel)
    def forward_vel_cal(self,vel_min,vel_max,vel_mult):
        vel = vel_min + (abs(vel_max-vel_min)*vel_mult)
        return min(vel,vel_max)

if __name__ == '__main__':
    run = Planner()
    run.spin()
