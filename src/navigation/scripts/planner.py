#!/usr/bin/env python
#add service to reload params
import rospy
from navigation.srv import *
#from navigation.msg import *
from std_msgs.msg import String
from navigation.msg import Goal,Planner_state
from sensors.msg import Imu,LaserScan
from man_ctrl.srv import *
from man_ctrl.msg import WheelRpm
import math
import thread
from termcolor import colored
import numpy as np

class Planner():

    def __init__ (self):
        rospy.init_node("Planner")

        #threads
        #thread.start_new_thread( self.obs_scanner,())

        #subscribers
        try:
            rospy.Subscriber("imu",Imu, self.imuCallback)
            rospy.Subscriber("goal",Goal,self.goalCallback)
            #rospy.Subscriber("curr_pos",..,self.distCallback)
            #rospy.Subscriber("scan",LaserScan,self.rplCallback)
        except Exception,e:
            print e

        #publishers
        self.pub_drive=rospy.Publisher("drive_inp",WheelRpm,queue_size=10)
        self.pub_planner_state=rospy.Publisher("planner_state",Planner_state,queue_size=2)

        #service server
        self.state_ser=rospy.Service('Planner_state_ctrl',plan_state,self.state_ctrl) #state service

        #service clients
        try:
            rospy.wait_for_service('rotator')
            # self.cli_drive_state = rospy.ServiceProxy('Drive_state_ctrl', drive_state)
            self.drive_rotate_srv = rospy.ServiceProxy('rotator', rotate)
        except Exception,e:
            print "Service call failed: %s"%e

        self.load_vars() #variables
        self.load_params() #param variables

    def spin(self):
        rate = rospy.Rate(1)
        self.bearing_dest = self.bearing_curr
        while not rospy.is_shutdown():
            self.main() #main func
            rate.sleep()

    def main(self):
        
        if(self.state=="run"):
                if(self.distance_to_dest > self.dist_tolerance): # replace with distacetodest > tolerance
                    self.pub_planner_state.publish(0)
                    if(abs(self.bearing_dest-self.bearing_curr)<self.bearing_tolerance):
                    	if(abs(self.bearing_dest-self.bearing_curr)<self.bearing_tolerance):
			                forward_vel = self.forward_vel_cal(self.forward_min,self.forward_max,2)
			                self.drive_pub(forward_vel,0,self.forward_max)  #setup a primitive pid w.r.t to diatnce to be travelled.
	                    else:
	                        try:
								print colored('\n Sending request for %f'%self.bearing_dest,'white')
								result = self.drive_rotate_srv(float(self.bearing_dest))
								print result
	                        except rospy.ServiceException,e :
	                            print "Service call failed: %s"%e
	                        #send service call to drive node to turn to self.bearing destination
                else:
                    self.pub_planner_state.publish(1)
		    		self.drive_pub(0.0,0.0,self.forward_max)
                    rospy.loginfo("destination reached")

        elif(self.state=="pause"):
            self.drive_pub(0.0,0.0,self.forward_max)
            pass
        elif(self.state=="stop"):
            #self.reset()
            self.distance_to_dest_init = self.distance_to_dest
            pass

    def obs_scanner(self):
        rate2= rospy.Rate(1)
        while not rospy.is_shutdown():
            indx = np.where(self.lidar > self.lidar_threshold) #where there are no obstacles
            if not np.all([np.isin(indx,[87:91])]): #if there is obstacle in -2deg to 2deg
                print colored('\n ----------- \nObstacle detected..... planner paused', 'white')

                self.state = 'pause'

                arr = np.zeros((5,180))             #array with -2deg to 2deg values at each -90deg to 90deg
                arr[0,:] = self.lidar[0:179]
                arr[1,:] = self.lidar[1:180]
                arr[2,:] = self.lidar[2:181]
                arr[-1,:] = self.lidar[-1:178]
                arr[-2,:] = self.lidar[-2:177]

                indx = np.all([arr > self.lidar_threshold],axis = 0)
                indx = np.where(indx == True)-90
                abs_angle = np.min(abs(indx))
                if abs_angle is in indx :
                    angle = abs_angle
                elif -abs_angle is in indx :
                    angle = -abs_angle

                print colored('No obstacle at %fdeg'%(angle),'white')

                try:
                    print colored('\n Sending request for %f to rotserver'%(self.bearing_curr+angle),'white')
                    result = self.drive_rotate_srv(float(self.bearing_curr+angle))
                    print result
                except rospy.ServiceException,e :
                    print "Service call failed: %s"%e

                #Move forward
                self.state = 'run'
                rate2.sleep()
        # rate2= rospy.Rate(1)
        # while not rospy.is_shutdown():
        #     print("hey")
        #     #main func
        #     rate2.sleep()
        #pass

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
        self.dist_tolerance     = float(rospy.get_param('~dist_tolerance', 1.5))        #in metres ; default 5 metre
        self.bearing_tolerance  = float(rospy.get_param('~bearing_tolerance', 5.0))    #in degrees ; default 10 degrees
        self.forward_max        = float(rospy.get_param('~forward_max', 40.0))          #in terms of pwm now
        self.forward_min        = float(rospy.get_param('~forward_min', 20.0))          #in terms of pwm now
        self.turn_vel_max       = float(rospy.get_param('~turn_max', 20.0))             #in terms of pwm value
        self.forward_mult       = float(rospy.get_param('~forward_mult', 1.0))
        self.lidar_threshold    = float(rospy.get_param('~lidar_thresh', 5.0))

    def load_vars(self):
        self.state                  = "stop"  # states are 'run','pause','stop'
        self.distance_to_dest_init  = 0.0
        self.distance_to_dest       = 400.0
        self.distance_travelled     = 0.0   #this is the distance that is travelled along the destination so need to convert it from the distance value from the distance calculator reset it when new goal is recieved
        self.bearing_dest           = 0.0
        self.bearing_curr           = 0.0   #current bearing of the rover
        self.lidar = np.zeros(360) 
	
	
    def imuCallback(self,msg):
        self.bearing_curr = msg.yaw

    def goalCallback(self,msg):# each time i am getting a new goal i have to reset the distance calculator node
        self.distance_to_dest = msg.distance
        self.bearing_dest = msg.bearing

    def distCallback(self,msg): #getting the position of the bot from the pos calculator
        pass

    def rplCallback(self,msg): #getting the position of the bot from the pos calculator
        self.lidar = np.array(scan)

    def reset(self): #for resetting all variables to start position, sending the distance calculator to reset etc
        self.load_vars()
        self.load_params()
		self.drive_pub(0.0,0.0,self.forward_max)
        #need to reset distance calculator

    def drive_pub(self,vel,omega,max_vel,theta=1000): #used to send the drive node the info, the value of theta taken is 0 to 359 if any other value is given the service won't be called.
        rpm =WheelRpm()
        rpm.vel=vel
        rpm.omega=omega
        self.pub_drive.publish(rpm)
    def forward_vel_cal(self,vel_min,vel_max,vel_mult):
        vel = vel_min + (abs(vel_max-vel_min)*vel_mult)
        return min(vel,vel_max)

if __name__ == '__main__':
    run = Planner()
    run.spin()
