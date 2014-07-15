#!/usr/bin/python
# -*- coding: utf-8 -*-
''' 
acen.py
	adnoddau darganfod acen a phwyslais
	AYG: dyn, cur:o, cel:wydd:og
	AYG: mae'r acen yn disgyn yn naturiol ar gwlwm llafariaid
'''

global debug
debug = True

import re
import cysonion as cy
import llinyn as ll


geiriau_lluosill_acenog = (
	'caniatâu',
	'mawrhad',
	'nesáu',
	'prinhau',
	'rhyddhad',	
)

geiriau_llafariad_hir = (
	'mud',
	'mab',
	'tad',
	'tir',
)

def aceniad(s_chw, s_dde):
	'''
	ffwythiant:	darganfod dosbarth aceniad dau linyn
	mewnbwn:	dau linyn (yr orffwysfa a'r brifodl)
	allbwn:		dosbarth aceniad (CAC,CDI,ADI,ADY)
	sylwadau:
		CAC: cytbwys acennog
			Rhaid i'r cytseiniaid ar ddechrau rhan gyntaf y linell (hyd pwyslais yr orffwysfa),
			gyfateb yn union a'r cytseiniaid ar ddechrau ail ran y linell (hyd pwyslais y brifodl).
		CDI: cytbwys ddiacen
			Fel CAC, ond hefyd rhaid i'r cytseiniaid rhwng acenion yr orffwysfa a'r cytseiniaid
			rhwng acenion y brifodl gyfateb yn union
		ADI: angytbwys ddisgynedig
			Fel CAC, ond hefyd rhaid i'r cytseiniaid rhwng acenion yr orffwysfa a'r 
			cytseiniaid sy'n dilyn acen y brifodl gyfateb yn union
		ADY: angytbwys ddyrchafedig
			Fel CAC, ond hefyd rhaid i'r cytseiniaid sy'n dilyn acen yr orffwysfa a'r 
			cytseiniaid rhwng acenion y brifodl gyfateb yn union
	'''

	if re.search(r'\s', s_chw) or re.search(r'\s', s_dde):
		return None

	pwy1 = pwyslais(s_chw)
	pwy2 = pwyslais(s_dde)
	if pwy1 == -1 and pwy2 == -1:
		return 'CAC'
	elif pwy1 == -1 and pwy2 != -1:
		return 'ADI'
	elif pwy1 != -1 and pwy2 == -1:
		return 'ADY'
	else:
		return 'CDI'

def acenion(s):
	'''
	ffwythiant:	darganfod mynegrifau acenion llinyn
	mewnbwn:	llinyn
	allbwn:		rhestr mynegrifau y llinyn sy'n cynnwys y llafariad sydd yn cario'r acen
	'''
	if re.search(r'\s', s):	
		return None
	
	ace = list()
	clymau = ll.clymau( s )
	
	j=0
	for k in range( len(clymau) ):
		cwlwm = clymau[ k ]
		# prosesu clymau llafariaid yn unig
		if not (k % 2):				
			# dianc os ydy'r cwlwm yn wag
			if not cwlwm:				
				continue
			# llafariad sengl
			if len(cwlwm) == 1:			
				ace.append( j )
			# llafariaid dwbl (deusain)
			elif len(cwlwm) == 2:	
				ds = ''.join(str(c) for c in cwlwm)
				ds = ll.ysgafn_yn_drwm(ds)
				dd = cy.dosbarth_deusain[ds.lower()]
				# deusain talgron (acen ar yr ail lafariad)
				if ds in cy.deuseiniaid['talgron']:				
					ace.append( j+1 )
				# gair deusill (acen ar y ddwy lafariad)
				elif ds in cy.deuseiniaid['deusill']:				
					ace.append( j )
					ace.append( j+1 ) 
				# deusain lleddf (acen ar y llafariad cyntaf)
				else:
					ace.append( j )	
		
			# tri neu fwy o lafariaid: defnyddio'r ail lafariad yn y cwlwm
			else:
				ace.append( j+1 )			
		# symud mynegrif y clymau i ddechrau'r cwlwm nesaf
		j += len(cwlwm)
	return tuple(ace)


def pwyslais(s):
	'''
	ffwythiant:	darganfod pwyslais gair
	mewnbwn:	rhestr nodau
	allbwn:		rhestr nodau
	sylwadau:	
		Mae angen helaethu ar ffyrdd i ddarganfod geiriau acennog lluosill
	'''
	if re.search(r'\s', s):	
		return None
	clymau = ll.clymau(s)
	
	# gwirio am ae o flaen y cwlwm cytseiniaid olaf (e.e. cymraeg)
	c_olaf = clymau[-1]
	c_olaf_ond_un = clymau[-2]
	if c_olaf and len(c_olaf_ond_un)==2 and ''.join(c_olaf_ond_un) == 'ae':
		return -1
	
	# gwirio am h o flaen y cwlwm llafariaid olaf (e.e. dyfalbarhau)
	if len(clymau)>2:
		cc_olaf_ond_un = clymau[-3]
		if cc_olaf_ond_un:
			if cc_olaf_ond_un[-1] == 'h' or cc_olaf_ond_un[-1] == 'rh':
				return -1
	
	# gwirio am lafariad hir fel cwlwm olaf (e.e. cangarŵ)
	if len(clymau)>2 and not clymau[-1] and clymau[-2][-1] in cy.llafariaid_hir:
		return -1
	
	# gwiriad syml
	if nifer_sillau(s) == 1: 
		return -1 # gair unsill
	else:
		return -2 # goben


def nifer_sillau(s):
	if re.search(r'\s', s):	
		return None
	clymau = ll.clymau(s)
	if clymau[0]:
		return len(clymau)/2
	else:
		return len(clymau)/2 -1


def llinyn_acenion(s, blanksymbol=' '):
	if re.search(r'\s', s):	
		return None
	ss = []
	nod = ll.nodau(s)
	ace = acenion(s)
	pwy = pwyslais(s)
	for j in range( len(nod) ):
		if j in ace:
			if j == ace[pwy]:
				ss.append('/')
			else:
				ss.append('v')
		else:
			ss.append( blanksymbol*len( nod[j] ) )
	return ''.join(ss)


def traeannu_cytseiniaid(s):
	'''
	ffwythiant: hollti cytseiniaid gair yn dri
	mewnbwn:	dim
	allbwn:		tri rhestr o glymau cytseiniaid
	sylwadau:
		mae hyn yn tybio fod yr acen yn disgyn ar y goben
		nid yw eto yn traeannu ar sail acen 
	'''	
	clymau = ll.clymau(s)
	pw = pwyslais(s)
	# dim cytseiniaid
	if not filter(None, clymau[1::2]):	
		return [], [], []
	# gair acennog
	if pw == -1:
		t = len(clymau) - 2
		pen = clymau[:t][1::2]
		can = []
		cwt = clymau[t:][1::2]
	# gair diacen
	else:
		t1 = len(clymau) + 2*pw
		t2 = t1 + 2
		pen = clymau[:t1][1::2]
		can = clymau[t1:t2][1::2]
		cwt = clymau[t2:][1::2]
	# datblygu un lefel
	pen = [y for x in pen for y in x]
	can = [y for x in can for y in x]
	cwt = [y for x in cwt for y in x]
	return pen, can, cwt


def traeannu(s, clymau=False):
	'''
	ffwythiant: hollti gair yn dri (pen, bol, cwt)
	mewnbwn:	llinyn
	allbwn:		tri rhestr nodau
	'''	
	cly = ll.clymau(s)
	pwy = pwyslais(s)
	# dim cytseiniaid
	if not filter(None, cly[1::2]):	
		return [], [], []
	# gair acennog
	if pwy == -1:
		pen = cly[:-2]
		can = []
		cwt = cly[-2:]
	# gair diacen
	else:
		pen = cly[:-4]
		can = cly[-4:-2]
		cwt = cly[-2:]
	if not clymau:
		pen = [z for x in pen for y in x for z in y]
		# can = [z for x in can for y in x for z in y]
		# cwt = [z for x in cwt for y in x for z in y]
		can = [z for x in can for z in x]
		cwt = [z for x in cwt for z in x]
	return pen, can, cwt


#------------------------------------------------
# TEST
def main():
	print 'acen.py'

	llinynau = (
		'prydferth',
		'duon',
		'eos',
		'cread',
		'credoau',
		'Dewi',
		'addewid',
		'gwrandawiad',
		'awen',
		'distewi',
		'dramodydd',
		'dyfalbarhad',
		'cymraeg',
		'gwaith',
		'anifeiliaid',
		'haleliwia',
		'gwrando',
		u'cangarŵ',
	)
	for s in llinynau:
		print '-------------------'
		print llinyn_acenion(s)
		print s
		print acenion(s)
		print pwyslais(s)

	# parau = (
	# 	('ci','drwg'),			# CAC
	# 	('blodyn','pert'),		# ADI
	# 	('ci','drewllyd'),		# CAC
	# 	('blodyn','banana'),	# CDI
	# )
	# for s1,s2 in parau:
	# 	print '--------------------'
	# 	print s1 + ' / ' + s2
	# 	print aceniad( s1, s2 )

if __name__ == '__main__': 
	main()