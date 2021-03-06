"""pygram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from app.views import *
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^', include('app.urls')),
    url(r'^chat/$', chat, name='chat'),
    #url(r'^settings/$', settings, name='settings'),
    url(r'^friends/$', friends, name='friends'),
    url(r'^settings/$', Settings, name='Settings'),

    url(r'^ajax/sendmessage/$', SendMessage, name='SendMessage'),
    url(r'^ajax/search/$', Search, name='Search'),
    url(r'^ajax/loadconversations/$', LoadConversations, name='LoadConversations'),
    url(r'^ajax/friendrequests/$', FriendRequests, name='FriendRequests'),
    url(r'^ajax/loadchat/(?P<chat_id>\d+)$', LoadChat, name='LoadChat'),
    url(r'^ajax/accept/(?P<user_id>\d+)$', Accept, name='Accept'),
    url(r'^ajax/decline/(?P<user_id>\d+)$', Decline, name='Decline'),
    url(r'^ajax/addfriend/(?P<user_id>\d+)$', AddFriend, name='AddFriend'),
    url(r'^ajax/loadmessages/(?P<chat_id>\d+)$', LoadMessages, name='LoadMessages'),
    url(r'^ajax/createconversation/(?P<receiver_id>\d+)$', CreateConversation, name='CreateConversation'),
    url(r'^ajax/getnewmessages/(?P<chat_id>\d+)/(?P<last_id>\d+)$', GetNewMessages, name='GetNewMessages'),


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)