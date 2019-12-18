#!/usr/bin/env python
import serial
import time

import rospy
from std_msgs.msg import String

def callback(data):
    	rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
	
	ser=serial.Serial("/dev/ttyUSB0",115200)
	if ser.isOpen():
		print(ser.name+'is open...')

	turn_time = 10*0.0106465

	command_theta = data.data

	if command_theta == "LEFT":
		ser.write(b'@0sB15\r')#regenerative braking at 15%
		ser.write(b'@1sB0\r')
		ser.write(b'@0sv5\r')
		ser.write(b'@1sv0\r')

		time.sleep(turn_time)

	if command_theta == "RIGHT":
		ser.write(b'@1sB15\r')#regenerative braking at 15%
		ser.write(b'@0sB0\r')
		ser.write(b'@1sv5\r')
		ser.write(b'@0sv0\r')

		time.sleep(turn_time)

	else:
		ser.write(b'@0sB0\r')#regenerative braking at 0%
		ser.write(b'@1sB0\r')
		ser.write(b'@0sv5\r')
		ser.write(b'@1sv5\r')

	command_theta = "STRAIGHT"

    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("Direction", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
