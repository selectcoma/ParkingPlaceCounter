import cv2
import pickle
import cvzone
import numpy as np

width, height = 107, 48
#Video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('CatParkPos', 'rb') as f:
    pos_list = pickle.load(f)


def check_parking_space(image):
    free_count = 0
    for pos in pos_list:
        x, y = pos
        cropped = image[y:y+height, x:x+width]
        count = cv2.countNonZero(cropped)
        str_free = "Free: "
        if count < 900:
            free_count += 1
            color = (0, 255, 0)
            thickness = 5
        else:
            color = (0, 0, 255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 5),
                           scale=1, thickness=2, offset=0, colorR=color)
    cvzone.putTextRect(
        img, str_free + str(free_count),
        (30, 50), scale=3, thickness=3, offset=0, colorR=(0, 255, 0))


while True:
    #loop the video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imblur = cv2.GaussianBlur(imgray, (3, 3), 1)
    img_threshold = cv2.adaptiveThreshold(
        imblur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 25, 15)
    img_median = cv2.medianBlur(img_threshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)

    check_parking_space(img_dilate)
    # for pos in pos_list:
    #     cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 0, 255), 2)
    cv2.imshow('Image', img)
    cv2.waitKey(1)


