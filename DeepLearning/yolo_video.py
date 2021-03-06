import cv2
import numpy as np
import roslibpy

"""
Code implementing Yolov3 and openCV using the camera of the computer (webcam) to detect someone or using the stream
of the raspberry camera (for that use the cv2.VideoCapture with the link in the parentheses).
"""

# cap = cv2.VideoCapture('http://172.16.16.171:8080/?action=snapshot')
cap = cv2.VideoCapture(0)
classesFile = 'coco.names'
client = roslibpy.Ros(host='172.16.16.25', port=9090)
client.run()

talker = roslibpy.Topic(client, '/chatter', 'std_msgs/String')

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
    """
        Receives the data from the server, waits for the packet to be full then compares if it is equal to Enreg,
        which is the green light in case someone has already been identified.
        :param clientSocket: bytes
        :return: data: string
    """
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
    """
        This functionalities in the output array of YOLO algorithm, analyses the numbers to see whether or not there is a
        an interesting thing, identifies it, draws the bounding box around it and returns the center of this box.
        :param outputs: array from the YOLO CNN
        :param img: array
        :return: x,y: tuple representing the coordinates of the center of the bounding box
    """
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []
    for output in outputs:
        for det in output:
            scores = det[5:]  # Only gets the first 5 elements of the array: center (x,y), width, height and probability
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:  # Only consider if confidence is high enough
                if classNames[classId] == 'person':  # We only want to detect person
                    w, h = int(det[2] * wT), int(det[3] * hT)
                    x, y = int(det[0] * wT - w / 2), int(det[1] * hT - h / 2)
                    bbox.append([x, y, w, h])
                    classIds.append(classId)
                    confs.append(float(confidence))
    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nms_threshold)

    if classIds:
        box = bbox[0]
        x, y, w, h = box[0], box[1], box[2], box[3]
        # mask = np.zeros((hT, wT), np.uint8) --> this part was to create a black mask around the bounding box,
        # not to be influenced by the background
        # mask[y:(y + int(1 * h)), x:(x + int(1 * w))] = 255
        # masked_img = cv2.bitwise_and(img, img, mask=mask)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
        cv2.putText(img, f'{classNames[classIds[0]].upper()} {int(confs[0] * 100)}%', (x, y - 10),
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 0, 255), 2)  # Draw the rectangle
    else:
        x, y = -1, -1  # if nothing is detected, return (-1, -1)
    return x, y


while True:
    """
    While loop, curbed with the time 0.3 sleep if activated. 
    """
    # cap = cv2.VideoCapture('http://172.16.16.171:8080/?action=snapshot') --> activate if streaming the camera
    cap.set(3, 640)
    cap.set(4, 480)
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
    print('Sending message...')
    # time.sleep(0.3)

talker.unadvertise()

client.terminate()
