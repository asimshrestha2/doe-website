import MySQLdb
#Data access object
class DatabaseManager:

    #Query for logging in 
    loginQuery = "select username from user where %s = password";
    
    #cusror.execute(loginQuery, (passwordparam,)) 
    #Query for getting names of some events perhaps to populate a list with a set amount of events
    #---in progress---
    populateEvents = "select" 
    #Query for registering
    registerQuery = "INSERT INTO user (user_id, name, email, phone_num, zip, user_type, username, password, user_address) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    def _init(self):
        pass
    
    def executeQuery(query):3
        #Parameters(hostname, username, password, dbname)
        db = MySQLdb.connect()

    if query:
        c=db.cursor()
        c.execute("""{}""".format(query))
        return c.fetchall()
    else:
        raise QueryError('Query Missing')

    c.close()
    db.close()

