#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' 
nodau.py
	creu a thrafod rhestri nodau:

	llinyn: cyfres o symbolau utf-8
	nod:	llythren (yn cynnwys ch, dd, ll, ...) neu atalnod/gofod/ayb	  
	cwlwm:	cyfres o lafariaid neu gytseiniaid
	rhestr_clymau: yn y drefn [CLL,CCY,CLL,CCY, ..., CLL,CCY]
'''

import cysonion as cy
import lliwiau as lliw

import logging
log = logging.getLogger(__name__)

#------------------------------------------------
class Nod(object):
	'''
	class: Nod
		 mewnbwn: llinyn (utf8)
	 ''' 
	
	def __init__(self, s):
		if type(s) != unicode:
			s = s.decode('utf-8')
		self.llinyn = s
		
	def __unicode__(self):
		return self.llinyn

	def __str__(self):
		return self.__unicode__().encode('utf-8')
		
	# pwysig: er mwyn i (nod1 == nod2) weithio'n iawn
	# h.y. profi os ydy'r ddau enw yn cyfeirio at yr un gwrthrych (nid os yw'r llinynnau yn cyfateb
	# e.e. mae hyn yn eing galluogi i ddefnyddio nodau.index(nod) er mwn darganfod lleoliad nod penodol mewn rhestr o nodau
	def __eq__(self, other):
		return isinstance(other, Nod) and self is other

	def isspace(self):
		return self.llinyn.isspace()

	def isatalnod(self):
		return self.llinyn in cy.atalnodau

	def isllafariad(self):
		return self.llinyn in cy.llafariaid

	def iscytsain(self):
		return self.llinyn in cy.cytseiniaid

	def hir2byr(self):
		s = self.llinyn
		if s == u'â' or s == u'á': return u'a'
		if s == u'ê' or s == u'ë': return 'e'
		if s == u'î' or s == u'ï': return 'i'
		if s == u'ô': return u'o'
		if s == u'û': return u'u'
		if s == u'ŵ': return u'w'
		if s == u'ŷ': return u'y'
		if s == u'â'.upper() or s == u'á'.upper(): return u'a'.upper()
		if s == u'ê'.upper() or s == u'ë'.upper(): return u'e'.upper()
		if s == u'î'.upper() or s == u'ï'.upper(): return u'i'.upper()
		if s == u'ô'.upper(): return u'o'.upper()
		if s == u'û'.upper(): return u'u'.upper()
		if s == u'ŵ'.upper(): return u'w'.upper()
		if s == u'ŷ'.upper(): return u'y'.upper()
		return s.lower()
		
#------------------------------------------------
class RhestrNodau(tuple):
	'''
	class: RhestrNodau
		mewnbwn: llinyn
		dyma lle mae llinynau yn cael mynediad i'r system
		felly mae angen trawsnewid i linynnau unicode (os oes angen) 
	 '''
	# override __new__ method (because tuples are immutable)
	def __new__(cls, s=None):

		# gwirio am linyn gwag
		if not s:
			return tuple.__new__(cls,[])

		# gwirio am linyn unicode
		elif type(s) == str or type(s) == unicode:
			if type(s) != unicode:
				s = s.decode('utf-8')

		# gwirio am restr o nodau
		elif type(s) == list:
			return tuple.__new__(cls,s)
		else:
			return tuple.__new__(cls,[])
			
		# adeiladu'r rhestr
		nodau = list()
		idx = 0
		while idx < len(s):
			c = s[idx]
			if c in ['c','d','f','n','l','p','r','s','t'] and idx < len(s) - 1:
				c_nesaf = s[idx+1]
				if	 c=='c' and c_nesaf=='h': nodau.append(Nod(u'ch')); idx += 1;
				elif c=='d' and c_nesaf=='d': nodau.append(Nod(u'dd')); idx += 1;
				elif c=='f' and c_nesaf=='f': nodau.append(Nod(u'ff')); idx += 1;
				elif c=='n' and c_nesaf=='g': nodau.append(Nod(u'ng')); idx += 1;
				elif c=='l' and c_nesaf=='l': nodau.append(Nod(u'll')); idx += 1;
				elif c=='p' and c_nesaf=='h': nodau.append(Nod(u'ph')); idx += 1;
				elif c=='r' and c_nesaf=='h': nodau.append(Nod(u'rh')); idx += 1;
				elif c=='t' and c_nesaf=='h': nodau.append(Nod(u'th')); idx += 1;
				elif c=='s' and c_nesaf=='h': nodau.append(Nod(u'sh')); idx += 1;
				else: 
					nodau.append(Nod(c))
			else: 
				nodau.append(Nod(c))
			idx += 1
		return tuple.__new__(cls, nodau)
			
	def __unicode__(self):
		return	u''.join([ nod.llinyn for nod in self ])
		
	def __str__(self):
		return self.__unicode__().encode('utf-8')
		
	def __eq__(self, other):
		return (
			isinstance(other, RhestrNodau) and
			len(self) == len(other) and 
			all( [a.llinyn==b.llinyn for a,b in zip(self,other) ])
		)
		
	def llinyn(self):
		return self.__unicode__()
		
	def rhestr_clymau(self, trwsio=True):
		return RhestrClymau(self, trwsio=True)
		
	def hir2byr(self):
		return ''.join([ nod.hir2byr() for nod in self ])

#------------------------------------------------
class Cwlwm(list):
	'''
	class Cwlwm 
	'''
	
	def __init__(self, nodau):
		super(Cwlwm, self).__init__()
		for nod in nodau:
			self.append(nod)

	def __eq__(self, other):
		return (
			isinstance(other, Cwlwm) and
			len(self) == len(other) and 
			all( [a.llinyn==b.llinyn for a,b in zip(self,other) ])
			# all( [a.llinyn.lower()==b.llinyn.lower() for a,b in zip(self,other) ])
		)

	def __unicode__(self):
		return u''.join([ c.llinyn for c in self ])

	def llinyn(self):
		return self.__unicode__()

#------------------------------------------------
class RhestrClymau(list):
	'''
	class RhestrClymau
	'''

	def __init__(self, nodau, trwsio=True):
		super(RhestrClymau, self).__init__()
		
		log.info("Creu rhestr clymau ar gyfer '%s'" % unicode(nodau))
		
		cwlwm_llafariaid = True
		c = []
		for nod in nodau:
			# estyn cwlwm llarariaid
			if cwlwm_llafariaid and nod.isllafariad():
					c.append( nod )

			# cau cwlwm llarariaid
			elif cwlwm_llafariaid and nod.iscytsain() : 
				self.append( Cwlwm(c) )
				cwlwm_llafariaid = False 
				c = [ nod ]
		
			# estyn cwlwm cytseiniaid
			elif not cwlwm_llafariaid and nod.iscytsain() : 
					c.append( nod )

			# cau cwlwm cytseiniaid
			elif not cwlwm_llafariaid and nod.isllafariad():
				self.append( Cwlwm(c) )
				cwlwm_llafariaid = True 
				c = [ nod ]

			# fel arall, atodi'r nod i'r cwlwm (ond eithrio atalnodau)
			else:
				if not nod.isatalnod() and not nod.isspace():
					c.append( nod )		

		# diweddeb
		self.append( Cwlwm(c) )
		if cwlwm_llafariaid:
			self.append( Cwlwm([]) )
					
		if trwsio:
			for j in range(0, len(self), 2):
				# if debug:
				#	print '----------'
				#	print self[j].llinyn()
				# print lliw.cyan( self[j].llinyn() )
				# print lliw.magenta(cw[2].llinyn)
				
				c = self[j]
				
				#-----------------------------
				# dau lafariad
				# ddeusain talgron w (e.e. wa,wy), ond nid ia,ie, i'r
				# cwlwm cytseiniaid olaf-ond-un e.g. 
				# .b.e.dw/d.e.d.wy.dd -> d.e.dw 
				# .m.e.d.i/y.ml.e.d.ia.d -> y.ml.e.di.a.d

				if len( self[j] ) == 2:
					ds = ''.join([ self[j][0].hir2byr() + self[j][1].hir2byr() ])
					if ds in cy.deuseiniaid['deusill']:
						olaf = self[j].pop() # nod
						self.insert(j+1, Cwlwm( [olaf] ))
						self.insert(j+1, Cwlwm( [] ))
				
				
				#-----------------------------
				# tri llafariad
				# hac: "hir2byr" fan hyn i osgoi e.e. dŵad -> d.ŵ..a.d)
				
				if len( self[j] ) == 3:
					ds1 = ''.join([ self[j][0].hir2byr() + self[j][1].hir2byr() ])
					if not cy.dosbarth_deusain.has_key(ds1):
						log.error('methu adnabod y ddeusain %s', ds1)
						break
					ds2 = ''.join([ self[j][1].hir2byr() + self[j][2].hir2byr() ])
					if not cy.dosbarth_deusain.has_key(ds2):
						log.error('methu adnabod y ddeusain %s', ds2)
						break
					
					log.debug( 'Triawd o lafariaid: %s/%s' % (cy.dosbarth_deusain[ds1], cy.dosbarth_deusain[ds2]) )
					
					# T-T: dim on dau posib: wiw neu iwi
					# wiw - tebyg i T-LL  (un sill)
					# gwiw: .g.wiw. -> .gw.iw.
					# iwi - tebyg i LL-T (dwy sill)
					# piwis: .p.iwi.s -> .p.iw..i.s
					if ds1 in cy.deuseiniaid['talgron'] and ds2 in cy.deuseiniaid['talgron']:
						if self[j].llinyn() == 'wiw':
							self[j].reverse()
							cyntaf = self[j].pop() # nod
							self[j].reverse()
							if j > 0:
								self[j-1].append( cyntaf )
							else:
								self.insert(j, Cwlwm( [cyntaf] ))
								self.insert(j, Cwlwm( [] ))
						if self[j].llinyn == 'iwi':
							olaf = self[j].pop() # nod
							self.insert(j+1, Cwlwm( [olaf] ) )
							self.insert(j+1, Cwlwm( [] ) )
						
					# T-LL : llafariad cyntaf naill ai yn 'i' neu 'w'
					# dim ond y rhan lleddf (y ddau olaf) sydd yn bwysig mewn odl (iaith, gwaith)
					# genwair: .g.e.n.wai.r -> .g.e.nw.ai.r
					# wair: wai.r -> .w.ai.r
					# iaith: iai.th -> .i.ai.th
					# gwaith: .g.wai.th -> .gw.ai.th
					elif ds1 in cy.deuseiniaid['talgron'] and ds2 not in cy.deuseiniaid['talgron']:
						self[j].reverse()
						cyntaf = self[j].pop() # nod
						self[j].reverse()
						if j > 0:
							self[j-1].append( cyntaf )
						else:
							self.insert(j, Cwlwm( [cyntaf] ))
							self.insert(j, Cwlwm( [] ))
							
					# LL-T 
					# mae'r trydydd llafariad yn cario sill ei hun
					# awen: awe.n -> aw..e.n
					# 
					elif ds1 not in cy.deuseiniaid['talgron'] and ds2 in cy.deuseiniaid['talgron']:
						olaf = self[j].pop()
						self.insert(j+1, Cwlwm( [olaf] ))
						self.insert(j+1, Cwlwm( [] ))
						
						# self.insert(j+1, Cwlwm( [olaf_ond_un, olaf] ))
						# self.insert(j+1, Cwlwm( [] ))

					# LL-LL
					# prin mewn cyfuniad o dri: aew, oew, auw, euw, ouw, eyw, oyw
					# gloyw: .gl.oyw. -> .gl.oy.w) ??
					# daear: .d.aea.r => .d.ae..a.r
					else:
						olaf = self[j].pop()
						self.insert(j+1, Cwlwm( [olaf] ))
						self.insert(j+1, Cwlwm( [] ))
				

				# pedwar llafariad
				# T-T: ieuanc: ieua.nc -> ie..ua.nc
				# LL-T: glawio: gl.awio. -> .gl.aw..io. | gl.oywi. -> gl.oy..wi.
				if len( self[j] ) == 4:
						olaf = self[j].pop() 
						olaf_ond_un = self[j].pop()
						self.insert(j+1, Cwlwm( [olaf_ond_un, olaf] ))
						self.insert(j+1, Cwlwm( [] ))

			# diwedd y pass cyntaf
			# if debug:
			#	print self

			#-----------------------------
			# Mân reolau i helpu darganfod w-gytsain
			
			# w-gytsain ar ddechrau gair 
			# gwl e.e. gwlad => .g.w.l.a.d -> .gwl.a.d
			# gwr e.e. gwroldeb -> .g.w.r.o.ld.e.b -> .gwr.o.ld.e.b
			if len(self) > 4 and not self[0] and self[1].llinyn() == 'g' and self[2].llinyn() == 'w' and self[3].llinyn() in ['r','rh','l'] :
				self[3].reverse()
				self[3].append( self[2].pop() )
				self[3].append( self[1].pop() )
				self[3].reverse()
				self.reverse()
				self.pop()
				self.pop()
				self.reverse()
				
			if len(self) > 2 and self[0].llinyn() == 'w' and self[1][0].llinyn in ['r','l'] :
				cyntaf = self[0].pop()
				self[1].reverse()
				self[1].append( cyntaf )
				self[1].reverse()
			
			# 'w' ar ddiwedd gair
			# Caiff hyn ei drafod yn AYG, ond mae CC yn hawlio bod geiriau fel 'bedw' bellach yn ddeusill 
			# if len(self) > 4 and not self[-1] and self[-2].llinyn() == 'w'and not any([ nodau.llinyn() in ['galw', 'acw', 'cwcw', 'dacw', 'hwnnw', 'lludw', 'pitw'] ]):
			#		olaf = self[-2].pop()
			#		self[-3].append( olaf )
			#		self.pop()
			#		self.pop()

			
					
	def __getitem__(self, offset):
		return list.__getitem__(self, offset)

	def __unicode__(self):
		return u'.'.join( [''.join([c.llinyn for c in cwlwm]) for cwlwm in self] )

	def __str__(self):
		return self.__unicode__().encode('utf-8')

	def llinyn(self):
		return self.__unicode__()

#------------------------------------------------
def main():
	print 'nodau.py'
		
	rhestr_llinynau = (
		# cyffredin
		'prydferth',
		'dramodydd',
		# desusain deusill
		'duon',
		'eos',
		'suo',
		# lluosill acennog
		'dyfalbarhau',
		'dyfalbarhad',
		'cymraeg',
		# w-gytsain ar y dechrau
		'gwrando',
		'gwr',
		'gwroldeb',
		'gwrhydri',
		'gwledd',
		'wlad',		
		# w-gytsain ar y diwedd
		'berw',
		'bedw',				
		 'pitw',			# eithriad
		'llw',
		# triawd T-T
		'haleliwia',	
		'anifeiliaid',	
		# triawd T-LL
		'iaith',			
		'gwaith',
		'genwair',			
		# triawd LL-T
		'awen',
		'distewi',
		'gwiw',
		'wiw',
		'piwis',
		'distewi',
		# triawd LL-LL
		'gloyw',
		# pedwarawd
		'gwrandawiad',
		'glawio',
		'ieuanc',
		'gloywi',
		'yw',

	)
	for s in rhestr_llinynau:
		print '-------------------'
		nodau = RhestrNodau(s)
		print nodau
		print nodau.rhestr_clymau(trwsio=True)
		
if __name__ == '__main__': 
	import logging.config
	logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
	main()


