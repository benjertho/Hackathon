#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic



#rosrun my_kinect_proj talker.py cmd_vel:=/turtle1/cmd_vel

import sys,tty,termios, time
import struct

#file = open( "/dev/input/mice", "rb" );
import roslib
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from brics_actuator.msg import JointVelocities, JointPositions, JointValue

from random import random



class _Getch:       
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch




'''
def getMouseEvent():
  buf = file.read(3);
  button = ord( buf[0] );
  bLeft = button & 0x1;
  bMiddle = ( button & 0x4 ) > 0;
  bRight = ( button & 0x2 ) > 0;
  x,y = struct.unpack( "bb", buf[1:] );
  print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) );
  return (x,y, bLeft, bMiddle)
'''
'''
rostopic pub /arm_1/arm_controller/velocity_command brics_actuator/JointVelocities "poisonStamp:
  originator: ''
  description: ''
  qos: 0.0
velocities:
- timeStamp:
    secs: 0
    nsecs: 0
  joint_uri: 'arm_joint_1'
  unit: 's^-1 rad'
  value: -0.035" 
'''
#/arm_1/arm_controller/velocity_command


selected_joint = 1;

def talker():
    mouse_pos = [0,0]; 
       
    #pub1 = rospy.Publisher("arm_1/arm_controller/velocity_command brics_actuator/JointVelocities", JointVelocities)
    rospy.init_node('my_keyboard', anonymous=True)
    r = rospy.Rate(10) # 10hz
    selected_joint = 1;
    pub = rospy.Publisher("arm_1/arm_controller/velocity_command", JointVelocities)
    pub2 = rospy.Publisher("arm_1/gripper_controller/position_command", JointPositions)
    max_v = 0.2

    grasp = False;
    key_input = _Getch();
    while not rospy.is_shutdown():
	
	#49 - 1 key
	#print "test output"
        #rospy.loginfo('str')
        #while(1):
        k = key_input();	
	# qwe 113 119 101
	
		

	o = ord(k)
	if o>=49 and o<=53:
		selected_joint = o-48
		print "joint ", o-48, " selected"
	
	jv = JointVelocities()
	jv.velocities.append(JointValue())
	jv.velocities[0].joint_uri = "arm_joint_" + str(selected_joint)
	jv.velocities[0].unit = "s^-1 rad"
	jv.velocities[0].value = 0 
	
	if o == 61:
		max_v = max_v*1.5;
		print "max_v ", max_v
	if o == 45:
		max_v = max_v/1.5;
		print "max_v ", max_v

	if o == 113:
		jv.velocities[0].value = -max_v 
	elif o == 119:
		jv.velocities[0].value = 0
	elif o == 101:
		jv.velocities[0].value = +max_v
        
	pub.publish(jv);

	if o==32:
		if grasp:
			val = 0.0115
		else:
			val = 0.0001
		jp = JointPositions()
		jp.positions.append(JointValue())
		jp.positions[0].unit = "m"
		jp.positions[0].joint_uri = "gripper_finger_joint_l"
		jp.positions[0].value = val		
		jp.positions.append(JointValue())
		jp.positions[1].unit = "m"
		jp.positions[1].joint_uri = "gripper_finger_joint_r"
		jp.positions[1].value = val
		pub2.publish(jp);
		grasp = not grasp
	#    if k!='':break
        print ord(k);
	
	if ord(k)!=27:
        	r.sleep()
	else:
		exit()
	
        
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
