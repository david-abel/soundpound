class FeaturePatch:

	def __init__(self, drummer, angle, start_frame, features):
		self.drummer = drummer
		self.angle = angle
		self.start_frame = start_frame
		
		# list of dicts, where each list represents a frame, and in each dict, 
		# key is a Point, value is representation of optical flow
		self.features = self._condense_features(features)

	def __str__(self):
		return "d:" + str(self.drummer) + "." + str(self.angle) + " f:" + str(self.start_frame)

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