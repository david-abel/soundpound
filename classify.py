# Python Modules
import sys
import math
from os import listdir
from os.path import isfile, join
from sklearn.neighbors import NearestNeighbors

# Soundpound Modules
from utils import *
import dense_optical_flow
import namespace


def nearest_neighbor(src, neighbors):
    '''
    Args:
        FeaturePatch: describes a patch from the source video
        neighbors(list of list of FeaturePatch): contains the entire dataset broken into patches

    Returns:
        list of FeaturePatch: contains the best FeaturePatch match from the neighbors for the given FeaturePatch in the src
    '''

    best_distance = sys.float_info.max
    best_patch = None

    # Find the best match
    for possible_match in neighbors:
        cur_dist = distance(src, possible_match)
        # Update best
        if cur_dist < best_distance:
            best_distance = cur_dist
            print "UPDATING:", cur_dist
            best_patch = possible_match

    return best_patch

def distance(frames_src, frames_target):
    '''
    Args:
        frames_src(FeaturePatch): a single FeaturePatch from the source video
        frames_target(FeaturePatch): a single FeaturePatch from a target video from the database

    Returns:
        int: the distance between the given FeaturePatch in optical flow space
    '''

    # print len(frames_src.features), len(frames_target.features)

    dist = 0
    for i in range(len(frames_target.features)):
        dist += (frames_src.features[i] - frames_target.features[i])**2
    return dist


def _load_test_set():
    '''
    Returns:
        dict: contains the feature representation for each slice of each video, where key=filename, val=feature dict.
    '''
    # Get all pickled files
    test_data_dir = namespace.TEST_DATA_FEAT_DIR
    all_pickle_files = [f for f in listdir(test_data_dir) if isfile(join(test_data_dir,f))]

    # Store each feature dict (represents set of namespace.NUM_FRAMES_PER_SLICE frames) with filename as the key
    all_feature_dicts = {}
    for pickle_file_name in all_pickle_files:
        if "DS_Store" in pickle_file_name:
            # Ignore silly Mac thing..
            continue
        all_feature_dicts[pickle_file_name] = open_feature_obj_from_file(join(test_data_dir,pickle_file_name))

    return all_feature_dicts


def main():
    if len(sys.argv) != 2:
        print "Usage: python classify.py <video_file>\n"
        quit()

    # Break source video into patches
    source_video = sys.argv[1]
    source_video_features = dense_optical_flow.apply_optical_flow_to_video(source_video, True)
    source_video_feature_patches = dense_optical_flow.slice_features_into_patches(source_video_features)

    print "Finished preprocessing input video..."

    # Load test data from pickled files into FeaturePatch objects
    test_data = _load_test_set()


    print "Finished loading dataset..."

    best_matches = []

    # For each temporal patch of features (FeaturePatch) in the source video, find a nearest neighbor
    for feature_patch in source_video_feature_patches:
        best_matches.append(nearest_neighbor(feature_patch, test_data.values()))
        print "Finished another patch"
    print "Done."

    print "Best matches:",
    for match in best_matches:
        print match,


if __name__ == "__main__":
    main()