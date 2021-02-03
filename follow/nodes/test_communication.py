#!/usr/bin/env python
import rospy
import math
import tf
import socket
import std_msgs
from tf2_geometry_msgs import PoseStamped
from image_geometry import PinholeCameraModel
from actionlib_msgs.msg import GoalID
import sensor_msgs.msg
import time


cam_info = sensor_msgs.msg.CameraInfo()
cam_info.width = 640
cam_info.height = 480
cam_info.D = [0.1639958233797625, -0.271840030972792, 0.001055841660100477, -0.00166555973740089, 0.0]
cam_info.K = [322.0704122808738, 0.0, 199.2680620421962, 0.0, 320.8673986158544, 155.2533082600705, 0.0, 0.0, 1.0]
cam_info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
cam_info. P = [329.2483825683594, 0.0, 198.4101510452074, 0.0, 0.0, 329.1044006347656, 155.5057121208347, 0.0, 0.0, 0.0, 1.0, 0.0]


def PointFromPixel(pixel, camera_model, depth=1000):
    ray = model.projectPixelTo3dRay(pixel)
    ray_z = [el/ray[2] for el in ray]
    pt = [el*depth for el in ray_z]
    return pt

def callback(data):


    yolo_goal = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
    cancel_pub = rospy.Publisher('move_base/cancel', GoalID, queue_size=1)

    print("Test", data)

    pixel_yolo = eval(data)
    print(type("pixel décodé", pixel_yolo)


    if pixel_yolo != (-1, -1):
        try:
            point_camera = PointFromPixel(pixel_yolo, model)
            p_camera = PoseStamped()
            p_camera.header.frame_id = 'camera_link'
            p_camera.pose.position.x = point_camera[0]
            p_camera.pose.position.y = point_camera[1]
            p_camera.pose.position.z = point_camera[2]
            p_camera.pose.orientation.w = 0
            now = rospy.Time.now()
            p_map = listener.transformPose('map', p_camera)
            print(p_map)

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print("erreur")
            continue

        print("publie")
        yolo_goal.publish(p_map)
        rate.sleep()

    elif pixel_yolo == None:
        pass

    else :
        cancel_msg = GoalID()
        cancel_pub.publish(cancel_msg)

if __name__ == '__main__':


    rospy.init_node('test_communication')

    model = PinholeCameraModel()
    model.fromCameraInfo(cam_info)

    listener = tf.TransformListener()

    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():

        yolo_subscriber = rospy.Subscriber("/chatter", std_msgs.msg.String, callback, queue_size = 10)

