import cv2
import time
import numpy as np
import socket

# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# clientSocket.connect(('172.16.16.149', 8080))
# cap = cv2.VideoCapture('http://172.16.16.171:8080/?action=snapshot')
cap = cv2.VideoCapture(0)
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
        # mask = np.zeros((hT, wT), np.uint8)
        # mask[y:(y + int(1 * h)), x:(x + int(1 * w))] = 255
        # masked_img = cv2.bitwise_and(img, img, mask=mask)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
        cv2.putText(img, f'{classNames[classIds[0]].upper()} {int(confs[0] * 100)}%', (x, y - 10),
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 0, 255), 2)
        return x, y


while True:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('172.16.16.211', 8080))
    deb = time.time()
    # cap = cv2.VideoCapture('http://172.16.16.171:8080/?action=snapshot')
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
    try:
        clientSocket.send(data2.encode())
        print(recvall(clientSocket))
    finally:
        clientSocket.close()
    # clientSocket.close()
    # fin = time.time()
    # print(f'time per frame:{fin - deb}')
    # print(findObjects(outputs, img, i))
