class FeaturePatch:

	def __init__(self, start_frame, num_frames, filename, features):
		self.start_frame = start_frame
		self.num_frames = num_frames
		self.filename = filename
		
		# list of dicts, where each list represents a frame, and in each dict, 
		# key is a Point, value is representation of optical flow
		self.features = self._condense_features(features)

	def __str__(self):
		return "FeaturePatch(" + self.filename + "." + str(self.start_frame) + "-" + str(self.start_frame + self.num_frames) + ")"

	def _condense_features(self, features):
	    '''
	    Notes:
	        Turns the feature for each frame from all keypoints to a consolidated representation (average, max, sum, etc)
	    '''
	    return self._sum_features(features)

	def _sum_features(self, features):
	    summed_feature_patches = []
	    for time_slice in features:
	    	summed_feature_patches.append(sum(time_slice.values()))

	    return summed_feature_patches