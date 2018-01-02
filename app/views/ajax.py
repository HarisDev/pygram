from django.http import JsonResponse
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from django.contrib.auth.models import User
from app.functions import *
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.dateformat import format
import datetime


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

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT sub.id, a1.username, a1.first_name, a1.last_name FROM 
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
            username = red[1]
            first_name = red[2]
            last_name = red[3]
            display_name = returnName(first_name, last_name, username)

            site += """
            <div onClick="chat.openChat('""" + str(id) + """');" class="row sideBar-body">
                        <div class="col-sm-3 col-xs-3 sideBar-avatar">
                          <div class="avatar-icon">
                            <img src="https://bootdey.com/img/Content/avatar/avatar1.png">
                          </div>
                        </div>
                        <div class="col-sm-9 col-xs-9 sideBar-main">
                          <div class="row">
                            <div class="col-sm-8 col-xs-8 sideBar-name">
                              <span class="name-meta">"""
            site += display_name + """
                            </span>
                            </div>
                            <div class="col-sm-4 col-xs-4 pull-right sideBar-time">
                              <span class="time-meta pull-right">18:18
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

    try:
        other_user = User.objects.get(id=rezultat[0])
    except  User.DoesNotExist:
        print("No user")

    username = other_user.username
    first_name = other_user.first_name
    last_name = other_user.last_name
    display_name = returnName(first_name, last_name, username)

    ispis = ""

    # Zaglavlje chat usera

    ispis += """
    <div class="row heading chathead" id='""" + chat_id + """'>
            <div class="col-sm-2 col-md-1 col-xs-3 heading-avatar">
              <div class="heading-avatar-icon">
                <img src="https://bootdey.com/img/Content/avatar/avatar6.png">
              </div>
            </div>
            <div class="col-sm-8 col-xs-7 heading-name">
              <a class="heading-name-meta">""" + display_name + """
              </a>
            </div>
            <div class="col-sm-1 col-xs-1  heading-dot pull-right">
              <i class="fa fa-circle " aria-hidden="true"></i> Online
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
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT
          messages.id,
          messages.message,
          messages.id_sender
          
        FROM messages
        WHERE id_conversation = '""" + chat_id + """' 
        ORDER BY time_sent
        """)
        rezultat = cursor.fetchall()
        site = ""
        for red in rezultat:

            id_poruke = red[0]
            poruka = red[1]
            id_sender = red[2]
            klase = ["", "", ""]

            if id_sender != request.user.id:
                try:
                    other_user = User.objects.get(id=id_sender)
                except  User.DoesNotExist:
                    print("No user")
                klase[0] = "message-main-receiver"
                klase[1] = "message-avatar"
                klase[2] = "receiver"
            else:
                klase[0] = "message-main-sender"
                klase[1] = "hidden"
                klase[2] = "sender"

            site += """
            <br />
            <div class="row message-body" id='""" + str(id_poruke) + """'>
              <div class="col-sm-12 """ + klase[0] + """">
                <div class="heading-avatar-icon """ + klase[1] + """">
                    <img src="https://bootdey.com/img/Content/avatar/avatar6.png">
                  </div>
                <div class='""" + klase[2] + """'>
                  <div class="message-text">
                   """ + poruka + """
                  </div>
                  <span class="message-time pull-right">
                    Sun
                  </span>
                </div>
              </div>
            </div>"""

        cursor.close();
    return HttpResponse(site)

def GetNewMessages(request, chat_id, last_id):

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT
          messages.id,
          messages.message,
          messages.id_sender
          
        FROM messages
        WHERE id_conversation = '""" + chat_id + """' and id > '""" + last_id + """' 
        ORDER BY time_sent
        """)
        rezultat = cursor.fetchall()
        site = ""
        if len(rezultat) > 0:
            for red in rezultat:

                id_poruke = red[0]
                poruka = red[1]
                id_sender = red[2]
                klase = ["", "", ""]

                if id_sender != request.user.id:
                    try:
                        other_user = User.objects.get(id=id_sender)
                    except  User.DoesNotExist:
                        print("No user")
                    klase[0] = "message-main-receiver"
                    klase[1] = "message-avatar"
                    klase[2] = "receiver"
                else:
                    klase[0] = "message-main-sender"
                    klase[1] = "hidden"
                    klase[2] = "sender"

                site += """
                <br />
                <div class="row message-body" id='""" + str(id_poruke) + """'>
                  <div class="col-sm-12 """ + klase[0] + """">
                    <div class="heading-avatar-icon """ + klase[1] + """">
                        <img src="https://bootdey.com/img/Content/avatar/avatar6.png">
                      </div>
                    <div class='""" + klase[2] + """'>
                      <div class="message-text">
                       """ + poruka + """
                      </div>
                      <span class="message-time pull-right">
                        Sun
                      </span>
                    </div>
                  </div>
                </div>"""

        cursor.close();
    return HttpResponse(site)
