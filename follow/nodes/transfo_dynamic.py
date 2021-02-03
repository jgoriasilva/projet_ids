#!/usr/bin/env python  
import rospy
import math
import tf
from tf2_geometry_msgs import PoseStamped
from image_geometry import PinholeCameraModel

def PointFromPixel(pixel, frame):
    model = PinholeCameraModel()
    depth = 10000 #valeur arbitraire
    ray = model.projectPixelTo3dRay(tuple(pixel))
    ray_z = [el/ray[2] for el in ray]
    pt = [el*depth for el in ray_z]
    point = PointStamped()
    point.header.frame_id = frame
    point.point.x = pt[0]
    point.point.y = pt[1]
    point.point.z = pt[2]
    return point
        
     

if __name__ == '__main__':
    rospy.init_node('transfo_dynamic')

    listener = tf.TransformListener()

    #yolo_goal = rospy.Publisher('yolo_goal', PoseStamped, queue_size=10)
    yolo_goal = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            p_camera = PoseStamped()
            p_camera.header.frame_id = 'camera_link'
            p_camera.pose.position.y = 0.5
            p_camera.pose.position.y = 0.1
            p_camera.pose.position.z = 10
            p_camera.pose.orientation.w = 0
            now = rospy.Time.now()
            p_map = listener.transformPose('map', p_camera)
            #rospy.loginfo("Pose expressed in 'map' using tf: \n%s\n", str(p_map))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        yolo_goal.publish(p_map)

        rate.sleep()

