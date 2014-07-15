#!/usr/bin/python
# -*- coding: utf-8 -*-
''' 
odl.py : adnoddau er mwyn darganfod a dosbarthu odl

	AYG: mud, hud, crud; braw, blaw, daw

	cyflawn: y ddwy sill olaf yn cyfateb 
		puro, suro, curo (ur:o)
		gwasgariad, cariad, darpariad (ar:iad)

	anghyflawn: y sill olaf yn cyfateb 
		curo, cludo, heno (:o)
		abad, cariad (:d)

dosbarthiadau:
	odl gyflawn
	proest cyflawn
	odl lafarog
	proest lafarog

nodiant:
	aa - cwlwm llafariad
	bb - cwlwm cytseiniaid
	ds - deusain

RHEOLAU:

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
				
patrwm_odl: 
	C = cytsain, 
	Y = llafariaid_ysgafn, 
	T = llafariaid_trwm,
	0 = deusain talgron,
	1 = deusain lleddf o'r dosbarth cyntaf
	2 = deusain lleddf o'r ail ddosbarth
	3 = deusain lleddf o'r trydydd dosbarth
	4 = deusain lleddf o'r bedwaredd dosbarth
	
TODO:
	odlau cudd
	odlau ewinog

'''

import re
import cysonion as cy
import llinyn as ll
import acen as ac

# from llinyn import nodau, ll.clymau, ysgafn_yn_drwm, llinyn_clymau_dethol
# from acen import nifer_sillau

from lliwiau import coch, piws

global debug
debug = False


def prawf_odl_ddwbl(s1,s2):
	odl_sengl = prawf_odl_sengl(s1,s2)
	c1 = ll.clymau(s1)
	c2 = ll.clymau(s2)
	if odl_sengl and len(c1) > 2 and len(c2) > 2:
		s3 = ''.join( [z for x in c1[:-2] for z in x] )
		s4 = ''.join( [z for x in c2[:-2] for z in x] )
		return prawf_odl_sengl(s3,s4)
	return None


def prawf_odl_sengl(s1,s2):
	clymau1 = ll.clymau(s1, w_gytsain=False)
	clymau2 = ll.clymau(s2, w_gytsain=False)
	
	if not clymau1 or not clymau2:
		return None

	odl = False
	
	# sylfaenol
	if clymau1[-2:] == clymau2[-2:]:
		odl = True
	
	# gwirio os ydyw'r clymau olaf yn cyfateb (clymau cytseiniaid, efallai byddant yn wag)
	if clymau1[-1] == clymau2[-1]:	
		c1 = clymau1[-2]
		c2 = clymau2[-2]
	
		# cywasgu deuseiniaid talgron
		if len(c1) > 1:
			ds1 = ''.join(c1[-2:]).lower()
			if ds1 in cy.deuseiniaid['talgron']:
				c1 = c1[-1:]
		if len(c2) > 1:
			ds2 = ''.join(c2[-2:]).lower()
			if ds2 in cy.deuseiniaid['talgron']:
				c2 = c2[-1:]
							
		# llafariaid sengl
		if len(c1) == 1 and len(c2) == 1 and c1 == c2:
				if debug: print '>> llafariaid sengl yn cyfateb: odl >>> ' + str([ c1, c2 ])
				odl = True
		
		# deuseiniaid lleddf
		if len(c1) > 1 and len(c2) > 1 and c1[-2:] == c2[-2:]:
				if debug: print '>> deuseiniaid yn cyfateb: odl >>>' + str( [c1[-2:], c2[-2:] ])
				odl = True
	if odl:
		m1 = len( [nod for x in clymau1[:-2] for nod in x] )
		n1 = len( [nod for x in clymau1 for nod in x] )
		m2 = len( [nod for x in clymau2[:-2] for nod in x] )
		n2 = len( [nod for x in clymau2 for nod in x] )
		return ( (m1,n1), (m2,n2), )
	return None


def oes_proest(s1,s2):
	if re.search(r'\s', s1) or re.search(r'\s', s2) :	
		return None

	def pwysau(nod):
		if nod in cy.llafariaid_hir:
			return 'Y'
		elif nod in cy.llafariaid_byr:
			return 'T'
		else:
			return None

	clymau1 = ll.clymau(s1, w_gytsain=False)
	clymau2 = ll.clymau(s2, w_gytsain=False)
	
	proest = False
	# gweld os yw'r clymau olaf yn cyfateb (clymau cytseiniaid, efallai yn wag)
	if clymau1[-1] == clymau2[-1]:
		
		c1 = clymau1[-2]
		c2 = clymau2[-2]
		
		# cywasgu deuseiniaid talgron
		if len(c1) > 1:
			ds1 = ''.join(c1[-2:]).lower()
			if ds1 in cy.deuseiniaid['talgron']:
				c1 = c1[-1]
		if len(c2) > 1:
			ds2 = ''.join(c2[-2:]).lower()
			if ds2 in cy.deuseiniaid['talgron']:
				c2 = c2[-1]
				
		# llafariaid sengl (neu deuseiniaid talgron wedi eu cywasgu)
		if len(c1) == 1 and len(c2) == 1 and c1 != c2 and pwysau(c1) == pwysau(c2):
			proest = True
			
		# deuseiniaid lleddf
		if len(c1) > 1 and len(c2) > 1 and c1 != c2 and cy.dosbarth_deusain[ds1] == cy.dosbarth_deusain[ds2]:
			proest = True
			
	if proest:
		m1 = len( [nod for x in clymau1[:-2] for nod in x] )
		n1 = len( [nod for x in clymau1 for nod in x] )
		m2 = len( [nod for x in clymau2[:-2] for nod in x] )
		n2 = len( [nod for x in clymau2 for nod in x] )
		return ( (m1,n1), (m2,n2), )
	return False


def prawf_odl_lusg(s1,s2):
	if re.search(r'\s', s1) or re.search(r'\s', s2) :	
		return None

	# rhaid i'r ail air fod yn lluosill
	if ac.nifer_sillau(s2) < 2:
		return False
	
	# bai trwm ac ysgafn yn amhosib os oes gair lluosill 
	s1 = ll.ysgafn_yn_drwm(s1)
	s2 = ll.ysgafn_yn_drwm(s2)
	
	clymau1 = ll.clymau(s1)
	clymau2 = ll.clymau(s2)
	
	# torri'r ddau gwlwm olaf (llafariaid, cytseiniaid) oddi ar yr ail linyn
	if clymau1[-1]:				# cwlwm olaf y gair cyntaf yn gwlwm cytseiniaid
		clymau2 = clymau2[:-2]
	else:						# cwlwm olaf y gair cyntaf yn gwlwm llafariaid
		clymau2 = clymau2[:-3]
	
	# ail-greu pen blaen yr ail linyn
	blaen = ''.join([nod for cwlwm in clymau2 for nod in cwlwm])
	# gwirio am odl rhwng s1 a phen blaen s2
	return prawf_odl(s1,blaen)
	

def llinyn_odl_goch(s1,s2):
	if re.search(r'\s', s1) or re.search(r'\s', s2) :	
		return None
	nodau1 = ll.nodau(s1)
	nodau2 = ll.nodau(s2)
	s = ''
	odl = prawf_odl(s1,s2)
	if not odl:
		odl = oes_proest(s1,s2)
	if odl:
		s += ''.join( [z for x in nodau1[ :odl[0][0] ] for z in x] )
		s += piws( ''.join( [z for x in nodau1[ odl[0][0]:odl[0][1] ] for z in x] ) )
		s += ''.join( [z for x in nodau1[ odl[0][1]: ] for z in x] )
		s += '/'
		s += ''.join( [z for x in nodau2[ :odl[1][0] ] for z in x] )
		s += piws( ''.join( [z for x in nodau2[ odl[1][0]:odl[1][1] ] for z in x] ) )
		s += ''.join( [z for x in nodau2[ odl[1][1]: ] for z in x] )
	return s

def llinyn_odl_lusg_goch(s1,s2):
	if re.search(r'\s', s1) or re.search(r'\s', s2) :	
		return None
	c2 = ll.clymau(s2)
	blaen = ''.join([z for x in c2[:-2] for z in x])
	cwt = ''.join([z for x in c2[-2:] for z in x])
	return llinyn_odl_goch(s1,blaen) + cwt

def prawf_odl(s1,s2):	
	if re.search(r'\s', s1) or re.search(r'\s', s2) :	
		return None
	odl = prawf_odl_ddwbl(s1,s2)
	if not odl:
		odl = prawf_odl_sengl(s1,s2)
	return odl

#------------------------------------------------
# TEST

def main():
	print 'odl.py'
	
	debug = True
	par = ('cath','math')
	par = ('puro','curo')
	par = ('gwlad','cariad')
	par = ('ceffyl mawr drewllyd','mae yn bewllyd')
	print par
	s1 = par[0]
	s2 = par[1]
	print prawf_odl(s1,s2)
	print llinyn_odl_goch(s1,s2)
	# print 'odl sengl: ' + str( prawf_odl_sengl(s1,s2) )
	# print 'odl ddwbl: ' + str( prawf_odl_ddwbl(s1,s2) )
	# print 'proest:    ' + str( oes_proest(s1,s2) )
	# print prawf_odl_lusg('bedw', 'dedwydd')
 	# print prawf_odl_lusg('distaw', 'gwrandawiad')
	# return

	odlau_cyflawn = (
		('cath','math'),
		('pren','llen'),
		('mafon','duon'),		# deusain ddwbl
		('calon','creulon'),
		('gwlad', 'cariad'),
		('galwad','cariad'),	# dwy ddeusiain talgron
	)
	odlau_llusg = (
		('beiddgar','cariad'),
		('tawel','heli'),
	)
	odlau_llafarog = (
		('tro','llo'),
		('cadno','banjo'),
	)
	proestau_cyflawn = (
		('hen','dyn'),
		('llawn','mewn'),
		('telyn','ystyrlon'),
	)
	proestau_llafarog = (
		('tew','byw'),
		('bro','da'),
	)
	dim_odlau = (
		('beic','haul'),
	)
	
	print '--------------------'
	print 'odlau llusg'
	print '--------------------'
	for s1,s2 in odlau_llusg:
		print s1 + '/' + s2
		print prawf_odl_lusg( s1, s2 )
		print llinyn_odl_lusg_goch(s1,s2)
		print '---------------'

	print '--------------------'
	print 'odlau cyflawn'
	print '--------------------'
	for s1,s2 in odlau_cyflawn:
		print s1 + '/' + s2
		print prawf_odl( s1, s2 )
		print llinyn_odl_goch(s1,s2)
		print '---------------'

	print '--------------------'
	print 'odlau llafarog'
	print '--------------------'
	for s1,s2 in odlau_llafarog:
		print s1 + '/' + s2
		print prawf_odl( s1, s2 )
		print llinyn_odl_goch(s1,s2)
		print '---------------'

	print '--------------------'
	print 'proestau cyflawn'
	print '--------------------'
	for s1,s2 in proestau_cyflawn:
		print s1 + '/' + s2
		print prawf_odl( s1, s2 )
		print llinyn_odl_goch(s1,s2)
		print '---------------'

	print '--------------------'
	print 'proestau llafarog'
	print '--------------------'
	for s1,s2 in proestau_llafarog:
		print s1 + '/' + s2
		print prawf_odl( s1, s2 )
		print llinyn_odl_goch(s1,s2)
		print '---------------'

	print '--------------------'
	print 'dim odl na phroest'
	print '--------------------'
	for s1,s2 in dim_odlau:
		print s1 + '/' + s2
		print prawf_odl( s1, s2 )
		print llinyn_odl_goch(s1,s2)
		print '---------------'

if __name__ == '__main__': 
	main()
	