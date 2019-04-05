import rospy
import matplotlib.pyplot as plt
from math import *
import thread
#from arm.msg import Joint_ang #b_l0,l0_l1,base
#base to l1 --> a
#l1 to l2 --> b

class Arm_plot:
	def __init__ (self):
		#rospy.init_node("Arm_viz")
		#rospy.Subscriber("joint_angle", Joint_ang, self.vizCallback) 
		
		self.a = 0.0
		self.b = 0.0
		self.c = 0.0

		ax1 = plt.subplot(1,2,1) 
		self.pt1, = plt.plot([0,cos(self.a)],[0,sin(self.a)],color='red', linewidth=2,label='Link0')
		self.pt2, = plt.plot([cos(self.a),cos(self.a)-cos(self.a+self.b)],[sin(self.a),sin(self.a)-sin(self.a+self.b)],color='blue', linewidth=2,label='Link1')
		ax1.set_xlim(-2,2); ax1.set_ylim(-2,2); ax1.legend()

		ax2 = plt.subplot(1,2,2) 
		self.pt3, = plt.plot([0,sin(self.c)],[0,cos(self.c)],color='green', linewidth=2,label='Base')
		ax2.set_xlim(-2,2); ax2.set_ylim(-2,2); ax2.legend()

	def plotCallback(self):
			self.pt1.remove()
			self.pt2.remove()
			self.pt3.remove()

			ax1 = plt.subplot(1,2,1) 
			self.pt1, = plt.plot([0,cos(self.a)],[0,sin(self.a)],color='red', linewidth=2,label='Link0')
			self.pt2, = plt.plot([cos(self.a),cos(self.a)-cos(self.a+self.b)],[sin(self.a),sin(self.a)-sin(self.a+self.b)],color='blue', linewidth=2,label='Link1')
			ax1.set_xlim(-2,2); ax1.set_ylim(-2,2); ax1.legend()

			ax2 = plt.subplot(1,2,2) 
			self.pt3, = plt.plot([0,sin(self.c)],[0,cos(self.c)],color='green', linewidth=2,label='Base')
			ax2.set_xlim(-2,2); ax2.set_ylim(-2,2); ax2.legend()
		
			plt.pause(0.005)

	def vizCallback(self,msg):
		self.a = radians(msg.b_l0)
		self.b = radians(msg.l0_l1)	
		self.c = radians(msg.base)
		self.plotCallback()
	
if __name__ == '__main__':
	x = Arm_plot()
	y = raw_input("Do you want to start viz? (y/n)")
	
	if(y == 'y'):
		plt.show()
	else:
		sys.exit()

	
	
	
