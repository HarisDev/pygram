from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponseRedirect

from app.forms import UserForm


def register(request):

    form = UserForm(request.POST or None, request.FILES)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/chat")
    context = {
        "form": form,
    }
    return render(request, 'main/register.html', context)
