from django.shortcuts import render

def friends(request):

    return render(request, 'main/friends.html')