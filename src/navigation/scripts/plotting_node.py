#!/usr/bin/env python
#Plotting requires -- matplotlib , termcolor , cartopy , cython , scipy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from termcolor import colored

import rospy
from sensor_msgs.msg import NavSatFix

max_way_lat = 0.0
max_way_lon = 0.0
min_way_lat = 0.0 
min_way_lon = 0.0

ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()
ax.coastlines()

def plot(msg):
	plt.plot(float(msg.latitude),float(msg.longitude),color='blue',
		 	linewidth=1, marker='.', transform=ccrs.Geodetic(),) 	
	global ax
	global max_way_lat
	global max_way_lon
	global min_way_lat
	global min_way_lon
	
	max_lat = max([max_way_lat,float(msg.latitude)])
	min_lat = min([min_way_lat,float(msg.latitude)])
	max_lon = max([max_way_lat,float(msg.longitude)])
	min_lon = min([min_way_lat,float(msg.longitude)])
	
	ax.set_extent((min_lat-0.0001,max_lat+0.0001,min_lon-0.0001,max_lon+0.0001))
	plt.show()
	plt.pause(0.05)
		
if __name__ == '__main__':
	x = raw_input("Do you want to start start plotting in cartopy? (y/n) : ")
	if(x == 'y'):
		dest_lat_cont,dest_lon_cont = [],[]
		print 'Enter GPS way-points one by one in latitude<>longitude format'
		print colored('$  Type ok once done', 'green')
		l = raw_input('GPSpromt>>>')
		while (l != 'ok'):
			row = l.split()
			dest_lat_cont.append(row[0])
			dest_lon_cont.append(row[1])
			l = raw_input('GPSpromt>>>')
			
		global max_way_lat
		global max_way_lon
		global min_way_lat
		global min_way_lon
		max_way_lat = float(max(dest_lat_cont));
		max_way_lon = float(max(dest_lon_cont));
		min_way_lat = float(min(dest_lat_cont));
		min_way_lon = float(min(dest_lon_cont));
		
		global ax
		ax.set_extent((min_way_lat-0.0001,max_way_lat+0.0001,min_way_lon-0.0001,max_way_lon+0.0001))
		for i in range(len(dest_lat_cont)):
			plt.plot(float(dest_lat_cont[i]),float(dest_lon_cont[i]),color='red',
			 	linewidth=1, marker='.', transform=ccrs.Geodetic(),)
		plt.show()
		
		try:
			rospy.init_node("cartopy_plotter")
		except Exception:
			print colored("$ Error initializing node @ cartopy_plotter",'red')
		try:
			rospy.Subscriber("fix",NavSatFix, plot)
		except Exception:
			print colored("$ Error opening subscriber @ fix",'red')
			
