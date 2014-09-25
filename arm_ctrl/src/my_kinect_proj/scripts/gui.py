#!/usr/bin/python

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

class KukaGUI(QtGui.QWidget):
    
	def __init__(self):
		super(KukaGUI, self).__init__()
        
		self.initUI()
        
	def initUI(self):               
        
		self.setGeometry(300, 300, 300, 350)        
		self.setWindowTitle('Kuka GUI')   

		hbox = QtGui.QHBoxLayout()
		
		for i in range(1,3):
			sld = QtGui.QSlider(QtCore.Qt.Vertical, self)
			sld.setGeometry(40*i,10, 30, 200);
			sld.setRange(0,1000)
			sld.setObjectName(str(i))
			#QtCore.QObject.connect(sld, QtCore.SIGNAL('valueChanged(int)'), KukaGUI.onSliderMove)
			if i==1:
				sld.setRange(0,1000)
				sld.setValue(0)
				sld.setValue(500)
				sld.setSingleStep(1);
			if i==2:
				sld.setRange(0,1000)
				sld.setValue(0)
				sld.setValue(500)
				sld.setSingleStep(1);	

			if (i == 3):
				sld.setValue(1000)
			sld.valueChanged.connect(self.onSliderMove)
			hbox.addWidget(sld)

		btn = QtGui.QPushButton("Stahp!",self)
		btn.setGeometry(40,250, 200, 40);
		hbox.addWidget(btn)
		btn.clicked.connect(self.claw)
        #btn.move(30, 250)

        


	def onSliderMove(self, value):
		global _joint_positions;
		#print value
		handle = self.sender()
		ind = int(handle.objectName())
		
		if ind == 1:
			_joint_positions[ind-1] = float(value)/1000.0 - 0.5
			print "dx", _joint_positions[ind-1] 
		elif ind == 2:
			_joint_positions[ind-1] = float(value)/1000.0 - 0.5
			print "dy", _joint_positions[ind-1] 

		'''
		if ind == 1:
			_joint_positions[ind-1] = value*(3.1415926 * (169 + 169) / 180 -0.02)/1000 + 0.01
		elif ind == 2:
			_joint_positions[ind-1] = value*(2.61-0.011)/1000 + 0.011
		elif ind == 3:
			_joint_positions[ind-1] = value*(-0.016+5.03)/1000 - 5.03
		elif ind == 4:
			_joint_positions[ind-1] = value*(3.42 - 0.021) /1000 + 0.021
		elif ind == 5:
			_joint_positions[ind-1] = value*(5.63-0.12)/1000 + 0.12
		print _joint_positions
		'''

	def claw(self):
		print "STAHP!"
		global _joint_positions;
		_joint_positions[5] = False;


		
        
	def closeEvent(self, event):
		global _ex
		reply = QtGui.QMessageBox.question(self, 'Message',
			"Are you sure to quit?", QtGui.QMessageBox.Yes | 
			QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.Yes:
			_ex = True
			event.accept()
		else:
			event.ignore()     

def eventin_cb(msg):
	rospy.loginfo("eventin_cb message: %s", msg.data)


def initlize_node():
	global _ex
	global _joint_positions
	'''
	Initilize node and spin which simply keeps python 
	from exiting until this node is stopped
	'''

	jc = JointController()

	rospy.init_node('candybot_arm_control', anonymous=False)
	rospy.loginfo("candybot_arm_control is now running")

	jointPositionsSubscriber = rospy.Subscriber("/joint_states", JointState, jc.refresh_joint_position)


	'''
	pub1 = rospy.Publisher("arm_1/gripper_controller/position_command", JointPositions)
	pub2 = rospy.Publisher("/arm_1/arm_controller/position_command", JointPositions)
	'''

	jvp = rospy.Publisher("arm_1/arm_controller/velocity_command", JointVelocities)


	r = rospy.Rate(20)

	while not rospy.is_shutdown():

		if _joint_positions[5]:
			jv = jc.get_joint_velocities(_joint_positions[0],_joint_positions[1])
			jvp.publish(jv);
			#rospy.loginfo("WORKING")
		else:
			#rospy.loginfo("STOPPED BY BUTTON")
			jv = jc.get_joint_velocities(0,0)
			jvp.publish(jv);


		#rospy.loginfo("main cycle")
		if _ex:
			rospy.shutdown()
		r.sleep()
    	

    #demo_class = DemoClass()
    #demo_class.initilize_parameters(10, 10.0)
	_ex = True
	print "ex set to ", _ex;
	exit();



def run_gui():

	app = QtGui.QApplication(sys.argv)
	w = KukaGUI()
	#w.resize(250, 150)
	#w.move(300, 300)
	#w.setWindowTitle('Simple')
	w.show()
	sys.exit(app.exec_())




def print_time(threadName, delay, counter):
    while not _ex:
		time.sleep(delay)
		#_joint_positions = (1,1)
		print _ex
		print "%s: %s" % (threadName, time.ctime(time.time()))
		counter -= 1



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


