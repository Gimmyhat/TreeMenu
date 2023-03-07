from django.shortcuts import render


def home(request, item=None):
    return render(request, 'home.html', {'item': item})
