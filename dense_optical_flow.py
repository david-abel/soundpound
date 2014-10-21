import cv2
import numpy as np
import sys
import namespace
import heapq
import pickle
from collections import defaultdict

def apply_optical_flow_to_video(video_file=namespace.TEST_VIDEO_FILE,output_file=namespace.TEST_VIDEO_OPT_FLOW_FILE):
    '''
    Args:
        video_file(String) [opt]: points to a video file to apply optical flow
        output_file(String) [opt]: the name of the output file to write to

    Notes:
        Takes as input a video file, and applies optical flow to each frame, and writes to file
    '''
    video_cap = cv2.VideoCapture(video_file)

    # Setup misc. objects
    ret, first_frame = video_cap.read()
    previous = cv2.cvtColor(first_frame,cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(first_frame)
    hsv[...,1] = 255

    # Create a filter to remove background noise (MOG without the 2 is also available)
    background_sub = cv2.BackgroundSubtractorMOG()

    # Define the codec and create VideoWriter object
    fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
    out = cv2.VideoWriter(namespace.OUT_DIR + output_file,fourcc, 20.0, (namespace.HEIGHT,namespace.WIDTH))

    # Loop over each frame, apply optical flow, save.
    _optical_flow_main_loop(video_cap, fourcc, out, previous, hsv, background_sub, output_file)


def _optical_flow_main_loop(video_cap, fourcc, out, previous, hsv, background_sub, output_file):
    '''
    Args:
        video_cap(cv2.VideoCapture): an object for reading each frame from the video
        fourcc(int): the codec for the video
        out(cv2.VideoWriter): an object for writing optical flow frames to file
        previous(numpy.ndarray): previous frame of the video
        hsv(numpy.ndarray): normalization matrix
        background_sub(cv2.BackgroundSubtractorMOG): an object for removing background noise from each frame
    '''

    # Stores a data structure of max keypoints per frame for each frame
    features = []

    # Loop over each frame
    while True:
        ret, next_frame = video_cap.read()

        if next_frame == None:
            # Reached the last frame
            break
        
        # Gets the next frame in proper color scheme.
        next = cv2.cvtColor(next_frame,cv2.COLOR_BGR2GRAY)

        # Remove background noise
        cleaned_frame = background_sub.apply(next)

        # Apply optical flow and normalization
        flow = cv2.calcOpticalFlowFarneback(previous,cleaned_frame,0.5,3,15,3,5,1.2,0)

        # If this frame contains no relevant keypoints, skip the frame
        if np.count_nonzero(flow) == 0:
            print "SKIPPING A FRAME"
            continue

        bag_of_max_optical_flow = find_max_keypoints(flow)
        features.append(bag_of_max_optical_flow)
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        hsv[...,0] = ang*180/np.pi/2
        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
        
        # Write the feature annotated frame
        out.write(rgb)

        # Set current frame to previous
        previous = cleaned_frame    

    save_feature_dict_to_file(features, output_file)

    video_cap.release()
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
    bag_of_max_optical_flow = defaultdict(_int_dict) # key is "col", then key is "row", then val is 0 or 1

    # Get the N largest optical flow keypoints
    max_rows, max_cols = nlargest_indices(flow_frame,namespace.NUM_KEYPOINTS)

    for x,y in zip(max_rows, max_cols):
        # print x, y
        bag_of_max_optical_flow[x][y] = 1

    return bag_of_max_optical_flow

def nlargest_indices(arr, n):
    '''
    Args:
        arr(numpy array): an array containing comparable data
        n(int): indicates the number of indices to return

    Returns:
        (A,B): where A and B contain the row and col respectively of the largest data points
    '''
    uniques = np.unique(arr)
    threshold = uniques[-n]
    a = np.where(arr >= threshold)
    return a[0], a[1]

def save_feature_dict_to_file(features, filename=namespace.TEST_VIDEO_FEAT_FILE):
    '''
    Args:
        features: a defaultdict containing the feature representation of an entire video
        filename (opt): the filename to save this feature dict to
    '''
    with open(namespace.FEATURE_CACHE + filename + ".pickle", 'wb') as handle:
        pickle.dump(features, handle)

def open_feature_dict_from_file(filename=namespace.TEST_VIDEO_FEAT_FILE):
    '''
    Args:
        filename (opt): the filename to load features from
    '''
    with open(filename, 'rb') as handle:
        data = pickle.load(handle)

    return data

def _int_dict():
    '''
    Notes: Used in place of lambda : defaultdict(int) so that we can pickle large defaultdicts

    Return:
        defaultdict(int)
    '''
    return defaultdict(int)

def main():
    if len(sys.argv) != 2:
        print "Usage: python dense_optical_flow.py <video_file>\n"
        quit()

    video_file = sys.argv[1]

    apply_optical_flow_to_video(video_file)


if __name__ == "__main__":
    main()