#!/usr/bin/env python3

### Imports

import rospy
import yaml
from geometry_msgs.msg import Pose, Point, Quaternion
#import threading as td
import math
import tf
import socketio
import socket
import std_msgs
from tf2_geometry_msgs import PoseStamped
from geometry_msgs.msg import Twist
from image_geometry import PinholeCameraModel
from actionlib_msgs.msg import GoalID
import sensor_msgs.msg
import time
from rospy_message_converter import message_converter
#from take_photo import TakePhoto
from go_to_specific_point_on_map import GoToPose

### Paramètres caméra
cam_info = sensor_msgs.msg.CameraInfo()
cam_info.width = 640
cam_info.height = 480
cam_info.D = [0.1639958233797625, -0.271840030972792, 0.001055841660100477, -0.00166555973740089, 0.0]
cam_info.K = [322.0704122808738, 0.0, 199.2680620421962, 0.0, 320.8673986158544, 155.2533082600705, 0.0, 0.0, 1.0]
cam_info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
cam_info.P = [329.2483825683594, 0.0, 198.4101510452074, 0.0, 0.0, 329.1044006347656, 155.5057121208347, 0.0, 0.0, 0.0, 1.0, 0.0]

### paramètres

i = 0


### Fonctions et classes

class ID_Check:
    def __init__(self):
        self.verification = None
    def identification_callback(data):
        self.verification = data


def PointFromPixel(pixel, camera_model, depth=2):
    pixel_sym = (640 - pixel[0], pixel[1])
    ray = model.projectPixelTo3dRay(pixel)
    ray_z = [el/ray[2] for el in ray]
    pt = [el*depth for el in ray_z]
    return pt

### Fonction callback

def navigation_callback(data):
    global detect
    global time_last_detection
    global follow
    global navigator
    global i

    dictionary = message_converter.convert_ros_message_to_dictionary(data)
    pixel_yolo = dictionary['data']
    pixel_yolo = eval(pixel_yolo)
    #print("pixel yolo",pixel_yolo)

    if not follow :
        if pixel_yolo == (-1,-1) or pixel_yolo == None:
            with open("/home/ubuntu/projet_ids/turtlebot/route.yaml", 'r') as stream:
                dataMap = yaml.load(stream)
                obj = dataMap[i]
                name = obj['filename']

                # Let the robot follow someone
                #while(lock.locked()):
                #   rospy.loginfo("Im locked")
                #rospy.sleep(1)

                # Navigation
                rospy.loginfo("Following route to %s pose", name[:-4])
                success = navigator.goto(obj['position'], obj['quaternion'])

                if success:
                    rospy.loginfo("Reached %s pose", name[:-4])
                    i += 1
                    if (i>=len(dataMap)):
                        i = 0
                else:
                    rospy.loginfo("Failed to reach %s pose", name[:-4])

        else:
            follow = True

    else:
        if pixel_yolo == (-1,-1): #si le robot ne voit personne
            now = rospy.Time.now()
            if detect and ((now - time_last_detection).to_nsec() < 1000000000):
                print("Personne perdue de vue")
                msg=Twist()
                msg.angular.z = 0.2
                cmd_pub.publish(msg)

            else:
                print("Retour à la ronde")
                follow = False

        elif pixel_yolo==(-2,-2): #procédure d'identification : STOP
            if id_check.verif == None:
                pass

            elif id_check.verif == "OK":
                detect = False

            elif if_check.verif == "Probleme":
                print("ERREUR D'IDENTIFICATION")
                detect = False

            else:
                pass

        else : #si le robot voit quelqu'un
            detect = True
            time_last_detection = rospy.Time.now()
            try:
                point_camera = PointFromPixel(pixel_yolo, model)
                p_camera = PoseStamped()
                p_camera.header.frame_id = 'camera_rgb_optical_frame'
                p_camera.pose.position.x = point_camera[0]
                p_camera.pose.position.y = point_camera[1]
                p_camera.pose.position.z = point_camera[2]
                p_map = tf_listener.transformPose('map', p_camera)
                p_map.pose.orientation.x = 0
                p_map.pose.orientation.y = 0
                p_map.pose.orientation.z = 0
                p_map.pose.orientation.w = 1
                print(p_map)
                pos = {'x': p_map.pose.position.x, 'y': p_map.pose.position.y}
                quat = {'r1': p_map.pose.orientation.x, 'r2': p_map.pose.orientation.y, 'r3': p_map.pose.orientation.z, 'r4': p_map.pose.orientation.w}

            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                print("erreur")
                pass

            print("publie")
            # yolo_goal.publish(p_map)
            success = navigator.goto(pos, quat)




### Main

if __name__ == '__main__':
    global detect
    global time_last_detection
    global navigator
    global i

    navigator = GoToPose()
    detect = False
    follow = False
    time_last_detection = rospy.Time(0)
    model = PinholeCameraModel()
    model.fromCameraInfo(cam_info)
    id_check = ID_Check()

    rospy.init_node('navigate')
    tf_listener = tf.TransformListener()
    cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)

    rate = rospy.Rate(3)

'''
    pt_base = PoseStamped()
    pt_base.header.frame_id = 'base_link'
    pt_base.pose.position.x = 0
    pt_base.pose.position.y = 0
    pt_base.pose.position.z = 0
    pt_loc_robot = tf_listener.transformPose('map', pt_base)
    sio.emit("position", {"x": pt_loc_robot.pose.position.x, "y": pt_loc_robot.pose.position.y})
    '''
    try:
        rospy.sleep(5)
        while not rospy.is_shutdown():
            print("AAAAAAAAAAAAAAAAAAAAAAAAA")
            identification_subscriber = rospy.Subscriber("/identificationn", std_msgs.msg.String, callback=id_check.identification_callback, queue_size = 1)
            yolo_subscriber = rospy.Subscriber("/chatterr", std_msgs.msg.String, callback=navigation_callback, queue_size = 1)
            rate.sleep()

    except KeyboardInterrupt:
        navigator.shutdown()
        #je sais pas quoi mettre là



