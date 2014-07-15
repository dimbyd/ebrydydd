#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
peiriant.py - peiriant dadansoddi cynghanedd

Gorffwysfa: y GAIR olaf yn y rhan gyntaf
	ni chaiff gair gwan fod ar yr orffwysfa
	y fannod (y, yr)
	rhagenwau (fy, dy, ei, ein, eich, eu)
	cysysllteiriau (a, ac, neu, na, yn, etc.)

	ADI: gorffwysfa ar un o'r tri sillaf cyntaf yn unig
	
	Nodiant AYG: Ochain cloch : a chanu clir
'''

# from acen import aceniad, nifer_sillau, pwyslais, traeannu_cytseiniaid
from odl import prawf_odl, prawf_odl_lusg
from cytseinedd import prawf_cytseinedd

import cysonion as cy
import llinyn as ll
import acen as ac
from llinell import Llinell

from adroddiad import Adroddiad

global debug
debug = False

# peiriant
class Peiriant(object):
	'''
	class Peiriant:
	'''
	def __init__(self): 
		pass
	# cynghanedd gytsain
	def prawf_cynghanedd_gytsain(self, s):
		'''
		ffwythiant: prawf_cynghanedd_gytsain
		mewnbwn:	llinyn
		allbwn:		adroddiad
		'''
		geiriau = s.split(' ')
		ybrifodl = geiriau[-1]

		# croes
		sillau = 0
		for j in range( len(geiriau)-1 ):
			# gwirio'r nifer sillau (AYG tud. 27)
			# CAC, ADI: rhaid i'r pwyslais ddod ar sill 1-4 (gorffwysfa yn acennog)
			# CDI, ADY: rhaid i'r pwyslais ddod ar sill 1-3	(gorffwysfa yn ddiacen)
			ace = ac.aceniad( geiriau[j], ybrifodl)
			sillau += ac.nifer_sillau( geiriau[j] )
			if ace in ['CAC','ADI'] and sillau  > 4:
				break
			if ace in ['CDI','ADY'] and sillau  > 3:
				break			
			
			# geiriau gwan (AYG tud. 28): bannod (article)
			if geiriau[j] in ['y','yn']:
				break
			# rhagenwau (pronouns)
			if geiriau[j] in ['fy','dy', 'di', 'ein', 'eich', 'eu']:
				break
			# cysyllteiriau (conjunctions)
			if geiriau[j] in ['a', 'ac', 'neu', 'na', 'yn', 'yw']:
				break
			
			chwith 	= ' '.join( geiriau[:j+1] )
			dde 	= ' '.join( geiriau[j+1:] ) 
			cyts, bai, data = prawf_cytseinedd(chwith, dde)
			# dianc os oes cytseinedd
			if cyts in ['CRO', 'COG']:
				data['gorffwysfa'] = (j),
				return Adroddiad(
					llinyn = s,
					cynghanedd = cyts,
					bai = bai,
					aceniad	= ac.aceniad( geiriau[j], ybrifodl ),
					data = data,
				)

		# traws
		sillau = 0
		for j in range( len(geiriau)-1 ):
			# gwirio'r nifer sillau
			sillau += ac.nifer_sillau( geiriau[j] )
			if sillau + ac.pwyslais( geiriau[j] ) > 4:
				break
			# geiriau gwan (AYG tud. 28): bannod (article)
			if geiriau[j] in ['y','yn']:
				break
			# rhagenwau (pronouns)
			if geiriau[j] in ['fy','dy', 'di', 'ein', 'eich', 'eu']:
				break
			# cysyllteiriau (conjunctions)
			if geiriau[j] in ['a', 'ac', 'neu', 'na', 'yn', 'yw']:
				break
			

			chwith 	= ' '.join( geiriau[:j+1] )
			dde 	= ' '.join( geiriau[j+1:] ) 
			cyts, bai, data = prawf_cytseinedd(chwith, dde)
			# dianc os oes cytseinedd
			if cyts in ['TRA', 'TRF']:
				data['gorffwysfa'] = (j),
				return Adroddiad(
					llinyn = s,
					cynghanedd = cyts,
					bai = bai,
					aceniad	= ac.aceniad( geiriau[j], ybrifodl ),
					data = data,
				)
		return None


	# cynghanedd lusg
	def prawf_cynghanedd_lusg(self, s):
		'''
		ffwythiant: prawf_cynghanedd_lusg
		mewnbwn: llinyn
		allbwn: adroddiad
		sylwadau:
			Rhaid i'r orffwysfa odli gyda pen blaen y brifodl
			Rhaid i'r brifodl fod yn air lluosill
			Mae'n bosib odli llafariad hir gyda'r llafariad ysgafn cyfatebol
		'''
		geiriau = s.split(' ')
		ybrifodl = geiriau[-1]
		# rhaid i'r brifodl for yn air lluosill
		if ac.nifer_sillau(ybrifodl) < 2:
			return None
		# iteru dros eiriau'r linell i ddarganfod yr orffwysfa
		for j in range( len(geiriau)-1 ):
			# if debug:
			# 	print geiriau[j] + ' / ' + ybrifodl
			
			# gwirio am odl lusg
			odl = prawf_odl_lusg( geiriau[j], ybrifodl )
		
			if odl:
				# dianc os oes odl gyflawn
				k = len(geiriau)-1
				return Adroddiad(
					llinyn = s,
					cynghanedd = 'LLU',
					data = {
						'gorffwysfa': (j,),
						'odl': ( ( j, odl[0] ), ( k, odl[1] ), )
					},
			)
		return None	


	# cynghanedd sain
	def prawf_cynghanedd_sain(self, s):
		'''
		ffwythiant: prawf_cynghanedd_sain
		mewnbwn: llinyn
		allbwn: adroddiad neu None
		'''
		geiriau = s.split(' ')
		ybrifodl = geiriau[-1]
		# iteru er mwyn darganfod yr orffwysfa gyntaf
		for j in range( len(geiriau)-2 ):
		
			yr_orffwysfa_gyntaf = geiriau[j]
		
			# iteru er mwyn darganfod yr ail orffwysfa
			for k in range( j+1, len(geiriau)-1 ):
			
				yr_ail_orffwysfa = geiriau[k]
				# if debug:
				# 	print yr_orffwysfa_gyntaf + ' / ' + yr_ail_orffwysfa + ' / ' + ybrifodl
				
				# gwirio am odl rhwng yr orffwysfa gyntaf a'r ail orffwysfa
				odl = prawf_odl( yr_orffwysfa_gyntaf, yr_ail_orffwysfa )
				# if debug:
				# 	print odl
				if odl:					
					# gwirio am gytseinedd rhwng yr ail orffwysfa a'r brifodl
					c1 = ac.traeannu_cytseiniaid( yr_ail_orffwysfa )[0]
					c2 = ac.traeannu_cytseiniaid( ybrifodl )[0]
					dosb = None
					if c1 and c2 and c1[-1] == c2[-1]:
						dosb = 'SAI'
					if not c1 and not c2:
						dosb = 'SAL'
					if dosb:
						return Adroddiad(
							llinyn = s,
							cynghanedd = dosb,
							data = {
								'gorffwysfa': (j,k),
								'odl': ( ( j, odl[0] ), ( k, odl[1] ), )
							}
						)
		return None

	# y cyfan
	def prawf_cynghanedd(self, s):
		# creu adroddiad
		adro = self.prawf_cynghanedd_sain(s)
		if not adro:
			adro = self.prawf_cynghanedd_lusg(s)
		if not adro:
			adro = self.prawf_cynghanedd_gytsain(s)
		if not adro:
			adro = Adroddiad( llinyn=s, data={} )

		# cofnodi data ychwanegol
		# dim ond y llinyn a'r mynegrifau - gall yr Adroddiad class greu html_strings
		# Mae angen cynnwys y linell ar ffurf Llinell object yn yr adroddiad 
		#	- yna gallwn fynd at y wybodaeth (h.y. rhestri mynegrifau i mewn i'r rhestr nodau) yn hawdd
		adro.data['geiriau'] = s.split(' ')
		adro.data['nifer_sillau'] = sum([ ac.nifer_sillau(g) for g in s.split(' ') ])
		adro.data['acenion'] = tuple([ (ac.acenion(g), ac.pwyslais(g)) for g in s.split(' ') ])

		return adro

#------------------------------------------------
def main():


	pe = Peiriant()
	s = None
	# s = "Ochain cloch a chanu clir"
	# s = "Awdur mad a dramodydd"
	# s = "Beiddgar yw geiriau cariad"
	# s = "Un distaw ei wrandawiad"
	# s = "Gwynt y rhew yn distewi"
	# s = "Y mae arogl yn goglais"
	# s = "Pell ydyw coed yr ellyll"
	# s = "Y mae Morfudd yn cuddio"
	# s = "Yr haul ar dawel heli"
	
	# s = "Y brawd o bellafion bro"
	# s = "Awdur mad yw'r dramodydd"
	# s = "Gwynt y rhew yn distewra"
	# s = "Y mae Morfudd yn cuddio"
	# s = "Heddychwr gwr rhagorol"
	# s = "Cân ddiddig ar frig y fron"
	# s = "Ochain cloch a chanu clir"
	
	# s = "canlyniad cariad yw cosb"
	# s = "Ni all lladd ond ennyn llid"
	
	
	if s:
		ll = Llinell(s)
		ad  = pe.prawf_cynghanedd(s)
		print ad
		# print ad.llinyn_acenion()
		# print ad.llinyn
		# print ad.llinyn_gorffwysfa()
		# print ad.llinyn_sillau_colon()
		# print ad.llinyn_cytseiniaid_cyfatebol()
		# print ad.llinyn_cytseiniaid_traws()
		# print ad.llinyn_cytseiniaid_cynffon()
		# print ad.llinyn_odl()
		return
	
	debug = False
	# data (llinellau)
	croes = (
		"Ochain cloch a chanu clir",
#		u"Si'r oerwynt a sêr araul",
		"Awdur mad a dramodydd",
		"Ei awen gref yn ei grym",	  		# n-ganolgoll ac w-gytsain
		)
	croes_o_gyswllt = (
		"Aderyn llwyd ar un llaw",
		"Daw geiriau Duw o'i gaer deg",		# un cytsain yn ateb dau gytsain
		"Gwr enwog yw o ran gwaith",
		)
	traws = (
		"Ochain cloch a gwreichion clir",
		"Ei awen brudd dros ein bro",		# w-gytsain
#		u"Si'r oerwynt dan sêr araul",
		"Awdur mad yw'r dramodydd",
		"Ni all lladd ond ennyn llid",		# dau yn ateb un
		"Onid teg yw ein tud",				# d/t yn ateb t
	)
	traws_fantach = (
#		u"Y gŵr aruchel ei gân",
		"Y brawd o bellafion bro",
		"Brwd yw aderyn brig",
		"Glaw ar ymylon y glyn",
	)
	llusg = (
		"Beiddgar yw geiriau cariad",
		"Y mae arogl yn goglais",
		"Pell ydyw coed yr ellyll",
		"Y mae Morfudd yn cuddio",
		"Yr haul ar dawel heli",
#		u"Taw â'th sôn, gad fi'n llonydd",
		"Ymysg y bedw yn ddedwydd",				# w-ansillafog
	)
	llusg_lafarog = (
		"Un distaw ei wrandawiad",				# w-ansillafog
		"Gwynt y rhew yn distewi",				# w-ansillafog
		"Gwynt y rhew yn distewra"
	)
	llusg_odl_gudd = (
		"Ac yma bu cydnabod",
		"Ac wele wychder Dewi",					# methiant
	)
	sain = (
		#"Cân ddiddig ar frig y fron",
		#"Gŵr amhur yn sur ei sen",
		"Bydd y dolydd yn deilio",
		"Canlyniad cariad yw cosb",
		#"Cân hardd croyw fardd Caerfyrddin",
		"Mae'n gas gennyf dras y dref",	  
		"Heddychwr gwr rhagorol",		  
	)
	sain_lafarog = (
		"Fe ddaeth pob croes i'w oes ef",
		"Didranc ieuanc ei awen",
		#"Pren gwyrddliw o wiw wead",
		#"Gŵr o ystryw ydyw ef",
	)

	# croes	
	print '========================='
	print '== Croes ================'
	print '========================='
	for s in croes:
		print pe.prawf_cynghanedd(s)

	print '=============================='
	print '== Croes o Gyswllt ==========='
	print '=============================='
	for s in croes_o_gyswllt:
		print pe.prawf_cynghanedd(s)

	# traws
	print '=============================='
	print '== Traws ====================='
	print '=============================='
	for s in traws:
		print pe.prawf_cynghanedd(s)

	print '=============================='
	print '== Traws Fantach ============='
	print '=============================='
	for s in traws_fantach:
		print pe.prawf_cynghanedd(s)

	# llusg
	print '=============================='
	print '== Llusg ====================='
	print '=============================='
	for s in llusg:
		print pe.prawf_cynghanedd(s)
	# print '\n== Llusg Lafarog ========'
	# for s in llusg_lafarog:
	# 	print pe.prawf_cynghanedd(s)
	# print '\n== Llusg Odl Gudd ======='
	# for s in llusg_odl_gudd:
	# 	print pe.prawf_cynghanedd(s)

	# sain
	print '=============================='
	print '== Sain ======================'
	print '=============================='
	for s in sain:
		print pe.prawf_cynghanedd(s)

	print '=============================='
	print '== Sain Lafarog =============='
	print '=============================='
	for s in sain_lafarog:
		print pe.prawf_cynghanedd(s)

if __name__ == '__main__': main()


		
