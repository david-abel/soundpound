# Hyperparameters

NUM_KEYPOINTS = 5 # per frame
NUM_FRAMES_PER_SLICE = 6 # number of frames per feature slice
SLICE_DELTA = 3 # number of frames to advance between slices (should be less than NUM_FRAMES_PER_SLICE)

# Video Specific Information

OUT_DIR="output_videos/"

FEATURE_CACHE="cached_representations/"

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