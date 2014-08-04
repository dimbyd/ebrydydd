# -*- coding: utf-8 -*-
'''
views.py (ebrydydd app)
'''

import random

from django import forms
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.template import RequestContext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from ebrydydd.models import Llinell, Dadansoddiad, Aelod
from ebrydydd.forms import LlinellForm, LlinellNewyddForm, LlinellCronfaForm, DadansoddiadForm, UserForm, AelodForm

import ebrydydd.peiriant as pe
#------------------------------
# Llinellau
#------------------------------
class Llinell_ListView(ListView):
	model = Llinell
	template_name = 'rhestr_llinellau.html'
	queryset = Llinell.objects.order_by('llinyn')	
	paginate_by = 10  
	success_url = reverse_lazy('rhestr-llinellau')
	def get_success_url(self):
		return reverse(OrderView.plain_view)

Llinell_ListView.plain_view = staticmethod(Llinell_ListView.as_view())

		
class Llinell_CreateView(CreateView):
	model = Llinell
	template_name = 'update_llinell.html'
	def get_success_url(self):
		return reverse('rhestr-llinellau')
	def get_context_data(self, **kwargs):
		context = super(Llinell_CreateView, self).get_context_data(**kwargs)
		context['action'] = reverse('create-llinell')
		return context		

class Llinell_UpdateView(UpdateView):
	model = Llinell
	template_name = 'update_llinell.html'
	def get_success_url(self):
		return reverse('rhestr-llinellau')
	def get_context_data(self, **kwargs):
		context = super(Llinell_UpdateView, self).get_context_data(**kwargs)
		context['action'] = reverse('update-llinell', kwargs={'pk': self.get_object().id})
		return context

class Llinell_DeleteView(DeleteView):
    model = Llinell
    template_name = 'delete_llinell.html'
    def get_success_url(self):
        return reverse('rhestr-llinellau')

class Llinell_DetailView(DetailView):
	model = Llinell
	template_name = 'llinell.html'
	def get_success_url(self):
		return reverse('rhestr-llinellau')
	def get_context_data(self, **kwargs):
		context = super(Llinell_DetailView, self).get_context_data(**kwargs)
		qset = Dadansoddiad.objects.filter(llinell=self.get_object().id).order_by('dadansoddwr')
		qset = list(qset)
		s = self.get_object().llinyn
		adroddiad = pe.Peiriant().oes_cynghanedd( pe.Llinell(s) )
		dad = Dadansoddiad(
			llinell 	= self.get_object(),
			cynghanedd 	= adroddiad.cynghanedd,
			aceniad 	= adroddiad.aceniad,
			bai 		= adroddiad.bai,
			sylwadau 	= adroddiad.sylwadau,
			dadansoddwr	= 'EBR'
			)
		qset.append(dad)
		context['dads']  = qset
		context['html_strings'] = ebr2html(adroddiad)
		context['next'] = self.get_object().get_next()
		context['prev'] = self.get_object().get_prev()
		return context


#------------------------------
# Aelodau
#------------------------------
class Aelod_ListView(ListView):
	model = Aelod
	template_name = 'rhestr_aelodau.html'
	def get_success_url(self):
		return reverse('cronfa')

class Aelod_DetailView(DetailView):
	model = Aelod
	template_name = 'aelod.html'
	def get_success_url(self):
		return reverse('rhestr-aelodau')
	def get_context_data(self, **kwargs):
		context = super(Aelod_DetailView, self).get_context_data(**kwargs)



#------------------------------
# Paratoi data
#------------------------------
def dad2dict(dad):
	return {
		'cynghanedd': 	dict(pe.LLYTHRENWAU['cynghanedd'])[dad.cynghanedd] if dad.cynghanedd else 'DIM',
		'aceniad': 		dict(pe.LLYTHRENWAU['aceniad'])[dad.aceniad] if dad.aceniad else '',
		'bai':			dict(pe.LLYTHRENWAU['bai'])[dad.bai] if dad.bai else '',
		'sylwadau':		dad.sylwadau,
		'dadansoddwr':	dad.dadansoddwr,
	
	}

# 
# def ebr2html(adroddiad, blanksymbol=' '):
# 	'''
# 	ffwythiant: trawsnewid adroddiad i linynau html 
# 	'''	
# 	# init
# 	s = adroddiad.llinyn
# 	html_strings = {
# 		'llinyn': s,
# 		'acenion': '',
# 		'gorffwysfa': '',
# 		'odl': '',
# 		'cytseiniaid': '',
# 	}
# 	# gorffwysfa (mynegrif y gair)
# 	if adroddiad.data.has_key('gorffwysfa'):
# 		gorffwysfa = adroddiad.data['gorffwysfa']
# 		if gorffwysfa:
# 			geiriau = s.split()
# 			ss = ''
# 			for j in range( len(geiriau) ):
# 				ss += blanksymbol*len(geiriau[j])
# 				if j in gorffwysfa:
# 					ss += '<span class="gorffwysfa">|</span>'
# 				else:
# 					ss += blanksymbol
# 			html_strings['gorffwysfa'] = ss[:-1]	
# 	# odl
# 	if adroddiad.data.has_key('odl'):
# 		odl = adroddiad.data['odl']
# 		if odl:
# 			cyntaf = odl[0]
# 			ail = odl[1]
# 			geiriau = s.split()
# 			ss = []
# 			for gair in geiriau[ :cyntaf[0] ]:
# 				ss.append( blanksymbol*(len(gair)+1) )
# 			gair = geiriau[ cyntaf[0] ]
# 			nodau = rhestr_nodau(gair)
# 			for nod in nodau[:cyntaf[1][0]]:
# 				ss.append( blanksymbol*len(nod) )
# 			ss.append( '<span class="odl">' + ''.join(nodau[cyntaf[1][0]:cyntaf[1][1]]) + '</span>' )
# 			for nod in nodau[cyntaf[1][1]:]:
# 				ss.append( blanksymbol*len(nod) )
# 			ss.append( blanksymbol )
# 			for gair in geiriau[ cyntaf[0]+1:ail[0] ]:
# 				ss.append( blanksymbol*(len(gair)+1 ) )
# 			gair = geiriau[ ail[0] ]
# 			nodau = rhestr_nodau(gair)
# 			for nod in nodau[:ail[1][0]]:
# 				ss.append( blanksymbol*len(nod) )
# 			ss.append( '<span class="odl">' + ''.join(nodau[ ail[1][0]:ail[1][1] ]) + '</span' )
# 			for nod in nodau[ail[1][1]:]:
# 				ss.append( blanksymbol*len(nod) )
# 			for gair in geiriau[ ail[0]+1: ]:
# 				ss.append( blanksymbol )
# 				ss.append( blanksymbol*len(gair) )
# 			html_strings['odl'] = ''.join(ss[:-1])
# 	# acenion
# 	if adroddiad.data.has_key('acenion'):
# 		acenion = adroddiad.data['acenion']
# 		print acenion
# 		ss = []
# 		geiriau = s.split()
# 		for i in range( len(geiriau) ):
# 			nodau = rhestr_nodau( geiriau[i] )
# 			mynegrifau = acenion[i][0]
# 			pw = acenion[i][1]
# 			for j in range( len(nodau) ):
# 				if j in mynegrifau:
# 					if j == mynegrifau[pw]:
# 						ss.append('/')
# 					else:
# 						ss.append('v')
# 				else:
# 					ss.append( blanksymbol*len( nodau[j] ) )
# 			ss.append(blanksymbol)
# 		html_strings['acenion'] = ''.join(ss[:-1])			
# 	return html_strings
# 

#------------------------------
# Prif dudalenau
#------------------------------
def hafan(request):
	context = {'uname': 'mrurdd'}
	context['llinell_form'] = LlinellForm()
	context['llinell_newydd_form'] = LlinellNewyddForm()
	context['llinell_cronfa_form'] = LlinellCronfaForm()
	context['dadansoddiad_form'] = DadansoddiadForm()
	context['hap'] = random.choice(Llinell.objects.all())
	return render(request, 'hafan.html', context)


def cronfa(request):
	'''
	ffwythiant: mynedfa i'r gronfa ddata
	'''
	context = {'uname': 'mrurdd'}
	return render(request, 'cronfa.html', context)


def cwis(request):
	context = {'uname': 'mrurdd'}
	llinell = random.choice(Llinell.objects.all())
	context['llinell_cwestiwn'] = llinell
	form = DadansoddiadForm( initial={'llinell':llinell} )
	form.fields['llinell'].widget = forms.HiddenInput()
	context['dadansoddiad_form'] = form
	return render(request, 'cwis.html', context)


def dyfarniad(request):
	'''
	ffwythniant: er mwyn cymharu dadansoddiadau defnyddiwr/cronfa/peiriant
	'''
	if request.method == 'POST':
		context = {'uname': 'mrurdd'}
		form = DadansoddiadForm(request.POST)
		
		if form.is_valid():
			llinell = form.cleaned_data['llinell']
			if llinell:
				context['llinyn'] = llinell.llinyn
								
				# dadansoddiad y defnyddiwr
				dad_def = Dadansoddiad(
					llinell 	= llinell,
					cynghanedd 	= form.cleaned_data['cynghanedd'],
					aceniad 	= form.cleaned_data['aceniad'],
					bai 		= form.cleaned_data['bai'],
					sylwadau 	= form.cleaned_data['sylwadau'],
					dadansoddwr	= form.cleaned_data['dadansoddwr'],
					)
				context['dad_defnyddiwr'] = dad2dict(dad_def)
			
				#  dadansoddiad y peiriant
				adroddiad = pe.Peiriant().oes_cynghanedd( llinell.llinyn )
				dad_ebr = Dadansoddiad(
					llinell 	= llinell,
					cynghanedd 	= adroddiad.cynghanedd,
					aceniad 	= adroddiad.aceniad,
					bai 		= adroddiad.bai,
					sylwadau 	= adroddiad.sylwadau,
					dadansoddwr	= 'EBR'
					)
				context['dad_peiriant'] = dad2dict(dad_ebr)
				context['data'] = adroddiad.data
				
				# dyfarnu os ydy'r defnyddiwr yn gywir (angen helaethu yma)
				s = ''
				if dad_def.cynghanedd == dad_ebr.cynghanedd:
					context['dyfarniad'] = 'Cywir'
				else:
					context['dyfarniad'] = 'Anghywir'
					
				# rhestr dadansoddiadau (yn cynnwys o'r gronfa)
				dadansoddiadau = list()
				dadansoddiadau.append( context['dad_defnyddiwr'] )
				dads = Dadansoddiad.objects.filter(llinell=llinell).order_by('dadansoddwr')
				for dad in list(dads):
					dadansoddiadau.append( dad2dict(dad) )
				dadansoddiadau.append( context['dad_peiriant'] )
				context['dads'] = dadansoddiadau
								
				# llinell hap
				context['hap'] = random.choice(Llinell.objects.all())
			else:
				context['neges'] = form.data
		else:
			# context['neges'] = 'methiant: ffurlen ddim yn ddilys' 
			# context['neges'] = form.cleaned_data
			context['neges'] = form.errors
			# context['neges'] = 'methiant'
		return render(request, 'dyfarniad.html', context)
	else:
		form = DadansoddiadForm() 
		return render(request, 'cwis.html', { 'form': form })

	
def dadansoddiad(request):
	if request.method == 'POST':
		context = {}
		llinell_ddewis = None	
		form = LlinellForm(request.POST) 
		if form.is_valid():
			llinyn = form.cleaned_data['llinyn']
			if not llinyn:
				llinell_ddewis = form.cleaned_data['llinell_ddewis']
				llinyn = llinell_ddewis.llinyn
			context['llinyn'] = llinyn
			# cyfrifiannu dadansoddiad y peiriant
			adroddiad = pe.Peiriant().oes_cynghanedd( pe.Llinell(llinyn) )
			cy = dict(pe.LLYTHRENWAU['cynghanedd'])[adroddiad.cynghanedd] if adroddiad.cynghanedd else '-'
			ac = dict(pe.LLYTHRENWAU['aceniad'])[adroddiad.aceniad] if adroddiad.aceniad else '-'
			ba = dict(pe.LLYTHRENWAU['bai'])[adroddiad.bai] if adroddiad.bai else '-'
			dad_yr_ebr = {
				'dadansoddwr':	'EBR',
				'cynghanedd': 	cy,
				'aceniad': 		ac,
				'bai':			ba,
				'sylwadau':		adroddiad.sylwadau,
				'data': 	adroddiad.data
			}
			context['dad'] = dad_yr_ebr
			
			# llinynau html
			# context['html_strings'] = ebr2html(adroddiad)
			
			# cyrchu dadansoddiadau o'r gronfa
			dadansoddiadau = list()
			if llinell_ddewis:
				dads = Dadansoddiad.objects.filter(llinell=llinell_ddewis).order_by('dadansoddwr')
				for dad in list(dads):
					cy = dict(pe.LLYTHRENWAU['cynghanedd'])[dad.cynghanedd] if dad.cynghanedd else '-'
					ac = dict(pe.LLYTHRENWAU['aceniad'])[dad.aceniad] if dad.aceniad else '-'
					ba = dict(pe.LLYTHRENWAU['bai'])[dad.bai] if dad.bai else '-'
					dadansoddiadau.append({
						'dadansoddwr':	dad.dadansoddwr,
						'cynghanedd': 	cy,
						'aceniad': 		ac,
						'bai':			ba,
						'sylwadau':		dad.sylwadau,
					})
					
			# atodi dadansoddiad y peiriant		
			dadansoddiadau.append(dad_yr_ebr)
			context['dads'] = dadansoddiadau
			
			# llinell hap
			context['hap'] = random.choice(Llinell.objects.all())
			
		else:
			context['neges'] = 'methiant: dim llinyn'
		return render(request, 'dadansoddiad.html', context)
	else:
		form_llinell = LlinellForm() 
		return render(request, 'hafan.html', { 'form_llinell': form_llinell })

		
#------------------------------
# AELODAU
#------------------------------
def cofrestru(request):
    context = RequestContext(request)
    cofrestrwyd = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        ffurflen_aelod = FfurflenAelod(data=request.POST)
        if user_form.is_valid() and ffurflen_aelod.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            aelod = ffurflen_aelod.save(commit=False)
            aelod.user = user
            # if 'picture' in request.FILES:
            #     profile.picture = request.FILES['picture']
            # profile.save()
            cofrestrwyd = True
        else:
	    	print user_form.errors, ffurflen_aelod.errors
    else:
        user_form = UserForm()
        ffurflen_aelod = FfurflenAelod()
    return render_to_response(
            'cofrestru.html',
            {'user_form': user_form, 'ffurflen_aelod': ffurflen_aelod, 'cofrestrwyd': cofrestrwyd},
            context)





