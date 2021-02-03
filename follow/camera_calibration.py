#!/usr/bin/env python
import rospy
import math
import tf
import socket
from tf2_geometry_msgs import PoseStamped
from image_geometry import PinholeCameraModel
from actionlib_msgs.msg import GoalID
import sensor_msgs.msg
import time

print(1)
model = PinholeCameraModel()
cam_info = sensor_msgs.msg.CameraInfo()
cam_info.width = 640
cam_info.height = 480
cam_info.D = [0.1639958233797625, -0.271840030972792, 0.001055841660100477, -0.00166555973740089, 0.0]
cam_info.K = [322.0704122808738, 0.0, 199.2680620421962, 0.0, 320.8673986158544, 155.2533082600705, 0.0, 0.0, 1.0]
cam_info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
cam_info. P = [329.2483825683594, 0.0, 198.4101510452074, 0.0, 0.0, 329.1044006347656, 155.5057121208347, 0.0, 0.0, 0.0, 1.0, 0.0]

model.fromCameraInfo(cam_info)
print(model.distortionCoeffs())
print(model.intrinsicMatrix())

print('a')

def PointFromPixel(pixel, camera_model, depth=1000):
    print('à')
    ray = model.projectPixelTo3dRay(pixel)
    ray_z = [el/ray[2] for el in ray]
    pt = [el*depth for el in ray_z]
    print('b')
    return pt

pixel1 = (11,34)
point = PointFromPixel(pixel1, model)
print(point)