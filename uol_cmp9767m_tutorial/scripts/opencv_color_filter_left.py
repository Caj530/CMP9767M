#!/usr/bin/env python

import rospy
import numpy as np
import cv2
#import imutils
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys

bridge = CvBridge()

def image_callback(ros_image):
  print('got an image')
  global bridge
  #convert ros_image into an opencv-compatible image
  try:
    cv_image = bridge.imgmsg_to_cv2(ros_image, "bgr8")
  except CvBridgeError as e:
      print(e)
  #from now on, you can work exactly like with opencv
  cv2.imshow("Image window", cv_image)
  cv2.waitKey(3)

  #convert the image into the HSV color space
  hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
  cv2.imshow("hsv image",hsv)

  #find the upper and lower bounds of the  color 
  #greenLower =(0, 0, 0)
  #greenUpper = (360, 70, 70)
  #greenLower =(0, 0, 0)
  #greenUpper = (10, 0, 44)
  greenLower =(0, 0, 0)
  greenUpper = (360, 0, 50)
  
  #define a mask using the lower and upper bounds of the color 
  mask = cv2.inRange(hsv, greenLower, greenUpper)

  cv2.imshow("mask image", mask)

  # Now detect the contours and count the number of grapes

  contours, hierarchy= cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  
  number_of_objects_in_image= len(contours)

  print ("The number of grapes in this image: ", str(number_of_objects_in_image))
  cv2.waitKey(0)
  cv2.destroyAllWindows()
