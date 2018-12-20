#!/usr/bin/env python
#Plotting requires -- matplotlib , termcolor , cartopy , cython , scipy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from termcolor import colored
import signal
import rospy
from sensor_msgs.msg import NavSatFix

class Plot():
	def __init__(self):
	
		self.max_way_lat = 0.0
		self.max_way_lon = 0.0
		self.min_way_lat = 0.0 
		self.min_way_lon = 0.0

		self.ax = plt.axes(projection=ccrs.PlateCarree())
		self.ax.stock_img()
		self.ax.coastlines()
	
		try:
			rospy.init_node("cartopy_plotter")
		except Exception:
			print colored("$ Error initializing node @ cartopy_plotter",'red')
			
		try:
			rospy.Subscriber("fix",NavSatFix, self.plot)
		except Exception:
			print colored("$ Error opening subscriber @ fix",'red')
		
		self.dest_lat_cont,self.dest_lon_cont = [],[]
		
		print 'Enter GPS way-points one by one in latitude<>longitude format'
		print colored('$  Type ok once done', 'green')
		l = raw_input('GPSpromt>>>')
		while (l != 'ok'):
			row = l.split()
			dest_lat_cont.append(row[0])
			dest_lon_cont.append(row[1])
			l = raw_input('GPSpromt>>>')
			
		self.max_way_lat = float(max(self.dest_lat_cont));
		self.max_way_lon = float(max(self.dest_lon_cont));
		self.min_way_lat = float(min(self.dest_lat_cont));
		self.min_way_lon = float(min(self.dest_lon_cont));
		self.ax.set_extent((self.min_way_lat-0.01,self.max_way_lat+0.01,self.min_way_lon-0.01,self.max_way_lon+0.01))
	
		for i in range(len(self.dest_lat_cont)):
			plt.plot(float(self.dest_lon_cont[i]),float(self.dest_lat_cont[i]),color='red',
				 	linewidth=0.005, marker='.', transform=ccrs.Geodetic(),)
		plt.show()
		
	
	def plot(self,msg):
		plt.plot(float(msg.longitude),float(msg.latitude),color='blue',
			 	linewidth=0.05, marker='.', transform=ccrs.Geodetic(),) 	
	
		'''max_lat = max([self.max_way_lat,float(msg.latitude)])
		min_lat = min([self.min_way_lat,float(msg.latitude)])
		max_lon = max([self.max_way_lat,float(msg.longitude)])
		min_lon = min([self.min_way_lat,float(msg.longitude)])
		self.ax.set_extent((min_lat-0.0001,max_lat+0.0001,min_lon-0.0001,max_lon+0.0001))'''
		
		plt.pause(0.05)
		
	def signal_handler(self,signal, frame):  #For catching keyboard interrupt Ctrl+C
		print "\nProgram exiting.....\n"
		sys.exit(0)
		
if __name__ == '__main__':
	x = raw_input("Do you want to start start plotting in cartopy? (y/n) : ")

	if(x == 'y'):
		xy = Plot()
		signal.signal(signal.SIGINT, xy.signal_handler)
	else:
		print "Exiting.... \n"
				
