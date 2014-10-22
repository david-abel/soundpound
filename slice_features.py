class SliceFeatures:

	def __init__(self, drummer, angle, start_frame, features):
		self.drummer = drummer
		self.angle = angle
		self.start_frame = start_frame
		self.features = features # dict where key is a Point, value is 0 or 1 (if feature active there).

	def __str__(self):
		return "d:" + str(self.drummer) + "." + str(self.angle) + " f:" + str(self.start_frame)