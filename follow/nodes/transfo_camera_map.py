#!/usr/bin/env python

import rospy
import tf
import tf2_ros
import tf2_geometry_msgs

rospy.init_node("transfo_camera_map")

tfbuffer = tf2_ros.Buffer()
#listener = tf2_ros.TransformListener(tfbuffer)

tf1_listener = tf.TransformListener()

# give listeners time to receive required transforms
rospy.sleep(1.0)

# make Pose in the 'b' frame
p_b = tf2_geometry_msgs.tf2_geometry_msgs.PoseStamped()
p_b.header.frame_id = 'camera_link'
p_b.pose.position.y = 0.5
p_b.pose.orientation.w = 1.0

# Use tf2 to transform pose to the 'a' frame and print results. Best practice
# would wrap this in a try-except:
#t_a_b = tfbuffer.lookup_transform('frame_a', 'frame_b', rospy.Time.now(), rospy.Duration(1.0))
#p_a = tf2_geometry_msgs.do_transform_pose(p_b, t_a_b)
#rospy.loginfo("Pose expressed in 'frame_a' using tf2: \n%s\n", str(p_a))

# Use tf to transform pose to the 'a' frame and print results. Best practice
# would wrap this in a try-except:
p_a_tf1 = tf1_listener.transformPose('map', p_b)
rospy.loginfo("Pose expressed in 'map' using tf: \n%s\n", str(p_a_tf1))
