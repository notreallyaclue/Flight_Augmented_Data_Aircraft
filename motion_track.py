# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size") #Change value of Defalt to change threshold
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    vs = VideoStream(src=0).start() #get from webcam
    time.sleep(1.0)

# otherwise, we are reading from a video file
else:
    vs = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
Previous_Frame = None


#### Initialise variables

Call = 'Getting Information'
Alt = 'Getting Information'
Spd = 'Getting Information'
Op = 'Getting Information'
Mdl = 'Getting Information'
Lat = 'Getting Information'
Long = 'Getting Information'

####


# loop over the frames of the video
while True:
    #### open text file and update variables
    f = open('filename.txt', 'r')
    message = f.readlines()
    if len(message) >= 1:
        Call = str(message[0])
        Alt = str(message[1])
        Spd = str(message[2])
        Op = str(message[3])
        Mdl = str(message[4])
        Lat = str(message[5])
        Long = str(message[6])
    f.close()
    ####

    # grab the current frame and initialize the occupied/unoccupied
    # text
    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=750)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current_frame = gray
    gray = cv2.GaussianBlur(gray, (25, 25), 0)

    # if the previous frame is None, initialize it
    #This is the reference frame for movement
    if Previous_Frame is None:
        Previous_Frame = gray
        continue



    # compute the absolute difference between the current frame and
    # previous frame


    frameDelta = cv2.absdiff(Previous_Frame, gray)
    thresh = cv2.threshold(frameDelta, 30, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)



        #Add extra information
        y = y-5
        cv2.putText(frame, Mdl, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        y = y - 20 #places on new line
        cv2.putText(frame, ('Altitude: ' + Alt), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        y = y - 20
        cv2.putText(frame, ('Speed: ' + Spd), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        y = y - 20
        cv2.putText(frame, ('Operator: ' + Op), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        y = y - 20
        cv2.putText(frame, ('Call Sign: ' + Call), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        #####to here

    Previous_Frame = current_frame #updates the frame to be ompared with. Next loop it will compare with this frame, which will then be the previous frame

    # show the frames, The Thresh and Frame Delta can be used to tweak settings. then can be commented out once done
    cv2.imshow("Live Camera With Overlay", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()