# Python Modules
from scipy.io.wavfile import read, write

# Soundpound modules
import utils
import namespace
import soundpound
import audio_utils

def main():

	# Run pipeline with eval video as input
	result_audio = soundpound.soundpound_pipeline(namespace.EVAL_VID_A)

	# Get ground truth sound
	sample_rate, ground_truth_audio = read(namespace.EVAL_AUDIO_A)

	# 2 Compute distance between original sound and the stitched sound
	error = audio_utils.audio_mean_squared_error(result_audio, ground_truth_audio)

	print "Mean Squared Error: ", error

if __name__ == "__main__":
	main()