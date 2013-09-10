'''
views.py yr ebrydydd (app sylfaenol)
'''

from django.shortcuts import render

def hafan(request):
    context = {'uname': 'MrUrdd'}
    return render(request, 'hafan.html', context)
