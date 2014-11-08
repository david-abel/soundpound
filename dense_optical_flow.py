# Python modules
import cv2
import numpy as np
import sys
import math
import heapq
import pickle
from collections import defaultdict

# Soundpound modules
import utils
import namespace
from feature_patch import FeaturePatch

def apply_optical_flow_to_video(video_file, save_video=False, output_file=namespace.TEST_VIDEO_FEAT_FILE):
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
    
    # Only write to file if instructed by parameters
    out = None
    if save_video:
        out = cv2.VideoWriter(namespace.OUT_DIR + output_file,fourcc, 20.0, (namespace.HEIGHT,namespace.WIDTH))

    # Loop over each frame, apply optical flow, save.
    features = _optical_flow_main_loop(video_cap, fourcc, out, previous, hsv, background_sub, output_file)

    return features

def _optical_flow_main_loop(video_cap, fourcc, out, previous, hsv, background_sub, output_file):
    '''
    Args:
        video_cap(cv2.VideoCapture): an object for reading each frame from the video
        fourcc(int): the codec for the video
        out(cv2.VideoWriter): an object for writing optical flow frames to file
        previous(numpy.ndarray): previous frame of the video
        hsv(numpy.ndarray): normalization matrix
        background_sub(cv2.BackgroundSubtractorMOG): an object for removing background noise from each frame
        output_file(str): a string pointing to the file to write

    Returns:
        features(list): contains all the features for each frame of the video (features[i] is the features at frame i)
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
            # SKIPPING FRAME: typically happens once per video?
            continue

        bag_of_max_optical_flow = find_max_keypoints(flow)
        features.append(bag_of_max_optical_flow)
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        hsv[...,0] = ang*180/np.pi/2
        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
        
        if out != None:
            # Write the feature annotated frame
            out.write(rgb)

        # Set current frame to previous
        previous = cleaned_frame    

    if out != None:
        out.release()

    video_cap.release()
    cv2.destroyAllWindows()
    
    return features

def slice_features_into_patches(features, output_file=namespace.TEST_VIDEO_FEAT_FILE, drummer=None, angle=None, save=False):
    '''
    Args:
        features(list): contains the feature representation of a slice of video
        output_file(str) [opt]: name of the file to save
        drummer(int) [opt]: the drummer number (1-3)
        angle(int) [opt]: the angle number (1-2)
        save(bool) [opt]: dictates whether or not you should save

    Returns:
        list: contains all the FeaturePatches objects for this video (representing the temporal feature patches)
    '''
    prefix = str(drummer) + "." + str(angle) + "."
    
    # If we're processing the test video
    if drummer == None:
        prefix = "testVid."

    all_feature_patches = []

    for start_frame in range(0, len(features) - namespace.NUM_FRAMES_PER_SLICE, namespace.SLICE_DELTA):
        
        # Loop over namespace.NUM_FRAMES_PER_SLICE of frames and create a FeaturePatch object to store the feature
        # representation of all those frames
        patches_over_time = []
        for delta in range(0, namespace.NUM_FRAMES_PER_SLICE):
            feature_slice = features[start_frame + delta]
            patches_over_time.append(feature_slice)
        feature_patch = FeaturePatch(start_frame, namespace.NUM_FRAMES_PER_SLICE, output_file, patches_over_time) # Now FeaturePatch stores a list "features", that itself contains features over time

        if save:
            utils.save_feature_obj_to_file(feature_patch, prefix + str(start_frame) + "_" + output_file)

        all_feature_patches.append(feature_patch) # Contains a list of Feature Patches.
    

    return all_feature_patches

def find_max_keypoints(flow_frame):
    '''
    Args:
        flow_frame(numpy.ndarray): an array containing the optical flow data for the n-th frame of a video

    Returns:
        defaultdict(int): A bag of words containing a 1 at the col,row for the max optical flow keypoitns
    '''
    # Store max optical flow keypoints per frame
    bag_of_max_optical_flow = defaultdict(int) # key is a Point, and the value is 0 or 1

    # Get the N largest optical flow keypoints
    max_rows, max_cols = utils.nlargest_indices(flow_frame,namespace.NUM_KEYPOINTS)

    # Full whatever
    # max_rows = range(0,len(flow_frame))
    # max_cols = range(0,len(flow_frame[0]))

    for x,y in zip(max_rows, max_cols):
        p = utils.Point(x,y)
        # NOTE: flow_frame[x][y] is a VECTOR of the dir of the keypoint from prev frame

        # BY MAGNITUDE
        magnitude = math.sqrt(flow_frame[x][y][0]**2 + flow_frame[x][y][1]**2)
        bag_of_max_optical_flow[p] = magnitude

        # BY BINARY
        # bag_of_max_optical_flow[p] = 1

    return bag_of_max_optical_flow


def main():
    if len(sys.argv) != 2:
        print "Usage: python dense_optical_flow.py <video_file>\n"
        quit()

    video_file = sys.argv[1]

    features = apply_optical_flow_to_video(video_file, True)

    feature_patches = slice_features_into_patches(features)

    _save_feature_patches(feature_patches)


if __name__ == "__main__":
    main()