#!/usr/bin/env python

import serial
import time

import rospy
from std_msgs.msg import String

def callback(data):

	command_theta="STRAIGHT"#angle in degres

	rospy.loginfo(rospy.get_caller_id(), data.data)

	ser=serial.Serial("/dev/ttyUSB0",115200)
	if ser.isOpen():
		print(ser.name+'is open...')

	turn_time = 50*0.0106465

	command_theta = data.data

	if command_theta == "RIGHT":
		ser.write(b'@0sB15\r')#regenerative braking at 15%
		ser.write(b'@1sB0\r')
		ser.write(b'@0sv5\r')
		ser.write(b'@1sv0\r')

		time.sleep(turn_time)

	if command_theta == "LEFT":
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

def sub():

	rospy.init_node('sub', anonymous=True)
	rospy.Subscriber('Direction', String, callback)

	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()

if __name__ == '__main__':
    sub()
