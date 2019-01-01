import matplotlib.pyplot as plt
from math import *
from arm.msg import Joint_ang #b_l0,l0_l1
#base to l1 --> a
#l1 to l2 --> b

class Arm_plot:
	def __init__ (self):
		rospy.init_node("Arm_viz")
		rospy.Subscriber("joint_angle", Joint_ang, self.vizCallback) 
		
		self.a = 0.0
		self.b = 0.0
		
	def start(self):
		while True:
			pt1, = plt.plot([0,cos(radians(a))],[0,sin(radians(a))],color='red', linewidth=2,label='Link0')
			pt2, = plt.plot([cos(a),cos(a)-cos(a+b)],[sin(a),sin(a)-sin(a+b)],color='blue', linewidth=2,label='Link1')
			plt.pause(0.005)
			pt1.remove()
			pt2.remove()
			
	def vizCallback(self,msg):
		self.a = radians(msg.b_l0)
		self.b = radians(msg.l0_l1)	
	
if __name__ == '__main__':
	x = Arm_plot()
	y = raw_input("Do you want to start viz? (y/n)")
	
	ax = plt.axes()
	ax.set_xlim(-2,2)
	ax.set_ylim(-2,2)
	plt.legend(loc='upper left', frameon=False)
	plt.plot([-0.5,0.5],[0,0],color='black')
	plt.show()
	
	if(y == 'y'):
		x.start()
	else:
		sys.exit()
