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


