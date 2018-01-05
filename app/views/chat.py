from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from app.functions import *

@login_required

def chat(request):
    logged_in = request.user.id
    friends_list = ""
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT a1.id, a1.username, a1.first_name, a1.last_name, a1.avatar FROM 
          ( SELECT 
            CASE WHEN c.id_first = '""" + str(logged_in) + """"' THEN id_second
                 WHEN c.id_second = '""" + str(logged_in) + """"' THEN id_first
            END AS other_id
            FROM friends as c
            WHERE c.accepted = '1'
          ) sub
        JOIN auth_user a1 ON a1.id = sub.other_id
        """)
        rezultat = cursor.fetchall()


        for red in rezultat:

            id = red[0]

            with connection.cursor() as cursor1:
                cursor1.execute("""
                SELECT id FROM conversations WHERE
                (id_first = '""" + str(id) + """"' or id_first = '""" + str(logged_in) + """"') 
                and (id_second = '""" + str(id) + """"' or id_second = '""" + str(logged_in) + """"')
                """)
                rez = cursor1.fetchone()
                if not rez:
                    jsfunction = "chat.createConversation('" + str(id) + "');"
                else:
                    jsfunction = "chat.openChat('" + str(rez[0]) + "');"

            cursor1.close()
            username = red[1]
            first_name = red[2]
            last_name = red[3]
            avatar = str('/media/'+str(red[4]))
            display_name = returnName(first_name, last_name, username)

            friends_list += """
            <div class="row sideBar-body" onClick=\"""" + jsfunction +  """\">
                        <div class="col-sm-3 col-xs-3 sideBar-avatar">
                          <div class="avatar-icon">
                            <img src='""" + avatar + """'>
                          </div>
                        </div>
                        <div class="col-sm-9 col-xs-9 sideBar-main">
                          <div class="row">
                            <div class="col-sm-8 col-xs-8 sideBar-name">
                              <span class="name-meta">"""
            friends_list += display_name + """
                            </span>
                            </div>
                            <div class="col-sm-4 col-xs-4 pull-right sideBar-time">
                              <span class="time-meta pull-right">
                            </span>
                            </div>
                          </div>
                        </div>
                      </div>
            """
    current_user_avatar = """<img width="40" src='/media/""" + str(request.user.avatar) + """' />"""
    return render(request, 'main/chat.html', {"friends_list": friends_list, 'current_user_avatar': current_user_avatar})