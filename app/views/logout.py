from django.contrib.auth import logout as django_logout
from django.http import *
from django.contrib.auth.decorators import login_required

@login_required
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/login')