#!/usr/bin/env python

import rospy
import numpy as np
import cv2
#import imutils
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys
import matplotlib.pyplot as plt

#This code is derived from Anis Kouba's github opencv repository 
# found here https://github.com/aniskoubaa/ros_essentials_cpp/blob/master/src/topic03_perception/image_pub_sub.py
#some of the code was also derevied from workshop 4
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

  #find the upper and lower bounds of the green color (tennis ball)
  #greenLower =(0, 0, 0)
  #greenUpper = (360, 70, 70)
  #greenLower =(0, 0, 0)
  #greenUpper = (10, 0, 44)
  greenLower =(0, 0, 0)
  greenUpper = (360, 0, 50)
  
  #define a mask using the lower and upper bounds of the green color 
  mask = cv2.inRange(hsv, greenLower, greenUpper)

  cv2.imshow("mask image", mask)

  # Now detect the contours and count the number of grapes

  contours, hierarchy= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  
  number_of_objects_in_image= len(contours)

  print ("The number of grapes in this image: ", str(number_of_objects_in_image))
  cv2.waitKey(0)
  cv2.destroyAllWindows()
def main(args):
  rospy.init_node('image_converter', anonymous=True)
  image_sub = rospy.Subscriber("/thorvald_001/kinect2_right_camera/hd/image_color_rect",Image, image_callback)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
