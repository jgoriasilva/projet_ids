#!/usr/bin/env python  
import rospy
import math
import tf
import socket
from tf2_geometry_msgs import PoseStamped
from image_geometry import PinholeCameraModel
from actionlib_msgs.msg import GoalID
from sensor_msgs.msg import CameraInfo
import time



serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("172.16.16.183",8080))
serverSocket.listen()


def PointFromPixel(pixel, camera_model, depth=1000):
    ray = model.projectPixelTo3dRay(pixel)
    ray_z = [el/ray[2] for el in ray]
    pt = [el*depth for el in ray_z]
    #point = PointStamped()
    #point.header.frame_id = frame
    #point.point.x = pt[0]
    #point.point.y = pt[1]
    #point.point.z = pt[2]
    return pt

if __name__ == '__main__':
    
    
    rospy.init_node('transfo_dynamic')
    
    model = PinholeCameraModel()
    camera_info = rospy.wait_for_message('/raspicam_node/camera_info', CameraInfo)
    model.fromCameraInfo(camera_info)
    
    #rospy.Subscriber('/raspicam_node/camera_info', CameraInfo, callback_camera_info, (model, ) )
    listener = tf.TransformListener()

    #yolo_goal = rospy.Publisher('yolo_goal', PoseStamped, queue_size=10)
    yolo_goal = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
    cancel_pub = rospy.Publisher('/move_base/cancel', GoalID, queue_size=1)
    
    #print(model.cameraInfo())

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        time.sleep(10)
        print('connexion')
        (clientConnected, clientAddress) = serverSocket.accept()
        try:
            dataFromClient = clientConnected.recv(9)
            print(dataFromClient)
    
            #dataFromServer = 'hello client.encode()
            #clientConnected.sendall(dataFromServer)
            data = dataFromClient.decode()
            print(data)
            #id = data.index(')')
            #data2 = data[:9 + 1]
            pixel_yolo = eval(data)
            print(type(pixel_yolo))
            print(pixel_yolo)
            print("pixel décodé")
            
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
        finally:
            clientConnected.close()

        
 

