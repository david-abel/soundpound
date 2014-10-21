import dense_optical_flow
import namespace
import sys
import random
from os import listdir
from os.path import isfile, join


def process_n_drummers(n=sys.float_info, random_sample=False):
	# For each drummer, for each angle, run optical flow on each video.
	for drummer in namespace.DRUMMERS.values():
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
				if num_videos > n:
					continue
				print "starting video: " + video_dir + video
				output_file = "OUT_" + video
				dense_optical_flow.apply_optical_flow_to_video(video_dir + video, output_file)
				num_videos += 1

def main():
	process_n_drummers(2,True)	


if __name__ == "__main__":
	main()