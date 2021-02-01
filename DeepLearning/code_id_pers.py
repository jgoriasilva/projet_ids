import numpy as np
import cv2
import socket
import time

#clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#clientSocket.connect(('172.16.16.149', 8080))

def boxing (res, img, liste_pers, liste_image, liste_im_ret, hist_intermediaire, image_intermediaire, clientSocket):
    newImage = np.copy(img)
    w, h, x, y = res[0], res[1], res[2], res[3]
    top_y = y - h // 2
    btm_y = y + h // 2
    top_x = x - w // 2
    btm_x = x + w // 2
    A = newImage[top_y:btm_y, top_x + h // 4:btm_x - h // 4]
    dim = (btm_y - top_y - 10) * (btm_x - top_x - 2 * h // 4)
    stop_top = newImage.shape[0] - btm_y
    stop_btm = top_y
    Enreg = False
    print(w*h)
    if Enreg:
        liste_pers.append(hist_intermediaire)
        liste_im_ret.append(image_intermediaire)

        Enreg = False
        hist_intermediaire = []
        image_intermediaire = []

        histR = 400 / dim * cv2.calcHist([A], [0], None, [256], [0, 256])
        histG = 400 / dim * cv2.calcHist([A], [1], None, [256], [0, 256])
        histB = 400 / dim * cv2.calcHist([A], [2], None, [256], [0, 256])

        liste_pers.append([histB, histG, histR])
        liste_im_ret.append(A)

        # Enreg = False
        #print('dedans')

    elif w*h > 9000:
        histR = 400 / dim * cv2.calcHist([A], [0], None, [256], [0, 256])
        histG = 400 / dim * cv2.calcHist([A], [1], None, [256], [0, 256])
        histB = 400 / dim * cv2.calcHist([A], [2], None, [256], [0, 256])

        l = [histR, histG, histB]

        proceed = identification(l, liste_pers)
        if proceed and stop_top < 30 and stop_btm < 30:
            envoyer(str(-1, -1), clientSocket)
            if not hist_intermediaire:
                hist_intermediaire.append(histR)
                hist_intermediaire.append(histG)
                hist_intermediaire.append(histB)
                image_intermediaire = A
        elif proceed:
            centre = str((x, y))
            envoyer(centre, clientSocket)


def comparaison (l1, l2):
    somme = 0
    for x, y in zip(l1, l2):
        z = np.abs(x - y)
        for e in z[10:-10]:
            somme += e[0]
    return somme / 3 / 230


def different (l1, l2):
    if comparaison(l1, l2) < 1.6:
        return True
    return False


def identification (l1, liste_pers):
    if not liste_pers:
        return True

    for x in liste_pers:
        if different(x, l1):
            return False

    return True


def envoyer(t, clientSocket):
    clientSocket.send(t.encode())
    print(t)
