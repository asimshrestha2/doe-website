from flask import url_for
from event import Event

#class for regular users
class User:
    name = ""
    title = "Public"
    rating = 0
    pictureUrl = ""
    events = []

    def serialize(self):
        serializedEvents = []
        for event in self.events:
                serializedEvents.append(event.serialize())
        return {
            'name':self.name,
            'title':self.title,
            'rating':self.rating,
            'pictureUrl':self.pictureUrl,
            'events': serializedEvents,
        }

    def __init__ (self, name, title, rating, pictureUrl, events):
        self.name = name
        self.title = title
        self.rating = rating
        self.pictureUrl = pictureUrl
        if(len(events) > 0):
            self.events = events
