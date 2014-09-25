

from planner_class import *
from brics_actuator.msg import JointVelocities, JointPosition, JointValue

def main():
  
  JP = JointVelocities()
  JP.positions.append(JointValue)
  JP.poisonStamp.originator = 'orig'
  JP.poisonStamp.description = 'desc'
  JP.poisonStamp.qos = 0.0

  # JP.positions.joint_uri = 0.2
  # JP.positions.unit = 'rad'
  # JP.positions.value = 0.3

  JP.positions[0].joint_uri = 'arm_joint_1'
  JP.positions[0].unit = 'rad'
  JP.positions[0].value = 0.3

  planner = PlannerClass()
  #planner.update([1,0,1,0,1], 0.5, -.01, False) 
  #action = planner.get_action() 


  answer = planner.update(JP,4.5,6.7, True)

  print answer
  #rospy.spin()

if __name__ == '__main__': 
 	main()