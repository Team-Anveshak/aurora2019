#!/usr/bin/env python
#Plotting requires -- matplotlib , termcolor , cartopy , cython , scipy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from termcolor import colored
import rospy,signal,sys,thread
from math import *
from sensor_msgs.msg import NavSatFix

class Plot():
	def __init__(self):
		self.n = 0
		
		ax = plt.axes(projection=ccrs.PlateCarree())
		ax.stock_img()
		ax.coastlines()
		self.pt = plt.text(0,0, 'hello', fontsize=8,transform=ccrs.Geodetic())
		
		
		
		self.dest_lat_cont,self.dest_lon_cont = [],[]
		
		#12.991454, 80.233577 -- GC
		self.dest_lat_cont.append(13.34525)
		self.dest_lon_cont.append(74.79737)
		#12.991812, 80.230981 -- CFI

		self.dest_lat_cont.append(13.34527)
		self.dest_lon_cont.append(74.79734)
		
		print 'Enter GPS way-points one by one in latitude<>longitude format'
		print colored('$  Type ok once done', 'green')
		l = raw_input('GPSprompt >>>')
		while (l != 'ok'):
			row = l.split()
			self.dest_lat_cont.append(row[0])
			self.dest_lon_cont.append(row[1])
			l = raw_input('GPSprompt >>>')
			
		max_way_lat = float(max(self.dest_lat_cont));
		max_way_lon = float(max(self.dest_lon_cont));
		min_way_lat = float(min(self.dest_lat_cont));
		min_way_lon = float(min(self.dest_lon_cont));
		ax.set_extent((min_way_lon-0.01,max_way_lon+0.01,min_way_lat-0.01,max_way_lat+0.01))
	
		for i in range(len(self.dest_lat_cont)):
			plt.plot(float(self.dest_lon_cont[i]),float(self.dest_lat_cont[i]),color='green', marker='$%d$'%(i+1), 				markersize=10, transform=ccrs.Geodetic(),)
		
		try:
			rospy.init_node("cartopy_plotter")
		except Exception:
			print colored("$ Error initializing node @ cartopy_plotter",'red')
		try:
			rospy.Subscriber("fix",NavSatFix, self.plot)
		except Exception:
			print colored("$ Error opening subscriber @ fix",'red')
	
	def plot(self,msg):
		plt.plot(float(msg.longitude),float(msg.latitude),color='blue',
			 	markersize=3, marker='.', transform=ccrs.Geodetic(),) 	
		
		lon1, lat1, lon2, lat2 = map(radians, [msg.longitude, msg.latitude,self.dest_lon_cont[self.n], 			self.dest_lat_cont[self.n]])
		dlon = lon2 - lon1
		dlat = lat2 - lat1
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2 * atan2(sqrt(a), sqrt(1-a))
		dist_gps = 6371 * c*1000
		bearing = atan2(sin(lon2-lon1)*cos(lat2), (cos(lat1)*sin(lat2))-(sin(lat1)*cos(lat2)*cos(lon2-lon1)))
		bearing = degrees(bearing)
		
		textstr = 'dist_gps(m)=%.5f\nbearing(deg)=%.5f\n'%(dist_gps, bearing)
		self.pt.remove()
		self.pt = plt.text(self.dest_lon_cont[self.n], self.dest_lat_cont[self.n], textstr, fontsize=10,transform=ccrs.Geodetic())
		
		plt.pause(0.05)
		
		
	def key_intrp(self):
		print "\n type ok when reached next point \n"
		flag = True
		while flag:
			text = raw_input('$GPS_plot >>>')
			if (text == 'ok'):
				if ( self.n < len(self.dest_lat_cont)-1 ):
					self.n = self.n+1
				else:
					print "All waypoints done"
					flag = False
	  		else:
  				print 'Invalid command'


		
def signal_handler(signal, frame):  #For catching keyboard interrupt Ctrl+C
	print "\nProgram exiting....."
	sys.exit(0)
		
if __name__ == '__main__':
	x = raw_input("Do you want to start start plotting in cartopy? (y/n) : ")
	
	if(x == 'y'):
		xy = Plot()
		
		signal.signal(signal.SIGINT, signal_handler)
		#thread.start_new_thread(xy.key_intrp,()) 
		plt.show()
	else:
		print "Exiting...."
				
