from django.conf.urls import url
from app.views import *
from django.contrib.auth.views import logout

app_name ='pygram'

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^register/$', register, name='register'),
    url(r'^login/$', login_user, name='login_user'),
    url(r'^logout/$', logout, {'next_page': '/login/'}, name='logout'),

]