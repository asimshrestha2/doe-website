from flask import Flask, url_for

class Event:
    name = ""
    description = ""
    pictureUrl = ""
    location = ""
    host = "" #URL TO PROFILE

    def serialize(self):
        return {
            'name':self.name,
            'description':self.description,
            'pictureUrl':self.pictureUrl,
            'location': self.location,
            'host': self.host,
        }
    
    def __init__ (self, name, description, pictureUrl, location, host):
        self.name = name
        self.description = description
        self.pictureUrl = pictureUrl
        self.location = location
        self.host = url_for('user', name = None)


    
