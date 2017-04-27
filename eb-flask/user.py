from flask import Flask

class User
    'Class for Regular Users with information and basic operations'
	userID = 0000001
    name = "None" #display name
	email = "" #email address where notifications/verfications/etc. will be sent
	phone = 0000000000 #phone number
	zip = 00000 #zip code
	usertype = "User"
    rating = 0 #rating of user as a customer
    pictureURL = https://asimshrestha2.github.io/portfoliov2/imgs/Asim_Ymi #url of picture for user profile

    def __init__(self, userID, name, email, phone, zip, usertype):
		self.userID = userID
        self.name = name
		self.email = email
		self.phone = phone
		self.zip = zip
		self.usertype = usertype
		self.rating = []
		self.events = []
		
    def join_event(event):
		event.create_ticket(self)
		event.add_user(self)
		events.append(event)
		
	def leave_event(event):
		event.remove_user(self)
		events.remove(event)
		
	def share(event, media_platform, commments):
	
	def rate(user, rating)
		user.rating.append(rating)
	
	def create_event:
		
	def edit_event(event):