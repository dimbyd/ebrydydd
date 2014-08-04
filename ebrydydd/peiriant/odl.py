#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' 
odl.py : adnoddau er mwyn darganfod a dosbarthu odl

	"cyflawn": y ddwy sill olaf yn cyfateb 
		puro, suro, curo (ur:o)
		gwasgariad, cariad, darpariad (ar:iad)

	"anghyflawn": y sill olaf yn cyfateb 
		curo, cludo, heno (:o)
		abad, cariad (:d)

	dosbarthiadau:
		odl gyflawn
		proest cyflawn
		odl lafarog
		proest lafarog

	RHEOLAU:
		aa - cwlwm llafariad
		bb - cwlwm cytseiniaid
		ds - deusain

	odl gyflawn:
		cwlwm olaf:			bb yn cyfateb
		cwlwm olaf-ond-un:	aa yn cyfateb, ac o'r un pwysau os ydy'r ddau yn acennog (e.e. cath/math, pren/llen)

	proest gyflawn:
		cwlwm olaf:			bb yn cyfateb
		cwlwm olaf-ond-un:	aa o'r un pwysau (e.e. hen/dyn)
							ds lleddf o'r un dosbarth  (e.e. llawn/mewn)
	odl lafarog:
		cwlwm olaf: aa yn cyfateb (e.e. tro/llo/bro)

	proest lafarog:
		cwlwm olaf: aa o'r un pwysau (e.e. bro/da/ci/te/du) 
					ds lleddf o'r un dosbarth (e.e. tew/byw)

	deuseiniaid talgron:
		odl:	gyda'r llafariaid unigol priodol (e.e. cariad/gwlad)
		proest: gyda sillau sy'n cynnwys unrhyw lafariaid unigol (e.e gwas/nes, creithiog/golwg)

	deuseiniaid lleddf:
		odl:	gyda'r un ddeusain
		proest: gyda deusain o'r un dosbarth	(e.e. tew/byw, llawn/mewn, dewr/awr)
					
	TODO:
		odlau cudd
		odlau ewinog

'''

import re
import cysonion as cy
# import llinyn as ll
# import acen as ac
from nodau import Nod, RhestrNodau, Cwlwm

from gair import Gair

import logging
out = logging.getLogger(__name__)

global debug
debug = False


def oes_odl_sengl(nodau1, nodau2, proest=False, trwm_ac_ysgafn=True):
	'''
	ffwythiant: oes_odl_sengl
	'''
	
	# if debug:
	# 	print 'oes_odl_sengl: ' + str(nodau1) + '/' + str(nodau2)

	# dim whitespace!
	if any([nod.isspace() for nod in nodau1]) or any([nod.isspace() for nod in nodau2]):
		return None

	clymau1 = nodau1.rhestr_clymau(trwsio=True)
	clymau2 = nodau2.rhestr_clymau(trwsio=True)
	if debug:
		print '**********'
		print clymau1
		print clymau2
	
	# problem fan hyn: da ni'n gofyn am bwysau deusain isod (proest)
	def pwysau(nod):
		if nod.llinyn in cy.llafariaid_hir:
			return 'Y'
		elif nod.llinyn in cy.llafariaid_byr:
			return 'T'
		else:
			return None
	
	# dianc os nad oes clymau (?)
	if not clymau1 or not clymau2:
		return None
	mae_odl = False
	mae_proest = False
	
	# gwiriad sylfaenol
	if clymau1[-1] == clymau2[-1] and clymau1[-2] == clymau2[-2]:
		mae_odl = True
	
	# gwirio os ydyw'r clymau olaf yn cyfateb (clymau cytseiniaid, efallai byddant yn wag)
	if clymau1[-1] == clymau2[-1]:	
		if debug:
			print '>> cytseiniaid terfynnol yn cyfateb: ' + clymau1[-1].llinyn() + '/' + clymau2[-1].llinyn()
	
		c1 = clymau1[-2]
		c2 = clymau2[-2]
		
		s1 = c1.llinyn()
		s2 = c2.llinyn()
		
		# if debug:
		# 	print '>> ceisio cyfateb: ' + s1 + '/' + s2
			
		# archwilio deuseiniaid
		if len(c1) > 1:		
			ds1 = c1.llinyn()
			if not cy.dosbarth_deusain.has_key(ds1):
				out.debug('methu adnabod y ddeusain %s', ds1)
		if len(c2) > 1:
			ds2 = c2.llinyn()
			if not cy.dosbarth_deusain.has_key(ds2):
				out.debug('methu adnabod y ddeusain %s', ds2)
								
		# llafariaid sengl
		if len(c1) == 1 and len(c2) == 1:
			if (trwm_ac_ysgafn and c1[0].llinyn == c2[0].llinyn) or (not trwm_ac_ysgafn and c1[0].hir2byr() == c2[0].hir2byr()):
				mae_odl = True
				if debug:
					print '>> llafariad+llafariad yn cyfateb: odl >>> ' + s1 + '/' + s2
			elif c1[0] != c2[0] and pwysau(c1[0]) == pwysau(c2[0]):
				mae_proest = True
				if debug:
					print '>> llafariad+llafariad o\'r un pwysau: proest >>> ' + s1 + '/' + s2
			else:
				pass
		
		# llafariad sengl a deusain talgron
		if len( c1 ) == 1 and len( c2 ) > 1 and ds2 and ds2 in cy.deuseiniaid['talgron']:
			if c1[0].hir2byr() == c2[1].hir2byr():
				mae_odl = True
				if debug:
					print '>> llafariad+deusain-talgron yn cyfateb: odl >>> ' + s1 + '/' + s2
			elif pwysau( c1[0] ) == pwysau( c2[1] ):
				mae_proest = True
				if debug:
					print '>> llafariad+deusain-talgron o\'r un pwysau: proest >>> ' + s1 + '/' + s2
			else:
				pass
		
		# deusain talgron a llafariad sengl
		if len( c1 ) > 1 and len( c2 ) == 1 and ds1 and ds1 in cy.deuseiniaid['talgron']:
			if c1[1].hir2byr() == c2[0].hir2byr():
				mae_odl = True
				if debug:
					print '>> deusain-talgron+llafariad yn cyfateb: odl >>> ' + s1 + '/' + s2
			elif pwysau( c1[1] ) == pwysau( c2[0] ):
				mae_proest = True
				if debug:
					print '>> deusain+llafariad o\'r un pwysau: proest >>> ' + s1 + '/' + s2
			else:
				pass
		
		# dwy ddeusain
		if len(c1) > 1 and len(c2) > 1:
			# print cy.dosbarth_deusain[ds1]
			# print cy.dosbarth_deusain[ds2]
			if ds1 and ds1 in cy.deuseiniaid['talgron']	and ds2 and ds2 in cy.deuseiniaid['talgron']:
				if c1[1].llinyn == c2[1].llinyn:
					mae_odl = True
					if debug:
						print '>> deusain-talgron+deusain-talgron yn cyfatb: odl >>>' + s1 + '/' + s2

			elif ds1 and ds1 in cy.deuseiniaid['lleddf'] and ds2 and ds2 in cy.deuseiniaid['lleddf']:
				if c1 == c2:
					mae_odl = True
					if debug:
						print '>> deusain-lleddf+deusain-lleddf yn cyfatb: odl >>>' + s1 + '/' + s2
				elif c1 != c2 and cy.dosbarth_deusain[ds1] == cy.dosbarth_deusain[ds2]:
					mae_proest = True
					if debug:
						print '>> deusain-lleddf+deusain-lleddf o\'r un dosbarth: proest >>> ' + s1 + '/' + s2
				else: 
					pass
	if debug:
		if mae_odl:			print 'odl'
		elif mae_proest:	print 'proest'
		else:				pass
		
	# diweddeb
	if (mae_odl and not proest) or (mae_proest and proest):
		nodau_odl1 = [nod for nod in c1+clymau1[-1]]
		nodau_odl2 = [nod for nod in c2+clymau2[-1]]
		return (nodau_odl1, nodau_odl2)
	else:
		return None

def oes_odl_ddwbl(nodau1, nodau2):
	'''
	ffwythiant: oes_odl_ddwbl
	'''
	if any([nod.isspace() for nod in nodau1]) or any([nod.isspace() for nod in nodau2]):
		return None
		
	odl_un = oes_odl_sengl(nodau1,nodau2)
	if odl_un:
		clymau1 = nodau1.rhestr_clymau(trwsio=True)
		clymau2 = nodau2.rhestr_clymau(trwsio=True)
		if len(clymau1) > 2 and len(clymau2) > 2:
			nodau3 = RhestrNodau([ nod for cwlwm in clymau1[:-2] for nod in cwlwm ])
			nodau4 = RhestrNodau([ nod for cwlwm in clymau2[:-2] for nod in cwlwm ])
			odl_dau = oes_odl_sengl(nodau3,nodau4)
			if odl_dau:
				return (odl_dau[0] + odl_un[0], odl_dau[1] + odl_un[1] )
	return odl_un



def oes_odl(cyntaf, ail, olynydd=None, trwm_ac_ysgafn=True):
	# rhaid i cyntaf, ail ac olynydd fod yn rhestri nodau
	if type(cyntaf)==Gair:
		cyntaf = cyntaf.nodau
	if type(ail)==Gair:
		ail = ail.nodau
	# if olynydd and type(olynydd)==Gair:
	# 	olynydd = olynydd.nodau
	nodau1 = RhestrNodau([ nod for nod in cyntaf ])
	nodau2 = RhestrNodau([ nod for nod in ail ])
	if not nodau1 or not nodau2:
		return None

	if debug:
		print 'oes_odl: ' + str(nodau1) + '/' + str(nodau2)

	syl = []

	# profi am odl sengl
	od = oes_odl_sengl(nodau1, nodau2, trwm_ac_ysgafn=trwm_ac_ysgafn)
	if od:
		return od, syl

	# --------------------------------
	# profi am odl gudd neu odl ewinog 
	# angen atal y peiriant rhag odli nod gyda'i hun.
	# hac: edrych ond ar eiriau olynol sy'n dechrau â chytsain
	if type(olynydd)==Gair and len(olynydd.nodau) > 0 and olynydd.nodau[0].iscytsain():

		# profi am odl gudd
		nodau3 = list(nodau1)	
		meddalu = False
		# print nodau1[-1].llinyn
		# print olynydd.nodau[0].llinyn.lower()
		# print cy.cytseiniaid_meddalu
		if nodau1[-1].llinyn in cy.cytseiniaid_meddalu and olynydd.nodau[0].llinyn.lower() == 'd':
			meddalu = True
			nodau3.append(Nod('t'))
		else:
			nodau3.append(olynydd.nodau[0])
			
		nodau3 = RhestrNodau(nodau3)

		# if debug:
			# print '++++++++++'
			# n3 = list(nodau1)
			# print [nod.llinyn for nod in n3]
			# n3.append( olynydd.nodau[0] )
			# print [nod.llinyn for nod in n3]
			# 
			# print olynydd.nodau[0].llinyn
			# print nodau1
			# print nodau2
			# print nodau3
			# print RhestrNodau(n3)

		cudd = oes_odl_sengl(nodau3, nodau2, trwm_ac_ysgafn=trwm_ac_ysgafn)
		dau_gytsain = False
		if len(olynydd.nodau) > 1 and olynydd.nodau[1].iscytsain(): # hac
			nodau4 = list(nodau3)
			nodau4.append( olynydd.nodau[1] )
			nodau4 = RhestrNodau(nodau4)
			cudd2 = oes_odl_sengl(nodau4, nodau2, trwm_ac_ysgafn=trwm_ac_ysgafn)	
			if cudd2:
				dau_gytsain = True
				cudd = cudd2
		if cudd:
			if meddalu:
				cudd[0].pop()
				cudd[0].append( olynydd.nodau[0] )
				if dau_gytsain:
					cudd[0].append( olynydd.nodau[1] )
			s0 = ''.join([nod.llinyn for nod in cudd[0]])						
			s1 = ''.join([nod.llinyn for nod in cudd[1]])						
			# syl.append('odl gudd: ' + s0 + '/' + s1)
			syl.append('odl gudd')
			return (cudd, syl) 
	
		# profi am odl ewinog (dim ond cytsain gyntaf yr olynydd)
		# method: amnewid e.e. (b,h) gan wrthrych newydd Nod('p')
		# yna os oes odl, amnewid y nodau gwreidiol am y nod newydd
		c1 = nodau1[-1].llinyn
		c2 = olynydd.nodau[0].llinyn
		if cy.dosbarth_ceseiliad.has_key( (c1,c2) ):
			llinyn_cyfwerth = cy.dosbarth_ceseiliad[ (c1,c2) ]
			if debug:
				print('oes_odl: paru_cytseiniaid: ' + c1 + '+' + c2 +  '=' + llinyn_cyfwerth )
			nod_newydd = Nod( llinyn_cyfwerth )
			nodau3 = RhestrNodau(list(nodau1[:-1])+[nod_newydd] )
			ewi = oes_odl_sengl( nodau3, nodau2, trwm_ac_ysgafn=trwm_ac_ysgafn )
			if ewi:
				# syl.append('odl ewinog')
				ewi[0].pop()
				ewi[0].append( nodau1[-1] )
				ewi[0].append( olynydd.nodau[0] )
				s0 = ''.join([nod.llinyn for nod in ewi[0]])						
				s1 = ''.join([nod.llinyn for nod in ewi[1]])						
				# syl.append('odl ewinog: ' + s0 + '/' + s1)
				syl.append('odl ewinog')
				return ewi, syl

	return None, None

def oes_proest(g1,g2):	
	pr = oes_odl_sengl(g1.nodau, g2.nodau, proest=True)
	sy = ''
	return pr, sy

def oes_odl_lusg(cyntaf, ail, olynydd=None):
	'''
	ffwythiant: oes_odl_lusg
	'''
	
	# rhaid i'r ail air fod yn lluosill
	if ail.nifer_sillau() < 2:
		return False
	
	# clymau
	clymau1 = cyntaf.nodau.rhestr_clymau(trwsio=True)
	clymau2 = ail.nodau.rhestr_clymau(trwsio=True)

	# tocio cynffon yr ail air (y ddau gwlwm olaf)
	clymau2.pop()
	clymau2.pop()
	if debug:
		print clymau1
		print clymau2

	# nodau'r gair cyntaf
	nodau1 = cyntaf.nodau

	# nodau pen blaen yr ail air
	nodau2 = RhestrNodau([ nod for cwlwm in clymau2 for nod in cwlwm ])
	
	# gwirio am odl rhwng y cyntaf a phen blaen yr ail
	return oes_odl(nodau1, nodau2, olynydd, trwm_ac_ysgafn=False)	


def llinyn_odl( g1, g2, olynydd=None, llusg=False, proest=False, blanksymbol='.'):
	if debug:
		print g1.clymau
		print g2.clymau
	if proest:
		odl = oes_proest(g1,g2)
	elif llusg:
		odl = oes_odl_lusg(g1,g2,olynydd=olynydd)
	else:
		odl = oes_odl(g1,g2,olynydd=olynydd)
	if odl:
		od = odl[0]
		sy = odl[1]
	else:
		od = None
		sy = None
	ss1 = []
	for nod in g1.nodau:
		if od and any([ nod is nod_odl for nod_odl in od[0] ]):
			ss1.append(nod.llinyn)
		else:
			ss1.append( blanksymbol*len( nod.llinyn ) )
	ss2 = []
	for nod in g2.nodau:
		if od and any([ nod is nod_odl for nod_odl in od[1] ]):
			ss2.append(nod.llinyn)
		else:
			ss2.append( blanksymbol*len( nod.llinyn ) )
		
	ss3 = []	
	if olynydd:
		for nod in olynydd.nodau:
			if od and any([ nod is nod_odl for nod_odl in od[0] ]):
				ss3.append(nod.llinyn)
			else:
				ss3.append( blanksymbol*len( nod.llinyn ) )
			
	s = g1.llinyn() 
	if olynydd:
		s += '+' + olynydd.llinyn() 
	s += '/' + g2.llinyn() + '\n'
	
	s += ''.join(ss1) 
	if olynydd:
		s += ' ' + ''.join(ss3) 
	s += '/' +	 ''.join(ss2) + '\n'
	
	if sy:
		s += '\n'.join(sy)
	return s

#------------------------------------------------
# TEST

def main():
	print 'odl.py'

	s1 = ''
	s2 = ''

	# s1 = 'bedw'
	# s2 = 'dedwydd'

	# s1 = 'berw'
	# s2 = 'derwydd'

	# # s1 = 'feinion'
	# # s2 = 'aflonydd'

	# # s1 = 'rhew'
	# # s2 = 'distewi'

	# # s1 = 'didranc'
	# # s2 = 'ieuanc'

	# # s1 = 'gwyrddliw'
	# # s2 = 'wiw'
	
	if s1 and s2:
		print llinyn_odl( Gair(s1), Gair(s2), lusg=True)
		return


	odlau = {
		'odlau_cyflawn': (
			('cath','math'),
			('pren','llen'),
			('mafon','duon'),		# deusain ddwbl
			('calon','creulon'),
			('gwlad', 'cariad'),
			('galwad','cariad'),	# dwy ddeusiain talgron
		),
		'odlau_llusg': (
			('beiddgar','cariad'),
			('tawel','heli'),
		),
		'odlau_llafarog': (
			('tro','llo'),
			('cadno','banjo'),
		),
		'proestau_cyflawn': (
			('hen','dyn'),
			('llawn','mewn'),
			('telyn','ystyrlon'),
		),
		'proestau_llafarog': (
			('tew','byw'),
			('bro','da'),
		),
		'odlau_llusg': (
			('beiddgar','cariad'),
			('morfudd','cuddio'),
			('tawel','heli'),
		),
		'odlau_llusg_cudd': (
			('yma', 'bu','cydnabod'),
			('wele','lid','gelyn'),
			('ddifa','lawer','calon'),
			('wiw','dyfiant','liwdeg'),
			('wele','wychder','Dewi'),
			('ddinas','draw','wastraff'),
		),
		'odlau_llusg_ewinog': (
			('wyneb','haul','Epynt'),
			('esgob','biau','popeth'),
			('nghariad','hyd','ato'),
			('garreg','hon','eco'),
		),
		'dim_odlau': (
			('beic','haul'),
		),
	}

	for key in [
			# 'odlau_cyflawn', 
			# 'odlau_llafarog', 
			# 'proestau_cyflawn', 
			# 'proestau_llafarog', 
			# 'odlau_llusg', 
			# 'odlau_llusg_ewinog', 
			'odlau_llusg_cudd', 
			# 'dim_odlau', 
		]:
		val = odlau[key]
		print '=============================='
		print key.upper()
		print '=============================='
		for s1,s2 in val:
			print '--------------------'
			print s1 + '/' + s2
			
			if key == 'odlau_llusg':
				print llinyn_odl( Gair(s1), Gair(s2), llusg=True )
			
			elif key in [ 'proestau_cyflawn', 'proestau_llafarog' ]:
				print llinyn_odl( Gair(s1), Gair(s2), proest=True )			
			
			elif key in ['odlau_llusg_cudd', 'odlau_llusg_ewinog']:
				print llinyn_odl( Gair(s1), Gair(s3), olynydd=Gair(s2), llusg=True )
			
			else:
				print llinyn_odl( Gair(s1), Gair(s2) )
	# 
	# 
	# odlau_triphlyg = {
	# 	'odlau_llusg_cudd': (
	# 		('yma', 'bu','cydnabod'),
	# 		('wele','lid','gelyn'),
	# 		('ddifa','lawer','calon'),
	# 		('wiw','dyfiant','liwdeg'),
	# 		('wele','wychder','Dewi'),
	# 		('ddinas','draw','wastraff'),
	# 	),
	# 	'odlau_llusg_ewinog': (
	# 		('wyneb','haul','Epynt'),
	# 		('esgob','biau','popeth'),
	# 		('nghariad','hyd','ato'),
	# 		('garreg','hon','eco'),
	# 	),
	# }
	# 
	# for key in [
	# 		'odlau_llusg_ewinog', 
	# 		'odlau_llusg_cudd', 
	# 	]:
	# 	val = odlau_triphlyg[key]
	# 	print '=============================='
	# 	print key.upper()
	# 	print '=============================='
	# 	for s1,s2,s3 in val:
	# 		print '--------------------'
	# 		print s1 + '+' + s2 + '/' + s3
	# 		if key in ['odlau_llusg_cudd', 'odlau_llusg_ewinog']:
	# 			print llinyn_odl( Gair(s1),Gair(s3), olynydd=Gair(s2), llusg=True )
	# 		else:
	# 			print llinyn_odl(Gair(s1),Gair(s3), olynydd=Gair(s2))
	# 

	return

if __name__ == '__main__': 
	main()
	