import numpy as np
import cv2 
import cv2.aruco as aruco
import numpy as np
from Marker import *

#the source code is from lab 10
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
detectorParams = cv2.aruco.DetectorParameters_create()
detectorParams.adaptiveThreshConstant = 15
lB = 125
lG = 125
lR = 125
hB = 255
hG = 255
hR = 255
lH = 0
lS = 0
lV = 0
hH = 179
hS = 255
hV = 255
wb = 0
expo = 0
f = "trackbar_defaults.txt"
def detect(frame, draw = True):
    detected = cv2.aruco.detectMarkers(frame, dictionary, parameters=detectorParams)

    if draw:
        cv2.aruco.drawDetectedMarkers(frame, detected[0], detected[1])
    markers = parseMarkers(detected)
    #print(markers[0].corners)
    return markers

def center(markers,id):
    for marker in markers:
        if marker.id == id:
             sum_x = sum(marker.corners[:,0])/4
             sum_y = sum(marker.corners[:,1])/4
             #print("x", sum_x, "y", sum_y)
             return [sum_x, sum_y]
    return None

def main():
    #camera = cv2.VideoCapture(0)
    global lH, lS, lV, hH, hS, hV, wb, expo
    try:
        with open(f, "r") as file:
            lH, lS, lV, hH, hS, hV, wb, expo= file.readlines()
    except FileNotFoundError:
        print("file was not found")
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    camera.set(cv2.CAP_PROP_AUTO_WB, 0)
    while True:
        print(cv2.getBuildInformation())
        cap = cv2.VideoCapture(0, cv2.CAP_PROP_BACKEND)
        # if not cap.isOpened():
        # raise SystemError("could not open")
        retval = cv2.videoio_registry.getBackendName(cv2.CAP_PROP_EXPOSUREPROGRAM)

        print(retval, cap)  # getBackendName(cap))
        cap.set(cv2.CAP_PROP_EXPOSURE, -11)
        print(cap.get(cv2.CAP_PROP_BACKEND))

        #frame = threshold.main()
        ret, frame = camera.read()

        camera.set(cv2.CAP_PROP_EXPOSURE, int(expo))
        camera.set(cv2.CAP_PROP_WB_TEMPERATURE, int(wb))
        lowerLimits = np.array([int(lH), int(lS), int(lV)])
        upperLimits = np.array([int(hH),int(hS),int(hV)])
        markers = detect(frame)
        #cv2.imshow('markers', frame)
        center(markers, 0)
        marker_1 = center(markers, 1)
        marker_2 = center(markers, 2)
        marker_3 = center(markers, 3)
        marker_4 = center(markers, 4)

        #print(markers)
        #print(marker_1)

        if marker_1 is not None and marker_2 is not None and marker_3 is not None and marker_4 is not None:
            # taken from https://theailearner.com/tag/cv2-warpperspective/
            print(marker_1)
            width_1_2 = np.sqrt(((marker_1[0] - marker_2[0]) ** 2) + ((marker_1[1] - marker_2[1]) ** 2))
            width_3_4 = np.sqrt(((marker_3[0] - marker_4[0]) ** 2) + ((marker_3[1] - marker_4[1]) ** 2))
            max_width = max(int(width_1_2), int(width_3_4))

            height_1_3 = np.sqrt(((marker_1[0] - marker_3[0]) ** 2) + ((marker_1[1] - marker_3[1]) ** 2))
            height_2_4 = np.sqrt(((marker_2[0] - marker_4[0]) ** 2) + ((marker_2[1] - marker_4[1]) ** 2))
            max_height = max(int(height_1_3), int(height_2_4))
            inputs = np.float32([marker_1, marker_2, marker_3, marker_4])
            outputs = np.float32([[0,0],[0, max_width - 1],[max_height-1, max_width-1],[max_height - 1, 0]])
            transformed = cv2.getPerspectiveTransform(inputs, outputs)
            wrapped_frame = cv2.warpPerspective(frame, transformed,(max_height, max_width),flags=cv2.INTER_LINEAR)
            frame = cv2.cvtColor(wrapped_frame, cv2.COLOR_BGR2HSV)
            thresholded = cv2.inRange(wrapped_frame, lowerLimits, upperLimits)
            width = wrapped_frame.shape[0]
            height = wrapped_frame.shape[1]

            return wrapped_frame
        cv2.imshow("wrapped", frame)

        #cv2.imshow("thresholded", thresholded)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()

