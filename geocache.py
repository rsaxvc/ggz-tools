class Geocache:
	def __init__(self):
		self.name=u""
		self.code=u""
		self.awesomeness = 3.0
		self.difficulty  = 3.0
		self.size        = 3.0
		self.terrain     = 3.0
		self.file_pos    = 0
		self.file_len    = 0
		self.lat         = 0.0
		self.lon         = 0.0
		self.type        = u""
		self.found_status = ""

	def __str__(self):
		return str(self.__dict__)

	def __eq__(self, other): 
		return self.__dict__ == other.__dict__



