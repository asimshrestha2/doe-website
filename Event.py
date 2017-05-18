from flask import Flask, url_for, 

class Event:
    name = ""
    description = ""
    pictureURL = ""
    location = ""
    host = "" #URL TO PROFILE

    def __init__ (self, name, description, pictureURL, location, host):
        self.name = name
        self.description = description
        self.pictureURL = pictureURL
        self.location = location
        self.host = url_for('user', name = None)


    
