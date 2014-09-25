import sys
import math
from sensor_msgs.msg import JointState
from brics_actuator.msg import JointVelocities, JointPositions, JointValue


class JointController:
    
	def __init__(self):
	
        # Declare arm constants 

		#0.0100692 and 5.84014
		#0.0100692 and 2.61799
		#-5.02655 and -0.015708 
		#0.0221239 and 3.4292
		#0.110619 and 5.64159 

		self.maxVelX = 1.7
		self.maxVelY = 1.7
		self.threshold = 0.5;

		self.jointConstraints = []
		self.jointConstraints.append((0.0100692, 5.84014))
		self.jointConstraints.append((0.0300692, 1.9))#2.61799))
		self.jointConstraints.append((-5.02655, -0.015708))
		self.jointConstraints.append((0.0221239, 3.4292))
		self.jointConstraints.append((0.110619, 5.64159))

		self.armInitialized = False;


	def refresh_joint_position(self, msg):
		if (not self.armInitialized):
			self.armInitialized = True;
		self.jointPositions = msg.position;
		for i in range(0,len(msg.name)):
			print msg.name[i],"\t", msg.position[i], "\t", msg.velocity[i]

	
	def get_joint_velocities(self, dx, dy):
		if (not self.armInitialized):
			dx = 0
			dy = 0

			mvx = 0
			mvy = 0

		else:

			mvx = self.maxVelX;
			mvy = self.maxVelY;

			if (dx>0):
				if self.jointConstraints[0][1]-self.jointPositions[0]<self.threshold:
					mvx = (self.jointConstraints[0][1]-self.jointPositions[0])*self.maxVelX;
					#print self.jointPositions[0], "mvx\t", mvx

			else:
				if -self.jointConstraints[0][0]+self.jointPositions[0]<self.threshold:
					mvx = (-self.jointConstraints[0][0]+self.jointPositions[0])*self.maxVelX;
					#print self.jointPositions[0], "mvx\t", mvx

			#print self.jointConstraints[1], "\t", self.jointPositions[1]#, "\t",  (self.jointConstraints[1][1]-self.jointPositions[1]) 
			if (dy>0):
				if self.jointConstraints[1][1]-self.jointPositions[1]<self.threshold:
					mvy = (self.jointConstraints[1][1]-self.jointPositions[1])*self.maxVelY;
					#print self.jointPositions[1], "mvy\t", mvy
			else:
				if -self.jointConstraints[1][0]+self.jointPositions[1]<self.threshold:
					mvy = (-self.jointConstraints[1][0]+self.jointPositions[1])*self.maxVelY;
					#print self.jointPositions[1], "mvy\t", mvy

			

		jv = JointVelocities()
		jv.velocities.append(JointValue())
		jv.velocities[-1].unit = "s^-1 rad"
		jv.velocities[-1].joint_uri = 'arm_joint_1'
		jv.velocities[-1].value = dx*mvx;
		jv.velocities.append(JointValue())
		jv.velocities[-1].unit = "s^-1 rad"
		jv.velocities[-1].joint_uri = 'arm_joint_2'
		jv.velocities[-1].value = dy*mvy;
		jv.velocities.append(JointValue())
		jv.velocities[-1].unit = "s^-1 rad"
		jv.velocities[-1].joint_uri = 'arm_joint_3'
		jv.velocities[-1].value = 0;
		jv.velocities.append(JointValue())
		jv.velocities[-1].unit = "s^-1 rad"
		jv.velocities[-1].joint_uri = 'arm_joint_4'
		jv.velocities[-1].value = 0;
		jv.velocities.append(JointValue())
		jv.velocities[-1].unit = "s^-1 rad"
		jv.velocities[-1].joint_uri = 'arm_joint_5'
		jv.velocities[-1].value = 0;



		return jv






