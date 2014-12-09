# Python Modules
from scipy.io.wavfile import read, write
import sys
import numpy as np
import copy

# Soundpound modules
import namespace
import utils

# NOTE: sample rate is 44,100, so each SECOND is 44,100 samples.

def chop_sound_file(sound_file, start_frame, num_frames):
	'''
	Args:
		sound_file(str): points to the raw audio file to load
		start_sec(int): the second to start the chop
		num_secs(int): number of seconds to grab from the audio file

	Returns:
		(list): raw audio data containing the chopped audio
	'''
	# audio_in_seconds = _get_sound_file_in_seconds(sound_file)

	sample_rate, audio = read(sound_file)
	start_sec = start_frame / namespace.VIDEO_FPS
	num_secs = num_frames / namespace.VIDEO_FPS

	chopped_audio = audio[start_sec * sample_rate: (start_sec + num_secs) * sample_rate] # NOTE: make sure it doesn't overflow
	return chopped_audio
  
def write_sound_to_file(filename, raw_sound_data, sample_rate=namespace.AUDIO_SAMPLE_RATE):
	'''
	Args:
		filename(str): the name of the output audio file
		raw_sound_data(numpy array): the raw audio data (list of ints) to write to the file
		sample_rate(int) [opt]: sample_rate, default set in namespace (41000).
	'''
	write(filename, sample_rate, raw_sound_data)

def stitch_sound_files_together(*args):
	'''
	Args:
		*args(list of audio data (list of ints)): contains the audio data to stitch together

	Returns:
		(list): contains the raw_audio data of the provided audio all stitched together
	'''
	result = copy.deepcopy(args[0])

	for raw_audio in args[1:]:
		result = np.concatenate([result, raw_audio])

	return result

def _get_sound_file_from_video_file(video_file, drummer):
    '''
    Args:
        video_file(str): points to the video file of interest

    Returns:
        (str): the sound_file (relative from soundpound root directory) corresponding to the classified video_file
    '''
    audio_dir = namespace.DRUMMERS_AUDIO[drummer]

    # Replace the mp4 ending with wav
    sound_file = audio_dir + video_file.replace(".mp4",".wav")

    return sound_file

def audio_distance(sound_file_a, sound_file_b):
	'''
	Args:
		sound_file_a (list): wav file from source video
		sound_file_b (list): wav file from target video

	Returns:
		(int): indicates how dissimilar the two sound files are
	'''

def main():

	test_file = namespace.D1_AUDIO_DIR + "001_hits_snare-drum_sticks_x6.wav"

	# Create sub chops
	chopped_audio = chop_sound_file(test_file, 0,2*namespace.VIDEO_FPS) # Seconds time Video FPS
	chopped_audio_two = chop_sound_file(test_file, 0,2*namespace.VIDEO_FPS)

	utils.dprint((len(chopped_audio), len(chopped_audio_two)))

	# Stitch them together
	result = stitch_sound_files_together(chopped_audio_two, [])

	utils.dprint(len(result))

	# Write them out to a .wav
	write_sound_to_file(namespace.AUDIO_FILE_OUT, result)


if __name__ == "__main__":
	main()