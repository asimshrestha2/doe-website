import dbconnection
import time

#instantiate DBManager
db = dbconnection.DBManager()

#[{'date':'8/4/2016', 'events':[{'title': "Event No. 1", 'discription': "This is something"},
#{'title': "Event No. 2", 'discription': "This is something"},
#{'title': "Event No. 3", 'discription': "This is something"}]},
#{'date':'9/4/2016', 'events':[{'title': "Event No. 1", 'discription': "This is something"},
#{'title': "Event No. 2", 'discription': "This is something"},
#{'title': "Event No. 3", 'discription': "This is something"}]},
#{'date':'10/4/2016', 'events':[]},
#{'date':'11/4/2016', 'events':[{'title': "Event No. 1", 'discription': "This is something"},
#{'title': "Event No. 2", 'discription': "This is something"}]}]

def getweekevents():
    day = int(time.strftime("%d"))
    month = int(time.strftime("%m"))
    year = int(time.strftime("%Y"))
    dates = __getDatesForWeek(day, month, year)
    wevents = []
    for date in dates:
        events = []
        rlt = db.executeQuery("SELECT * FROM event WHERE date='{}'".format(date))
        if rlt:
            rlt = list(rlt)
            for row in rlt:
                events.append({'title':row[1],'discription':row[11]})
            wevents.append({'date':date, 'events':events})
    return wevents

def __getDatesForWeek(day, month, year):
    dates = []
    for i in range(0, 6):
        #print(i)
        dates.append("{}-{}-{}".format(year, month, (day + i)))
    return dates
