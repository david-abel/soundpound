# Python modules
import math
import numpy

# Soundpound modules
import namespace

class FeaturePatch:

    def __init__(self, start_frame, num_frames, filename, features, drummer, angle):
        self.start_frame = start_frame
        self.num_frames = num_frames
        self.filename = filename
        self.drummer = drummer
        self.angle = angle
        
        # list of dicts, where each list represents a frame, and in each dict, 
        # key is a Point, value is SOME representation of optical flow
        self.features = self._condense_features(features)

    def __str__(self):
        return "FeaturePatch(" + self.filename + "." + str(self.start_frame) + "-" + str(self.start_frame + self.num_frames) + ")"

    def _condense_features(self, features):
        '''
        Notes:
            Turns the feature for each frame from all keypoints to a consolidated representation (average, max, sum, etc)
        '''

        if namespace.FEATURES_ARE_VECTORS:
            # VECTORS
            return self._max_amplitude_direction(features)
        else:
            # MAGNITUDES
            # return self._sum_features(features)
            return self._avg_features(features)

    def _sum_features(self, features):
        summed_feature_patches = []
        for time_slice in features:
            summed_feature_patches.append(sum(time_slice.values()))

        return summed_feature_patches

    def _avg_features(self, features):
        avged_feature_patches = []
        for time_slice in features:
            avged_feature_patches.append(float(sum(time_slice.values()) / len(time_slice.values())))

        return avged_feature_patches

    def _max_features(self, features):
        max_feature_patches = []
        for time_slice in features:
            max_feature_patches.append(max(time_slice.values()))

        return max_feature_patches

    def _max_amplitude_direction(self, features):
        # NOTE: assumes features are VECTORS, not AMPLITUDES
        max_dirs = []
        
        for time_slice in features:
            max_amp = 0
            max_amp_theta = 0 # Angle from 0 (like unit circle)

            for opt_flow in time_slice.values():
                magnitude = math.sqrt((opt_flow[0] + opt_flow[1])**2)
                if magnitude > max_amp:
                    max_amp = magnitude
                    max_amp_theta = math.atan2(opt_flow[1], opt_flow[0])
                    print max_amp_theta
            max_dirs.append(max_amp_theta)

        return max_dirs
