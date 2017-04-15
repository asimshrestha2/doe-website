import MySQLdb

def executeQuery(query):
    if query:
        c=db.cursor()
        c.execute("""{}""".format(query))
        return c.fetchall()
    else:
        raise QueryError('Query Missing')
