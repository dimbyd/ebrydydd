#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' 
cytseinedd.py
	darganfod cytseinedd rhwng dau restr nodau

	TRA: Traws 
		Rhaid cael o leiaf un gytsain o flaen acen yr orffwysfa

	TRF: Traws Fantach
		Traws gyda'r orffwysfa ar y sill gyntaf. 

	COG: Croes o Gyswllt
		1. cytsain olaf y rhan gyntaf i ateb cytsain wreiddgoll
		2. dwy gytsain olaf y rhan gyntaf i ateb dwy gytsain wreiddgoll
		Nid yw'n bwysig os yw'r cytseiniaid a fenthycir yn dod cyn yr acen neu beidio, dim ond iddynt ddod yn yr un drefn.

	EITHRIADAU:
		Nid oes angen ateb y gytsain 'h'
		Gellir ateb r gyda rh, neu s gyda sh
		
	CDI: rhaid hefyd cyfateb y cytseiniaid rhwng y ddwy acen

	ADI: rhaid cyfateb y cytseiniaid ar ol acen yr orffwysfa gyda'r cytseiniaid rhwng acenion y brifodl
	
	CDI/ADI: os yw acen yr orffwysfa yn llafarog (h.y. heb gytsain o gwbl), rhai i acen y brifodl hefyd fod yn llafarog
		h.y. dim cytsain rhwng y ddau bwyslais (Cain yw awen cân eos)
	
'''
import cysonion as cy
from nodau import Nod, RhestrNodau
from gair import Gair
# from odl import oes_odl

import logging
out = logging.getLogger(__name__)

global debug
debug = False

def cyfateb(s1, s2):
	s1 = s1.lower()
	s2 = s2.lower()

	if s1 == s2:
		return True, '' 
	elif s1 == 'r' and s2 == 'rh':
		return True, 'r-yn-ateb-rh'
	elif s1 == 'rh' and s2 == 'r':
		return True, 'rh-yn-ateb-r'
	elif s1 == 's' and s2 == 'sh':
		return True, 's-yn-ateb-sh'
	elif s1 == 'sh' and s2 == 's':
		return True, 'sh-yn-ateb-s'
	elif s1 == 'ph' and s2 == 'ff':
		return True, 'ph-yn-ateb-ff'
	elif s1 == 'ff' and s2 == 'ph':
		return True, 'ff-yn-ateb-ph'
	else:
		return False, ''

def paru_cytseiniaid(x_nodau, y_nodau):
	'''
	ffwythiant: ceisio paru dau restr nodau
	mewnbwn:	dau restr geiriau
	allbwn:		dosbarth cytseinedd (neu dosbarth bai)
	sylwadau:
	'''
	if debug:
		print 'ffwythiant: paru_cytseiniaid'
		
	if not x_nodau or not y_nodau:
		return [],[Nod('phantom')],[Nod('phantom')],['dim nodau']
		
	# ffwythiant i echdynnu rhestr cytseiniaid o'r rhestr nodau
	def rhestr_cytseiniaid(rhestr_nodau):
		xx = list(rhestr_nodau)
		xx.reverse()
		x_list = []
		while xx:
			pre = []
			nod = xx.pop()
			while xx and not nod.iscytsain():
				pre.append(nod)
				nod = xx.pop()
			if nod.iscytsain():
				x_list.append( (nod, pre) )
		return x_list

	x_list = rhestr_cytseiniaid(x_nodau)
	y_list = rhestr_cytseiniaid(y_nodau)


	# info
	if debug:
		print '__________________'
		# for a,b in x_list:
		#	print a.llinyn + '\t' + str([nod.llinyn for nod in b])
		print ' '.join([ a.llinyn for a,b in x_list])
		print '________'
		# for a,b in y_list:
		#	print a.llinyn + '\t' + str([nod.llinyn for nod in b])
		print ' '.join([ a.llinyn for a,b in y_list])
		print '__________________'

	# pan nad oes cytseiniaid ...
	if not x_list and not y_list:
		return [], [], [], ['dim cytseiniaid o gwbl']
	elif not x_list and y_list:
		return [], [], [a for a,b in y_list], ['dim cytseiniaid yn y rhestr cyntaf']
	elif x_list and not y_list:
		return [], [a for a,b in x_list], [], ['dim cytseiniaid yn yr ail restrs']
	else:
		pass

	
	# init
	sylwadau = []
	parau = []
	
	# mae o leiaf un gytsain yn y ddwy restr erbyn hyn
	x_curr, x_pre = x_list.pop()
	y_curr, y_pre = y_list.pop()
	
	# prif ddolen
	while x_curr and y_curr:
		x_inter = x_pre
		y_inter = y_pre
		x_prev, x_pre = x_list.pop() if x_list else (None, None)
		y_prev, y_pre = y_list.pop() if y_list else (None, None)
		
		if debug:
			print '--------------------'
			xs = x_prev.llinyn if x_prev else ' '
			ys = y_prev.llinyn if y_prev else ''
			print 'x_prev: ' + xs + '\t x_curr: ' + x_curr.llinyn + '\t x_inter:' + ''.join([ nod.llinyn for nod in x_inter ])
			print 'y_prev: ' + ys + '\t y_curr: ' + y_curr.llinyn + '\t y_inter:' + ''.join([ nod.llinyn for nod in y_inter ])

			print 'x: (%s,%s)' % (xs, x_curr.llinyn)
			print 'y: (%s,%s)' % (ys, y_curr.llinyn)
		
		# ceseiliad yn y nodau chwith
		x_dosb = None
		if x_prev and all(nod.isspace() for nod in x_inter) and cy.dosbarth_ceseiliad.has_key( (x_prev.llinyn, x_curr.llinyn) ):
			x_dosb = cy.dosbarth_ceseiliad[ (x_prev.llinyn, x_curr.llinyn) ]
			out.debug('paru_cytseiniaid: x_dosb: ' + str(x_dosb))

		# ceseiliad yn y nodau dde
		y_dosb = None
		if y_prev and all(nod.isspace() for nod in y_inter) and cy.dosbarth_ceseiliad.has_key( (y_prev.llinyn, y_curr.llinyn) ):
			y_dosb = cy.dosbarth_ceseiliad[ (y_prev.llinyn, y_curr.llinyn) ]
			out.debug('paru_cytseiniaid: y_ces: ' + str(y_dosb))
		
		# ceseiliad ar y chwith a'r dde
		if x_dosb and y_dosb and not any(nod.iscytsain() for nod in x_inter) and not any(nod.iscytsain() for nod in y_inter):
			cyf, syl = cyfateb(x_dosb,y_dosb)
			if syl: sylwadau.append(syl)
			if cyf:
				parau.append([ x_curr, y_curr ])
				parau.append([ x_curr, y_prev ])
				parau.append([ x_prev, y_curr ])
				parau.append([ x_prev, y_prev ])
				sylwadau.append(x_prev.llinyn + '/'+ x_curr.llinyn + '-yn-ateb-' + y_prev.llinyn + '/' + y_curr.llinyn)
				x_curr = x_prev
				x_prev, x_inter = x_list.pop() if x_list else (None, None)
				y_curr = y_prev
				y_prev, y_inter = y_list.pop() if y_list else (None, None)
		
		# ceseiliad ar y chwith
		elif x_dosb and not y_dosb and not any(nod.iscytsain() for nod in x_inter):
			cyf, syl = cyfateb(x_dosb, y_curr.llinyn)
			if syl: sylwadau.append(syl)
			if cyf:
				parau.append([ x_curr, y_curr ])
				parau.append([ x_prev, y_curr ])
				sylwadau.append(x_prev.llinyn + '/' + x_curr.llinyn + '-yn-ateb-' + y_curr.llinyn)
				x_curr = x_prev
				x_prev, x_inter = x_list.pop() if x_list else (None, None)
			
		# ceseiliad ar y dde
		elif not x_dosb and y_dosb and not any(nod.iscytsain() for nod in y_inter):
			cyf, syl = cyfateb(x_curr.llinyn, y_dosb)
			if syl: sylwadau.append(syl)
			if cyf:
				parau.append([ x_curr, y_curr ])
				parau.append([ x_curr, y_prev ])
				sylwadau.append(x_curr.llinyn + '-yn-ateb-' + y_prev.llinyn + '/' + y_curr.llinyn)
				y_curr = y_prev
				y_prev, y_inter = y_list.pop() if y_list else (None, None)

		# dim ceseilio (felly cymharu x_curr a y_curr)
		else:
			cyf, syl = cyfateb(x_curr.llinyn, y_curr.llinyn)
			if syl: sylwadau.append(syl)
			if cyf:
				# x_curr a y_curr yn cyfateb
				parau.append([ x_curr, y_curr ])
				# un-yn-ateb-dau
				if y_prev and (x_curr.llinyn == y_prev.llinyn) and not any(nod.iscytsain() for nod in y_inter):
					if not x_prev or x_prev and not (x_prev.llinyn == y_prev.llinyn):
						parau.append([ x_curr,y_prev ])
						sylwadau.append( x_curr.llinyn + '-yn-ateb-' + y_curr.llinyn + '/' + y_prev.llinyn )
						y_curr = y_prev
						y_prev, y_inter = y_list.pop() if y_list else (None, None)
			
				# dau-yn-ateb-un
				if x_prev and (x_prev.llinyn == y_curr.llinyn) and not any(nod.iscytsain() for nod in x_inter):
					if not y_prev or y_prev and not (x_prev.llinyn == y_prev.llinyn):
						parau.append([ x_prev, y_curr ])
						sylwadau.append( x_curr.llinyn + '/' + x_prev.llinyn + '-yn-ateb-' + y_curr.llinyn)
						x_curr = x_prev
						x_prev, x_inter = x_list.pop() if x_list else (None, None)

			# dim cyfatebiaeth o hyd
			else:
				# h-heb-ei-hateb
				if x_curr and y_curr and x_curr.llinyn == 'h' and y_curr.llinyn != 'h':
					sylwadau.append('h-heb-ei-hateb')
					x_curr = x_prev
					x_prev, x_inter = x_list.pop() if x_list else (None, None)
					continue
				elif x_curr and y_curr and x_curr.llinyn != 'h' and y_curr.llinyn == 'h':
					sylwadau.append('h-heb-ei-hateb')
					y_curr = y_prev
					y_prev, y_inter = y_list.pop() if y_list else (None, None)
					continue
				else:
					if debug:
						print 'dim cyfatebiaeth lawn'
					# hack: pan nad yw'r ddwy gytsain gyntaf yn cyfateb
					x_prev = x_curr
					y_prev = y_curr
					break

		# meddalu (c+t-> d)
		if x_prev and len(x_inter) == 0:
			if x_curr == 't' and y_curr == 'd' and x_prev in cy.cytseiniaid_meddalu:		
				parau.append([ x_curr, y_curr ])
				sylwadau.append( x_prev.llinyn + '+' + x_curr.llinyn + '-yn-ateb-' + y_curr.llinyn )
		
		elif y_prev and len(y_inter) == 0:
			if x_curr == 'd' and y_curr == 't' and y_prev in cy.cytseiniaid_meddalu:		
				parau.append([ x_curr, y_curr ])
				sylwadau.append( x_curr.llinyn + '-yn-ateb-' + y_prev.llinyn + '+' + y_curr.llinyn	)
		else:
			pass # dim meddalu


		# symud i'r nesaf
		x_curr = x_prev
		y_curr = y_prev
	
	
	# info
	out.debug( 'x_list:' + str(x_list) )
	out.debug( 'y_list:' + str(y_list) )
	
	# casglu'r gweddill (heb anghofio'r x_prev neu y_prev sydd heb eu prosesu)
	x_pen = [x_prev] if x_prev and x_prev.llinyn not in ['h','H'] else []
	while x_list: 
		par = x_list.pop()
		if par[0].llinyn not in ['h','H']:
			x_pen.append( par[0] )

	# if debug:
	#	print [nod.llinyn for nod in x_pen]
	# 
	y_pen = [y_prev] if y_prev and y_prev.llinyn not in ['h','H'] else []
	while y_list: 
		par = y_list.pop()
		if par[0].llinyn not in ['h','H']:
			y_pen.append( par[0] )

	# if debug:
	#	print [nod.llinyn for nod in y_pen]
	# 
	return parau, x_pen, y_pen, sylwadau

		
def oes_cytseinedd( x_geiriau, y_geiriau ):
	'''
	ffwythiant: darganfod cytseinedd rhwng dau restr geiriau
	mewnbwn:	dau restr geiriau
	allbwn:		dosbarth cytseinedd (neu dosbarth bai)
	sylwadau:
		mae'r ffwythiant yn traeannu'r ddau restr geiriau: 
			x_blaen, x_canol, x_cwt
			y_blaen, y_canol, y_cwt
		ac yn ceisio darganfod cytseinedd rhwng
			x_blaen a y_blaen
			x_canol a y_canol
		data:
			parau			parau cytseiniaid rhwng x_blaen a y_blaen
			parau_canol		parau cytseiniaid rhwng x_canol a y_canol
			x_pen:			n-wreiddgoll, cytseiniaid pengoll
			y_pen:			n-ganolgoll, cytseiniaid traws
			x_cwt:
			y_cwt:
			
	cynghanedd drychben:

	anghytbwys ddisgynedig: rhaid cyfateb x_cwt a y_canol
		methiant os

		if aceniad == ADI and x_cwt.llinyn in cyfuniadau_trychben:
			nod = x_cwt.pop()
			y_blaen.reverse()
			y_blaen.append( nod )
			y_blaen.reverse()
			
	'''
	if not x_geiriau or not y_geiriau:
		return (None, None, None)
		
	# type check (rhoi gair unigol mewn rhestr)
	if type(x_geiriau)==Gair:
		x_geiriau = [ x_geiriau ]
	if type(y_geiriau)==Gair:
		y_geiriau = [ y_geiriau ]

	# if debug:
	#	print '-------------------------'
	#	print 'ffwythiant: oes_cytseinedd'
	#	# print [g.llinyn() for g in x_geiriau]
	#	# print [g.llinyn() for g in y_geiriau]
	#	print ' '.join([ g.llinyn() for g in x_geiriau ]) + '/' + ' '.join({ g.llinyn() for g in y_geiriau })
	
	# info
	sx = ' '.join([ g.llinyn() for g in x_geiriau ]) 
	sy = ' '.join([ g.llinyn() for g in y_geiriau ])
	out.info('oes_cytseinedd: ' + sx + '/' + sy)
	if debug:
		print 'oes_cytseinedd: ' + sx + '/' + sy
	
	# rhestri nodau
	x_blaen, x_canol, x_cwt = x_geiriau[-1].traeannu()
	y_blaen, y_canol, y_cwt = y_geiriau[-1].traeannu()
	
	# print x_blaen
	# print y_blaen
	# print '++++++++'
	# print '|'.join([nod.llinyn for nod in x_blaen])
	# print '|'.join([nod.llinyn for nod in y_blaen])
	# print [nod.llinyn for nod in y_blaen]
	
	# estyn pen-blaen y ddwy hanner (dim bylchau)
	# xb = []
	# for g in x_geiriau[:-1]:
	#	xb = xb + list(g.nodau)
	xb = [nod for g in x_geiriau[:-1] for nod in g.nodau]
	x_blaen = xb + list(x_blaen)
	# yb = []
	# for g in y_geiriau[:-1]:
	#	yb = yb + list(g.nodau)
	yb = [nod for g in y_geiriau[:-1] for nod in g.nodau]
	y_blaen = yb + list(y_blaen)


	# info
	if debug:
		print ([nod.llinyn for nod in x_blaen], [nod.llinyn for nod in x_canol], [nod.llinyn for nod in x_cwt])
		print ([nod.llinyn for nod in y_blaen], [nod.llinyn for nod in y_canol], [nod.llinyn for nod in y_cwt])
	
	out.debug(
		''.join( [nod.llinyn for nod in x_blaen] ) 
		+ ':' + ''.join( [nod.llinyn for nod in x_canol] )
		+ ':' + ''.join( [nod.llinyn for nod in x_cwt] )
	)
	out.debug(
		''.join( [nod.llinyn for nod in y_blaen] ) 
		+ ':' + ''.join( [nod.llinyn for nod in y_canol] )
		+ ':' + ''.join( [nod.llinyn for nod in y_cwt] )
	)
	# out.debug([nod.llinyn for nod in y_blaen], [nod.llinyn for nod in y_canol], [nod.llinyn for nod in y_cwt])

	# data ar gyfer y view functions
	data = {'sylwadau': [],}
	
	#--------------------
	# paratoi
	#--------------------

	#--------------------
	# parau canol
	#--------------------
	trychben = []
	cysylltben = []
	parau_canol = []

	# cytbwys ddiacen: cyfateb x_canol a y_canol
	if x_canol and y_canol:
		pa, xp, yp, sy = paru_cytseiniaid(x_canol, y_canol)
		
		# cyfatebiaeth lawn (dim cytseiniaid yn weddill)
		if not xp and not yp:
			parau_canol = pa
		else:
			out.debug('oes_cytseinedd: cytbwys ddiacen: x_canol a y_canol heb gyfateb') 
			return (None, 'XXX', None)			

	# anghytbwys ddisgynedig: cyfateb x_cwt a y_canol
	elif not x_canol and y_canol:
		cc = RhestrNodau(x_cwt).rhestr_clymau()
		x_cwt_llinyn = ''.join([ nod.llinyn for nod in cc[-1] ])
		# print x_cwt_llinyn
		pa, xp, yp, sy = paru_cytseiniaid(x_cwt, y_canol)

		# cyfatebiaeth lawn (dim cytseiniaid yn weddill)
		if not xp and not yp:
			parau_canol = pa
			x_cwt = []
		# profi am gynghanedd drychben
		elif x_cwt_llinyn in cy.cyfuniadau_trychben:
			if debug:
				print 'Profi am gynghanedd drychben'
			nod_trychben = x_cwt.pop()
			pa2, xp2, yp2, sy2 = paru_cytseiniaid(x_cwt, y_canol)
			if not xp2 and not yp2:
				parau_canol = pa2
				trychben.append(nod_trychben)
		# profi am gynghanedd gysylltben:
		elif y_blaen:
			if debug:
				print 'Profi am gynghanedd gysylltben'
			nod_cysylltben = y_blaen[0]
			# print nod_cysylltben.llinyn
			x_cwt_newydd = list(x_cwt)
			x_cwt_newydd.append( nod_cysylltben )
			# print [nod.llinyn for nod in x_cwt_newydd ]
			pa3, xp3, yp3, sy3 = paru_cytseiniaid(x_cwt_newydd, y_canol)
			if not xp3 and not yp3:
				parau_canol = pa3
				cysylltben.append( nod_cysylltben )
			else:
				out.debug('oes_cytseinedd: anghytbwys ddisgynedig: x_cwt a y_canol ddim yn cyfateb') 
				return (None, 'XXX', None)
		else:
			pass
											
	# anghytbwys ddyrchafedig:
	elif x_canol and not y_canol:
		pass
	# cytbwys acenog
	else:
		pass
	
	# print trychben[0].llinyn if trychben else 'dim trychben'
	# print cysylltben[0].llinyn if cysylltben else 'dim cysylltben'
	# print 'parau_canol: ' + ' '.join([ a.llinyn + '/' + b.llinyn for a,b in parau_canol ])
		
	out.debug('parau_canol: ' + ' '.join([ a.llinyn + '/' + b.llinyn for a,b in parau_canol ]) )

	#--------------------
	# parau blaen
	#--------------------
	# print '>>>>>>>DING'
	parau, x_pen, y_pen, syl = paru_cytseiniaid( x_blaen, y_blaen ) 
	if syl:
		data['sylwadau'].extend(syl)
	# print '>>>>>>>DONG'
	# print x_pen
	#--------------------
	# paratoi a chasglu data
	parau.reverse()
	parau_canol.reverse()
	x_cwt = [ nod for nod in x_cwt if nod.iscytsain() ]
	y_cwt = [ nod for nod in y_cwt if nod.iscytsain() ]
	
	data['pengoll_chwith'] = x_pen
	data['pengoll_dde'] = y_pen
	data['parau'] = parau + parau_canol 
	data['cwt_chwith'] = x_cwt
	data['cwt_dde'] = y_cwt
	data['trychben'] = trychben
	data['cysylltben'] = cysylltben
	
	out.debug('pen_ch: ' + ' '.join([ nod.llinyn for nod in data['pengoll_chwith'] ]) )
	out.debug('pen_dd: ' + ' '.join([ nod.llinyn for nod in data['pengoll_dde'] ]) )
	out.debug('parau  : ' + ' '.join([ a.llinyn + '/' + b.llinyn for a,b in data['parau'] ]) )
	out.debug('cwt_ch: ' + ' '.join([ nod.llinyn for nod in data['cwt_chwith'] ]) )
	out.debug('cwt_dd: ' + ' '.join([ nod.llinyn for nod in data['cwt_dde'] ]) )
	out.debug('trychben: ' + ' '.join([ nod.llinyn for nod in data['trychben'] ]) )
	out.debug('cysylltben: ' + ' '.join([ nod.llinyn for nod in data['cysylltben'] ]) )

	#--------------------
	# dosbarthu
	
	# proest i'r odl
	# if x_cwt and y_cwt and cyfateb(x_cwt[-1].llinyn, y_cwt[-1].llinyn):
	#	return (None, 'PRO', data)

	# cyfatebiaeth lawn (croes)
	if parau and not x_pen and not y_pen:
		if trychben:
			return ('CRD', None, data)
		elif cysylltben:
			return ('CRG', None, data)
		else:
			return ('CRO', None, data)
	
	# cytseiniaid chwith yn weddill (n-wreiddgoll, croes-o-gyswllt)
	elif parau and x_pen and not y_pen:

		# n-wreiddgoll
		if len(x_pen) == 1 and x_pen[0].llinyn.lower() == 'n':
			data['sylwadau'].append('n-wreiddgoll')
			if trychben:
				return ('CRD', None, data)
			elif cysylltben:
				return ('CRG', None, data)
			else:
				return ('CRO', None, data)

		# croes-o-gyswllt
		x_nodau = [nod for g in x_geiriau for nod in g.nodau]
		pa, xp, yp, sy = paru_cytseiniaid(x_pen,x_nodau)
		if pa and not xp:
			if len(pa) > 1:
				return ('CGG', None, data)
			else:
				return ('COG', None, data)

		# sain (os oes o leiaf un par yn cyfateb, mae hynny'n ddigon am gynghanedd sain)
		if trychben:
			return ('SAD', None, data)
		elif cysylltben:
			return ('SAG', None, data)
		else:
			return ('SAI', None, data)
			
	# cytseiniaid dde yn weddill (n-ganolgoll, traws)
	elif parau and not x_pen and y_pen:

		# n-ganolgoll
		if len(y_pen) == 1 and y_pen[0].llinyn == 'n':
			data['sylwadau'].append('n-ganolgoll')
			return ('CRO', None, data)
		# traws
		else:
			if len(x_geiriau) == 1 or len(x_geiriau) == 2 and not any(nod.iscytsain() for nod in x_geiriau[0].nodau): # hac
				if trychben:
					return ('TFD', None, data)
				elif cysylltben:
					return ('TFG', None, data)
				else:
					return ('TRF', None, data)
			else:
				if trychben:
					return ('TRD', None, data)
				elif cysylltben:
					return ('TRG', None, data)
				else:
					return ('TRA', None, data)

	# os nad oes parau, o leiaf mae popeth yn sain-lafarog!
	else:
		# if trychben:
		# 	return ('SLD', None, data)
		# elif cysylltben:
		# 	return ('SLG', None, data)
		# else:
		# 	return ('SAL', None, data)
		return ('LLA', None, data)


#------------------------------------------------
# TEST

def main():
	print 'cytseinedd.py'

	# # x = "Can hardd croyw fardd"
	# # y = "Caerfyrddin"
	# x = "ail y carw"
	# y = "olwg gorwyllt"
	# x = "y cawn ar lan"
	# y = "Conwy'r wledd"
	# x = "wleidyddol"
	# y = "hirdymor"
	# # x = 'arolwg'
	# # y = 'chwaraeon'
	# # x = "Hen derfyn"
	# # y = "nad yw'n darfod"
	# x = 'Hyd y tywyn haul,'
	# y = 'duw wyt yn hon.'
	# x = 'wiw'
	# y = 'wead'
	# x = 'ieuanc'
	# y = 'awen'
	# 
	# x = "ond hiroes"
	# y = "yw braint derwen"
	# 
	# x = "Nid yn aml"
	# y = "y down yma"
	# 
	# print x + '/' + y
	# xx = [Gair(s) for s in x.split(' ')]
	# yy = [Gair(s) for s in y.split(' ')]
	# zz = oes_cytseinedd(xx,yy)
	# print zz
	# data = zz[2]
	# print data["sylwadau"]
	# print [x.llinyn for x in data['pengoll_chwith']]
	# print [x.llinyn for x in data['pengoll_dde']]
	# # print [(a.llinyn,b.llinyn) for a,b in data['parau_canol']]
	# print [(a.llinyn,b.llinyn) for a,b in data['parau']]
	# print [x.llinyn for x in data['cwt_chwith']]
	# print [x.llinyn for x in data['cwt_dde']]
	# print [x.llinyn for x in data['trychben']]
	# return
	
	llinynnau = {
		'croes': (
			('Ochain cloch', 'a chanu clir'),
			('Awdur mad', 'a dramodydd'),
			('Am eu hawr', 'yn ymaros'),
		),
		'croes_o_gyswllt': (
			('Daw geiriau duw', "o'i gaer deg"),
			('Aderyn llwyd', 'ar un llaw'),
		),
		'traws': (
			('Ochain cloch', 'a gwreichion clir'),
			('Ei awen brudd', 'dan ein bro'),
		),
		'traws_fantach': (
			('Y brawd', 'o bellafion bro'),
			('Brwd', 'yw aderyn brig')
		),
		'proest_ir_odl':  (
			('dyn a merch', "a dawn a march"),
		),
		'trychben': (
			('Canu mydr', 'cyn ymadael'),
			('Nid yn aml', 'y down yma'),	
			('Ond daw gwefr', 'cyn atgofion'),
			('ei hofn', 'hefyd'),
			('anabl','anniben'),				# methiant: cam-acennu "anabl"
		),
		'cysylltben':  (
			('Yma bu', "nwyf i'm beunydd"),
			('Onid bro', 'dy baradwys'),
			('A ddaw', 'fy mab i Ddyfed'),
			('gwae', 'nid gweniaith'),
		),
	}
	
	for key in [
			# 'croes',
			# 'croes_o_gyswllt',
			# 'traws',
			# 'traws_fantach',
			# 'proest_ir_odl',
			# 'trychben',
			'cysylltben',
		]:
		val = llinynnau[key]
		print '--------------------'
		print key.upper()
		print '--------------------'
		for s1,s2 in val:
			print s1 + ' / ' + s2
			xx = [Gair(s) for s in s1.split(' ')]
			yy = [Gair(s) for s in s2.split(' ')]
			cy, ba, data = oes_cytseinedd( xx, yy )
			print cy
			if data:
				print [ nod.llinyn for nod in data['pengoll_chwith'] ]
				print [ nod.llinyn for nod in data['pengoll_dde'] ]
				print [ (p[0].llinyn, p[1].llinyn) for p in data['parau']]
				print [ nod.llinyn for nod in data['cwt_chwith'] ]
				print [ nod.llinyn for nod in data['cwt_dde'] ]
				print [ nod.llinyn for nod in data['trychben'] ]
				print [ nod.llinyn for nod in data['cysylltben'] ]
				print data['sylwadau']
			print ('==========')

if __name__ == '__main__': 
	main()
