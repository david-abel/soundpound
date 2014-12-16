# Hyperparameters

NUM_KEYPOINTS = 100 # per frame
NUM_FRAMES_PER_SLICE = 25 # number of frames to advance per feature slice (24 means each slice will be 25 total) | 25 = each slice is 1 second of video.
SLICE_DELTA = 25 # number of frames to advance between slices

# Video Specific Information

DEBUG = True

# --- VIDEO PATHS ---
OUT_DIR = "output_videos/"

VIDEO_FILE_OUT = "output_final.mp4"
AUDIO_FILE_OUT = "output_audio.wav"

TEST_DATA_FEAT_DIR = "cached_representations/full_data_sum_feat/"

TEST_VIDEO_FILE = "output"
TEST_VIDEO_OPT_FLOW_FILE = "output_optical_flow"
TEST_VIDEO_FEAT_FILE = "test_vid"

_drumming_eval_dir="evaluation/drumming/"

EVAL_VID_A = _drumming_eval_dir + "001_hits_snare-drum_sticks_x6.mp4"
EVAL_AUDIO_A = _drumming_eval_dir + "001_hits_snare-drum_sticks_x6.wav"
EVAL_VID_B = _drumming_eval_dir + "010_hits_crash-cymbal_sticks_x5.mp4"
EVAL_AUDIO_B = _drumming_eval_dir + "010_hits_crash-cymbal_sticks_x5.wav"

EVAL_HARBAUGH = "evaluation/drumming/harbaugh.mp4"
EVAL_BALLMER = "evaluation/drumming/steve.mp4"


DRUMMER_ONE = "data/DVD-video/drummer_1/video/"
DRUMMER_TWO = "data/DVD-video/drummer_2/video/"
DRUMMER_THREE = "data/DVD-video/drummer_3/video/"
DRUMMERS = {1:DRUMMER_ONE,2:DRUMMER_TWO,3:DRUMMER_THREE}

ANGLE_ONE = "angle_1/"
ANGLE_TWO = "angle_2/" 
ANGLES = {1:ANGLE_ONE,2:ANGLE_TWO}

D1_AUDIO_DIR = "data/ENST-drums-public/drummer_1/audio/snare/"
D2_AUDIO_DIR = "data/ENST-drums-public/drummer_2/audio/snare/"
D3_AUDIO_DIR = "data/ENST-drums-public/drummer_3/audio/snare/"
DRUMMERS_AUDIO = {1:D1_AUDIO_DIR, 2:D2_AUDIO_DIR, 3:D3_AUDIO_DIR}


# -- VIDEO META INFO --
VIDEO_FPS = 25 # Videos are 25 fps.
HEIGHT = 720
WIDTH = 576
AUDIO_SAMPLE_RATE = 44100

START_DELIM="#"
END_DELIM="$"

# -- FEATURE + MISC. INFO --
FEATURES_ARE_VECTORS = False # Features are either Vectors or their Magnitudes
RANDOM_SELECTION = False
WEIGHTED_AVG_DIR = False

