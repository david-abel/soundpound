# Python Modules
from scipy.io.wavfile import read, write
import argparse
import sys

# Soundpound modules
import utils
import namespace
import soundpound
import audio_utils

def main():

    # Setup command line arguments
    parser = argparse.ArgumentParser(description='Specify a particular file for Soundpounding.')
    parser.add_argument("-r", "--random", help="use random features", action="store_true")
    parser.add_argument("-d", "--datasetsize", type=int, help="specify the number of segments to use in the data set")
    args = parser.parse_args()

    # Randomize features if specified
    if args.random:
        namespace.RANDOM_SELECTION = True
    
    if args.datasetsize:
        data_set_size = args.datasetsize
    else:
        data_set_size = sys.maxint

    # Run pipeline with eval video as input
    result_audio = soundpound.soundpound_pipeline(namespace.EVAL_VID_A, num_segments_to_load=data_set_size)

    # Get ground truth sound
    sample_rate, ground_truth_audio = read(namespace.EVAL_AUDIO_A)

    # 2 Compute distance between original sound and the stitched sound
    # mean_squared_error = audio_utils.mean_squared_error(result_audio, ground_truth_audio)
    # total_temporal_error = audio_utils.total_temporal_error(result_audio, ground_truth_audio)
    mean_temporal_error = audio_utils.mean_temporal_error(result_audio, ground_truth_audio)

    # print "Mean Squared Error: ", mean_squared_error
    # print "Temporal Error: ", total_temporal_error
    print "Mean Segment Temporal Error: ", mean_temporal_error

if __name__ == "__main__":
    main()