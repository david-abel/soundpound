# Python Modules
from scipy.io.wavfile import read, write
import sys
import numpy as np
import copy

# Soundpound modules
import namespace

# NOTE: sample rate is 44,100, so each SECOND is 44,100 samples.

def chop_sound_file(sound_file, start_sec, num_secs):
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

def stitch_sound_files_together(sound_file, *args):
	'''
	Args:
		*args(list of audio data (list of ints)): contains the audio data to stitch together

	Returns:
		(list): contains the raw_audio data of the provided audio all stitched together
	'''
	result = copy.deepcopy(sound_file)

	for raw_audio in args:
		result = np.concatenate([result, raw_audio])

	return result

def main():

	test_file = namespace.D1_AUDIO_DIR + "001_hits_snare-drum_sticks_x6.wav"

	# Create sub chops
	chopped_audio = chop_sound_file(test_file, 0,5)
	chopped_audio_two = chop_sound_file(test_file, 5,5)

	# Stitch them together
	result = stitch_sound_files_together(chopped_audio, chopped_audio_two)

	# Write them out to a .wav
	write_sound_to_file(namespace.AUDIO_FILE_OUT, result)


if __name__ == "__main__":
	main()