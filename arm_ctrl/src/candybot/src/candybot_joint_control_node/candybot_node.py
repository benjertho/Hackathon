#!/usr/bin/env python

#-*- encoding: utf-8 -*-
__author__ = 'ivan vishniakou'

import rospy
import thread
import time
import rospy
import sys
from PyQt4 import QtGui, QtCore

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from brics_actuator.msg import JointVelocities, JointPositions, JointValue
from sensor_msgs.msg import JointState

from KukaJointController import JointController
from gui import KukaGUI
from tracker.msg import proto

def initlize_node():
	global guiWidget;
	global _ex;

	jointController = JointController();
	
	rospy.init_node('candybot_arm_control', anonymous=False)
	rospy.loginfo("candybot_arm_control is now running")

	jointPositionsSubscriber = rospy.Subscriber("/joint_states", JointState, jointController.refresh_joint_position)
	trackerSubscriber = rospy.Subscriber("/tracker/tracker_data", proto, jointController.refresh_tracker)
	jvp = rospy.Publisher("arm_1/arm_controller/velocity_command", JointVelocities)

	print "test"

	r = rospy.Rate(20)

	while not rospy.is_shutdown():
		
		guiInput = guiWidget.getSliderPositions();

		#print guiInput[-1]
		if guiInput[-1]:

			jv = jointController.get_joint_velocities(guiInput[0],guiInput[1], guiInput[2])
			jvp.publish(jv);
			#rospy.loginfo("WORKING")
		else:
			#rospy.loginfo("STOPPED BY BUTTON")
			jv = jointController.get_zero_velocities()
			jvp.publish(jv);
		


		#rospy.loginfo(guiWidget.getSliderPositions())
		#if _ex:
		#	rospy.shutdown()
		r.sleep()
		

	#demo_class = DemoClass()
	#demo_class.initilize_parameters(10, 10.0)
	_ex = True
	print "ex set to ", _ex;
	exit();


def run_gui():
	global guiWidget;
	global _ex;
	app = QtGui.QApplication(sys.argv)
	guiWidget = KukaGUI()
	#print guiWidget.getSliderPositions()
	guiWidget.show()
	_ex = True
	sys.exit(app.exec_())


def main(): 
	_ex = False
	try:
		#thread.start_new_thread( print_time, ("Thread-2", 4, 1) )
		thread.start_new_thread( run_gui, () )
		
	except:
		print "Error: unable to start thread"
	
	initlize_node()
	while not _ex:
		pass
	exit()


if __name__ == '__main__':
	global _joint_positions
	_joint_positions = [0.0,0.00,-0.01,0.0025,0.012, True]
	_ex = False
	main()

