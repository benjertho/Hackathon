

from planner_class import *
#from brics_actuator.msg import JointVelocities, JointPosition, JointValue

def main():

  planner = PlannerClass()
  time.sleep(1)

  # update(self, jp, X, Y, R, start):
  # Initialize
  JP = [0.1,0.005,-.005,.005,3.0]
  X = 1
  Y = 1
  R = 0.001
  START = False

  # IDLE_STATE
  # Test Case: if (jp[0] < 0.19) and (jp[1] < 0.01) and (jp[2] > -0.01) and (jp[3] < 0.01) and (jp[4] > 2.90):
  START = True
  print planner.update(JP,X, Y, R, START)
  time.sleep(1)

  # SEARCH_STATE
  # Test Case: if (X > -0.15) and (X < 0.15) and (Y > -0.15) and (Y < 0.15):
  X = 0.1
  Y = -0.1
  print planner.update(JP, X, Y, R, START)
  time.sleep(1)
  
  # REACH_STATE
  # Test Case:  if (R > 1.1):
  R = 1.5
  print planner.update(JP,X, Y, R, START)
  time.sleep(5)
  
  # GRASP_STATE
  #  Test Case: time.sleep(5)
  print planner.update(JP,X, Y, R, START)
  time.sleep(1)
  
  # RETRACT_STATE
  # position: [0.190187186028859, 1.4503283315783957, -0.012943361732789947, 0.46816367706065926, 2.9282962115245876, 0.0, 0.0]
  # position: [0.190187186028859, 1.4974924982111346, -0.06613052535806514, 0.4682079248445126, 2.9282962115245876, 0.0, 0.0]
  # Test Case:  if (jp[2] > -0.06):
  JP[2] = -.005
  print planner.update(JP,X, Y, R, START)
  time.sleep(1)
  
  # POINT_UP_STATE
  # position: [0.190187186028859, 0.0063234621360717625, -0.01229933523880404, 0.2141371499584198, 2.9282962115245876, 0.0, 0.0]
  # position: [0.190187186028859, 0.14065675569870453, -0.01229933523880404, 0.22110617591532672, 2.9282962115245876, 0.0, 0.0]
  # Test Case:  if (jp[1] < 0.14) and (jp[2] > -0.01):
  JP[1] = 0.1
  JP[2] = -.005
  print planner.update(JP,X, Y, R, START)
  time.sleep(1)
  
  # VERIFY_STATE
  # Test Case:  if ((X > SavedX-.1)and(X < SavedX+.1)) and ((Y > SavedY-.1)and(Y < SavedY+.1)):
  X = X + .03
  Y = Y - .02
  #X = 0.1
  #Y = -0.1
  print planner.update(JP,X, Y, R, START)
  time.sleep(1)
  
  # TRAY_ROT_STATE
  #Target: position: [2.9811196980761374, 0.14065675569870453, -0.01080707872834889, 0.22084068921220645, 2.9282298398488074, 0.0, 0.0]
  #Lower: position: [2.8325485455001203, 0.14065675569870453, -0.01080707872834889, 0.22084068921220645, 2.928207715956881, 0.0, 0.0]
  # Upper: position: [3.0615625945810376, 0.14065675569870453, -0.01080707872834889, 0.22084068921220645, 2.928207715956881, 0.0, 0.0]
  # Test Case:  if (jp[0] > 2.83) and (jp[0] < 3.06) 
  JP[0] = 3.01
  print planner.update(JP,X, Y, R, START)
  time.sleep(1)
  
  # TRAY_ORIENT_STATE
  # Target: position: [2.9339756698578445, 0.3931723344382072, -2.872688030405775, 0.20535396486352436, 2.9281634681730275, 0.0, 0.0]
  # Bound: position: [2.9329083338922017, 0.4456127656558214, -2.7558364916555025, 0.2056858232424247, 2.9281413442811006, 0.0, 0.0]
  # Test Case:  if  (jp[1] > 0.39) and (jp[1] < 0.44) and (jp[2] > -2.87) and (jp[2] < -2.76) and (jp[3] > 0.20) and (jp[3] < 0.21):
  JP[1] = 0.41
  JP[2] = -2.8
  JP[3] = .205
  print planner.update(JP,X, Y, R, START)
  time.sleep(5)
  
  # RELEASE_STATE
  # Test Case:  time.sleep(5)
  print planner.update(JP,X, Y, R, START)
  time.sleep(1)
  
  # IDLE_ORIENT_STATE
  # Test Case:  if (jp[1] < 0.01) and (jp[2] > -0.01) and (jp[3] < 0.01) and (jp[4] > 2.90)
  JP[1] = 0.005
  JP[2] = -0.005
  JP[3] = 0.005
  JP[4] = 2.95
  print planner.update(JP,X, Y, R, START)
  time.sleep(1)
  
  # IDLE_ROT_STATE
  # Test Case:  if (jp[0] < 0.19):
  JP[0] = .01
  print planner.update(JP,X, Y, R, START)
  
  #rospy.spin()

if __name__ == '__main__': 
 	main()