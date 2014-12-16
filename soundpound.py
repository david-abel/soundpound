# Soundpound | David Abel

# Python Modules
import sys
import subprocess as sp
import numpy as np
import argparse

# Soundpound Modules
import classify
import dense_optical_flow
import audio_utils
import namespace
import utils

def soundpound_pipeline(input_video, stitch_sound=True, num_segments_to_load=sys.maxint):
    '''
    Args:
        input_video (str): filename of input video to run system on
        stitch_sound (bool) [opt]: indicates if we should stitch the sound to the output video file

    Returns:
        (list): the sound file resulting from running soundpound
    '''
    # Featurize input and find best matches in the dataset
    utils.dprint("Featurizing input...")
    input_feature_patches = dense_optical_flow.get_feature_patches_from_video(input_video)

    # Find nearest neighbors
    utils.dprint("Finding best matches...")
    matched_feature_patches = classify.get_nearest_neighbors(input_feature_patches, input_video, num_segments_to_load)

    if len(matched_feature_patches) == 0:
        print "No matches found. Quitting."
        quit()


    # Get all matched sound files, chop them according to the match, then put them in order
    utils.dprint("Processing media...")
    final_sound = []
    first_check = True
    for match in matched_feature_patches:

        # Make sure we've processed some DATA
        if match == None:
            print "Make sure data has been preprocessed (is the dir cached_representations/ empty? Try running pre_process_data.py"
            quit()

        # Get full sound file
        next_sound_file = audio_utils._get_sound_file_from_video_file(match.filename, match.drummer)

        # Remove uneccessary info from file name:
        preamble_start = next_sound_file.index(namespace.START_DELIM)
        preamble_end = next_sound_file.index(namespace.END_DELIM)
        next_sound_file = next_sound_file[:preamble_start] + next_sound_file[preamble_end + 1:]

        # Get subset of audio from the matched FeaturePatch and stitch together
        next_sound_file_chopped = audio_utils.chop_sound_file(next_sound_file, match.start_frame, match.num_frames)
        
        if first_check:
            final_sound = audio_utils.stitch_sound_files_together(next_sound_file_chopped, final_sound)
            first_check = False
        else:
            final_sound = audio_utils.stitch_sound_files_together(final_sound, next_sound_file_chopped)

    if stitch_sound:
        _sound_helper(input_video, final_sound)

    return final_sound

def _sound_helper(input_video, final_sound):

    utils.dprint("Reticulating spleens... " + str(len(final_sound)))

    # Write to file
    audio_utils.write_sound_to_file(namespace.AUDIO_FILE_OUT, final_sound)

    # Call the command to add the stitched audio to the video
    stitch_command = ["ffmpeg", "-i", namespace.AUDIO_FILE_OUT, "-i", input_video, namespace.VIDEO_FILE_OUT]
    sp.call(stitch_command)

    # Open the file
    open_command = ["open", namespace.VIDEO_FILE_OUT]
    sp.call(open_command)

def main():
    # Get video file
    parser = argparse.ArgumentParser(description='Specify a particular file for Soundpounding.')
    parser.add_argument("-j", "--jim", help="use Jim Harbaugh video",
                    action="store_true")
    parser.add_argument("-s", "--steve", help="use Jim Harbaugh video",
                    action="store_true")
    args = parser.parse_args()

    if args.jim:
        # HARBAUGH
        # Adjust camera params (TODO: do this automatically)
        namespace.HEIGHT = 640
        namespace.WIDTH = 360
        input_video = namespace.EVAL_HARBAUGH
    elif args.steve:
        # BALLMER

        # Adjust camera params
        namespace.HEIGHT = 320
        namespace.WIDTH = 240
        namespace.VIDEO_FPS = 30
        input_video = namespace.EVAL_BALLMER
    else:
        # Regular output file
        input_video = namespace.TEST_VIDEO_FILE

    # Run full pipeline
    soundpound_pipeline(input_video)
    


if __name__ == "__main__":
    main()