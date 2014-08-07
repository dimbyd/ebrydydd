#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
adroddiad.py 
	
	harddu allbwn y peiriant (ar gyfer y wê)
'''

# from acen import aceniad, nifer_sillau, pwyslais, traeannu_cytseiniaid
# from odl import prawf_odl, prawf_odl_lusg
# from cytseinedd2 import prawf_cytseinedd

# import cysonion as cy
# import odl as od

import lliwiau as lliw

global debug
debug = False

# adroddiad
class Adroddiad(object):
	'''
	class Adroddiad:
		Yn cynnwys...
			(a) dosbarthiadau/sylwadau ar gyfer Dadansoddiad(cynghanedd, aceniad, bai, sylwadau, dadansoddwr=EBR)
			(b) data ychwanegol e.e. safle'r orrfwysfa, mynegrifau '
		Nodiadau:
			Mae'r mynegrifau yn cyfeirio at rhestr nodau y llinyn
	'''
	def __init__(self, llinell, cynghanedd=None, aceniad=None, bai=None, sylwadau=None, data=dict()): 
		self.llinell = llinell
		self.cynghanedd = cynghanedd
		self.aceniad = aceniad
		self.bai = bai
		self.sylwadau = sylwadau
		self.data = data

	def __unicode__(self):
		ss = []
		ss.append( '------------------------------' )
		# ss.append( 'Adroddiad:' )
		ss.append( self.llinell.llinyn() )
		ss.append( lliw.cyan( self.cynghanedd ) )
		# 
		# if self.cynghanedd:	
		# 	ss.append( 'CNG: ' + self.cynghanedd )
		# if self.aceniad:	
		# 	ss.append( 'ACE: ' + self.aceniad )
		# if self.bai:		
		# 	ss.append( 'BAI: ' + self.bai )
		# if self.sylwadau:	
		# 	ss.append( 'SYL: ' + self.sylwadau )
		if self.data:
			ss.append( self.text_strings() )
		ss.append( '------------------------------' )
		return '\n'.join(ss)

	def __str__(self):
		return self.__unicode__().encode('utf-8')


	def text_strings(self, blanksymbol=' '):
		ss = []
		ss.append( self.llinell.llinyn_acenion() )
		ss.append( self.llinyn_ac_odl(blanksymbol=blanksymbol) )
		if not all([ c==blanksymbol for c in self.llinyn_cytseiniaid_cyfatebol() ]):
			ss.append( self.llinyn_cytseinedd(blanksymbol=blanksymbol) )
		if self.data.has_key('sylwadau'):
			ss.append('[' + ':'.join( self.data['sylwadau'] ) + ']' )
		return '\n'.join(ss)

	def html_strings(self, blanksymbol=' '):
		hs = dict()
		hs['llinyn']		= self.llinell.llinyn()
		hs['acenion'] 		= self.llinell.llinyn_acenion()
		# hs['acenion_colon']	= self.llinyn_acenion_colon(html=True, blanksymbol=blanksymbol)
		hs['toriadau'] 		= self.llinyn_toriadau(html=True, blanksymbol=blanksymbol)
		hs['gorffwysfeydd'] = self.llinyn_gorffwysfa(html=True, blanksymbol=blanksymbol)
		hs['odlau']			= self.llinyn_odl(html=True, blanksymbol=blanksymbol)
		hs['cytseiniaid_cyfatebol']	= self.llinyn_cytseiniaid_cyfatebol(html=True, blanksymbol=blanksymbol)
		hs['cytseiniaid_traws']	= self.llinyn_cytseiniaid_traws(html=True, blanksymbol=blanksymbol)
		hs['cytseiniaid_cwt']	= self.llinyn_cytseiniaid_cynffon(html=True, blanksymbol=blanksymbol)
		hs['cytseinedd']	= self.llinyn_cytseinedd(html=True, blanksymbol=blanksymbol)

		if self.data.has_key('sylwadau'):
			hs['sylwadau']	= u''.join(self.data['sylwadau'])

		return hs

	def llinyn_acenion(self):
		return self.llinell.llinyn_acenion()

	def llinyn_ac_odl(self, html=False, blanksymbol=' '):
		ss_lli = list( self.llinell.llinyn() )
		ss_odl = list( self.llinyn_odl(html=html, blanksymbol=blanksymbol) )
		ss = []
		for j in range( len(ss_lli) ):
			if ss_odl[j] == blanksymbol:
				ss.append( ss_lli[j] )
			else:
				ss.append( lliw.magenta( ss_odl[j] ) )
		return ''.join( ss )

	def llinyn_cytseinedd(self, html=False, blanksymbol=' '):
		if not html:
			ss_tor = list( self.llinyn_toriadau(blanksymbol=blanksymbol) )
			ss_par = list( self.llinyn_cytseiniaid_cyfatebol(blanksymbol=blanksymbol) )
			ss_tra = list( self.llinyn_cytseiniaid_traws(blanksymbol=blanksymbol) )
			ss_cwt = list( self.llinyn_cytseiniaid_cynffon(blanksymbol=blanksymbol) )
			ss_col = list( self.llinyn_acenion_colon(blanksymbol=blanksymbol) )
			ss = []
			for j in range( len(ss_col) ):
				if ss_tor[j] != blanksymbol:
					ss.append( ss_tor[j] )
				elif ss_par[j] != blanksymbol:
					ss.append( lliw.cyan( ss_par[j] ) )
				elif ss_tra[j] != blanksymbol:
					ss.append( lliw.coch( ss_tra[j] ) )
				elif ss_cwt[j] != blanksymbol:
					ss.append( lliw.melyn( ss_cwt[j] ) )
				elif ss_col[j] != blanksymbol:
					ss.append( ss_col[j] )
				else:
					ss.append( blanksymbol )
			return ''.join( ss )
		else:
			nodau_cyfatebol = []
			if self.data.has_key('parau'):
				nodau_cyfatebol += [nod for par in self.data['parau'] for nod in par]
			nodau_traws = []
			if self.data.has_key('pengoll_dde'):
				nodau_traws += self.data['pengoll_dde']
			nodau_cwt = []
			if self.data.has_key('cwt_chwith'):
				nodau_cwt += self.data['cwt_chwith']
			if self.data.has_key('cwt_dde'):
				nodau_cwt += self.data['cwt_dde']
			geiriau_dethol = []
			if self.data.has_key('gorffwysfeydd'):
				gorffwysfeydd = self.data['gorffwysfeydd']
				if len(gorffwysfeydd) < 3: # sain
					geiriau_dethol.append( gorffwysfeydd[-1] )
				else: # sain gadwynog	
					geiriau_dethol.append( gorffwysfeydd[-2] )
			geiriau_dethol.append(self.llinell.geiriau[-1])
				
			ss = []
			for g in self.llinell.geiriau:
				nodau_acen = []
				if g in geiriau_dethol:
					ace = g.nodau_acennog()
					nodau_acen = [ ace[-1] ]
					if g.pwyslais() == -2:
						nodau_acen.append( ace[-2] )
				s = []
				for nod in g.nodau:
					if nod in nodau_acen:
						s.append( ':' )
					elif nod in nodau_cyfatebol:
						s.append( '<span class="cytseiniaid_cyfatebol">' + nod.llinyn + '</span>' )
					elif nod in nodau_traws:
						s.append( '<span class="cytseiniaid_traws">' + nod.llinyn + '</span>' )
					elif nod in nodau_cwt:
						s.append( '<span class="cytseiniaid_cwt">' + nod.llinyn + '</span>' )
					else:
						s.append( blanksymbol*len(nod.llinyn) )
				ss.append( ''.join(s) )
				if g in geiriau_dethol[:-1]:
					ss.append( '<span class="toriadau">|</span>' )
				else:
					ss.append( blanksymbol )
			return ''.join(ss)
			

	def llinyn_acenion_colon(self, html=False, blanksymbol=' '):
		geiriau_dethol = []
		if self.data.has_key('gorffwysfeydd'):
			gorff = self.data['gorffwysfeydd']
			if len(gorff) < 3: # sain
				geiriau_dethol.append( gorff[-1] )
			else: # sain gadwynog	
				geiriau_dethol.append( gorff[-2] )
		geiriau_dethol.append(self.llinell.geiriau[-1])
		ss = []
		for g in self.llinell.geiriau:
			if g in geiriau_dethol:
				if html:	
					ss.append( '<span class="acenion_colon">' + g.llinyn_acenion_colon(blanksymbol=blanksymbol) + '</span>' )
				else:
					ss.append( g.llinyn_acenion_colon(blanksymbol=blanksymbol) )
			else:
				ss.append( ''.join([ blanksymbol*len(nod.llinyn) for nod in g.nodau ]) ) 
		return blanksymbol.join( ss )

	def llinyn_toriadau(self, html=False, blanksymbol=' '):
		geiriau_dethol = []
		if self.data.has_key('gorffwysfeydd'):
			geiriau_dethol = self.data['gorffwysfeydd']
		ss = []
		for g in self.llinell.geiriau:
			ss.append( ''.join([ blanksymbol*len(nod.llinyn) for nod in g.nodau ]) ) 
			if g in geiriau_dethol:
				if html:	
					ss.append( '<span class="toriadau">|</span>' )
				else:
					ss.append( '|' )
			else:
				ss.append(' ')
		return ''.join( ss[:-1] )

	def llinyn_gorffwysfa(self, html=False, blanksymbol=' '):
		geiriau_dethol = []
		if self.data.has_key('gorffwysfeydd'):
			geiriau_dethol += self.data['gorffwysfeydd']
		ss = []
		for g in self.llinell.geiriau[:-1]:
			if g in geiriau_dethol:
				if html:	
					ss.append( '<span class="gorffwysfeydd">' + g.llinyn() + '</span>' )
				else:
					# ss.append( ''.join([ nod.llinyn.upper() for nod in g.nodau ]) )
					ss.append( lliw.coch(g.llinyn()) )
			else:
				ss.append( ''.join([ blanksymbol*len(nod.llinyn) for nod in g.nodau ]) ) 
		g = self.llinell.geiriau[-1]
		if html:
			ss.append( '<span class="prifodl">' + g.llinyn() + '</span>' )
		else:
			# ss.append( ''.join([ nod.llinyn.upper() for nod in g.nodau ]) )		
			ss.append( lliw.coch(g.llinyn()) )

		return blanksymbol.join( ss )

	def llinyn_odl(self, html=False, blanksymbol=' '):
		nodau_dethol = []
		if self.data.has_key('odl'):
			nodau_dethol += [nod for nodau in self.data['odl'] for nod in nodau]
		ss = []
		for g in self.llinell.geiriau:
			s = []
			for nod in g.nodau:
				if nod in nodau_dethol:
					if html:
						s.append( '<span class="odlau">' + nod.llinyn + '</span>' )
					else:
						s.append(nod.llinyn)
				else:
					s.append( blanksymbol*len(nod.llinyn) )
			ss.append( ''.join(s) )
		return blanksymbol.join(ss)

	def llinyn_cytseiniaid_cyfatebol(self, html=False, blanksymbol=' '):
		nodau_dethol = []
		if self.data.has_key('parau'):
			nodau_dethol += [nod for par in self.data['parau'] for nod in par]
		ss = []
		for g in self.llinell.geiriau:
			s = []
			for nod in g.nodau:
				if nod in nodau_dethol:
					if html:
						s.append( '<span class="cytseiniaid_cyfatebol">' + nod.llinyn + '</span>' )
					else:
						s.append(nod.llinyn)
				else:
					s.append( blanksymbol*len(nod.llinyn) )
			ss.append( ''.join(s) )
		return blanksymbol.join(ss)

	def llinyn_cytseiniaid_traws(self, html=False, blanksymbol=' '):
		nodau_dethol = []
		if self.data.has_key('pengoll_dde'):
			nodau_dethol += self.data['pengoll_dde']
		ss = []
		for g in self.llinell.geiriau:
			s = []
			for nod in g.nodau:
				if nod in nodau_dethol:
					if html:
						s.append( '<span class="cytseiniaid_traws">' + nod.llinyn + '</span>' )
					else:
						s.append( nod.llinyn )
				else:
					s.append( blanksymbol*len(nod.llinyn) )
			ss.append( ''.join(s) )
		return blanksymbol.join(ss)
	
	def llinyn_cytseiniaid_cynffon(self, html=False, blanksymbol=' '):
		nodau_dethol = []
		if self.data.has_key('cwt_chwith'):
			nodau_dethol += self.data['cwt_chwith']
		if self.data.has_key('cwt_dde'):
			nodau_dethol += self.data['cwt_dde']
		ss = []
		for g in self.llinell.geiriau:
			s = []
			for nod in g.nodau:
				if nod in nodau_dethol:
					if html:
						s.append( '<span class="cytseiniaid_cwt">' + nod.llinyn + '</span>' )
					else:
						s.append(nod.llinyn)
				else:
					s.append( blanksymbol*len(nod.llinyn) )
			ss.append( ''.join(s) )
		return blanksymbol.join(ss)

#------------------------------------------------
def main():
	print 'adroddiad.py'


if __name__ == '__main__': main()


		
