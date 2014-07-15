#!/usr/bin/python
# -*- coding: utf-8 -*-
''' 
llinyn.py
	adnoddau er mwyn trafod llinynau
	
	Geirfa:
		llinyn: cyfres o symbolau utf-8
		nodyn: llythyren, yn cynnwys ch, dd, ll, a.y.b.
		cwlwm: cyfres o lafariaid neu gytseiniaid
		
	Nodau:
		bydd pob mynegrif yn cyfeirio at safle yn y rhestr nodau (nid yn y llinyn)
		o ganlyniad, gellir newid llythrennau unigol (tra bod llinynau yn "immutable")

	Clymau:
		clymau: yn y drefn [LL,CY,LL,CY, ..., LL,CY]

	Cwestiynnau
	Mae angen ffordd o adnabod llafariaid hir (sillaf ysgafn) heb hirnod.
	Oes angen dechrau geiriadur?
'''

import re
import cysonion as cy

global debug 
debug = False

def nodau(s):
	'''
	ffwythiant: trawnewid llinyn i restr nodau
	mewnbwn:	llinyn
	allbwn:		rhestr nodau
	'''
	# if re.search(r'\s', s):	return None
	nodau = list() 
	idx = 0
	while idx < len(s):
		c = s[idx]
		if c in ['c','d','f','n','l','p','r','s','t'] and idx < len(s) - 1:
			c_nesaf = s[idx+1]
			if	 c=='c' and c_nesaf=='h': nodau.append(u'ch'); idx += 1;
			elif c=='d' and c_nesaf=='d': nodau.append(u'dd'); idx += 1;
			elif c=='f' and c_nesaf=='f': nodau.append(u'ff'); idx += 1;
			elif c=='n' and c_nesaf=='g': nodau.append(u'ng'); idx += 1;
			elif c=='l' and c_nesaf=='l': nodau.append(u'll'); idx += 1;
			elif c=='p' and c_nesaf=='h': nodau.append(u'ph'); idx += 1;
			elif c=='r' and c_nesaf=='h': nodau.append(u'rh'); idx += 1;
			elif c=='t' and c_nesaf=='h': nodau.append(u'th'); idx += 1;
			elif c=='s' and c_nesaf=='h': nodau.append(u'sh'); idx += 1;
			else: 
				nodau.append(c)
		else: 
			nodau.append(c)
		idx += 1
	return nodau
	
def rhestr_nodau(s):
	return [ nodau(g) for g in s.split(' ') ]


def ysgafn_yn_drwm(s):
	if re.search(r'\s', s):	return None
	'''
	ffwythiant: trawsnewid llafariaid hir i'r llafariaid byr cyfatebol
	mewnbwn:	llinyn
	allbwn:		llinyn
	'''
	def hir2byr(s):
		if s == u'â': return u'a'
		if s == u'ê' or s == u'ë': return 'e'
		if s == u'î' or s == u'î': return 'i'
		if s == u'ô': return u'o'
		if s == u'û': return u'u'
		if s == u'ŵ': return u'w'
		if s == u'ŷ': return u'y'
		if s == u'â'.upper(): return u'a'.upper()
		if s == u'ê'.upper() or s == u'ë'.upper(): return u'e'.upper()
		if s == u'î'.upper() or s == u'î': return u'i'.upper()
		if s == u'ô'.upper(): return u'o'.upper()
		if s == u'û'.upper(): return u'u'.upper()
		if s == u'ŵ'.upper(): return u'w'.upper()
		if s == u'ŷ'.upper(): return u'y'.upper()
		return s
	nod = nodau(s)
	for idx in range( len(nod) ):
		nodyn = nod[idx]
		if nodyn in cy.llafariaid_hir:
			nod[idx] = hir2byr(nodyn)
	return ''.join(str(nodyn) for nodyn in nod)


def rhestr_clymau(s, w_gytsain=True):
	return [ clymau(g, w_gytsain=w_gytsain) for g in s.split(' ') ]


def clymau(s, w_gytsain=True):
	if re.search(r'\s', s):	return None
	nod = nodau(s)
	clymau = list()
	cwlwm_llafariaid = True
	c = list()
	n = len(nod)
	j = 0
	while j < len(nod):

		# estyn cwlwm llarariaid
		if cwlwm_llafariaid and nod[j] in cy.llafariaid : 

			# gwirio am 'w' rhwng dau lafariad
			if w_gytsain and c and (j>0) and (j < n-1) and (nod[j] == 'w') and (nod[j+1] in cy.llafariaid):
				clymau.append(c)
				clymau.append(['w'])
				c = list()

			# gwirio am ddeusain dwbl
			elif (j > 0) and (nod[j-1] in cy.llafariaid) and (nod[j-1]+nod[j]).lower() in cy.deuseiniaid['deusill']:
				# c.append( nod[j] )
				clymau.append(c)
				clymau.append([])
				c = list([ nod[j] ])
			
			else:
				c.append( nod[j] )

		# cau cwlwm llarariaid
		elif cwlwm_llafariaid and nod[j] in cy.cytseiniaid : 
			clymau.append(c)
			cwlwm_llafariaid = False 
			c = list([ nod[j] ])
		
		# estyn cwlwm cytseiniaid
		elif not cwlwm_llafariaid and nod[j] in cy.cytseiniaid : 
				c.append( nod[j] )

		# cau cwlwm cytseiniaid
		elif not cwlwm_llafariaid and nod[j] in cy.llafariaid:
			# 'w' ar ddiwedd gair
			if w_gytsain and (j == n-1) and (nod[j] == 'w') and (s not in ['galw', 'acw', 'cwcw', 'dacw', 'hwnnw', 'lludw', 'pitw']):
				c.append( nod[j] )
			# 'w' ar ddechrau gair (gwlad, gwrando)
			elif w_gytsain and (j < n-3) and (nod[j] == 'g') and (nod[j+1] == 'w') and (nod[j+2] in ['r','l']) and (nod[j+3] in ['a','e']):
				c.append( nod[j] )
			else:
				clymau.append(c)
				cwlwm_llafariaid = True 
				c = list([ nod[j] ])
		
		# fel arall, atodi'r nod i'r cwlwm, yn eithrio atalnodau a gofodau
		else:
			if nod[j] not in cy.atalnodau and not nod[j].isspace():
				c.append( nod[j] )
		
		# symud
		j = j + 1
	
	# diweddeb
	clymau.append(c)
	if cwlwm_llafariaid:
		clymau.append([])

	return clymau


def llinyn_llafariaid(s, blanksymbol=' '):
	if re.search(r'\s', s):	
		return None
	
	ss = list()
	for nod in nodau(s):
		if nod.isspace():
			ss.append(' ')
		elif nod in cy.llafariaid:
			ss.append(nod)
		else:
			ss.append(blanksymbol*len(nod))
	return ''.join(ss)


def llinyn_cytseiniaid(s, blanksymbol=' '):
	ss = list()
	for nod in nodau(s):
		if nod.isspace():
			ss.append(' ')
		elif nod in cy.cytseiniaid:
			ss.append(nod)
		else:
			ss.append(blanksymbol*len(nod))
	return ''.join(ss)


def llinyn_nodau_dethol(s, mynegrifau, blanksymbol=' '):
	nod = nodau(s)
	ss = ''
	for j in range( len(nod) ):
		if j in mynegrifau:
			ss += nod[j]
		else:
			ss += blanksymbol*len(nod[j])
	return ss


def llinyn_clymau_dethol(s, mynegrifau, blanksymbol=' '):
	cly = clymau(s)
	ss = ''
	for j in range( len(cly) ):
		s = ''.join( cly[j] ) 
		if j in mynegrifau:
			ss += llinyn
		else:
			ss += blanksymbol*len(s)
	return ss


def oes_cytseiniaid(s):
	for nod in nodau(s):
		if nod in cy.cytseiniaid:
			return True
	return False
		
#------------------------------------------------
def main():
	print 'main: llinyn.py'
	
	s = 'gwrandawiad'
	print s
	print nodau(s)
	print clymau(s)
	print rhestr_clymau(s)
	return

	rhestr_llinynau = (
		# 'prydferth',
		# 'duon',
		'eos',
		# 'suo',
		# 'gwrandawiad',
		# 'awen',
		# 'distewi',
		# 'dramodydd',
		# 'dyfalbarhau',
		# 'dyfalbarhad',
		# 'cymraeg',
		# 'anifeiliaid',
		# 'berw',
		'gwaith',			# y cyntaf o dri
		'awen',				# yr ail o dri
		'distewi',			# yr ail o dri
		'haleliwia',		# yr ail o bedwar
		'bedw',				# yr olaf
		# 'pitw',				# yr olaf, on eithriad
		'gwrando',
		u'cangarŵ',			# w-hir yn olaf
		'gwr',
		'gwroldeb',
		'gwrhydri',
	)
	for s in rhestr_llinynau:
		print '-------------------'
		# print ''
		print s
		print nodau(s)
		print clymau(s)
		# print llinyn_cytseiniaid(s)
		# print llinyn_nodau_dethol(s, [1,3])
		# print llinyn_clymau_dethol(s, [1,3])
		print ''
		
if __name__ == '__main__': 
	main()


