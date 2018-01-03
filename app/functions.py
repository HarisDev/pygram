import datetime
from django.utils.dateformat import format
from django.db import connection

def returnName(first_name, last_name, username):

    display_name = ""

    if first_name == "":
        display_name = username
    else:
        display_name = first_name + " " + last_name

    return display_name

def ofonline(userid):
    timestamp_string = str(format(datetime.datetime.now(), u'U'))
    with connection.cursor() as c1:
        c1.execute("""
            SELECT last_seen FROM auth_user WHERE id = '""" + str(userid) + """'
        """)
        f = c1.fetchone()
        if not f:
            datex = 0
        else:
            datex = f[0]

    if int(datex)+60 > int(timestamp_string):
        return True
    else:
        return False

def seen_before(timestamp):

    if timestamp <= 3600:
        return str(int(timestamp/60)) + "m"
    elif timestamp > 3600 and timestamp < 86400:
        return str(int(timestamp/3600)) + "h"
    else:
        return "none"

