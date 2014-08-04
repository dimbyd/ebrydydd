#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, re
from gair import Gair
from llinell import Llinell
from peiriant import Peiriant

import odl as od
import lliwiau as lliw

import logging
out = logging.getLogger(__name__)

import re
global debug
debug = True

class Cwpled:
	'''
	class Cwpled:
	mewnbwn: dau linyn safonol yn y drefn gywir 
	'''

	def __init__(self, x_llinell, y_llinell):
		self.cyntaf = x_llinell
		self.ail	= y_llinell

	def __unicode__(self):
		return self.cyntaf.llinyn() + '\n' + self.ail.llinyn()

	def __str__(self):
		return self.__unicode__().encode('utf-8')
		
	def oes_cwpled_cywydd(self):
		out.info('prawf: cwpled cywydd')

		sylwadau = []
		pe = Peiriant()
		adro1 = pe.oes_cynghanedd(self.cyntaf)
		adro2 = pe.oes_cynghanedd(self.ail)

		ateb = False
		# nifer sillau
		if self.cyntaf.nifer_sillau() != 7 :
			out.info('cwpled cywydd: methiant: nid oes saith sill yn y linell gyntaf')
		elif self.ail.nifer_sillau() != 7:
			out.info('cwpled cywydd: methiant: nid oes saith sill yn yr ail linell')
		# acenion
		elif self.cyntaf.ybrifodl.pwyslais() == self.ail.ybrifodl.pwyslais():
			out.info('cwpled cywydd: methiant: acenion o\'r un fath')
		# cynghanedd
		elif adro1.cynghanedd == 'DIM':
			out.info('cwpled cywydd: methiant: dim cynghanedd yn y linell gyntaf')
		elif adro2.cynghanedd == 'DIM':
			out.info('cwpled cywydd: methiant: dim cynghanedd yn yr ail linell')
		elif adro2.cynghanedd in ['LLU', 'LLL']:
			out.info('cwpled cywydd: methiant: cynghanedd lusg yn yr ail linell')
		# odl
		elif not od.oes_odl( self.cyntaf.geiriau[-1], self.ail.geiriau[-1] ) :
			sylwadau.append('cwpled cywydd: methiant: dim odl')
		else:
			ateb = True

		return ateb, [adro1, adro2], sylwadau

	def oes_toddaid(self, byr=False, hir=False):
		enw = 'toddaid'
		if byr: enw += ' byr'
		if hir: enw += ' hir'
		out.info('prawf: ' + enw)
		sylwadau = []
		pe = Peiriant()
		ateb = True

		# llinell gyntaf (hollti ar y gysylltnod)
		y_cyntaf = []		# geiriau o flaen y gysylltnod
		cyrch = []		# geiriau yn dilyn y gysylltnod (cyrch)
		o_flaen = True
		for gair in self.cyntaf.geiriau:
			if gair.llinyn() == '-':
				o_flaen = False
			elif o_flaen:
				y_cyntaf.append(gair)
			else:
				cyrch.append(gair)

		# profi presenoldeb cysylltnod
		if o_flaen:
			out.info(enw + ': methiant: nid oes cysylltnod yn y linell gyntaf.')
			ateb = False
		
		# profi hyd y cyrch
		ns_cyrch = sum([ g.nifer_sillau() for g in cyrch ])
		if ns_cyrch < 1 or ns_cyrch > 3:
			out.info(enw + ': methiant: nid oes 1-3 sill yn y cyrch.')
			ateb = False
		
		# profi am air luosill ar ddiwedd yr ail linell
		if self.ail.geiriau[-1].nifer_sillau() < 2:
			out.info(enw + ': methiant: dim gair lluosill ar ddiwedd yr ail linell.')
			ateb = False

		# ail linell (dibynnu ar pa fath o doddaid -/hir/byr)
		if hir:
			yr_ail = list(cyrch)
			pengoll = []
			cynghanedd = False
			for gair in self.ail.geiriau:
				if not cynghanedd:
					yr_ail.append(gair)
					adro = pe.oes_cynghanedd( Llinell( yr_ail ) )
					if adro.cynghanedd not in ['DIM', 'LLU', 'LLL']:
						cynghanedd = True
				else:
					pengoll.append(gair)
	
			
		llinell_1 = Llinell( y_cyntaf )
		llinell_2 = Llinell( yr_ail )
							
		# cynghanedd
		adro1 = pe.oes_cynghanedd(llinell_1)
		if adro1.cynghanedd == 'DIM':
			sylwadau.append('toddaid byr: dim cynghanedd yn y linell gyntaf')
			ateb = False
		adro2 = pe.oes_cynghanedd(llinell_2)
		if adro2.cynghanedd == 'DIM':
			sylwadau.append('toddaid byr: dim cynghanedd yn yr ail linell')
			ateb = False
		
		# odl
		if not geiriau_d:
			if not od.oes_odl( y_cyntaf[-1], yr_ail[-1] ):
				sylwadau.append(enw + 'methiant: dim odl')
				ateb = False
		else:
			if not od.oes_odl( geiriau_a[-1], geiriau_d[-1] ) :
				sylwadau.append(enw + 'methiant: dim odl')
				ateb = False

		# nifer sillau
		if byr and self.cyntaf.nifer_sillau() != 10:
			out.info(enw + ': nid oes 10 sill i\'r linell gyntaf')
			ateb = False
		if self.ail.nifer_sillau() != 6:
			out.info(enw + ': nid oes 6 sill i\'r ail linell')
			ateb = False




		# wedi pasio
		return ateb, [adro1, adro2], sylwadau




	def oes_toddaid_byr(self):
		out.info('prawf: toddaid byr')
		sylwadau = []
		pe = Peiriant()
		ateb = True

		# nifer sillau
		if self.cyntaf.nifer_sillau() != 10:
			sylwadau.append('torr mesur (toddaid byr): nid oes 10 sill i\'r linell gyntaf')
			ateb = False
		if self.ail.nifer_sillau() != 6:
			sylwadau.append('torr mesur (toddaid byr): nid oes 6 sill i\'r ail linell')
			ateb = False

		# llinell gyntaf
		geiriau_a = []
		geiriau_b = []
		rhan_un = True
		for gair in self.cyntaf.geiriau:
			if gair.llinyn() == '-':
				rhan_un = False
			elif rhan_un:
				geiriau_a.append(gair)
			else:
				geiriau_b.append(gair)

		# profi presenoldeb cysylltnod
		if rhan_un:
			sylwadau.append('torr mesur (toddaid byr): nid oes cysylltnod yn y linell gyntaf.')
			ateb = False

		# profi hyd y cyrch
		ns_cyrch = sum([ g.nifer_sillau() for g in geiriau_b ])
		if ns_cyrch < 1 or ns_cyrch > 3:
			sylwadau.append('torr mesur (toddaid byr): nid oes 1-3 sill yn y cyrch.')
			ateb = False
		
		# ail linell
		geiriau_c = list(geiriau_b)
		geiriau_d = []
		cyng = False
		for gair in self.ail.geiriau:
			if not cyng:
				geiriau_c.append(gair)
				adro = pe.oes_cynghanedd( Llinell(geiriau_c) )
				if adro.cynghanedd not in ['DIM', 'LLU', 'LLL']:
					cyng = True
			else:
				geiriau_d.append(gair)
		
		# profi am air luosill ar ddiwedd yr ail linell
		if self.ail.geiriau[-1].nifer_sillau() < 2:
			sylwadau.append('torr mesur (toddaid byr): dim gair luosill ar ddiwedd yr ail linell.')
			ateb = False
			
		llinell_1 = Llinell( geiriau_a )
		llinell_2 = Llinell( geiriau_c )
		pengoll = geiriau_d
							
		# cynghanedd
		adro1 = pe.oes_cynghanedd(llinell_1)
		if adro1.cynghanedd == 'DIM':
			sylwadau.append('toddaid byr: dim cynghanedd yn y linell gyntaf')
			ateb = False
		adro2 = pe.oes_cynghanedd(llinell_2)
		if adro2.cynghanedd == 'DIM':
			sylwadau.append('toddaid byr: dim cynghanedd yn yr ail linell')
			ateb = False
		
		# odl
		if not geiriau_d:
			if not od.oes_odl( geiriau_a[-1], geiriau_c[-1] ):
				sylwadau.append('toddaid byr: dim odl')
				ateb = False
		else:
			if not od.oes_odl( geiriau_a[-1], geiriau_d[-1] ) :
				sylwadau.append('toddaid byr: dim odl')
				ateb = False

		# wedi pasio
		return ateb, [adro1, adro2], sylwadau

	def oes_toddaid_hir(self):
		out.info('prawf toddaid hir')
		sylwadau = []
		pe = Peiriant()
		ateb = True

		# nifer sillau
		if self.cyntaf.nifer_sillau() != 10:
			sylwadau.append('torr mesur (toddaid hir): nid oes 10 sill i\'r linell gyntaf')
			ateb = False
		if self.ail.nifer_sillau() != 10:
			sylwadau.append('torr mesur (toddaid hir): nid oes 10 sill i\'r ail linell')
			ateb = False

		# llinell gyntaf
		geiriau_a = []
		geiriau_b = []
		rhan_un = True
		for gair in self.cyntaf.geiriau:
			if gair.llinyn() == '-':
				rhan_un = False
			elif rhan_un:
				geiriau_a.append(gair)
			else:
				geiriau_b.append(gair)

		# profi presenoldeb cysylltnod
		if rhan_un:
			sylwadau.append('torr mesur (toddaid hir): nid oes cysylltnod yn y linell gyntaf.')
			ateb = False

		# profi hyd y cyrch
		ns_cyrch = sum([ g.nifer_sillau() for g in geiriau_b ])
		if ns_cyrch < 1 or ns_cyrch > 3:
			sylwadau.append('torr mesur (toddaid hir): nid oes 1-3 sill yn y cyrch.')
			ateb = False

		llinell_a = Llinell( geiriau_a )
		cyrch = geiriau_b
							
		# cynghanedd
		adro1 = pe.oes_cynghanedd( llinell_a )
		if adro1.cynghanedd == 'DIM':
			sylwadau.append('toddaid hir: dim cynghanedd yn y linell gyntaf')
			ateb = False
		adro2 = pe.oes_cynghanedd( self.ail )
		if adro2.cynghanedd == 'DIM':
			sylwadau.append('toddaid hir: dim cynghanedd yn yr ail linell')
			ateb = False
		
		# odl
		# print [g.llinyn() for g in geiriau_a]
		# print cyrch
		# print rhan_un
		# if cyrch and adro2.data.has_key('gorffwysfa'):
		#	for gorffwysfa in adro2.data['gorffwysfa'] :
		if not od.oes_odl( llinell_a.geiriau[-1], self.ail.geiriau[-1] ):
			sylwadau.append('toddaid: dim odl')
			ateb = False

		# wedi pasio
		return ateb, [adro1, adro2], sylwadau

class Cerdd(object):
	'''
	class Cerdd:
	'''
	def __init__(self, llinellau):
		self.llinellau = llinellau

	def __unicode__(self):
		return '\n'.join([ llinell.llinyn() for llinell in self.llinellau ])

	def __str__(self):
		return self.__unicode__().encode('utf-8')
		
	def oes_cywydd(self):
		out.info('prawf cywydd')
		ateb = True
		adro = []
		sylwadau = []

		llinellau = list(self.llinellau)
		llinellau.reverse()
		while llinellau:
			cyntaf = llinellau.pop()
			if not llinellau:
				sylwadau.append('torr mesur (cywydd): llinell unigol')
				ateb = False
			ail = llinellau.pop()
			cwpled = Cwpled(cyntaf,ail)
			# check
			ateb_cc, adro_cc, sylwadau_cc = cwpled.oes_cwpled_cywydd()
			if not ateb_cc:
				sylwadau.append('torr mesur (cywydd): ' + ':'.join(sylwadau_cc))
				ateb = False
			adro.extend(adro_cc)
		return ateb, adro, sylwadau

	def oes_englyn(self):
		out.info('prawf englyn')
		ateb = True
		adro = []
		sylwadau = []

		llinellau = list(self.llinellau)
		if not llinellau or len(llinellau) != 4:
			sylwadau.append('torr mesur (englyn): nid oes 4 llinell')
			ateb = False

		cwpled_1 = Cwpled( llinellau[0], llinellau[1] )
		ateb_tb, adro_tb, syl_tb = cwpled_1.oes_toddaid_byr()
		if adro_tb[1].cynghanedd in ['LLU','LLL']:
			sylwadau.append('torr mesur (englyn): cynghanedd lusg rhwng y cyrch a\'r ail linell')
			ateb = False

		cwpled_2 = Cwpled( llinellau[2], llinellau[3] ) 
		ateb_cc, adro_cc, syl_cc = cwpled_2.oes_cwpled_cywydd()
		
		if adro_cc[1].cynghanedd in ['LLU','LLL']:
			sylwadau.append('torr mesur (englyn): cynghanedd lusg yn y linell olaf')
			ateb = False
		# print '+++++'
		# print adro_tb[0]
		# print adro_tb[1]
		# print adro_cc[0]
		# print adro_cc[1]
		
		ateb = ateb_tb and ateb_cc
		return ateb, adro_tb + adro_cc, syl_tb + syl_cc

	def oes_cyhydedd_nawban(self):
		out.info('prawf cyhydedd nawban')
		pe = Peiriant()
		ateb = True
		sylwadau = []
		adro = []
		# nifer sillau
		if not self.llinellau or len(self.llinellau) != 4:
			sylwadau.append('torr mesur (cyhydedd nawban): nid oes 4 llinell')
			ateb = False
		else:
			for llinell in self.llinellau:
				if llinell.nifer_sillau() != 9:
					sylwadau.append('torr mesur (cyhydedd nawban): rhaid cael naw sill ymhob llinell')
					ateb = False
				ad = pe.oes_cynghanedd( llinell )
				adro.append(ad)
				if ad.cynghanedd == 'DIM':
					sylwadau.append( 'torr mesur (cyhydedd nawban): dim cynghanedd (%s)' % llinell.llinyn() )
					ateb = False
					break
		
		for j in range( len(self.llinellau) - 1 ):
			odl = od.oes_odl(self.llinellau[j].geiriau[-1], self.llinellau[j+1].geiriau[-1])
			if not odl:
				sylwadau.append('torr mesur (cyhydedd nawban): dim odl')
				ateb = False
				break

		return ateb, adro, sylwadau
		
		
	def oes_hir_a_thoddaid(self):
		out.info('prawf hir-a-thoddaid')
		pe = Peiriant()
		ateb = True
		adro = []
		sylwadau = []

		llinellau = list(self.llinellau)
		llinellau.reverse()
		
		# creu rhestr cwpledi
		cwpledi = []
		while llinellau:
			cyntaf = llinellau.pop()
			if not llinellau:
				sylwadau.append('torr mesur (hir-a-thoddaid): llinell unigol')
				ateb = False
			ail = llinellau.pop()
			cwpledi.append( Cwpled(cyntaf,ail) )
		
		if len(cwpledi) < 2:
			sylwadau.append('torr mesur (hir-a-thoddaid): dim digon o linellau')
			ateb = False
		
		# profi cynghanedd y cwpledi, ar wahan i'r olaf
		adro = []
		for cwpled in cwpledi[:-1]:
			# nifer sillau
			if cwpled.cyntaf.nifer_sillau() != 10 or cwpled.ail.nifer_sillau() != 10:
				sylwadau.append('torr mesur (hir-a-thoddaid): mae angen 10 sill fan hyn')
				ateb = False
			# cynghanedd
			adro1 = pe.oes_cynghanedd( cwpled.cyntaf )
			if adro1.cynghanedd == 'DIM':
				sylwadau.append('torr mesur (hir-a-thoddaid): dim cynghanedd yn y linell gyntaf')
				ateb = False
			adro2 = pe.oes_cynghanedd( cwpled.ail )
			if adro2.cynghanedd == 'DIM':
				sylwadau.append('torr mesur (hir-a-thoddaid): dim cynghanedd yn yr ail linell')
				ateb = False
			# odl
			if not od.oes_odl( cwpled.cyntaf.geiriau[-1], cwpled.ail.geiriau[-1] ) :
				sylwadau.append('torr mesur (hir-a-thoddaid): dim odl')
				ateb = False
			adro.extend([ adro1, adro2 ])
			
		# profi toddaid hi cwpled olaf
		# olaf = cwpledi[-1]
		ateb_tb, adro_tb, syl_tb = cwpledi[-1].oes_toddaid_hir()
		if ateb_tb == False:
			sylwadau.append('torr mesur (hir-a-thoddaid): dim toddaid byr yn y ddwy linell olaf')
			ateb = False
		adro.extend( adro_tb )
		
		return ateb, adro, sylwadau


#------------------------------------------------
def main():

	print '------------------------------'
	print 'OES_CWPLED_CYWYDD'
	print '------------------------------'
	# x = "Drwy eu sain a'u hystyr sydd"
	# y = "Yn galw ar ei gilydd."
	s1 = "Hen linell bell nad yw'n bod,"
	s2 = "Hen derfyn nad yw'n darfod."

	cwpled = Cwpled( Llinell(s1), Llinell(s2) )
	print cwpled.cyntaf.llinyn()
	print cwpled.ail.llinyn()
	
	ateb, adro, syl = cwpled.oes_cwpled_cywydd()
	
	print lliw.magenta('CWPLED CYWYDD') if ateb else lliw.magenta('XXX')
	print adro[0]
	print adro[1]

	print '------------------------------'
	print 'OES_TODDAID_BYR'
	print '------------------------------'
	s1 = "Talog, boed law, boed heulwen, - y saif hi"
	s2 = "Er oes faith, anniben;"
	cwpled = Cwpled( Llinell(s1), Llinell(s2) )
	print cwpled
	
	ateb, adro, syl = cwpled.oes_toddaid_byr()

	print syl
	
	print lliw.magenta('TODDAID BYR') if ateb else lliw.magenta('XXX')
	for ad in adro:
		print ad

	print '------------------------------'
	print 'OES_TODDAID_HIR'
	print '------------------------------'
	s1 = "Ac yn nyfnder y weryd - gwn y car"
	s2 = "Ei gusan olaf megis anwylyd."
	cwpled = Cwpled( Llinell(s1), Llinell(s2) )
	print cwpled
	
	ateb, adro, syl = cwpled.oes_toddaid_hir()

	print syl
	
	print lliw.magenta('TODDAID HIR') if ateb else lliw.magenta('XXX')
	for ad in adro:
		print ad
	
	print '------------------------------'
	print 'OES_CYWYDD'
	print '------------------------------'
	s = "Pa eisiau dim hapusach,\n Na byd yr aderyn bach?\nByd o hedfan a chanu\nA hwylio toc i gael tu."
	llinynnau = s.split('\n')
	llinellau = [ Llinell(s.strip()) for s in llinynnau ]
	cerdd = Cerdd( llinellau )
	print cerdd
	
	ateb, adro, syl = cerdd.oes_cywydd()

	print lliw.magenta('CYWYDD') if ateb else lliw.magenta('XXX')
	print syl
	for ad in adro:
		print ad

	print '------------------------------'
	print 'OES_ENGLYN'
	print '------------------------------'
	s = "Talog, boed law, boed heulwen, - y saif hi\nEr oes faith, anniben;\nDaw ein byw sydyn i ben\nOnd hiroes yw braint derwen."
	llinynnau = s.split('\n')
	llinellau = [ Llinell(s) for s in llinynnau ]
	cerdd = Cerdd( llinellau )
	print cerdd
	
	ateb, adro, syl = cerdd.oes_englyn()
	
	print lliw.magenta('ENGLYN') if ateb else lliw.magenta('XXX')
	for ad in adro:
		print ad


	print '------------------------------'
	print 'OES_CYHYDEDD_NAWBAN'
	print '------------------------------'
	s = "Cyfled yw dy gred â daear gron,\nTery ffiniau tir a phennod ton;\nHyd yr êl yr hylithr awelon,\nHyd y tywyn haul, duw wyt yn hon."
	llinynnau = s.split('\n')
	llinellau = [ Llinell(s) for s in llinynnau ]
	cerdd = Cerdd( llinellau )
	print cerdd
	
	ateb, adro, syl = cerdd.oes_cyhydedd_nawban()

	print syl
	
	print lliw.magenta('CYHYDEDD NAWBAN') if ateb else lliw.magenta('XXX')
	for ad in adro:
		print ad


if __name__ == '__main__': main()



