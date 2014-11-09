# Python modules
import numpy as np
import pickle
from collections import defaultdict

# Soundpound modules
import namespace
from feature_patch import FeaturePatch

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "P(" + x + "," + y + ")"

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

def save_feature_obj_to_file(feature_patches, filename=namespace.TEST_VIDEO_FEAT_FILE):
    '''
    Args:
        features: a FeaturePatchs object containing the feature representation of an entire video
        filename (opt): the filename to save this feature dict to
    '''
    with open(namespace.TEST_DATA_FEAT_DIR + filename + ".pickle", 'wb') as handle:
        pickle.dump(feature_patches, handle)

def open_feature_obj_from_file(filename=namespace.TEST_VIDEO_FEAT_FILE):
    '''
    Args:
        filename (opt): the filename to load features from

    Returns:
        data(FeaturePatchs): contains the relevant feature information (and drummer ID, angle, etc.).
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

def dprint(debug_text):
    '''
    Args:
        debug_text(str): string to be printed if debug mode is on
    '''
    if namespace.DEBUG:
        print debug_text
