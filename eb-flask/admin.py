class Admin(User):
	def __init__(self, userID):
		object.__setattr__(self, "userID", userID)
		object.__setattr__(self, "name", "admin")
	
	def __setattr__(self, *args):
		raise TypeError
		
    def __delattr__(self, *args):
        raise TypeError
	
	def ban_user(user):
		
	def ban_school(school):