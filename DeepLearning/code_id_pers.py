import numpy as np
import cv2
import socket
import time


def boxing(res, img, list_pers, list_saved_im, intermediaryHist, intermediaryImage, clientSocket):
    """choose what to do with the input image : save it, send it or nothing

    res : list of characteristics from the yolo's object's detection
    img : image captured by the camera
    list_pers : list of histograms that characterise the already identified persons
    list_saved_im : list of the photos of the already identified persons
    intermediaryHist : list of the RGB histograms that characterize the person who is being identified
    intermediaryImage : image of the person who is being identified
    clientSocket : connection's object to ROS
    """

    newImage = np.copy(img)
    w, h, x, y = res[0], res[1], res[2], res[3]  # width, length, centre_x and centre_y of the box
    top_y = y - h // 2
    btm_y = y + h // 2
    top_x = x - w // 2
    btm_x = x + w // 2

    A = newImage[top_y:btm_y, top_x + h // 4:btm_x - h // 4]  # selection of the new image of work
    dim = (btm_y - top_y - 10) * (btm_x - top_x - 2 * h // 4)
    stop_top = newImage.shape[0] - btm_y
    stop_btm = top_y

    saving = False  # The server's signal to save someone characteristics

    if saving:
        list_pers.append(intermediaryHist)
        list_saved_im.append(intermediaryImage)

        # Reset of the parameters of capture

        saving = False
        intermediaryHist = []
        intermediaryImage = []

    elif w * h > 9000:  # Only if the box is big enough

        histR = 400 / dim * cv2.calcHist([A], [0], None, [256], [0, 256])
        histG = 400 / dim * cv2.calcHist([A], [1], None, [256], [0, 256])
        histB = 400 / dim * cv2.calcHist([A], [2], None, [256], [0, 256])
        char = [histR, histG, histB]

        proceed = identification(char, list_pers)  # Check if the person has already been identified

        if proceed and stop_top < 30 and stop_btm < 30:
            # The person has not been identified, and it is close enough
            # for the robot to stop

            send(str((-1, -1)), clientSocket)

            if not hist_intermediaire:
                # check if the robot has already begin to identify someone, on a previous call to boxing

                intermediaryHist.append(histR)
                intermediaryHist.append(histG)
                intermediaryHist.append(histB)
                intermediaryImage = A

        elif proceed:
            # Send the coordinates of the centre of the box. ROS will convert this into coordinates

            centre = str((x, y))
            send(centre, clientSocket)


def compare(l1, l2):
    """compare two persons, by sump up the absolut difference between there RGB histograms

    l1, l2 : list of three histograms each
    """

    somme = 0
    for x, y in zip(l1, l2):
        z = np.abs(x - y)
        for e in z[10:-10]:
            somme += e[0]

    return somme / 3 / 230  # /690 is just to have the difference's mean on a special color tone


def different(l1, l2):
    """ return whether or not the lists l1 and l2 represent the same person

    l1, l2 : list of three histograms each
    """

    if compare(l1, l2) < 1.6:
        # the 1.6 is an empirical parameter
        return True

    return False


def identification(l1, list_pers):
    """check if the person represented by l1 has already been identified,
    that is to say if its histograms are already in list_pers

    l1 : list of the histograms of the recognise person
    list_pers : list of each identified persons, each person being represented by its histograms
    """

    if not list_pers:
        # The robot needs to identify the first person it sees
        return True

    for x in list_pers:
        if different(x, l1):
            # if l1 looks like one the person, than l1 doesn't need to be identified
            return False

    return True


def send(data, clientSocket):
    """ send the data to the ROS server

    data : string of a tuple of two figures
    clientSocket : communication's object of the Socket module
    """
    clientSocket.send(data.encode())
