'''
views.py (app rheolau)
'''

from django.shortcuts import render

def hafan(request):
    context = {}
    return render(request, 'dadansoddwr/hafan.html', context)

