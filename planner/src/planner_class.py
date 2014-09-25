#!/usr/bin/env python

#import rospy
import time
#from sensor_msgs.msg import JointState
#from brics_actuator.msg import JointPositions 


class PlannerClass:
#from brics_actuator.msg import JointPositions lass PlannerClass():
  def __init__(self):
    #print "\n-------------\nInitialized!\n-------------\n"
    
    self.XYTolerance = 0.15
    self.TargetRadius = 140
    self.GripperDelayInt = 5

    self.IDLE_STATE = 0
    self.SEARCH_STATE = 1
    self.REACH_STATE = 2
    self.GRASP_STATE = 3
    self.RETRACT_STATE = 4
    self.POINT_UP_STATE = 5
    self.VERIFY_STATE = 6
    self.TRAY_ROT_STATE = 7
    self.TRAY_ORIENT_STATE = 8
    self.RELEASE_STATE = 9
    self.IDLE_ORIENT_STATE = 10
    self.IDLE_ROT_STATE = 11

    self.State = self.IDLE_STATE
    # State machine state constants 


  def jnt_pos_cb(self): 
    print "simple call completed"

  def update(self, jp, X, Y, R, start):
    print 
    if  self.State == self.IDLE_STATE:
      # If run command has been sent 
      if (start == True): 
        # If the joint positions are close enough to zero
        # Ideal
        #position: [0.007189413957253565, 0.00016110731556870733, -3.1415926535897935e-05, 4.4247783853377367e-05, 2.9282962115245876, 0.0, 0.0]
        # Bound
        #position: [0.19009656316385162, 0.00017117652279175153, -3.1415926535897935e-05, 4.4247783853377367e-05, 2.9282962115245876, 0.0, 0.0]
        if (jp[0] < 0.19) and (jp[1] < 0.01) and (jp[2] > -0.01) and (jp[3] < 0.01) and (jp[4] > 2.90):
          # we can confidently start the search
          self.State = self.SEARCH_STATE
          print "Entering SEARCH_STATE"
          return ["SEARCH_STATE"]
        else:
          print "Joints are not in initial position"
          return ["IDLE_STATE",[0.007189413957253565, 0.00016110731556870733, -3.1415926535897935e-05, 4.4247783853377367e-05, 2.9282962115245876]]
          

    elif self.State == self.SEARCH_STATE:
      if (X > -self.XYTolerance) and (X < self.XYTolerance) and (Y > -self.XYTolerance) and (Y < self.XYTolerance):
        self.State = self.REACH_STATE
        print "Entering REACH_STATE"
        return ["REACH_STATE"]
      else:
        print "Target not yet found and centered"
        return ["SEARCH_STATE"]        

    elif self.State == self.REACH_STATE:
      if (R > 1.1):
        self.State = self.GRASP_STATE
        print "Entering GRASP_STATE"
        # save candy position for future verification
        self.SavedX = X
        self.SavedY = Y
        return ["GRASP_STATE"]
      else:
        print "Target not within range"
        return ["REACH_STATE"]
        
    elif self.State == self.GRASP_STATE:
      # allow 5 seconds for grasping
      time.sleep(self.GripperDelayInt)
      self.State = self.RETRACT_STATE
      print "Entering RETRACT_STATE"
      return ["RETRACT_STATE"]

    elif self.State == self.RETRACT_STATE:
      # If the joint positions are close enough to zero
      # Ideal
      # position: [0.190187186028859, 1.4503283315783957, -0.012943361732789947, 0.46816367706065926, 2.9282962115245876, 0.0, 0.0]
      # Bound
      # position: [0.190187186028859, 1.4974924982111346, -0.06613052535806514, 0.4682079248445126, 2.9282962115245876, 0.0, 0.0]
      if (jp[2] > -0.06):
        self.State = self.POINT_UP_STATE
        print "Entering POINT_UP_STATE"
        return ["POINT_UP_STATE"]
      else:
        print "Arm has not been fully retracted"
        return ["RETRACT_STATE"]        

    elif self.State == self.POINT_UP_STATE:
      # position: [0.190187186028859, 0.0063234621360717625, -0.01229933523880404, 0.2141371499584198, 2.9282962115245876, 0.0, 0.0]
      # position: [0.190187186028859, 0.14065675569870453, -0.01229933523880404, 0.22110617591532672, 2.9282962115245876, 0.0, 0.0]
      if (jp[1] < 0.14) and (jp[2] > -0.01):
        self.State = self.VERIFY_STATE
        print "Entering VERIFY_STATE"
        return ["VERIFY_STATE"]
      else:
        print "Arm has not been oriented vertically" 
        return ["POINT_UP_STATE"]

    elif self.State == self.VERIFY_STATE:
      if ((X > self.SavedX-.1)and(X < self.SavedX+.1)) and ((Y > self.SavedY-.1)and(Y < self.SavedY+.1)):
        self.State = self.TRAY_ROT_STATE
        print "Entering TRAY_ROT_STATE"
        return ["TRAY_ROT_STATE",[2.9811196980761374,None,None,None,None]]
      else:
        print "Target cannot be verified - Aborting"
        return ["IDLE_ORIENT_STATE",[None, 0.00016110731556870733, -3.1415926535897935e-05, 4.4247783853377367e-05, 2.9282962115245876]]

    elif self.State == self.TRAY_ROT_STATE:
      #Target: position: [2.9811196980761374, 0.14065675569870453, -0.01080707872834889, 0.22084068921220645, 2.9282298398488074, 0.0, 0.0]
      #Lower: position: [2.8325485455001203, 0.14065675569870453, -0.01080707872834889, 0.22084068921220645, 2.928207715956881, 0.0, 0.0]
      # Upper: position: [3.0615625945810376, 0.14065675569870453, -0.01080707872834889, 0.22084068921220645, 2.928207715956881, 0.0, 0.0]
      if (jp[0] > 2.83) and (jp[0] < 3.06):
        self.State = self.TRAY_ORIENT_STATE
        print "Entering TRAY_ORIENT_STATE"
        return ["TRAY_ORIENT_STATE",[None, 0.3931723344382072, -2.872688030405775, 0.20535396486352436, 2.9281634681730275]]
      else:
        print "Arm has not been rotated towards tray"
        return ["TRAY_ROT_STATE",[2.9811196980761374,None,None,None,None]]

    elif self.State == self.TRAY_ORIENT_STATE:
      # TRAY_ORIENT_STATE
      # Target: position: [2.9339756698578445, 0.3931723344382072, -2.872688030405775, 0.20535396486352436, 2.9281634681730275, 0.0, 0.0]
      # Bound: position: [2.9329083338922017, 0.4456127656558214, -2.7558364916555025, 0.2056858232424247, 2.9281413442811006, 0.0, 0.0]
      if  (jp[1] > 0.39) and (jp[1] < 0.44) and (jp[2] > -2.87) and (jp[2] < -2.76) and (jp[3] > 0.20) and (jp[3] < 0.21):
        self.State = self.RELEASE_STATE
        print "Entering RELEASE_STATE"
        return ["RELEASE_STATE"]
      else:
        print "Arm has not been oriented for tray deposit"
        return ["TRAY_ORIENT_STATE",[None, 0.3931723344382072, -2.872688030405775, 0.20535396486352436, 2.9281634681730275]]

    elif self.State == self.RELEASE_STATE:   
      # allow 5 seconds for grasping
      time.sleep(self.GripperDelayInt)
      self.State = self.IDLE_ORIENT_STATE
      print "Entering IDLE_ORIENT_STATE"
      return ["IDLE_ORIENT_STATE",[None, 0.00016110731556870733, -3.1415926535897935e-05, 4.4247783853377367e-05, 2.9282962115245876]]

    elif self.State == self.IDLE_ORIENT_STATE:
      if (jp[1] < 0.01) and (jp[2] > -0.01) and (jp[3] < 0.01) and (jp[4] > 2.90):
        self.State = self.IDLE_ROT_STATE
        print "Entering IDLE_ROT_STATE"
        return ["IDLE_ROT_STATE"]
      else:
        print "Arm has not been oriented vertically"
        return ["IDLE_ORIENT_STATE",[None, 0.00016110731556870733, -3.1415926535897935e-05, 4.4247783853377367e-05, 2.9282962115245876]]
      
    elif self.State == self.IDLE_ROT_STATE:
      if (jp[0] < 0.19):
        self.State = self.IDLE_STATE
        print "Entering IDLE_STATE"
        return ["IDLE_STATE",[0.007189413957253565, 0.00016110731556870733, -3.1415926535897935e-05, 4.4247783853377367e-05, 2.9282962115245876, 0.0, 0.0]]
      else:
        print "Arm has not been rotated to zero"
        return ["IDLE_ROT_STATE"]

    else:
      self.State = self.IDLE_STATE

    #print joint_positions[0]
    #print joint_positions[1]
    #print joint_positions[2]
    #print joint_positions[3]
    #print joint_positions[4]
    #print X
    #print Y

