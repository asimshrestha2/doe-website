class School(User):
	def __init__(self, schoolID, name, address, zip):
		self.name = name
		self.schoolID = schoolID
		self.address = address
		self.zip = zip
		self.facilities = []
		self.rating = []
	
	def add_facility(self, facility):
		self.facilities.append(facility)
		
	def delete_facility(facility):
		self.facilities.remove(facility)
		
	def edit_facility(facility):