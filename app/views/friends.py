from django.shortcuts import render
from django.db import connection

def friends(request):
    logged_in=request.user.id
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT a1.id, a1.username, a1.first_name, a1.last_name FROM 
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
            site+="""<img src="https://bootdey.com/img/Content/avatar/avatar1.png" /><br /> <br />  """
            site+="<span class='ime'>"+red[2]+" "+red[3]+"</span>"
            site+="""</div>"""
            x+=1
    cursor.close()
    with connection.cursor() as c1:
        c1.execute("""
            select username, avatar from auth_user order by id desc limit 9
        """)
        korisnici=c1.fetchall()
        lista=" "
        for redx in korisnici:

            lista += """<div class='  col-md-4  find'>"""
            lista += """<img src="https://bootdey.com/img/Content/avatar/avatar1.png" /><br /> <br />  """
            lista += "<span class='ime'>" + redx[0] + "</span>"
            lista += """</div>"""


    return render(request, 'main/friends.html', {'varijabla': site,'lista': lista})