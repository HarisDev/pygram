from django.shortcuts import render
from django.db import connection

def friends(request):
    logged_in=request.user.id
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

        redovi=cursor.fetchall()
        x=0
        site=""
        for red in redovi:
            if x==2:
                klasa="col-md-4"
            else:
                klasa="col-md-2"
            site+="""<div class='""" + klasa + """'>"""
            site+="""<img src='/media/""" +  str(red[4]) + """'
             /><br /> <br />  """
            site+="<span class='ime'>"+red[2]+" "+red[3]+"</span>"
            site+="""</div>"""
            x+=1
    cursor.close()
    with connection.cursor() as c1:
        c1.execute("""
            
            SELECT sub.other_id, a1.username, a1.avatar FROM 
              ( SELECT id,
                CASE WHEN c.id_first = '""" + str(logged_in) + """"' THEN id_second
                     WHEN c.id_second = '""" + str(logged_in) + """"' THEN id_first
                END AS other_id
                FROM friends as c
                WHERE time_sent != '""" + str(logged_in) + """' and accepted = '0'
              ) sub
            JOIN auth_user a1 ON a1.id = sub.other_id
            
        """)
        korisnici=c1.fetchall()
        lista=" "
        for redx in korisnici:

            lista += """<div class='  col-md-12  find' id='request-""" + str(redx[0]) + """'>"""
            lista += """<img src='/media/""" +  str(redx[2]) + """' style="float:left; margin-right: 25px; border-radius:50%;" />  """
            lista += "<br /><span class='ime' style='color:white;margin-top:15px;'>" + redx[1] + "</span> <div class='request'><a style='background:rgb(48, 169, 33);' class='ime' href='javascript:;' onClick=\"friends.accept('" + str(redx[0]) + "')\">Accept</a> <a class='ime' style='background:rgba(255, 27, 49, 0.77);' href='javascript:;' onClick=\"friends.decline('" + str(redx[0]) + "')\">Decline</a></div>"
            lista += """</div><br style="clear:both" /><br />"""


    return render(request, 'main/friends.html', {'varijabla': site,'lista': lista})