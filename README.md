# Project summary

This project provides a solution to make the Thorvald robot count the grapes in a vineyard mostly autonomously. It first uses movebase to move Thorvald to different points on the topological map and then opencv is used to detect and count the number of grapes at that specific point. Then the same task is carried out using topological navigation to guide Thorvald to specified points adjacent to the grapevine then count the number of grapes at each point and then return to its starting point
#  Setup
Create a ros workspace.
You can either gitclone my forked copy of the LCAS repository which contains my code which can be accessed by typing the following in you terminal (make sure that you put it in the src folder of your workspace.

      git clone https://github.com/Caj530/CMP9767M.git   
      
Or you can use the original lcas repository, which can be accessed by cloning it into your src folderwith the following terminal command:

        git clone https://github.com/LCAS/CMP9767M.git
        
However if you use this method, you will need to add the return.py, opencv_color_filter_right.py, and opencv_color_filter_left.py files to the scripts folder in the uol_cmp9767m_tutorial package/folder.
- Before you can run opencv, you need to make sure that it is downloaded on your virtual machine. SO firstly in the terminal do the following:
# INSTALL OPENCV
The installation of OpenCV in ROS Noetic on Ubuntu 20.04 has changed.
Use the following command instead
-	sudo apt-get update
-	sudo apt-get install ros-noetic-vision-opencv
In principle, this should work.
In case you face a problem with imshow (as I faced a similar one), you may try the following solution
- sudo apt-get install libopencv-*
- pip install opencv-contrib-python
use pip3 if you use Python 3
This should solve any problem with OpenCV (in case it happens) when you work with ROS Noetic.
In case you still face problems, it is recommended to make a fresh installation of ROS Noetic.

# Experiment one navigation
-First launch the environment by typing the following in the terminal:

      roslaunch bacchus_gazebo vineyard_demo.launch world_name:= vineyard_small_s4_coarse
 
- Then start move base by typing the following in the terminal:

             roslaunch uol_cmp9767m_tutorial move_base.launch

- In rviz add visualisations for local and global paths: rviz option "Add/By topic/" and then thorvald_001/TrajectoryPlannerROS/global_plan and .../local_plan. Change colours so you can differentiate between the paths. Finally, change the navigation goal topic by selecting from rviz menu "Panels/Tool Properties" and prepending '/thorvald_001' to the 2D Nav Goal topic. You should be able now to send the robot from the rviz interface to any place by specifying 2D Nav Goal from the top menu. You can select the target position of the robot in the map and its orientation using the arrow.
- Now make sure that you are in the  uol_cmp9767m_tutorial package and then make sure you are in the scripts folder found within this package.
Move the robot close to the grape vine and type: 

        python3 opencv_color_filter_right.py
 
- This assumes that you are using the right-hand side camera, if you are using the left-hand side camera type the following instead:

       python3 opencv_color_filter_left.py

- Do this along the length of the grapevine (you may need to open a new terminal each time), the results should be displayed on the terminal at each point.

#                                Experiment 2 topological navigation
#                                 Step one launching the simulation

- Type the following into the terminal:

      roslaunch bacchus_gazebo vineyard_demo.launch world_name:= vineyard_small_s4_coarse 
      
- once this is complete then launch the following launch file in the terminal:

#               roslaunch uol_cmp9767m_tutorial topo_nav.launch
               
- Now open the topological map visualisation config for RVIZ in uol_cmp9767m_tutorial/config/topo_nav.rviz.
- If you cloned my git hub repository then once the map is loaded click the green arrows at the nodes seen in RVIZ to send topological_navigation goals to the robot.If you cloned the ordinary course repository then follow step 2

#       Step two edge creation

- If you have not cloned my repository, you will need to make the map from scratch as follows:
- Move the robot to waypoint 0 by clicking on the green arrow assigned to waypoint 0 on the map.Once at waypoint 0 then type the following into the terminal to create a 6th waypoint:

                    rosservice call /topological_map_manager2/add_topological_node "
                    
name: WayPoint6
pose:
  position:
    x: -2.0
    y: -5.0
    z: 0.0
  orientation:
    x: 0.0
    y: 0.0
    z: 0.0
    w: 1.0
add_close_nodes: false"

- To connect this way point to waypoint 0 in the terminal type:

rosservice call /topological_map_manager2/add_edges_between_nodes "
origin: WayPoint0
destination: WayPoint6
action: move_base
edge_id: WayPoint0_WayPoint6"

- Now we need to create an adjacent waypoint called waypoint 7. To create this way point type the following in the terminal:

rosservice call /topological_map_manager2/add_topological_node "
name: WayPoint7
pose:
  position:
    x: 0.0
    y: -5.0
    z: 0.0
  orientation:
    x: 0.0
    y: 0.0
    z: 0.0
    w: 1.0
add_close_nodes: false"

- To attach waypoint 7 to waypoint 6 we need to type the following in the terminal: 
- 
rosservice call /topological_map_manager2/add_edges_between_nodes "
origin: WayPoint6
destination: WayPoint7
action: move_base
edge_id: WayPoint6_WayPoint7"

- Now we need to make a new waypoint next to waypoint 7 called waypoint 8, again to create this node type the following in the terminal to create this new waypoint:

rosservice call /topological_map_manager2/add_topological_node "
name: WayPoint8
pose:
  position:
    x: 2.0
    y: -5.0
    z: 0.0
  orientation:
    x: 0.0
    y: 0.0
    z: 0.0
    w: 1.0
add_close_nodes: false"

- Now to attach it to waypoint 7 type the following in the terminal:

rosservice call /topological_map_manager2/add_edges_between_nodes "
origin: WayPoint7
destination: WayPoint8
action: move_base
edge_id: WayPoint7_WayPoint8"

- To make the last waypoint called waypoint 9 type the following in the terminal:

rosservice call /topological_map_manager2/add_topological_node "
name: WayPoint9
pose:
  position:
    x: 4.0
    y: -5.5
    z: 0.0
  orientation:
    x: 0.0
    y: 0.0
    z: 0.0
    w: 1.0
add_close_nodes: false"

- To attach this waypoint to waypoint8 type this command in the terminal:

rosservice call /topological_map_manager2/add_edges_between_nodes "
origin: WayPoint8
destination: WayPoint9
action: move_base
edge_id: WayPoint8_WayPoint9"


- Then to connect waypoint 9(the end of the vineyard) to waypoint 1 execute the following in the terminal:

rosservice call /topological_map_manager2/add_edges_between_nodes "
origin: WayPoint9
destination: WayPoint1
action: move_base
edge_id: WayPoint9_WayPoint1"


- This should build a fully connected map for Thorvald to follow. Save it by executing the following command in your terminal:
- 
rosservice call /topological_map_manager2/write_topological_map "filename: '`pwd`/foo2.tmap2'"

#                                           Step four: moving Thorvald
- Much like in experiment one you need to. make sure that you are in the  uol_cmp9767m_tutorial package and then make sure you are in the scripts folder found within this package.

- Move the robot from waypoint 0 to waypoint 6 by clicking on the arrow at waypoint 6. Once the robot is at waypoint6 execute the following in the terminal:

              python3 opencv_color_filter.py 

- Then move the robot from waypoint 6 to waypoint 7 by clicking on the arrow at waypoint 6. Once the robot is at waypoint8 execute the following in the terminal:

             python3 opencv_color_filter.py 

- Now move Thorvald from waypoint 7 to waypoint 8 by clicking on the arrow at waypoint 8. Once the robot is at waypoint8, once again execute the following in the terminal:

             python3 opencv_color_filter.py 

- Finally move the robot from waypoint 8 to waypoint9 by clicking on the arrow at waypoint 9. Again once the robot is at waypoint6 execute the following in the terminal:

             python3 opencv_color_filter.py 
             
- Now to return the robot back to waypoint 6 (the start) type the following in the terminal:
