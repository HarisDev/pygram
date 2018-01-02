from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render
from app.forms import UserForm
from django.http import HttpResponseRedirect


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/chat")
            else:
                return HttpResponseRedirect("/login", {'error_message': 'Your account has been disabled'})
        else:
            return HttpResponseRedirect("/login", {'error_message': 'Invalid login'})
    return render(request, 'main/login.html')

def logout(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
