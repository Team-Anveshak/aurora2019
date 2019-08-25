#!/usr/bin/env python
import rospy
from science.msg import Science
from sensor_msgs.msg import Joy
import math
import time

class Test():

    def __init__(self):

        rospy.init_node("JoyScience")
        self.pub_motor = rospy.Publisher("Science_data",Science,queue_size=10)
        rospy.Subscriber("/joy_arm",Joy,self.joyCallback)
        self.direction1 = 0
        self.direction2 = 0
        self.direction3 = 0
        self.S1 = 0
        self.S2 = 0
        self.S3 = 0
        self.Servo1 = 0
        self.Servo2 = 0
        self.N_wire = 0
        self.P1 = 0
        self.P2 = 0
        self.manual = 1
        self.x = 0
        self.y = 0
        self.z = 0
        self.zero = 0
        self.one = 0
        self.two = 0
        self.three = 0
    def spin(self):
        #rate = rospy.Rate(10)
        
        while not rospy.is_shutdown():
            

            if(self.zero==1):
                self.direction1=0
                self.direction3=0
                self.direction2=0
                self.S1=0
                self.S2=0
                self.manual=1
                self.zero=0
            if(self.manual==1):
            	if(self.direction1!=0):
                	self.main(1,0,0,self.direction1,self.direction2,self.direction3)
                	self.main(0,0,0,self.direction1,self.direction2,self.direction3)
            	elif(self.direction2!=0):
                	self.main(0,1,0,self.direction1,self.direction2,self.direction3)
                	self.main(0,0,0,self.direction1,self.direction2,self.direction3)
            	elif(self.direction3!=0):
                	self.main(0,0,1,self.direction1,self.direction2,self.direction3)
                	self.main(0,0,0,self.direction1,self.direction2,self.direction3)
            	else:
                	self.main(0,0,0,0,0,0)

            

            if(self.one==1):
	        	self.manual = 0
	        	self.Servo2 = (1.0 - 90/180.0)*3276.8; self.S1 = 1;
        		t=time.time()
	            	while(time.time()-t<10):
	            		self.P1 = 1
	            		self.main(0,0,0,0,0,0)
	        	self.P1 = 0
                	num = 0
	            	while(num<5):
	            		turns = 0
	                    	while(turns<5000):
        						print (turns)
        						print (self.direction1)
        						self.direction2 = 0; self.direction1 = 1
        						self.direction3 = 0
        						self.P1 = 0
        						self.main(1,0,0,self.direction1,self.direction2,self.direction3)
        						self.main(0,0,0,self.direction1,self.direction2,self.direction3)
        						turns = turns + 1
                		num = num + 1
                		t=time.time()
	                    	while(time.time()-t<3):
	                    		self.P1 = 1
	                    		self.main(0,0,0,0,0,0)
	            		self.P1 = 0
	        	self.S1 = 0
        		self.S2 = 1
        		t=time.time()
	            	while(time.time()-t<10):
	            		self.P1 = 1
	            		self.main(0,0,0,0,0,0)
	        	self.P1 = 0
	        	self.Servo2 = (1.0 + 240/180.0)*3276.8;
	        	turns = 0       	
	            	while(turns<6000):
	            		self.direction1 = 0
	            		self.direction2 = -1
	            		self.direction3 = 0
	            		#print self.direction3
	            		self.main(0,1,0,self.direction1,self.direction2,self.direction3)
	                	self.main(0,0,0,self.direction1,self.direction2,self.direction3)
	            		turns = turns + 1
	        	self.one = 0
	    if(self.two==1):
	        	self.manual = 0
	        	self.Servo2 = (1.0 - 90/180.0)*3276.8; self.S1 = 1
        		t=time.time()
	            	while(time.time()-t<10):
	            		self.P1 = 1
	            		self.main(0,0,0,0,0,0)
	        	self.P1 = 0
	        	num = 0
	            	while(num<5):
	            		turns = 0
	                    	while(turns<5000):
        						print (turns)
        						print (self.direction1)
        						self.direction2 = 0; self.direction1 = -1
        						self.direction3 = 0
        						self.P2 = 0
        						self.main(1,0,0,self.direction1,self.direction2,self.direction3)
        						self.main(0,0,0,self.direction1,self.direction2,self.direction3)
        						turns = turns + 1
                		num = num + 1
                		t=time.time()
	                    	while(time.time()-t<3):
	                    		self.P1 = 1
	                    		self.main(0,0,0,0,0,0)
	            		self.P1 = 0
	        	self.S1 = 0
        		self.S2 = 1
        		t=time.time()
	            	while(time.time()-t<10):
	            		self.P1 = 1
	            		self.main(0,0,0,0,0,0)
	        	self.P1 = 0
	        	self.Servo2 = (1.0 + 240/180.0)*3276.8;
	        	turns = 0       	
	            	while(turns<6000):
	            		self.direction1 = 0
	            		self.direction2 = -1
	            		self.direction3 = 0
	            		#print self.direction3
	            		self.main(0,1,0,self.direction1,self.direction2,self.direction3)
	                	self.main(0,0,0,self.direction1,self.direction2,self.direction3)
	            		turns = turns + 1
	        	self.two = 0

        rospy.spin()

    def main(self,period1,period2,period3,dirn1,dirn2,dirn3):
        step = Science()  
        #rate = rospy.Rate(200)
        step.steps1 = dirn1
        step.steps2 = dirn2
        step.steps3 = dirn3
        step.period1 = period1
        step.period2 = period2
        step.period3 = period3
        step.s1 = self.S1
        step.s2 = self.S2
        step.n_wire = self.N_wire
        step.ser1 = self.Servo1
        step.ser2 = self.Servo2
        step.pump1 = self.P1
        step.pump2 = self.P2
        self.pub_motor.publish(step)
        #rate.sleep()
        time.sleep(0.0004)
        #print "hgk"

    def joyCallback(self,msg):
    
    	
        self.direction1  = msg.axes[5]
        self.direction2  = msg.axes[4]
        
        if(msg.buttons[0]==1):
            self.zero = 1
        
        if(msg.buttons[1]==1):
            self.one = 1
        
        if(msg.buttons[3]==1):
        	self.three = 1
        
        if(msg.buttons[2]==1):
        	self.two = 1
        	
        if(msg.buttons[4]==1 and self.y==0):
            self.y=1
            self.Servo1 = (1.0 + 25/180.0)*3276.8
        elif(msg.buttons[4]==1 and self.y==1):
            self.y=0
            self.Servo1 = (1.0 + 180/180.0)*3276.8
            
        if(msg.buttons[3]==1 and self.z==0):
            self.z=1
            self.P2 = -1
        elif(msg.buttons[3]==1 and self.z==1):
            self.z=0
            self.P2 = 0
        if(msg.buttons[5]==1 and self.x==0):
            self.x=1
            self.P1 = 1
        elif(msg.buttons[5]==1 and self.x==1):
            self.x=0
            self.P1 = 0
        

if __name__ == '__main__':
    run = Test()
    run.spin()
    #pwm = (1.0 + pos/180.0)*3276.8;

