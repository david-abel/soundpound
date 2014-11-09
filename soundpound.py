# Soundpound | David Abel

# Python Modules
import sys
import subprocess as sp

# Soundpound Modules
import classify
import dense_optical_flow
import audio_utils
import namespace
import utils

def main():
    if len(sys.argv) != 2:
        print "Usage: python classify.py <video_file>\n"
        quit()

    # Break source video into patches
    input_video = sys.argv[1]

    utils.dprint("Featurizing input...")

    # Featurize input and find best matches in the dataset
    input_feature_patches = dense_optical_flow.get_feature_patches_from_video(input_video)
    matched_feature_patches = classify.get_nearest_neighbors(input_feature_patches)

    utils.dprint("Finding matches...")

    # Get all matched sound files, chop them according to the match, then put them in order
    soundfiles_to_stitch = []
    for match in matched_feature_patches:
        # Get full sound file
        next_sound_file = audio_utils._get_sound_file_from_video_file(match.filename, match.drummer)

        # Get subset of audio from the matched FeaturePatch
        next_sound_file_chopped = audio_utils.chop_sound_file(next_sound_file, match.start_frame, match.num_frames)
        raw_sound_to_stitch[index].append(next_sound_file)

    utils.dprint("Reticulating spleens...")

    # Stitch matched sound_files together
    final_sound = audio_utils.stitch_sound_files_together(soundfiles_to_stitch)

    # Write to file (TO BE REPLACED BY SMASHING INTO VIDEO)
    audio_utils.write_sound_to_file(namespace.AUDIO_FILE_OUT, final_sound)

    # Call the command to add the stitched audio to the video
    command = ["ffmpeg", "-i", namespace.AUDIO_FILE_OUT, "-i", input_video, namespace.VIDEO_FILE_OUT]
    sp.call(command)


if __name__ == "__main__":
    main()