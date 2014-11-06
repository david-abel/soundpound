# Hyperparameters

NUM_KEYPOINTS = 100 # per frame
NUM_FRAMES_PER_SLICE = 6 # number of frames per feature slice
SLICE_DELTA = 3 # number of frames to advance between slices (should be less than NUM_FRAMES_PER_SLICE)
SPATIAL_PYRAMID_FRACTIONS = [2, 3, 4] # spatial pooling for each l/2 x w/2, l/3 x w/3, and l/4 x w/r region

# Video Specific Information

OUT_DIR="output_videos/"

TEST_DATA_FEAT_DIR="cached_representations/"

TEST_VIDEO_FILE="output"
TEST_VIDEO_OPT_FLOW_FILE="output_optical_flow"
TEST_VIDEO_FEAT_FILE="test_vid"

HEIGHT = 720
WIDTH = 576

DRUMMER_ONE = "data/DVD-video/drummer_1/video/"
DRUMMER_TWO = "data/DVD-video/drummer_2/video/"
DRUMMER_THREE = "data/DVD-video/drummer_2/video/"
DRUMMERS={1:DRUMMER_ONE,2:DRUMMER_TWO,3:DRUMMER_THREE}

ANGLE_ONE = "angle_1/"
ANGLE_TWO = "angle_2/"
ANGLES={1:ANGLE_ONE,2:ANGLE_TWO}