from django.shortcuts import render


def home(request, item=None):
    print()
    return render(request, 'home.html', {'item': item})
