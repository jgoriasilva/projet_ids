#!/usr/bin/env python3

import rospy
import yaml
from geometry_msgs.msg import Pose, Point, Quaternion
import threading as td

# from take_photo import TakePhoto
# from go_to_specific_point_on_map import GoToPose

def followroute:
    with open("/home/ubuntu/turtlebot/route.yaml", 'r') as stream:
        dataMap = yaml.load(stream)
    try:
        navigator = GoToPose()
        while not rospy.is_shutdown():
            for obj in dataMap:
                name = obj['filename']
                
                # Let the robot follow someone
                while(locked):
                    pass

                # Navigation
                rospy.loginfo("Following route to %s pose", name[:-4])
                navigator.goto(obj['position'], obj['quaternion'])

                if not success:
                    rospy.loginfo("Failed to reach %s pose", name[:-4])
                    continue
                rospy.loginfo("Reached %s pose", name[:-4])
                
                rospy.sleep(1)

def followperson:


if __name__ == '__main__':
    '''
    # Read information from yaml file
    with open("/home/ubuntu/turtlebot/route.yaml", 'r') as stream:
        dataMap = yaml.load(stream)

    try:
        # Initialize
        pub = rospy.Publisher('points', Pose, queue_size=10)
        rospy.init_node('follow_route', anonymous=False)
        #navigator = GoToPose()
        #camera = TakePhoto()
        
        while not rospy.is_shutdown():
            for obj in dataMap:
                
                name = obj['filename']
                    
                    p = Pose()
                    p.position.x = obj['position']['x']
                    p.position.y = obj['position']['y']
                    p.position.z = 0.0
                    p.orientation.x = obj['quaternion']['r1']
                    p.orientation.y = obj['quaternion']['r2']
                    p.orientation.z = obj['quaternion']['r3']
                    p.orientation.w = obj['quaternion']['r4']
                    
                # Navigation
                rospy.loginfo("Going to %s pose", name[:-4])
                navigator.goto(obj['position'], obj['quaternion'])


                if not success:
                    rospy.loginfo("Failed to reach %s pose", name[:-4])
                    continue
                rospy.loginfo("Reached %s pose", name[:-4])
            
                    # Take a photo
                    if camera.take_picture(name):
                        rospy.loginfo("Saved image " + name)
                    else:
                        rospy.loginfo("No images received")
            
                rospy.sleep(1)
    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")
    '''
    a
