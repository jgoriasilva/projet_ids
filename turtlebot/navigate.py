#!/usr/bin/env python3

import rospy
import yaml
from geometry_msgs.msg import Pose, Point, Quaternion
import threading as td

# from take_photo import TakePhoto
from go_to_specific_point_on_map import GoToPose


def followroute(lock, navigator):
    with open("/home/ubuntu/project_ids/turtlebot/route.yaml", 'r') as stream:
        dataMap = yaml.load(stream)
    try:        
        i = 0
        while not rospy.is_shutdown():
            obj = dataMap[i]
            name = obj['filename']
               
            # Let the robot follow someone
            while(lock.Locked()):
                pass

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
                continue
            
            rospy.sleep(1)
    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")

def followperson(data, args):
    # args[0] is lock, args[1] is navigator

    args[0].acquire(blocking=False)
    
    # follow someone
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
        # yolo_goal.publish(p_map)
        success = navigator.goto(p_map.pose.position, p_map.pose.orientation)
        rate.sleep()

    elif pixel_yolo == None:
        pass

    else :
        #cancel_msg = GoalID()
        #cancel_pub.publish(cancel_msg)

        # even if it's called shutdown, should just cancel actual goal without shuting down the system
        navigator.shutdown()
    
    # quand il arrive à la personne...
    # envoyer information via serveur pour executer security4.py

    args[0].release()



if __name__ == '__main__':
    
    lock = td.Lock()
    navigator = GoToPose()

    td_route = td.Thread(target=followroute, args=(lock, navigator))
    td_person = td.Thread(target=followperson, args = (lock, navigator))

    td_route.start()
    td_person.start()

    rospy.init_node('test_communication')

    model = PinholeCameraModel()
    model.fromCameraInfo(cam_info)
    

    listener = tf.TransformListener()

    rate = rospy.Rate(10.0)
    try:
        while not rospy.is_shutdown():
            yolo_subscriber = rospy.Subscriber("/chatter", std_msgs.msg.String, callback=followperson, callback_args=(lock, navigator), queue_size = 10)

    except KeyboardInterrupt:
        td_route.join()
        td_person.join()
