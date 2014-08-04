#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
gair.py 
	Gair class: rhestr nodau
	hefyd adnoddau darganfod acenion a phwyslais
		AYG: dyn, cur:o, cel:wydd:og (mae'r acen yn disgyn yn naturiol ar gwlwm llafariaid)
'''

global debug
debug = True

import re

import cysonion as cy
from nodau import RhestrNodau, RhestrClymau


#------------------------------------------------
# Gair class
#------------------------------------------------
class Gair(object):
	'''
	class: Gair
		 mewnbwn: llinyn (utf8)
	 ''' 
	def __init__(self, s):
		s = s.strip()
		if re.search(r'\s', s):	
			raise ValueError( "Wedi methu creu Gair o'r llinyn '%s'" % s )
		self.nodau = RhestrNodau(s)
		self.clymau = self.nodau.rhestr_clymau(trwsio=True)

	def __unicode__(self):
		return  self.nodau.__unicode__()
				
	def __str__(self):
		return self.__unicode__().encode('utf-8')		
		
	def nodau_acenog(self):
		'''
		ffwythiant:	darganfod y nodau sy'n cario'r acenion
		allbwn:		rhestr nodau (llafariaid) sy'n cario'r acenion
		'''
		ace = list()
		for cwlwm in self.clymau[::2]:	# clymau llafariaid yn unig
			if cwlwm and cwlwm[0].isllafariad():
				# llafariad sengl
				if len(cwlwm) == 1:			
					ace.append( cwlwm[0] )
				# llafariaid dwbl (deusain)
				elif len(cwlwm) == 2:	
					ds = ''.join(nod.hir2byr() for nod in cwlwm)
					if cy.deuseiniaid.has_key(ds):
						dd = cy.dosbarth_deusain[ds.lower()]
						# deusain talgron (acen ar yr ail lafariad)
						if ds in cy.deuseiniaid['talgron']:				
							ace.append( cwlwm[1] )
						# gair deusill (acen ar y ddwy lafariad)
						elif ds in cy.deuseiniaid['deusill']:				
							ace.append( cwlwm[0] )
							ace.append( cwlwm[1] ) 
					# deusain lleddf (acen ar y llafariad cyntaf)
					else:
						ace.append( cwlwm[0] )	
		
				# tri neu fwy o lafariaid: defnyddio'r ail lafariad yn y cwlwm
				else:
					ace.append( cwlwm[1] )			
		return tuple(ace)
	
		
	def nifer_sillau(self):
		return len( self.acenion() )
	
	def shownodau(self):
		print [nod.llinyn for nod in self.nodau]
	
	def showclymau(self):
		print [cwl.llinyn() for cwl in self.clymau]

	def pwyslais(self):
		'''
		ffwythiant:	darganfod pwyslais gair
		mewnbwn:	rhestr nodau
		allbwn:		mynegrif: (-1 = sill olaf, -2 = sill olaf ond un)
		sylwadau:	
			Mae angen helaethu ar ffyrdd i ddarganfod geiriau acennog lluosill
		'''
		# dianc os nad oes o leiaf un llafariad (e.e. y cysylltnod mewn englyn)
		if not any([ nod.isllafariad() for nod in self.nodau ]):
			return 0

		olaf = self.clymau[-1]
		olaf_ond_un = self.clymau[-2]
		olaf_ond_dau = self.clymau[-3] if len(self.clymau) > 2 else None

		# gwirio am ae o flaen y cwlwm cytseiniaid olaf (e.e. cymraeg)
		# ond dyw hyn ddim yn gweithio gyda 'ymadael'
		# if olaf and olaf_ond_un and olaf_ond_un.llinyn() == u'ae':
		# 	# print 'ding 1'
		# 	return -1	
		# gwirio am h o flaen y cwlwm llafariaid olaf (e.e. dyfalbarhau)
		if olaf_ond_dau and olaf_ond_dau[-1].llinyn in ['h','rh']:
			# print 'ding 2'
			return -1
		# gwirio am lafariad hir fel cwlwm olaf (e.e. cangarŵ)
		if olaf_ond_un and unicode(olaf_ond_un[-1]) in cy.llafariaid_hir:
			# print 'ding 3'
			return -1
		# gwiriad syml
		if self.nifer_sillau() == 1: 
			return -1 # gair unsill
		else:
			return -2 # goben
	
	def traeannu(self, cytseiniaid=False):
		'''
		ffwythiant: hollti gair yn dri (pen, canol, cwt)
		allbwn:		tri rhestr nodau
		'''	
		pwy = self.pwyslais()
		# dim cytseiniaid
		# if not filter(None, self.clymau[1::2]):	
		# 	return [], [], []
		# gair acennog
		if pwy == -1:
			pen = self.clymau[:-2]
			can = []
			cwt = self.clymau[-2:]
		# gair diacen
		else:
			pen = self.clymau[:-4]
			can = self.clymau[-4:-2]
			cwt = self.clymau[-2:]
		# cytseiniaid yn unig
		if cytseiniaid:
			pen = pen[1::2]
			can = can[1::2]
			cwt = cwt[1::2]
		# datod
		pen = [z for x in pen for z in x]
		can = [z for x in can for z in x]
		cwt = [z for x in cwt for z in x]
		return pen, can, cwt
	
		
	# allbwn
	def llinyn(self):
		return ''.join( [nod.llinyn for nod in self.nodau] )
				
	def llinyn_llafariaid(self, blanksymbol=' '):
		ss = list()
		for nod in self.nodau:
			if nod.isllafariad():	ss.append(nod.llinyn)
			else:					ss.append(blanksymbol*len(nod.llinyn))
		return ''.join(ss)

	def llinyn_cytseiniaid(self, blanksymbol=' '):
		ss = list()
		for nod in self.nodau:
			if nod.iscytsain():		ss.append(nod.llinyn)
			else:					ss.append(blanksymbol*len(nod.llinyn))
		return ''.join(ss)

	def llinyn_acenion(self, blanksymbol=' '):
		ace = self.nodau_acenog()

		if self.pwyslais() == 0:
			return ''.join([ blanksymbol*len(nod.llinyn) for nod in self.nodau ])
		pwy = ace[ self.pwyslais() ]

		ss = list()
		for nod in self.nodau:
			if any([nod is x for x in ace]):
				if nod is pwy:	ss.append('/')
				else:			ss.append('v')
			else:
				ss.append( blanksymbol*len( nod.llinyn ) )				
		return ''.join(ss)

	def llinyn_acenion_colon(self, blanksymbol=' '):
		ace = self.nodau_acenog()
		ss = [blanksymbol*len(nod.llinyn) for nod in self.nodau ]
		ss[ self.nodau.index(ace[-1]) ] = ':'
		if self.pwyslais() == -2:
			ss[ self.nodau.index(ace[-2]) ] = ':'
		return ''.join(ss)

	# man ffwythiannau
	def nifer_sillau(self):
		return len( self.nodau_acenog() )
	

#------------------------------------------------
def main():
	print 'gair.py'
	
	s = 'ceffyl'
	s = 'ieuanc'
	g = Gair(s)
	print g.llinyn_acenion()
	print g.llinyn()
	print g.clymau
	a,b,c = g.traeannu()
	print [nod.llinyn for nod in a]
	print [nod.llinyn for nod in b]
	print [nod.llinyn for nod in c]
	# return

	llinynnau = (
		'prydferth',
		'anifeiliaid',
		'cuddio',
		'dramodydd',
		'rhôm',
		"â'th",
		# deuseiniaid
		'haleliwia',
		# deusainiaid ddeusill
		'duon',			
		'eos',			
		'suo',			
		# geiriau lluosill acenog
		'cymraeg',
		u'cangarŵ',		
		'dramodydd',
		'dyfalbarhau',
		'dyfalbarhad',
		# w-gytsain
		'awen',
		# w-gytsain yn olaf
		'berw',
		'pitw',	
		# w-gytsain gwr, gwl	
		'gwaith',		
		'gwledd',
		'wledd',	
		'gwrandawiad',
		'wrandawiad',
		'gwrando',
		'gwr',
		'gwroldeb',
		'gwrhydri',
		'gŵr',
		'llw',		
		'bedw',			
		'dedwydd',
		'daear',
		'ffiniau',
		'ymadael',		
	)
	# llinynnau = ('anifeiliaid',)
	for s in llinynnau:
		g = Gair(s)
		print '-------------------'

		print g.llinyn_acenion()
		print g.llinyn()
		print g.clymau

		# pe, ca, cw = g.traeannu(cytseiniaid=True)
		# print
		# print [nod.llinyn for nod in pe]
		# print [nod.llinyn for nod in ca]
		# print [nod.llinyn for nod in cw]


if __name__ == '__main__': 
	main()

		
