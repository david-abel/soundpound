import cv2
import numpy as np
import sys
import namespace
import heapq
from collections import defaultdict

def apply_optical_flow_to_video(video_file):
    '''
    Args:
        video_file(String): points to a video file to apply optical flow
    '''
    cap = cv2.VideoCapture(video_file)

    # Setup misc. parameters
    ret, frame1 = cap.read()
    prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[...,1] = 255

    # Create a filter to remove background noise (MOG without the 2 is also available)
    fgbg = cv2.BackgroundSubtractorMOG()

    # Define the codec and create VideoWriter object
    fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
    out = cv2.VideoWriter('output_optical_flow',fourcc, 20.0, (namespace.HEIGHT,namespace.WIDTH))

    # Stores a data structure of max keypoints per frame for each frame
    features = []

    i = 1
    while(1):
        print i
        i += 1
        ret, frame2 = cap.read()

        if frame2 == None:
            # Reached the last frame
            break
        
        # Gets the next frame in proper color scheme.
        next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

        # Removed background
        cleaned = fgbg.apply(next)

        flow = cv2.calcOpticalFlowFarneback(prvs,cleaned,0.5,3,15,3,5,1.2,0)
        bag_of_max_optical_flow = find_max_keypoints(flow)
        features.append(bag_of_max_optical_flow)

        features.append(bag_of_max_optical_flow)

        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        hsv[...,0] = ang*180/np.pi/2
        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
        
        # cv2.imshow('frame2',rgb)

        # write the feature annotated frame
        out.write(rgb)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        elif k == ord('s'):
            cv2.imwrite('opticalfb.png',frame2)
            cv2.imwrite('opticalhsv.png',rgb)
        prvs = cleaned    

    for frame in features:
        print frame

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def find_max_keypoints(flow_frame):
    '''
    Args:
        flow_frame(numpy.ndarray): an array containing the optical flow data for the n-th frame of a video

    Returns:
        defaultdict(lambda: defaultdict(int)): A bag of words containing a 1 at the col,row for the max optical flow keypoitns
    '''
    # Store max optical flow keypoints per frame
    bag_of_max_optical_flow = defaultdict(lambda: defaultdict(int)) # key is "col", then key is "row", then val is 0 or 1

    # Get the N largest optical flow keypoints
    max_rows, max_cols = nlargest_indices(flow_frame,20)

    for x,y in zip(max_rows, max_cols):
        bag_of_max_optical_flow[x][y] = 1

    return bag_of_max_optical_flow

def nlargest_indices(arr, n):
    uniques = np.unique(arr)
    threshold = uniques[-n]
    a = np.where(arr >= threshold)
    return a[0], a[1]

def main():
    if len(sys.argv) != 2:
        print "Usage: python dense_optical_flow.py <video_file>\n"
        quit()

    video_file = sys.argv[1]

    apply_optical_flow_to_video(video_file)



if __name__ == "__main__":
    main()