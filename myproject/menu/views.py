from django.shortcuts import render
from .models import Menu


def home(request):
    menus = Menu.objects.all()
    context = {'menus': menus}
    return render(request, 'home.html', context=context)

