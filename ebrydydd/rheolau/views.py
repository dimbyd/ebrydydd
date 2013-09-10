'''
views.py ar gyfer app rheolau
'''

from django.shortcuts import render

from django.core.urlresolvers import reverse

from ebrydydd.sylfaen.models import Cynghanedd

def hafan(request):
    rhestr_cynganeddion = Cynghanedd.objects.all()
    context = {'rhestr_cynganeddion': rhestr_cynganeddion}
    return render(request, 'rheolau/hafan.html', context)

