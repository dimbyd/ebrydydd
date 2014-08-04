'''
models.py (ebrydydd app)
'''

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# from peiriant.cysonion import LLYTHRENWAU

import peiriant.cysonion as pc
import ebrydydd.cysonion as ec

class Awdur(models.Model):
	enw = models.CharField(max_length=140, null=True, blank=True)	   
	def __unicode__(self):
		return self.enw

class Llinell(models.Model):
	llinyn = models.CharField(max_length=140)
	awdur = models.CharField(max_length=140, null=True, blank=True)	   
	def __unicode__(self):
		return self.llinyn
	def get_absolute_url(self):
		return reverse('llinell', kwargs={'pk': self.id})
	def get_next(self):
		next = Llinell.objects.filter(id__gt=self.id)
		# next = Llinell.objects.order_by('llinyn').filter(id__gt=self.id)
		if next:
			return next[0]
   		return False
	def get_prev(self):
		prev = Llinell.objects.filter(id__lt=self.id).order_by('-pk')
		if prev:
			return prev[0]
		return False

class Cwpled(models.Model):
	cyntaf = models.ForeignKey(Llinell, related_name="llinell_cyntaf")
	ail = models.ForeignKey(Llinell, related_name="ail_linell")
	awdur = models.ForeignKey(Awdur, null=True)	   
	def __unicode__(self):
		return self.cyntaf.llinyn + '\n' + self.ail.llinyn 

class ToddaidByr(models.Model):
	cyntaf = models.CharField(max_length=140)
	cyrch = models.CharField(max_length=140)
	ail = models.CharField(max_length=140)
	awdur = models.ForeignKey(Awdur, null=True)	   
	def __unicode__(self):
		return self.cyntaf + ' - ' + cyrch  + '\n' + self.ail

class Englyn(models.Model):
	paladr = models.ForeignKey(ToddaidByr)
	esgyll = models.ForeignKey(Cwpled)
	awdur = models.ForeignKey(Awdur, null=True)	   
	def __unicode__(self):
		return str(paladr) + '\n' + str(esgyll)


class Dadansoddiad(models.Model):
	llinell		= models.ForeignKey(Llinell)
	cynghanedd	= models.CharField(max_length=3, choices=pc.LLYTHRENWAU['cynghanedd'], null=True, blank=True)
	aceniad		= models.CharField(max_length=3, choices=pc.LLYTHRENWAU['aceniad'], null=True, blank=True)
	bai			= models.CharField(max_length=3, choices=pc.LLYTHRENWAU['bai'], null=True, blank=True) 
	dadansoddwr = models.CharField(max_length=140, null=True, blank=True)
	sylwadau	= models.CharField(max_length=140, null=True, blank=True)
	
	def __unicode__(self):
		s = str(self.llinell) + '\n' 
		if self.cynghanedd:
			s = s + self.cynghanedd + '\n'
		if self.aceniad:
			s = s + ':' + self.aceniad
		if self.bai:
			s += ':[' + self.bai + ']'
		if self.dadansoddwr:
			s = s + '{' + self.dadansoddwr + '}\n'
		if self.sylwadau:
			s = s + '<' + str(self.sylwadau) + '>'
		return s

class Aelod(models.Model):
	user = models.OneToOneField(User)
	ffugenw = models.CharField(max_length=10)
	statws = models.CharField(max_length=3, choices=ec.LLYTHRENWAU['statws'])
	# darlun = models.ImageField(upload_to='darluniau_aelodau', null=True, blank=True)
	def __unicode__(self):
		return self.user.username
	def get_absolute_url(self):
		return reverse('aelod', kwargs={'pk': self.id})
