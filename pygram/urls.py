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


urlpatterns = [
    url(r'^', include('app.urls')),
    url(r'^chat/$', chat, name='chat'),
    #url(r'^settings/$', settings, name='settings'),
    url(r'^friends/$', friends, name='friends'),
    url(r'^settings/$', Settings, name='Settings'),

    url(r'^ajax/sendmessage/$', SendMessage, name='SendMessage'),
    url(r'^ajax/loadconversations/$', LoadConversations, name='LoadConversations'),
    url(r'^ajax/loadchat/(?P<chat_id>\d+)$', LoadChat, name='LoadChat'),
    url(r'^ajax/loadmessages/(?P<chat_id>\d+)$', LoadMessages, name='LoadMessages'),
    url(r'^ajax/createconversation/(?P<receiver_id>\d+)$', CreateConversation, name='CreateConversation'),
    url(r'^ajax/getnewmessages/(?P<chat_id>\d+)/(?P<last_id>\d+)$', GetNewMessages, name='GetNewMessages'),


]
