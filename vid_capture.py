import numpy as np
import cv2
import cv
import namespace

cap = cv2.VideoCapture(0)
cap.set(3,namespace.HEIGHT)
cap.set(4,namespace.WIDTH)

# Define the codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
out = cv2.VideoWriter('output',fourcc, 20.0, (namespace.HEIGHT,namespace.WIDTH))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
