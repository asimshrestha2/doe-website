import MySQLdb

class DBManager:

    #Query for logging in 
    loginQuery = r"""select * from user where '{}' = username and '{}' = password"""
    #Query for getting attendence
    eventAttendingQuery = r"""select * from event where event_id in (
                              select event_id from attendance where user_id = {})"""
    #Query for getting location
    locQuery = r"""select school_address, facility_name from school, facility where school.school_id = facility.school_id and school.school_id = 1 and facility_id = 2""" 

    #Query for registering
    registerQuery = "INSERT INTO user (user_id, name, email, phone_num, zip, user_type, username, password, user_address) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    #---in progress---
    #Query for getting names of some events perhaps to populate a list with a set amount of events
    populateEvents = "select event_name, facility_name" 
    
    def _init(self):
        pass

    def executeQuery(self, query): #pass the query in
        db = MySQLdb.connect() #populate this with connection information.  Hidden so can be on github

        if query:
            c=db.cursor() #db cursor used to iterate over records
            c.execute("""{}""".format(query))
            if(c.rowcount > 0): #if we have something to return inside our table
                return c.fetchall() #return all the rows in some array
        else:
            raise QueryError('Query Missing')

        c.close()
        db.close()

