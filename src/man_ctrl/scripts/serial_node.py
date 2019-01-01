#!/usr/bin/env python

import rospy
from rosserial_python import SerialClient, RosSerialServer
from serial import SerialException
from time import sleep
import multiprocessing

import sys

if __name__=="__main__":

    rospy.init_node("drive_arduino")
    rospy.loginfo("ROS Serial Python Node")

    port_name = rospy.get_param('~port','/dev/drive')
    baud = int(rospy.get_param('~baud','57600'))

    # for systems where pyserial yields errors in the fcntl.ioctl(self.fd, TIOCMBIS, \
    # TIOCM_DTR_str) line, which causes an IOError, when using simulated port
    fix_pyserial_for_test = rospy.get_param('~fix_pyserial_for_test', False)

    # TODO: should these really be global?
    tcp_portnum = int(rospy.get_param('/rosserial_embeddedlinux/tcp_port', '11411'))
    fork_server = rospy.get_param('/rosserial_embeddedlinux/fork_server', False)

    # TODO: do we really want command line params in addition to parameter server params?
    sys.argv = rospy.myargv(argv=sys.argv)
    if len(sys.argv) >= 2 :
        port_name  = sys.argv[1]
    if len(sys.argv) == 3 :
        tcp_portnum = int(sys.argv[2])

    if port_name == "tcp" :
        server = RosSerialServer(tcp_portnum, fork_server)
        rospy.loginfo("Waiting for socket connections on port %d" % tcp_portnum)
        try:
            server.listen()
        except KeyboardInterrupt:
            rospy.loginfo("got keyboard interrupt")
        finally:
            rospy.loginfo("Shutting down")
            for process in multiprocessing.active_children():
                rospy.loginfo("Shutting down process %r", process)
                process.terminate()
                process.join()
            rospy.loginfo("All done")

    else :          # Use serial port
        while not rospy.is_shutdown():
            rospy.loginfo("Connecting to %s at %d baud" % (port_name,baud) )
            try:
                client = SerialClient(port_name, baud, fix_pyserial_for_test=fix_pyserial_for_test)
                client.run()
            except KeyboardInterrupt:
                break
            except SerialException:
                sleep(1.0)
                continue
            except OSError:
                sleep(1.0)
                continue

