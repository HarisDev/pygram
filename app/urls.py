from django.conf.urls import url
from app.views import *

app_name ='app'

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^register/$', register, name='register'),
    url(r'^login/$', login_user, name='login'),
    url(r'^accounts/login/$', login_user, name='login'),
    url(r'^logout/$', logout, name='logout'),

]