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
        SELECT a1.id, a1.username, a1.first_name, a1.last_name FROM 
          ( SELECT 
            CASE WHEN c.id_first = '""" + str(logged_in) + """"' THEN id_second
                 WHEN c.id_second = '""" + str(logged_in) + """"' THEN id_first
            END AS other_id
            FROM pygram.friends as c
            WHERE c.accepted = '1'
          ) sub
        JOIN auth_user a1 ON a1.id = sub.other_id
        """)
        rezultat = cursor.fetchall()


        for red in rezultat:

            id = red[0]
            username = red[1]
            first_name = red[2]
            last_name = red[3]
            display_name = returnName(first_name, last_name, username)

            friends_list += """
            <div class="row sideBar-body">
                        <div class="col-sm-3 col-xs-3 sideBar-avatar">
                          <div class="avatar-icon">
                            <img src="https://bootdey.com/img/Content/avatar/avatar1.png">
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
                              <span class="time-meta pull-right">18:18
                            </span>
                            </div>
                          </div>
                        </div>
                      </div>
            """

    return render(request, 'main/chat.html', {"friends_list": friends_list})