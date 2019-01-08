#!/usr/bin/env python
import rospy
from science.msg import Science
import sys

class SCIsubscriber():
    def __init__(self):
        self.data = 0
    
    def callback_science(self,data):
        txtfile = open("Temperature.txt","w")
        txtfile.write(str(data.Temp))
        txtfile.close()
      
        txtfile = open("pressure.txt","w")
        txtfile.write(str(data.pressure))
        txtfile.close()

        txtfile = open("uvintensity.txt","w")
        txtfile.write(str(data.UVintensity))
        txtfile.close()

        txtfile = open("luminosity.txt","w")
        txtfile.write(str(data.luminosity))
        txtfile.close()
   
    def subscribe(self):
        rospy.Subscriber("Science_data", Science,self.callback_science)
        rospy.spin()
if(__name__ == "__main__"):
    ABC = SCIsubscriber()
    ABC.subscribe()
