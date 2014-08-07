#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
mesurau.py - chwilio am linellau cynghenedd mewn cyfundrefn dilys
'''

from llinell import Llinell
from dadansoddwr import Dadansoddwr
from pennill import Cwpled, Pennill

import odl as od
import lliwiau as lliw

import logging
log = logging.getLogger(__name__)

class DadansoddwrPennill(object):
	'''
	class DadansoddwrPennill
	'''
	def __init__(self): 
		pass


	def oes_cwpled_cywydd(self, cwpled):
		log.info('prawf: cwpled cywydd')

		sylwadau = []
		dad = Dadansoddwr()
		adro1 = dad.oes_cynghanedd(cwpled.cyntaf)
		adro2 = dad.oes_cynghanedd(cwpled.ail)

		ateb = True
		if cwpled.cyntaf.nifer_sillau() != 7 :
			sylwadau.append('cwpled cywydd: methiant: nid oes saith sill yn y linell gyntaf')
			ateb = False
		if cwpled.ail.nifer_sillau() != 7:
			sylwadau.append('cwpled cywydd: methiant: nid oes saith sill yn yr ail linell')
			ateb = False
		if cwpled.cyntaf.ybrifodl.pwyslais() == cwpled.ail.ybrifodl.pwyslais():
			sylwadau.append('cwpled cywydd: methiant: acenion o\'r un fath')
			ateb = False
		if adro1.cynghanedd == 'DIM':
			sylwadau.append('cwpled cywydd: methiant: dim cynghanedd yn y linell gyntaf')
			ateb = False
		if adro2.cynghanedd == 'DIM':
			sylwadau.append('cwpled cywydd: methiant: dim cynghanedd yn yr ail linell')
			ateb = False
		if adro2.cynghanedd in ['LLU', 'LLL']:
			sylwadau.append('cwpled cywydd: methiant: cynghanedd lusg yn yr ail linell')
			ateb = False
		if not od.oes_odl( cwpled.cyntaf.geiriau[-1], cwpled.ail.geiriau[-1] ) :
			sylwadau.append('cwpled cywydd: methiant: dim odl')
			ateb = False

		return [ateb, [adro1, adro2], sylwadau]
	

	def oes_toddaid(self, cwpled, byr=False, hir=False):
		if byr: 
			enw = 'toddaid_byr'
		elif hir:
			enw = 'toddaid_hir'
		else:
			enw = 'toddaid'
		log.info('prawf: ' + enw)
		
		sylwadau = []
		dad = Dadansoddwr()
		ateb = True
		
		# profi am air luosill ar ddiwedd yr ail linell
		if cwpled.ail.geiriau[-1].nifer_sillau() < 2:
			sylwadau.append(enw + ': methiant: dim gair lluosill ar ddiwedd yr ail linell.')
			ateb = False
			
		# profi nifer sillau
		if cwpled.cyntaf.nifer_sillau() != 10:
			sylwadau.append(enw + ': nid oes 10 sill yn y linell gyntaf')
			ateb = False
		if byr:
			if cwpled.ail.nifer_sillau() != 6:
				sylwadau.append(enw + ': nid oes 6 sill i\'r ail linell')
				ateb = False
		elif hir:
			if cwpled.ail.nifer_sillau() != 10:
				sylwadau.append(enw + ': nid oes 10 sill i\'r ail linell')
				ateb = False
		else:
			if cwpled.ail.nifer_sillau() != 9:
				sylwadau.append(enw + ': nid oes 9 sill i\'r ail linell')
				ateb = False

		# prosesu'r linell gyntaf (hollti ar gysylltnod)
		rhestr_cyntaf = []		
		rhestr_cyrch = []		
		heibio = False
		for gair in cwpled.cyntaf.geiriau:
			if gair.llinyn() == '-':
				heibio = True
			elif not heibio:
				rhestr_cyntaf.append(gair)
			else:
				rhestr_cyrch.append(gair)
		
		llinell_cyntaf = Llinell( rhestr_cyntaf )

		# profi presenoldeb cysylltnod
		if not heibio:
			sylwadau.append(enw + ': methiant: dim cysylltnod yn y linell gyntaf.')
			ateb = False
		
		# profi nifer sillau y cyrch
		ns_cyrch = sum([ g.nifer_sillau() for g in rhestr_cyrch ])
		if ns_cyrch < 1 or ns_cyrch > 3:
			sylwadau.append(enw + ': methiant: nid oes 1-3 sill yn y cyrch.')
			ateb = False

		# profi am gynghanedd yn y linell gyntaf
		adro1 = dad.oes_cynghanedd(llinell_cyntaf)
		if adro1.cynghanedd == 'DIM':
			sylwadau.append(enw + ': dim cynghanedd yn y linell gyntaf')
			ateb = False
		
		# prosesu'r ail linell (dibynnu ar pa fath o doddaid)
		if not byr:
			adro2 = dad.oes_cynghanedd(cwpled.ail) # cyrch yn bengoll mewn toddaid neu doddaid hir
			if adro2.cynghanedd == 'DIM':
				sylwadau.append(enw + ': dim cynghanedd yn yr ail linell')
				ateb = False
		else:
			rhestr_ail = list(rhestr_cyrch)
			rhestr_pengoll = []
			llwyddiant = False
			for gair in cwpled.ail.geiriau:
				if not llwyddiant:
					rhestr_ail.append(gair)
					adro2 = dad.oes_cynghanedd( Llinell( rhestr_ail ) )
					if adro2.cynghanedd not in ['DIM', 'LLU', 'LLL']:
						llwyddiant = True
				else:
					rhestr_pengoll.append(gair)
			if not llwyddiant: 
				sylwadau.append(enw + ': dim cynghanedd yn y cyrch a rhan gyntaf yr ail linell')
				ateb = False
		
		# mae bob amser angen odl rhwng prifodl y gynghanedd gyntaf a diwedd yr ail linell
		if not od.oes_odl( rhestr_cyntaf[-1], cwpled.ail.geiriau[-1] ):
			sylwadau.append(enw + 'methiant: dim odl rhwng prifodl y gynghanedd gyntaf a diwedd yr ail linell')
			ateb = False

		# os toddaid neu doddaid hir, mae hefyd angen odl rhwng y cyrch a gorffwysfa'r ail linell
		# TODO: os oes mwy nag un gorffwysfa (e.e. sain), gall y cyrch odli gyda unrhyw un ohonynt
		if not byr:
			if adro2.data.has_key('gorffwysfeydd'):
				gorffwysfeydd = adro2.data['gorffwysfeydd']
				if rhestr_cyrch and not any([ od.oes_odl(rhestr_cyrch[-1], gorff) for gorff in gorffwysfeydd ]):
					sylwadau.append(enw + 'methiant: dim odl rhwng y cyrch a gorffwysfa yr ail linell')
					ateb = False
		
		# print ateb
		# print adro1
		# print adro2
		# print sylwadau
		# diwedd
		return [ateb, [adro1, adro2], sylwadau]
	

	def oes_cywydd(self, pennill):
		log.info('prawf cywydd')
		ateb = True
		adro = []
		sylwadau = []

		llinellau = list(pennill.llinellau)
		llinellau.reverse()
		while llinellau:
			cyntaf = llinellau.pop()
			if not llinellau:
				sylwadau.append('torr mesur (cywydd): llinell unigol')
				ateb = False
				break
			ail = llinellau.pop()
			print cyntaf
			print ail
			cwpled = Cwpled(cyntaf,ail)
			cwc  = self.oes_cwpled_cywydd( cwpled )
			if not cwc[0]:
				sylwadau.append('torr mesur (cywydd): ' + ':'.join( cwc[2] ))
				ateb = False
			adro.extend(cwc[1])

		return [ateb, adro, sylwadau]

	# englyn
	def oes_englyn(self, pennill):
		log.info('prawf englyn')
		ateb = True
		adro = []
		sylwadau = []

		llinellau = list(pennill.llinellau)
		if not llinellau or len(llinellau) != 4:
			sylwadau.append('torr mesur (englyn): nid oes 4 llinell')
			ateb = False
			return [ ateb, [], sylwadau]
		# paladr
		paladr = Cwpled( llinellau[0], llinellau[1] )
		tob = self.oes_toddaid( paladr, byr=True)
		if tob[1][1].cynghanedd in ['LLU','LLL']:
			sylwadau.append('torr mesur (englyn): cynghanedd lusg rhwng y cyrch a\'r ail linell')
			ateb = False
		
		# esgyll
		esgyll = Cwpled( llinellau[2], llinellau[3] ) 
		cwc = self.oes_cwpled_cywydd( esgyll )
		if cwc[1][1].cynghanedd in ['LLU','LLL']:
			sylwadau.append('torr mesur (englyn): cynghanedd lusg yn y linell olaf')
			ateb = False
			
		# TODO: mae angen gwirio odlau
		
		ateb = ateb and tob[0] and cwc[0]
		return [ ateb, tob[1]+cwc[1], sylwadau+tob[2]+cwc[2] ]
	

	def oes_cyhydedd_nawban(self, pennill):
		log.info('prawf cyhydedd nawban')
		dad = Dadansoddwr()
		ateb = True
		sylwadau = []
		adro = []

		# nifer llinellau
		if not pennill.llinellau or len(pennill.llinellau) != 4:
			sylwadau.append('torr mesur (cyhydedd nawban): nid oes 4 llinell')
			ateb = False
		
		# llinellau unigol
		for llinell in pennill.llinellau:

			# nifer sillau
			if llinell.nifer_sillau() != 9:
				sylwadau.append('torr mesur (cyhydedd nawban): rhaid cael naw sill ymhob llinell')
				ateb = False
			
			# cynghanedd
			ad = dad.oes_cynghanedd( llinell )
			adro.append(ad)
			if ad.cynghanedd == 'DIM':
				sylwadau.append( 'torr mesur (cyhydedd nawban): dim cynghanedd (%s)' % llinell.llinyn() )
				ateb = False
				break
		# odl
		for j in range( len(pennill.llinellau) - 1 ):
			odl = od.oes_odl(pennill.llinellau[j].geiriau[-1], pennill.llinellau[j+1].geiriau[-1])
			if not odl:
				sylwadau.append('torr mesur (cyhydedd nawban): dim odl')
				ateb = False
				break

		return [ ateb, adro, sylwadau ]
	
		
	def oes_hir_a_thoddaid(self, pennill):
		log.info('prawf hir-a-thoddaid')
		dad = Dadansoddwr()
		ateb = True
		adro = []
		sylwadau = []

		llinellau = list(pennill.llinellau)
		llinellau.reverse()
		
		# creu rhestr cwpledi
		cwpledi = []
		while llinellau:
			cyntaf = llinellau.pop()
			if not llinellau:
				sylwadau.append('torr mesur (hir-a-thoddaid): llinell unigol')
				ateb = False
				break
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
			adro1 = dad.oes_cynghanedd( cwpled.cyntaf )
			if adro1.cynghanedd == 'DIM':
				sylwadau.append('torr mesur (hir-a-thoddaid): dim cynghanedd yn y linell gyntaf')
				ateb = False
			adro2 = dad.oes_cynghanedd( cwpled.ail )
			if adro2.cynghanedd == 'DIM':
				sylwadau.append('torr mesur (hir-a-thoddaid): dim cynghanedd yn yr ail linell')
				ateb = False
			# odl
			if not od.oes_odl( cwpled.cyntaf.geiriau[-1], cwpled.ail.geiriau[-1] ) :
				sylwadau.append('torr mesur (hir-a-thoddaid): dim odl')
				ateb = False
			# adro.extend([ adro1, adro2 ])
			adro.append(adro1)
			adro.append(adro2)
			
		# profi toddaid hi cwpled olaf
		# olaf = cwpledi[-1]
		toh = self.oes_toddaid( cwpledi[-1], hir=True )
		if not toh[0]:
			sylwadau.append('torr mesur (hir-a-thoddaid): dim toddaid byr yn y ddwy linell olaf')
			ateb = False
		# adro.extend( toh[1] )
		adro.append( toh[1][0] )
		adro.append( toh[1][0] )
		
		return [ ateb, adro, sylwadau ]
	

	# y cyfan
	def oes_mesur(self, pennill):

		# print [llinell.llinyn() for llinell in pennill.llinellau ]
		# if not pennill or not pennill.llinellau:
		# 	return None
		log.info('prawf mesur: %s a.y.b.', pennill.llinellau[0] )

		dad = DadansoddwrPennill()
		
		# profi am linell unigol
		if len(pennill.llinellau) < 2:
			log.info('prawf mesur: llinell unigol')
			return None
			
		# cwpled
		if len(pennill.llinellau) == 2:
			cwpled = Cwpled( pennill.llinellau[0], pennill.llinellau[1] )
			print cwpled.cyntaf
			print cwpled.ail
			cwc = dad.oes_cwpled_cywydd( cwpled )
			if cwc[0]:	
				cwc[0] = 'CWC'	
				return cwc
			tod = dad.oes_toddaid( cwpled )
			if tod[0]:
				tod[0] = 'TOD'	
				return tod
			tob = dad.oes_toddaid( cwpled, byr=True )
			if tob[0]:
				tob[0] = 'TOB'
				return tob
			toh = dad.oes_toddaid( cwpled, hir=True )		
			if toh[0]:
				toh[0] = 'TOH'	
				return toh

		# cywydd, englyn, ayb.
		cyw = dad.oes_cywydd( pennill )
		if cyw[0]:		
			cyw[0] = 'CYW'	
			return cyw
		eng = dad.oes_englyn( pennill )
		if eng[0]:	
			eng[0] = 'ENG'
			return eng
		cyh = dad.oes_cyhydedd_nawban( pennill )
		if cyh[0]:
			cyh[0] = 'CYH'
			return cyh
		hat = dad.oes_hir_a_thoddaid( pennill )		
		if hat[0]:
			hat[0] = 'HAT'
			return hat
		
		# dim byd
		return ('DIM', cyw[1], cyw[2])


#------------------------------------------------
def main():
	
	s1 = "Hen linell bell nad yw'n bod,"
	s2 = "Hen derfyn nad yw'n darfod."
	
	s1 = "Talog, boed law, boed heulwen, - y saif hi"
	s2 = "Er oes faith, anniben;"
	
	# s1 = "Wedi blwng ymosod blin, - encilio:"
	# s2 = "Wedi'n creithio dianc i'r eithin."

	s1 = "A'u gweld yn eu dillad gwaith - trwy'r oriau"
	s2 = "Yn rhwygo o greigiau eu goreugwaith"

	# s1 = "Mae antur dan y mintys - ac anial"
	# s2 = "Yw'r creithiau mâl lle bu'r crythau melys."

	s1 = "Wele rith fel ymyl rhod - o'n cwmpas,"
	s2 = "Campwaith dewin hynod;"
	
	s1 = "Rhwydd gamwr, hawdd ei gymell - i'r mynydd"
	s2 = "a'r mannau anghysbell"


	cwpled = Cwpled( Llinell(s1), Llinell(s2) )
	
	dad = DadansoddwrPennill()	
	cwc = dad.oes_cwpled_cywydd( cwpled )
	tod = dad.oes_toddaid( cwpled )
	tob = dad.oes_toddaid( cwpled, byr=True )
	toh = dad.oes_toddaid( cwpled, hir=True )
	if cwc[0]:
		print lliw.cyan('CWC')
		for ad in cwc[1]: print ad
		print cwc[2]
	elif tod[0]:
		print lliw.cyan('TOD')
		for ad in tod[1]: print ad
		print tod[2]
	elif tob[0]:
		print lliw.cyan('TOB')
		for ad in tob[1]: print ad
		print tob[2]
	elif toh[0]:
		print lliw.cyan('TOH')
		for ad in toh[1]: print ad
		print toh[2]
	else:
		print lliw.cyan('DIM')
		for ad in tob[1]: print ad
		print tob[2]


if __name__ == '__main__': main()



