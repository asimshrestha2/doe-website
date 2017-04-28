import MySQLdb

class DBManager:

    #Query for logging in 
    loginQuery = r"""select * from user where '{}' = username and '{}' = password"""
    
    #cusror.execute(loginQuery, (passwordparam,)) 
    #Query for getting names of some events perhaps to populate a list with a set amount of events
    #---in progress---
    populateEvents = "select event_name, facility_name" 
    #Query for registering
    registerQuery = "INSERT INTO user (user_id, name, email, phone_num, zip, user_type, username, password, user_address) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    def _init(self):
        pass

    def executeQuery(self, query): #pass the query in
        db = MySQLdb.connect() #populate this with connection information.  Hidden so can be on github

        if query:
            c=db.cursor()
            c.execute("""{}""".format(query))
            if(c.rowcount > 0): #if we have something to return inside our table
                return c.fetchall() #return all the rows in some array
        else:
            raise QueryError('Query Missing')

        c.close()
        db.close()

