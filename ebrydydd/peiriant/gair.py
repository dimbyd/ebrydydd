#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cysonion as cy

global debug

def trawsnewid_symbolau(s, insymbols, outsymbol=u' '):
	'''
	ffwythiant: trawsnewid symbolau penodol i symbol di-nod
	'''
	translate_table = dict((ord(insymbol), outsymbol) for insymbol in insymbols)
	return s.translate(translate_table)


def rhestr_llythrennau(s):
	llythrennau = list() 
	idx = 0
	while idx < len(s):
		c = s[idx]
		if c in ['c','d','f','n','l','p','r','t'] and idx < len(s) - 1:
			c_nesaf = s[idx+1]
			if	 c=='c' and c_nesaf=='h': llythrennau.append(u'ch'); idx += 1;
			elif c=='d' and c_nesaf=='d': llythrennau.append(u'dd'); idx += 1;
			elif c=='f' and c_nesaf=='f': llythrennau.append(u'ff'); idx += 1;
			elif c=='n' and c_nesaf=='g': llythrennau.append(u'ng'); idx += 1;
			elif c=='l' and c_nesaf=='l': llythrennau.append(u'll'); idx += 1;
			elif c=='p' and c_nesaf=='h': llythrennau.append(u'ph'); idx += 1;
			elif c=='r' and c_nesaf=='h': llythrennau.append(u'rh'); idx += 1;
			elif c=='t' and c_nesaf=='h': llythrennau.append(u'th'); idx += 1;
			else: 
				llythrennau.append(unicode(c))
		else: 
			llythrennau.append(unicode(c))
		idx += 1
	return llythrennau


def rhestr_clymau(s):
	clymau = list()
	llythrennau = rhestr_llythrennau(s)
	cwlwm_llafariaid = False
	if llythrennau[0] in cy.llafariaid:
		cwlwm_llafariaid = True
	c = list([llythrennau[0]])
	for llythyren in llythrennau[1:]: 
		if cwlwm_llafariaid and llythyren in cy.cytseiniaid:
			clymau.append(c)
			cwlwm_llafariaid = False 
			c = list([llythyren])
		elif not cwlwm_llafariaid and llythyren in cy.llafariaid:
			clymau.append(c)
			cwlwm_llafariaid = True 
			c = list([llythyren])
		else:
			if llythyren not in cy.atalnodau:
				c.append(llythyren)
	clymau.append(c)
	return clymau


def safleoedd_acenion(s):
	safleoedd = list()
	idx = 0
	clymau = rhestr_clymau(s)
	for cwlwm in clymau:
		if cwlwm[0] in cy.llafariaid:
			safleoedd.append(idx)
		idx = idx + len(cwlwm)
	return safleoedd


def safle_pwyslais(s):
	# mae angen gwirio am eeiriau afreolus fan hyn
	safleoedd = safleoedd_acenion(s)
	idx = -2 # goben
	if len(safleoedd) == 1: 
		idx = -1 # gair unsill
	return safleoedd[idx]


def patrwm_odl(s):
	'''
	ffwythiant: patrwm_odl
		darganfod patrwm odl (drwy ddefnyddio rhestr clymau)
		C - cystsain
		T - llafariad trwm
		Y - llafariad ysgafn
		0 - deusain talgron
		1 - deusain lleddf o'r dosbarth cyntaf
		2 - deusain lleddf o'r ail ddosbarth
		3 - deusain lleddf o'r trydydd dosbarth
	'''
	patrwm = list();
	for cwlwm in rhestr_clymau(s):
		if cwlwm[0] in cy.cytseiniaid:					
			patrwm.append('C')							# cytsain
		else:
			if len(cwlwm) == 1:						
				if cwlwm[0] in cy.llafariaid_ysgafn:
					patrwm.append('Y')					# llafariad ysgafn
				else:
					patrwm.append('T')					# llafariad trwm
			else:						
				ds = ''.join(cwlwm[-2:])				# y ddau lafariad olaf 
				dods = cy.dosbarth_deuseiniaid[ds.lower()]		# dosbarth y ddeusain
				patrwm.append(dods)						# atodi'r ddeusain
	return ''.join(patrwm)


class Gair(object):
	'''
	class: Gair
		 mewnbwn: llinyn yn y ffurf safonol
	 ''' 
	def __init__(self, s):
		# self.llinyn = s.encode('utf-8')
		self.llinyn = unicode(s)
		self.llythrennau = rhestr_llythrennau(self.llinyn)
		self.rhestr_clymau = rhestr_clymau(self.llinyn)
		# self.patrwm_odl = patrwm_odl(self.llinyn)
		self.safleoedd_acenion = safleoedd_acenion(self.llinyn)
		self.safle_pwyslais = safle_pwyslais(self.llinyn)
 
	def __unicode__(self):
		return self.llinyn
 
	def nifer_sillau(self):
		return len(self.safleoedd_acenion)

	def nifer_clymau(self):
		return len(self.rhestr_clymau)
   
	  
	def llinyn_acenion(self, symbol=' '):
		ss = []
		for idx in range(len(self.llythrennau)):
			if idx in self.safleoedd_acenion:
				if idx == self.safle_pwyslais:
					ss.append('/')
				else:
					ss.append('v')
			else:
				c = self.llythrennau[idx]
				ss.append(symbol*len(c))
		
		return ''.join(ss)
	
	def llinyn_llafariaid(self):
		ss = list()
		for c in self.llythrennau:
			if c in cy.llafariaid:
				ss.append(c)
			else:
				ss.append('.'*len(c))
		return ''.join(ss)

	def llinyn_cytseiniaid(self):
		ss = list()
		for c in self.llythrennau:
			if c in cy.cytseiniaid:
				ss.append(c)
			else:
				ss.append('.')
		return ''.join(ss)
	
	def pen_a_chynffon(self):
		'''
		ffwythiant: pen_a_chynffon
		mewn: rhestr llythrennau
		allan: dau rhestr llythrennau
		'''
		n = len(self.llythrennau)
		k = self.safle_pwyslais
		pen = self.llythrennau[0:k+1]
		k = k+1
		while k < n and self.llythrennau[k] in cy.llafariaid:
			pen.append(self.llythrennau[k])
			k = k+1
		while k < n and self.llythrennau[k] in cy.cytseiniaid:
			pen.append(self.llythrennau[k])
			k = k+1
		cwt = self.llythrennau[k:]
		return pen, cwt

	def pen_acen_cwt(self):
		'''
		ffwythiant: pen_acen_cwt
		mewn: rhestr llythrennau
		allan: tri rhestr llythrennau
		'''
		n = len(self.llythrennau)
		k = self.safle_pwyslais
		pen = self.llythrennau[0:k]
		ace = self.llythrennau[k:k+1]
		k = k+1
		while k < n	 and self.llythrennau[k] in cy.llafariaid:
			ace.append(self.llythrennau[k])
			k = k+1
		cwt = self.llythrennau[k:]
		return pen, ace, cwt

	def llinyn_prifacen(self):
		pen, ace, cwt = self.pen_acen_cwt()	  
		pac = [''.join(pen), ''.join(ace).upper(), ''.join(cwt)]
		return ''.join(pac)



#------------------------------------------------
def main():

	global debug
	debug = True
	# g = Gair('tractor')
	# g = Gair('a\'u')
	g = Gair(u'rhôm')
	# g = Gair('anifeiliaid')
	# g = Gair('chwaethus')
	# g = Gair('ChwaeThus')
	# g = Gair('plantos')

	print g.llinyn
	print g.llythrennau
	print g.rhestr_clymau
	print g.safleoedd_acenion
	print g.safle_pwyslais

	print '\n'
	print g.llinyn_acenion()
	print g.llinyn
	print g.llinyn_cytseiniaid()
	print g.llinyn_llafariaid()

if __name__ == '__main__': 
	main()

		
