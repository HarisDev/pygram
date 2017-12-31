from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth.models import models
from app.forms import UserForm
from django.conf import settings

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_user',
                                         blank=True, null=True, editable=False)
                return render(request, 'main/index.html')
            else:
                return render(request, 'main/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'main/login.html', {'error_message': 'Invalid login'})
    return render(request, 'main/login.html')

def logout(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }