import dbconnection

#instantiate DBManager
db = dbconnection.DBManager()

def getfeaturedevent():
    feres = db.executeQuery("select * from event where event_id in (select event_id from featured_events) and date >= curdate()")
    fe = None if feres is None else feres
    events = []
    if fe:
        for result in fe:
            schoolres = db.executeQuery("select school_id, school_name, school_address from school where school_id=" + str(result[3]) + ";")
            school = {'school_name':"Location Not Found"} if schoolres is None else {'school_id': schoolres[0][0],
                    'school_name':schoolres[0][1], 'school_address':schoolres[0][2]}
            event = {'id': result[0], 'name': result[1], 'school': school, 'event_type': result[9],
                'host': result[4], 'time_start': result[5], 'description': result[11],
                'event_price': result[10], 'pictureUrl': 'https://asimshrestha2.github.io/imgs/content/environment.png' }
            events.append(event)
    return events
