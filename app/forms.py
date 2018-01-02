from django import forms
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True  )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
