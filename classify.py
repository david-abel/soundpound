# Python Modules
import sys
import math
from os import listdir
from os.path import isfile, join
from sklearn.neighbors import NearestNeighbors

# Soundpound Modules
import utils
import dense_optical_flow
import namespace


def get_nearest_neighbors(input_feature_patches):
    test_data = _load_test_set()

    i = 0
    for fp in test_data.values():
        if type(fp) == list:
            i += 1

    utils.dprint("Finished loading dataset...")

    best_matches = []

    # For each temporal patch of features (FeaturePatch) in the source video, find a nearest neighbor
    for feature_patch in input_feature_patches:
        best_matches.append(_nearest_neighbor(feature_patch, test_data.values()))
        utils.dprint("Finished another patch")
    utils.dprint("Done.")

    return best_matches

def _nearest_neighbor(src, neighbors):
    '''
    Args:
        FeaturePatch: describes a patch from the source video
        neighbors(list of list of FeaturePatch): contains the entire dataset broken into patches

    Returns:
        FeaturePatch: contains the best FeaturePatch match from the neighbors for the given FeaturePatch in the src
    '''

    best_distance = sys.float_info.max
    best_patch = None

    # Find the best match
    for possible_match in neighbors:
        cur_dist = distance(src, possible_match)
        # Update best
        if cur_dist < best_distance:
            best_distance = cur_dist
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
    if type(frames_target) == list:
        utils.dprint("FOUND A LIST IN DISTANCE")
        return sys.float_info.max

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
        all_feature_dicts[pickle_file_name] = utils.open_feature_obj_from_file(join(test_data_dir,pickle_file_name))

    return all_feature_dicts

def main():
    if len(sys.argv) != 2:
        print "Usage: python classify.py <video_file>\n"
        quit()

    # Break source video into patches
    source_video = sys.argv[1]
    source_video_feature_patches = dense_optical_flow.get_feature_patches_from_video(source_video)

    print "Finished preprocessing input video..."

    # Load test data from pickled files into FeaturePatch objects
    test_data = _load_test_set()

    print "Finished loading dataset..."

    best_matches = []

    # For each temporal patch of features (FeaturePatch) in the source video, find a nearest neighbor
    for feature_patch in source_video_feature_patches:
        best_matches.append(_nearest_neighbor(feature_patch, test_data.values()))
        print "Finished another patch"
    print "Done."

    print "Best matches:",
    for match in best_matches:
        print match,


if __name__ == "__main__":
    main()