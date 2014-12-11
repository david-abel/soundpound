# Python modules
import sys
import random
from os import listdir
from os.path import isfile, join

# Soundpound modules
import namespace
import dense_optical_flow


def process_n_drummer_videos(n=sys.maxint, random_sample=False):
    '''
    Notes: Loops through the dataset and extracts features for each relevant slice in each video and
    caches the result in cached_representations.

    Args:
        n(int) [opt]: specifies the number of videos to grab per drummer, per angle.
        random_sample(bool) [opt]: if true, we randomly sample from the space of videos.
    '''
    # For each drummer, for each angle, run optical flow on each video.
    drummer_num = 1
    for drummer in namespace.DRUMMERS.values():
        angle_num = 1
        for angle in namespace.ANGLES.values():
            # Get the video files assocaited with this drummer/camera angle
            video_dir = drummer + angle
            video_files = [f for f in listdir(video_dir) if isfile(join(video_dir,f))]

            # If we want to get a random subset
            if random_sample:
                random.shuffle(video_files)

            num_videos = 0

            # Loop over the files, only process n of them
            for video in video_files:
                
                print "starting video: " + video_dir + video

                # Format the output file name 
                output_file = namespace.START_DELIM + "OUT_" + str(drummer_num) + "." + str(angle_num) + namespace.END_DELIM + video

                # Apply optical flow and save feature representation
                features = dense_optical_flow.apply_optical_flow_to_video(video_dir + video, output_file)

                # Takes the features and splits it into patches, saves each patch w/ pickle.
                feature_patches = dense_optical_flow.slice_features_into_patches(features, output_file, drummer_num, angle_num, save=True)

                # If we've processed enough files, quit.
                num_videos += 1
                if num_videos == n:
                    break

            angle_num += 1
        drummer_num += 1

def main():
    process_n_drummer_videos(1, True)   


if __name__ == "__main__":
    main()