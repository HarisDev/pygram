from django.contrib.auth import logout
from django.shortcuts import render
from app.forms import UserForm

def logout(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'main/login.html')