import MySQLdb

def executeQuery(query):
    db = MySQLdb.connect()

    if query:
        c=db.cursor()
        c.execute("""{}""".format(query))
        return c.fetchall()
    else:
        raise QueryError('Query Missing')

    c.close()
    db.close()
