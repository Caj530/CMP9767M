#! /usr/bin/env python
# ----------------------------------
# @author: gpdas
# @email: pdasgautham@gmail.com
# @date:
# ----------------------------------

import rospy
import actionlib
import time
from topological_navigation_msgs.msg import GotoNodeAction, GotoNodeGoal

if __name__ == '__main__':
    
    rospy.init_node('topological_navigation_client')
    client = actionlib.SimpleActionClient('/thorvald_001/topological_navigation', GotoNodeAction)
    client.wait_for_server()

    # This script is designed to make the robot autonomously return to it's base after it has finished counting the grapes at waypoint 9
    
    #sends the robot from end of the line to way point one
    goal = GotoNodeGoal()
    goal.target = "WayPoint1"
    rospy.loginfo("going to %s", goal.target)
    # Fill in the goal here
    client.send_goal(goal)
    status = client.wait_for_result() # wait until the action is complete
    result = client.get_result()
    rospy.loginfo("status is %s", status)
    rospy.loginfo("result is %s", result)
    
    

    #sends the robot from waypoint 1 to waypoint 6(which is the start of the line)
    goal.target = "WayPoint6"
    rospy.loginfo("going to %s", goal.target)
    # Fill in the goal here
    client.send_goal(goal)
    status = client.wait_for_result() # wait until the action is complete
    result = client.get_result()
    rospy.loginfo("status is %s", status)
    rospy.loginfo("result is %s", result)
    rospy.sleep(3000000)
