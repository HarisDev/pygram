from django.http import JsonResponse
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from app.functions import *
from app.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.dateformat import format
import datetime
import pytz


@login_required

def SendMessage(request):

    poruka = request.POST.get('message', "null")
    id_conversation = str(request.POST.get('idconv', "null"))
    timestamp_string = str(format(datetime.datetime.now(), u'U'))
    logged_in = str(request.user.id)


    if poruka != "null":
        with connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO messages (id_conversation, id_sender, message, time_sent) VALUES (
            '""" + id_conversation + """',
            '""" + logged_in + """',
            '""" + str(poruka) + """',
            '""" + timestamp_string + """'
            )
        """)

        cursor.close()
    return HttpResponse(id_conversation)

def LoadConversations(request):

    logged_in = request.user.id

    timestamp_string = str(format(datetime.datetime.now(), u'U'))
    with connection.cursor() as c1:
        c1.execute(
            """
                UPDATE auth_user SET last_seen = '""" + str(timestamp_string)  + """'
                WHERE id = '""" + str(logged_in) + """' and
                last_seen+60 < '""" + str(timestamp_string) + """'
            """
        )
    c1.close()

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT sub.id, a1.username, a1.first_name, a1.last_name, a1.id, a1.avatar FROM 
          ( SELECT id,
            CASE WHEN c.id_first = '""" + str(logged_in) + """"' THEN id_second
                 WHEN c.id_second = '""" + str(logged_in) + """"' THEN id_first
            END AS other_id
            FROM conversations as c
          ) sub
        JOIN auth_user a1 ON a1.id = sub.other_id
        """)
        rezultat = cursor.fetchall()
        site = ""
        for red in rezultat:

            id = red[0]
            slika = str('/media/'+red[5])

            if ofonline(red[4]) == True:
                ofonlinex = "avatar-online"
            else:
                ofonlinex = "avatar-offline"

            username = red[1]
            first_name = red[2]
            last_name = red[3]
            display_name = returnName(first_name, last_name, username)

            with connection.cursor() as cursor1:
                cursor1.execute("""
                    SELECT message, time_sent FROM messages WHERE id_conversation = '""" + str(id) + """' ORDER BY id DESC 
                    LIMIT 1
                """)
                fetch = cursor1.fetchone()

                if not fetch:
                    # do nothing
                    lastmsg = ""
                    datex = ""
                else:
                    lastmsg = fetch[0]
                    tz = pytz.timezone("Europe/Sarajevo")
                    datex = str(datetime.datetime.fromtimestamp(fetch[1], tz).strftime("%H:%M"))

            cursor1.close()

            with connection.cursor() as cursor2:
                cursor2.execute("""
                    SELECT COUNT(*) FROM messages WHERE id_conversation = '""" + str(id) + """' 
                    and id_sender != '""" + str(logged_in) + """' and aread = '0'
                """)
                fetchx = cursor2.fetchone()

                if not fetchx or fetchx[0] == 0:
                    # do nothing
                    count = ""
                    unreadmsg = ""
                else:
                    unreadmsg = "unread-msg"
                    count = "<div class='unread'>" + str(fetchx[0]) + "</div>"

            cursor2.close()

            site += """
            <div onClick="chat.openChat('""" + str(id) + """');" class="row sideBar-body """ + unreadmsg + """ ">
                        <div class="col-sm-3 col-xs-3 sideBar-avatar">
                          <div class="avatar-icon">
                          """ + count + """
                          <div class='""" + ofonlinex + """'>&nbsp;</div>
                            <img src='""" + slika + """'>
                          </div>
                        </div>
                        <div class="col-sm-9 col-xs-9 sideBar-main">
                          <div class="row">
                            <div class="col-sm-8 col-xs-8 sideBar-name">
                              <span class="name-meta">"""
            site += display_name + """<br />
            <small>""" + lastmsg[:30] + """</small>
                            </span>
                            </div>
                            <div class="col-sm-4 col-xs-4 pull-right sideBar-time">
                              <span class="time-meta pull-right">""" + datex + """
                            </span>
                            </div>
                          </div>
                        </div>
                      </div>
            """
    cursor.close()

    return HttpResponse(site)

def LoadChat(request, chat_id):

    logged_in = request.user.id


    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT sub.other_id FROM 
          ( SELECT id,
            CASE WHEN c.id_first = '""" + str(logged_in) + """"' THEN id_second
                 WHEN c.id_second = '""" + str(logged_in) + """"' THEN id_first
            END AS other_id
            FROM conversations as c
            WHERE id = '""" + chat_id + """'
          ) sub
        JOIN auth_user a1 ON a1.id = sub.other_id
        """)
        rezultat = cursor.fetchone()
    other_id = rezultat[0]
    other_user = User.objects.get(id=other_id)


    with connection.cursor() as cx:
        cx.execute("""
            SELECT last_seen FROM auth_user WHERE id = '""" + str(other_id) + """'
        """)
        fetch = cx.fetchone()
        lastseen = fetch[0]

    username = other_user.username
    first_name = other_user.first_name
    last_name = other_user.last_name
    avatar  = str('/media/'+str(other_user.avatar))
    display_name = returnName(first_name, last_name, username)
    lasttimestamp = lastseen

    ispis = ""

    # Zaglavlje chat usera

    if ofonline(other_id) == True:
        status = """<i style="color:green;" class="fa fa-circle " aria-hidden="true"></i> <span style="color:green" >Online</span>"""
        lastactive = "Active now"
    else:
        status = """<i style="color:grey;" class="fa fa-circle " aria-hidden="true"></i> <span style="color:grey" >Offline</span>"""
        timestamp_string = int(format(datetime.datetime.now(), u'U'))-int(lasttimestamp)
        lastactive = "Active " + seen_before(timestamp_string) + " ago"

    ispis += """
    <div class="row heading chathead" id='""" + chat_id + """'>
            <div class="col-sm-2 col-md-1 col-xs-3 heading-avatar">
              <div class="heading-avatar-icon">
                <img src='""" + avatar + """'>
              </div>
            </div>
            <div class="col-sm-8 col-xs-7 heading-name">
              <a class="heading-name-meta">""" + display_name + """<br />
              </a>
              <small>&nbsp; """ + lastactive + """</small>
              
            </div>
            <div class="col-sm-1 col-xs-1  heading-dot pull-right">
              """ + status + """
            </div>
          </div>
    """

    ispis += """
    <div class="row message" id="conversation">
            <br />
            <br />
            <br />
            <br />
            <br />
              <center>
                  <img width="84" src='""" + static('images/reload.png') +  """' /><br />
                  <br />
                  <span style="color: #A1A1A1; font-family: 'Ubuntu', sans-serif;">Loading messages..</span>
              </center>
          </div>
    """
    return HttpResponse(ispis)





def LoadMessages(request, chat_id):

    with connection.cursor() as cursorx:
        cursorx.execute("""
            UPDATE messages SET aread = '1' 
            WHERE id_conversation = '""" + str(chat_id) + """' and
            id_sender != '""" + str(request.user.id) + """'
        """)
    cursorx.close()

    with connection.cursor() as cursor:
        cursor.execute("""
        
        
        select * from (
            select 
                messages.id,
                messages.message,
                messages.id_sender,
                messages.time_sent from messages 
                WHERE  id_conversation = '""" + chat_id + """' 
                order by id desc limit 5
        ) tmp order by tmp.id asc
        
        """)
        rezultat = cursor.fetchall()
        site = ""
        if not rezultat:
            site += """
                <center>
                    <br />
                    <br />
                    <img width="64" src=\"""" + static('images/waving-hand.png') +  """\" /><br />
                  <br />
                  <span style="color: #A1A1A1; font-family: 'Ubuntu', sans-serif;">There are no messages. Say hello!</span>
                </center>
            """
        for red in rezultat:

            id_poruke = red[0]
            poruka = red[1]
            id_sender = red[2]
            time_sent = red[3]
            tz = pytz.timezone("Europe/Sarajevo")
            time_fixed = str(datetime.datetime.fromtimestamp(time_sent, tz).strftime("%H:%M"))
            klase = ["", "", ""]
            other_user = User.objects.get(id=id_sender)
            if id_sender != request.user.id:

                klase[0] = "message-main-receiver"
                klase[1] = "message-avatar"
                klase[2] = "receiver"
            else:
                klase[0] = "message-main-sender"
                klase[1] = "hidden"
                klase[2] = "sender"

            avatar  = str('/media/' + str(other_user.avatar))

            site += """
            <br />
            <div class="row message-body" id='""" + str(id_poruke) + """'>
              <div class="col-sm-12 """ + klase[0] + """">
                <div class="heading-avatar-icon """ + klase[1] + """">
                    <img src='""" + avatar + """'>
                  </div>
                <div class='""" + klase[2] + """'>
                  <div class="message-text">
                   """ + poruka + """
                  </div>
                  <span class="message-time pull-right">
                    """ + time_fixed + """
                  </span>
                </div>
              </div>
            </div>"""

        cursor.close();
    return HttpResponse(site)

def GetNewMessages(request, chat_id, last_id):

    with connection.cursor() as cursorx:
        cursorx.execute("""
            UPDATE messages SET aread = '1' 
            WHERE id_conversation = '""" + str(chat_id) + """' and
            id_sender != '""" + str(request.user.id) + """' and
            aread = '0'
        """)
    cursorx.close()

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT
          messages.id,
          messages.message,
          messages.id_sender,
          messages.time_sent
          
        FROM messages
        WHERE id_conversation = '""" + chat_id + """' and id > '""" + last_id + """' 
        ORDER BY id 
        
        """)
        rezultat = cursor.fetchall()
        site = ""
        if len(rezultat) > 0:
            for red in rezultat:

                id_poruke = red[0]
                poruka = red[1]
                id_sender = red[2]
                time_sent = red[3]
                tz = pytz.timezone("Europe/Sarajevo")
                time_fixed = str(datetime.datetime.fromtimestamp(time_sent, tz).strftime("%H:%M"))
                klase = ["", "", ""]
                avatar = ""
                other_user = User.objects.get(id=id_sender)
                avatar  = str('/media/'+str(other_user.avatar))
                if id_sender != request.user.id:

                    klase[0] = "message-main-receiver"
                    klase[1] = "message-avatar"
                    klase[2] = "receiver"
                else:
                    klase[0] = "message-main-sender"
                    klase[1] = "hidden"
                    klase[2] = "sender"

                site += """
                
                <div class="row message-body" id='""" + str(id_poruke) + """'>
                  <div class="col-sm-12 """ + klase[0] + """">
                    <div class="heading-avatar-icon """ + klase[1] + """">
                        <img src='""" + avatar + """'>
                      </div>
                    <div class='""" + klase[2] + """'>
                      <div class="message-text">
                       """ + poruka + """
                      </div>
                      <span class="message-time pull-right">
                        """ + time_fixed + """
                      </span>
                    </div>
                  </div>
                </div>"""

        cursor.close();
    return HttpResponse(site)

def CreateConversation(request, receiver_id):

    logged_in = request.user.id
    timestamp_string = str(format(datetime.datetime.now(), u'U'))

    with connection.cursor() as cursor:

        cursor.execute("""
            INSERT INTO conversations (id_first, id_second, time_started) VALUES 
            ('""" + str(logged_in) + """', '""" + str(receiver_id) + """', '""" + str(timestamp_string) + """')
        """)
        returnid = cursor.lastrowid

    return HttpResponse(returnid)

def Search(request):
    text = request.POST.get("text", "none")
    site = ""
    with connection.cursor() as c1:
        c1.execute("""
            SELECT id, username, avatar FROM auth_user WHERE username LIKE '%""" + str(text) + """%' or 
            first_name LIKE '%""" + str(text) + """%' or last_name LIKE '%""" + str(text) + """%'
        """)
        redovi = c1.fetchall()

        site += """<div class="row" >"""
        for red in redovi:



            site += """     <div style="margin-bottom:15px;" class="col-md-4" id=\"add-""" + str(red[0]) + """\">"""
            site += """         <img style="width: 64px;margin-bottom:15px;" width="64" height="64" src=\"""" + '/media/' + str(red[2]) + """\" />"""
            site += """         <br />"""
            site += """         <span class='imesmall'>""" + str(red[1]) + """</span> <br /><br />"""
            site += """         <span onClick="friends.addFriend('""" + str(red[0]) + """');" style="font-size:9px; cursor:pointer;" class='imesmall addf'>Add Friend</span> """
            site += """     </div>"""

        site += "</div>"


    return HttpResponse(site)

def AddFriend(request, user_id):

    logged_in = request.user.id

    with connection.cursor() as c1:

        c1.execute("SELECT COUNT(*) FROM friends WHERE (id_first = '" + str(logged_in) + "' or id_second = '" + str(logged_in) + "') and (id_first = '" + str(user_id) + "' or id_second = '" + str(user_id) + "') ")

        re = c1.fetchone()

        if re[0] == 0:

            c1.execute("INSERT INTO friends (id_first, id_second, time_sent) VALUES ('" + str(logged_in) + "', '" + str(user_id) + "', '" + str(logged_in) + "')")



    return HttpResponse("ok")

def Accept(request, user_id):
    logged_in = request.user.id
    with connection.cursor() as c:
        c.execute("""
        UPDATE friends SET accepted = '1' WHERE 
        (id_first = '""" + str(user_id) + """' or id_second = '""" + str(user_id) + """') and
        (id_first = '""" + str(logged_in) + """' or id_second = '""" + str(logged_in) + """')
        """)

    return HttpResponse("accepted")

def Decline(request, user_id):
    logged_in = request.user.id
    with connection.cursor() as c:
        c.execute("""
            DELETE FROM friends WHERE 
            (id_first = '""" + str(user_id) + """' or id_second = '""" + str(user_id) + """') and
            (id_first = '""" + str(logged_in) + """' or id_second = '""" + str(logged_in) + """')
        """)

    return HttpResponse("declined")

def FriendRequests(request):

    logged_in = request.user.id

    with connection.cursor() as c1:

        c1.execute("SELECT COUNT(*) FROM friends WHERE (id_first = '" + str(logged_in) + "' or id_second = '" + str(logged_in) + "') and accepted = '0' and time_sent != '" + str(logged_in) + "'")

        re = c1.fetchone()
    if re:
        return HttpResponse(re)
    else:
        return HttpResponse("0")