import cv2
import time
import numpy as np
from code_id_pers import identification, different, comparaison, boxing
import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('172.16.16.149', 8080))
Enreg = False

# cap = cv2.VideoCapture('http://172.16.16.171:8080/?action=snapshot')
cap = cv2.VideoCapture(0)
classesFile = 'coco.names'
classNames = []
whT = 320
confThreshold = 0.5
nms_threshold = 0.3
liste = []
liste_dim = []
liste_image = []
liste_pers = []
liste_im_ret = []
intermediaryHist = []
intermediaryImage = []

with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfiguration = 'yolov3.cfg'
modelWeights = 'yolov3.weights'
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


def findObjects (outputs, img):
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    res = []
    confs = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int(det[0] * wT - w / 2), int(det[1] * hT - h / 2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))
                res = [w, h, x, y]
    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nms_threshold)

    if classIds:
        box = bbox[0]
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
        cv2.putText(img, f'{classNames[classIds[0]].upper()} {int(confs[0] * 100)}%', (x, y - 10),
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 0, 255), 2)
    return res


while True:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('172.16.16.149', 8080))
    #data = clientSocket.recv(256)
    #if data != b'':
        #Enreg = True
    deb = time.time()
    # cap = cv2.VideoCapture('http://172.16.16.171:8080/?action=snapshot')
    success, img = cap.read()
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], crop=False)
    net.setInput(blob)
    layerNames = net.getLayerNames()
    net.getUnconnectedOutLayers()
    outputNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(outputNames)
    res = findObjects(outputs, img)
    if res:
        boxing(res, img, liste_pers, liste_image, intermediaryHist, intermediaryImage, clientSocket)
        cv2.imshow('frame', img)
    cv2.waitKey(1)
    fin = time.time()
    #print(f'time per frame:{fin - deb}')
