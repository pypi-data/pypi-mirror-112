class FSUser:
	def __init__(self, user_id, attributes):
		self.user_id = str(user_id)
		self.attributes = attributes
	
	def add_attribute(self, key, value):
		if not key:
			return
		if not self.attributes:
			self.attributes = {}
		self.attributes[key] = value
