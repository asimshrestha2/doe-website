import MySQLdb

def executeQuery(query): #pass the query in
    db = MySQLdb.connect() #populate this with connection information.  Hidden so can be on github

    if query:
        c=db.cursor()
        c.execute("""{}""".format(query))
        if(c.rowcount > 0) #if we have something to return inside our table
        return c.fetchall()
    else:
        raise QueryError('Query Missing')

    c.close()
    db.close()

