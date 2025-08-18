from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import UserProfile

def index(request):
    context = {
        'title': 'Главная страница',
        'users': UserProfile.objects.all(),
    }
    return render(request, 'users/index.html', context)

def user_list(request):
    context = {
        'title': 'Список',
        'users': UserProfile.objects.all(),
    }
    return render(request, 'users/user_list.html', context)

@login_required
def user_detail(request, id):
    user = UserProfile.objects.get(id=id)
    context = {
        'title': f'{user.name} {user.family}',
        'user': user,
    }
    return render(request, 'users/user_detail.html', context)