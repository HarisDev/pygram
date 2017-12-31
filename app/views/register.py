from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth.models import models
from django.conf import settings

from app.forms import UserForm


def register(request):
    form = UserForm(request.POST or None)
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
                user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_user',
                                         blank=True, null=True, editable=False)
                return render(request, 'main/base.html', {'forms': form})
    context = {
        "form": form,
    }
    return render(request, 'main/register.html', context)
