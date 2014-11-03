# Python Modules
import sys
from os import listdir
from os.path import isfile, join
from sklearn.neighbors import NearestNeighbors

# Soundpound Modules
from utils import *
# import utils
import namespace


def nearest_neighbor(src, others):
    pass

def distance(frames_src, frames_target):
    pass

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
    # if len(sys.argv) != 2:
    #     print "Usage: python classify.py <video_file>\n"
    #     quit()

    test_data = _load_test_set()
    
    # for item in test_data.values():
    #     print item
    print test_data.values()[0].features

if __name__ == "__main__":
    main()