import cv2
import time
import numpy as np
import roslibpy

"""
This is the code implemented in the jetson nano
"""

GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, ' \
                     'framerate=21/1 ! nvvidconv flip-method=0 ! video/x-raw, width=640, height=480, ' \
                     'format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink ' \
                     'wait-on-eos=false max-buffers=1 drop=True '
client = roslibpy.Ros(host='172.16.16.25', port=9090)
client.run()
talker = roslibpy.Topic(client, '/chatter', 'std_msgs/String')
cap = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)

classesFile = 'coco.names'

whT = 320
confThreshold = 0.5
nms_threshold = 0.3

with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfiguration = 'yolov3-tiny.cfg'
modelWeights = 'yolov3-tiny.weights'
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
Enreg = False


def recvall (clientSocket):
    data = ''
    while True:
        packet = clientSocket.recv(16)
        packet = packet.decode()
        if not packet: break
        data += packet
        if data == 'Enreg':
            Enreg = True
    return data


def findObjects (outputs, img):
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                if classNames[classId] == 'person':
                    w, h = int(det[2] * wT), int(det[3] * hT)
                    x, y = int(det[0] * wT - w / 2), int(det[1] * hT - h / 2)
                    bbox.append([x, y, w, h])
                    classIds.append(classId)
                    confs.append(float(confidence))
    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nms_threshold)

    if classIds:
        box = bbox[0]
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
        cv2.putText(img, f'{classNames[classIds[0]].upper()} {int(confs[0] * 100)}%', (x, y - 10),
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 0, 255), 2)

    else:
        x, y = -1, -1
    return x, y


while True:
    deb = time.time()
    # cap = cv2.VideoCapture('http://172.16.16.171:8080/?action=snapshot')
    # cap.set(3, 640)
    # cap.set(4, 480)
    success, img = cap.read()
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], crop=False)
    net.setInput(blob)
    layerNames = net.getLayerNames()
    net.getUnconnectedOutLayers()
    outputNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(outputNames)
    findObjects(outputs, img)
    cv2.imshow('Image', img)
    cv2.waitKey(1)
    data = findObjects(outputs, img)
    data2 = str(data)
    talker.publish(roslibpy.Message({'data': data2}))
    print('send')
    time.sleep(0.3)

talk.unadvertise()
client.terminate()
