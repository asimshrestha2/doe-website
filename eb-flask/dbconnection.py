import MySQLdb

class DBManager:

    #Query for logging in 
    loginQuery = r"""select * from user where '{}' = username and '{}' = password;"""
    #Query for getting attendence
    eventAttendingQuery = r"""select * from event where event_id in (
                              select event_id from attendance where user_id = {});"""
    #Query for getting event location 
    locQuery = r"""select school_address, facility_name from school, facility where school.school_id = facility.school_id and school.school_id = {} and facility_id = {};""" 

    #Query for getting users (1 filter)
    selectUserQuery = r"""select * from user where username = '{}';"""

    #Query for getting basic upcoming event information for user
    selectUserEventQuery = r"""select event_id, event_name, description from event where host_id = {} and date >= curdate();"""
    #Query for registering
    registerQuery = r"""INSERT INTO user (name, email, phone_num, zip, user_type, username, password, user_address, user_rating)
                        VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {});"""

    #Query for getting detailed event information
    selectEventQueryD = r"""select * from event where event_id = {} and event_name = '{}';"""

    #Query for getting host of an event
    selectHostQuery = r"""select username from user where user_id={};"""
    
    #Query for getting user e-mail
    getUserEmailQuery = r"""select email from user where username = '{}';"""

    #Check if username already exists
    chkUsernameQuery = r"""select username from user where username = '{}';"""

    #Get school info
    schoolInfoQuery = r"""select * from school where school_id = {};"""

    #Get facility name
    selectFName = r"""select facility_name from facility where facility_id = {} and school_id = {};"""
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
            db.commit()
            if(c.rowcount > 0): #if we have something to return inside our table
                return c.fetchall() #return all the rows in some array
        else:
            raise QueryError('Query Missing')

        c.close()
        db.close()

