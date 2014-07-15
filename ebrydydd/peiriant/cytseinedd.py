# coding=utf-8
''' 
cytseinedd.py
	darganfod cytseinedd rhwng dau linyn

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
		** gwyliwch am w-gytsain **
		
	cytsain-cytsain
	cytsain-par_cyffelyb (heb gytsain rhyngddynt)
	c=g/g (heb gytsain na llafariad rhyngddynt)
	p=b/b
	t=d/d
		
	
'''
from llinyn import nodau, clymau
from acen import traeannu_cytseiniaid, traeannu
from odl import prawf_odl

import cysonion as cy
import llinyn as ll
import acen as ac
import odl as od

global debug
debug = False

def cyfateb(c1, c2):
	c1 = c1.lower()
	c2 = c2.lower()
	if c1 == c2:
		return True, ''	
	elif c1 == 'r' and c2 == 'rh':
		return True, 'r-yn-ateb-rh'
	elif c1 == 'rh' and c2 == 'r':
		return True, 'rh-yn-ateb-r'
	elif c1 == 's' and c2 == 'sh':
		return True, 's-yn-ateb-sh'
	elif c1 == 'sh' and c2 == 's':
		return True, 'sh-yn-ateb-s'
	elif c1 == 'ph' and c2 == 'ff':
		return True, 'ph-yn-ateb-ff'
	elif c1 == 'ff' and c2 == 'ph':
		return True, 'ff-yn-ateb-ph'
	else:
		return False, ''


def cyfatebiaeth(x,y, reverse=False):
	'''
	ffwythiant: dadansoddi cyfatebiaeth cytseiniaid
	mewnbwn: dau linyn
	allbwn: rhestr o barau mynegrifau nodau
	'''
	sylwadau = []
	
	nodau_x = ll.nodau(x)
	nodau_y = ll.nodau(y)
	
	if reverse:
		nodau_x.reverse()
		nodau_y.reverse()
		
	# print nodau_x
	# print nodau_y
	# print 'len(nodau_x) = ' + str(len(nodau_x))
	# print 'len(nodau_y) = ' + str(len(nodau_y))
	
	parau = []
	ix = 0
	iy = 0
	while ix < len(nodau_x) and nodau_x[ix] not in cy.cytseiniaid: ix = ix + 1
	while iy < len(nodau_y) and nodau_y[iy] not in cy.cytseiniaid: iy = iy + 1
		
	# prif ddolen
	while ix < len(nodau_x) and iy < len(nodau_y):
		# if debug:
		# print '----------'
		# print 'curr: ' + str((nodau_x[ix],nodau_y[iy]))
		# print ix
		# print iy
			
		jx = ix + 1
		while jx < len(nodau_x) and nodau_x[jx] not in cy.cytseiniaid: jx = jx + 1
		
		jy = iy + 1
		while jy < len(nodau_y) and nodau_y[jy] not in cy.cytseiniaid: jy = jy + 1
		
		# h-heb-ei-hateb
		if nodau_x[ix] == 'h' and nodau_y[iy] != 'h':
			sylwadau.append('h-heb-ei-hateb')
			ix = jx
			jx = ix + 1
			while jx < len(nodau_x) and nodau_x[jx] not in cy.cytseiniaid: jx = jx + 1
			continue
		if nodau_x[ix] != 'h' and nodau_y[iy] == 'h':
			sylwadau.append('h-heb-ei-hateb')
			iy = jy
			jy = iy + 1
			while jy < len(nodau_y) and nodau_y[jy] not in cy.cytseiniaid: jy = jy + 1
			continue
		
		# nodau cyntaf yn cyfateb
		cyf = cyfateb(nodau_x[ix], nodau_y[iy])
		if cyf[0]:
			parau.append((ix,iy))
			if cyf[1]: sylwadau.extend(cyf[1])
			
			# un-yn-ateb-dau
			if jy < len(nodau_y) and nodau_x[ix] == nodau_y[jy] and all(c not in cy.cytseiniaid for c in nodau_y[iy+1:jy]):
				if jx < len(nodau_x) and not nodau_x[jx] == nodau_y[jy]:
					parau.append((ix,jy))
					sylwadau.append( str(nodau_x[ix]) + '-yn-ateb-' + str(nodau_y[iy]) + '/' + str(nodau_y[jy]) )
					iy = jy
					jy = iy + 1
					while jy < len(nodau_y) and nodau_y[jy] not in cy.cytseiniaid: jy = jy + 1
					
			# dau-yn-ateb-un
			elif jx < len(nodau_x) and nodau_x[jx] == nodau_y[iy] and all(c not in cy.cytseiniaid for c in nodau_x[ix+1:jx]):
				if jy < len(nodau_y) and not nodau_x[jx] == nodau_y[jy]:
					parau.append((jx,iy))
					sylwadau.append( str(nodau_x[ix]) + '/' + str(nodau_x[jx]) + '-yn-ateb-' + str(nodau_y[iy]) )
					ix = jx
					jx = ix + 1
					while jx < len(nodau_x) and nodau_x[jx] not in cy.cytseiniaid: jx = jx + 1
					
			# caledu: un yn ateb dau
			elif jy < len(nodau_y) and all(c not in cy.cytseiniaid for c in nodau_y[iy+1:jy]) and (
					(nodau_x[ix] == 'p' and nodau_y[iy] == 'p' and nodau_y[jy] == 'b') or 
					(nodau_x[iy] == 't' and nodau_y[iy] == 't' and nodau_y[jy] == 'd') or
					(nodau_x[iy] == 'c' and nodau_y[iy] == 'c' and nodau_y[jy] == 'g') or 
					(nodau_x[ix] == 'ff' and nodau_y[iy] == 'ff' and nodau_y[jy] == 'f') or 
					(nodau_x[iy] == 'll' and nodau_y[iy] == 'll' and nodau_y[jy] == 'll') or
					(nodau_x[iy] == 'th' and nodau_y[iy] == 'th' and nodau_y[jy] == 'dd')
				):
				sylwadau.append( str(nodau_x[ix]) + '-yn-ateb-' + str(nodau_y[iy]) + '/' + str(nodau_y[jy]) )
				parau.append((ix,jy))
				iy = jy
				jy = iy + 1
				while jy < len(nodau_y) and nodau_y[jy] not in cy.cytseiniaid: jy = jy + 1
		
			elif jx < len(nodau_x) and all(c not in cy.llythrennau for c in nodau_x[ix+1:jx]) and (
					(nodau_x[ix] == 'p' and nodau_x[jx] == 'b' and nodau_y[iy] == 'p') or
					(nodau_x[ix] == 't' and nodau_x[jx] == 'd' and nodau_y[iy] == 't') or
					(nodau_x[ix] == 'c' and nodau_x[jx] == 'g' and nodau_y[iy] == 'c') or
					(nodau_x[ix] == 'ff' and nodau_x[jx] == 'f' and nodau_y[iy] == 'p') or
					(nodau_x[ix] == 'll' and nodau_x[jx] == 'l' and nodau_y[iy] == 't') or
					(nodau_x[ix] == 'th' and nodau_x[jx] == 'dd' and nodau_y[iy] == 'c')				
				):
				sylwadau.append( str(nodau_x[ix]) + '/' + str(nodau_x[jx]) + '-yn-ateb-' + str(nodau_y[iy]) )
				parau.append((jx,iy))
				ix = jx
				jx = ix + 1
				while jx < len(nodau_x) and nodau_x[jx] not in cy.cytseiniaid: jx = jx + 1
			else:
				pass
				
		# caledu cytseiniaid: dau yn ateb un
		elif jx < len(nodau_x) and all(c not in cy.llythrennau for c in nodau_x[ix+1:jx]) and (
				(nodau_x[ix] == 'b' and nodau_x[jx] == 'b' and nodau_y[iy] == 'p') or
				(nodau_x[ix] == 'd' and nodau_x[jx] == 'd' and nodau_y[iy] == 't') or
				(nodau_x[ix] == 'g' and nodau_x[jx] == 'g' and nodau_y[iy] == 'c') or
				(nodau_x[ix] == 'b' and nodau_x[jx] == 'p' and nodau_y[iy] == 'p') or
				(nodau_x[ix] == 'd' and nodau_x[jx] == 't' and nodau_y[iy] == 't') or
				(nodau_x[ix] == 'g' and nodau_x[jx] == 'c' and nodau_y[iy] == 'c') or
				(nodau_x[ix] == 'f' and nodau_x[jx] == 'ff' and nodau_y[iy] == 'ff') or
				(nodau_x[ix] == 'l' and nodau_x[jx] == 'll' and nodau_y[iy] == 'll') or
				(nodau_x[ix] == 'dd' and nodau_x[jx] == 'th' and nodau_y[iy] == 'th') 
			):
			sylwadau.append( str(nodau_x[ix]) + '/' + str(nodau_x[jx]) + '-yn-ateb-' + str(nodau_y[iy]) )
			parau.append((ix,iy))
			parau.append((jx,iy))
			ix = jx
			jx = ix + 1
			while jx < len(nodau_x) and nodau_x[jx] not in cy.cytseiniaid: jx = jx + 1
					
		# caledu cytseiniaid: un yn ateb dau
		elif jy < len(nodau_y) and all(c not in cy.llythrennau for c in nodau_y[iy+1:jy]) and (
				(nodau_x[ix] == 'p' and nodau_y[iy] == 'b' and nodau_y[jy] == 'b') or 
				(nodau_x[iy] == 't' and nodau_y[iy] == 'd' and nodau_y[jy] == 'd') or
				(nodau_x[iy] == 'c' and nodau_y[iy] == 'g' and nodau_y[jy] == 'g') or 
				(nodau_x[ix] == 'p' and nodau_y[iy] == 'b' and nodau_y[jy] == 'p') or 
				(nodau_x[iy] == 't' and nodau_y[iy] == 'd' and nodau_y[jy] == 't') or
				(nodau_x[iy] == 'c' and nodau_y[iy] == 'g' and nodau_y[jy] == 'c') or 
				(nodau_x[ix] == 'ff' and nodau_y[iy] == 'f' and nodau_y[jy] == 'ff') or 
				(nodau_x[iy] == 'll' and nodau_y[iy] == 'l' and nodau_y[jy] == 'll') or
				(nodau_x[iy] == 'th' and nodau_y[iy] == 'dd' and nodau_y[jy] == 'th')
			):
			sylwadau.append( str(nodau_x[ix]) + '-yn-ateb-' + str(nodau_y[iy]) + '/' + str(nodau_y[jy]) )
			parau.append((ix,iy))
			parau.append((ix,jy))
			iy = jy
			jy = iy + 1
			while jy < len(nodau_y) and nodau_y[jy] not in cy.cytseiniaid: jy = jy + 1
		else:
			# print 'dim cyfatebiaeth lawn'
			break
		# symud i'r nesaf
		ix = jx
		iy = jy
	# diweddeb		
	cynffon_x = []
	while ix < len(nodau_x):
		if nodau_x[ix] in cy.cytseiniaid: cynffon_x.append(ix)
		ix = ix + 1
	cynffon_y = []
	while iy < len(nodau_y):
		if nodau_y[iy] in cy.cytseiniaid: cynffon_y.append(iy)
		iy = iy + 1		
	
	if reverse:
		parau.reverse()
		cynffon_x.reverse()
		cynffon_y.reverse()
		parau = [ (len(nodau_x)-i-1,len(nodau_y)-j-1) for i,j in parau ]
		cynffon_x = [ len(nodau_x)-i-1 for i in cynffon_x ]
		cynffon_y = [ len(nodau_y)-j-1 for j in cynffon_y ]
	return parau, cynffon_x, cynffon_y, sylwadau


def prawf_cytseinedd(x,y):
	'''
	ffwythiant:	darganfod cytseinedd rhwng dau linyn
	mewnbwn:	dau linyn
	allbwn:		dosbarth cytseinedd (neu dosbarth bai)
	sylwadau:
	'''
	data = dict()
	data['sylwadau'] = []
	
	x = x.lower()
	y = y.lower()

	nodau_x = ll.nodau(x)
	nodau_y = ll.nodau(y)
	
	xx = x.split(' ')
	yy = y.split(' ')
	
	# rhestri nodau
	xa, xb, xc = ac.traeannu( xx[-1] )
	ya, yb, yc = ac.traeannu( yy[-1] )
	
	if len(xx) > 1:	xa = ll.nodau( ' '.join(xx[:-1]) ) + [' '] + xa
	if len(yy) > 1:	ya = ll.nodau( ' '.join(yy[:-1]) ) + [' '] + ya

	if debug:
		print xa, xb, xc
		print ya, yb, yc
	
	#--------------------
	# parau
	cc = cyfatebiaeth(xa,ya,reverse=True)	
	blaen = cc[0] 		if cc[0] else []
	pen_x = cc[1] 		if cc[1] else []
	pen_y = cc[2] 		if cc[2] else []
	if cc[3]: data['sylwadau'].extend(cc[3])	

	#--------------------
	# canol
	canol = []
	ccc = None
	# cytbwys ddiacen: cyfateb xb a yb
	if xb and yb:
		cc = cyfatebiaeth(xb,yb)
		if not cc[1] and not cc[2]:
			canol = cc[0]
			ccc = cyfatebiaeth(xc,yc)
		else:
			if debug: print 'xb a yb ddim yn cyfateb'
	# anghytbwys ddisgynedig: cyfateb xc a yb
	elif yb and not xb:
		cc = cyfatebiaeth(xc,yb)
		if not cc[1] and not cc[2]:
			canol = cc[0]
			ccc = cyfatebiaeth('',yc)
		else:
			if debug: print 'xc a yb ddim yn cyfateb'
	# anghytbwys ddyrchafedig: cyfateb xb a yc
	elif xb and not yb:
		cc = cyfatebiaeth(xb,yc)
		if not cc[1] or not cc[2]:
			canol = cc[0]
			ccc = cyfatebiaeth(xc,'')
		else:
			if debug: print 'xb a yc ddim yn cyfateb'
	# cytbwys acenog
	else:
		ccc = cyfatebiaeth(xc,yc)

	blaen = [ (a,1+len(nodau_x)+b) for a,b in blaen ]
	canol = [ (len(xa)+a,1+len(nodau_x)+len(ya)+b) for a,b in canol ]	
	
	#--------------------
	# cynffon
	cwt_x = [ len(xa+xb)+i for i in ccc[1] ] if ccc else []
	cwt_y = [ len(nodau_x)+len(ya+yb)+i for i in ccc[2] ] if ccc else []

	#--------------------
	# casglu data
	data['pen_x'] = pen_x
	data['pen_y'] = [ 1+len(nodau_x)+a for a in pen_y ]
	data['parau'] = blaen + canol
	data['cwt_x'] = cwt_x
	data['cwt_y'] = cwt_y

	#--------------------
	# bai rhy debyg
	if ccc and ccc[0]:
		return (None, 'RHY', data)

	#--------------------
	# dosbarthu
	# cyfatebiaeth lawn (croes)
	if blaen and not pen_x and not pen_y:
		return ('CRO', None, data)
	
	# cytseiniaid chwith yn weddill (croes-n-wreiddgoll, croes-o-gyswllt)
	elif blaen and pen_x and not pen_y:

		# n-wreiddgoll
		if len(pen_x) == 1 and nodau_x[ pen_x[0] ] == 'n':
			data['sylwadau'].extend('n-wreiddgoll')
			return ('CRO', None, data)

		# croes-o-gyswllt
		cc = cyfatebiaeth(pen_x,x)
		if cc and not cc[1]:
			return ('COG', None, data)
			
	# cytseiniaid dde yn weddill (n-ganolgoll, traws)
	elif blaen and not pen_x and pen_y:

		# n-ganolgoll
		if len(pen_y) == 1 and nodau_y[ pen_y[0] ] == 'n':
			data['n-ganolgoll'] = [ pen_y[0] ]
			return ('CRO', None, data)

		# traws
		else:
			if len(xx) == 1 or len(xx) == 2 and all(c not in cy.cytseiniaid for c in xx[0]): # hac
				return ('TRF', None, data)
			else:
				return ('TRA', None, data)
	else:
		return (None, None, None)	


#------------------------------------------------
# TEST

def main():
	print 'cytseinedd.py'
	
	# print cyfatebiaeth('och','ir')
	
	x = 'affacadash'
	y = 'ephecedes'
	# print cyfatebiaeth(x,y)
	x = 'rstabcd'
	y = 'rstefgh'
	# oes_cytseinedd(x,y)
	# print oes_cytseinedd('pqOchain cloch', 'rsa chanu clir')
	print cyfatebiaeth('Ni all ll', 'ond ennyn ll', reverse=True),

	return
	
	croes = (
		('Ochain cloch', 'a chanu clir'),
		('Awdur mad', 'a dramodydd'),
		('Am eu hawr', 'yn ymaros'),
	)
	croes_o_gyswllt = (
		('Daw geiriau duw', "o'i gaer deg"),
		('Aderyn llwyd', 'ar un llaw'),
	)
	traws = (
		('Ochain cloch', 'a gwreichion clir'),
		('Ei awen brudd', 'dan ein bro'),
	)
	traws_fantach = (
		('Y brawd', 'o bellafion bro'),
		('Brwd', 'yw aderyn brig')
	)
	rhy_debyg = (
		('rhy debyg', "mae'n debyg"),
	)
		
	print '--------------------'
	print 'Croes'
	print '--------------------'
	for s1,s2 in croes:
		print s1 + ' / ' + s2
		print prawf_cytseinedd( s1, s2 )
	print ''
	
	
	print '--------------------'
	print 'Croes o gyswllt'
	print '--------------------'
	for s1,s2 in croes_o_gyswllt:
		print s1 + ' / ' + s2
		print prawf_cytseinedd( s1, s2 )
	print ''
	print '--------------------'
	print 'Traws'
	print '--------------------'
	for s1,s2 in traws:
		print s1 + ' / ' + s2
		print prawf_cytseinedd( s1, s2 )
	print ''
	print '--------------------'
	print 'Traws fantach'
	print '--------------------'
	for s1,s2 in traws_fantach:
		print s1 + ' / ' + s2
		print prawf_cytseinedd( s1, s2 )
	print ''

	return

	print '--------------------'
	print 'Rhy debyg'
	print '--------------------'
	for s1,s2 in rhy_debyg:
		print s1 + ' / ' + s2
		print prawf_cytseinedd( s1, s2 )
	print ''

if __name__ == '__main__': 
	main()
