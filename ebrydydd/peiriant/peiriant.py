#!/usr/bin/env python
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

import cysonion as cy

from acen import aceniad
from odl import oes_odl, oes_odl_lusg
from cytseinedd import oes_cytseinedd

from llinell import Llinell
from adroddiad import Adroddiad

import logging
out = logging.getLogger(__name__)

global debug
debug = False


# peiriant
class Peiriant(object):
	'''
	class Peiriant:
	'''
	def __init__(self): 
		pass

	# croes
	def oes_croes(self, llinell):
		'''
		ffwythiant: oes_croes
		mewnbwn: llinell
		allbwn: adroddiad neu None
		'''
		out.info('prawf croes')
		if debug: 
			print '=============================='
			print llinell
			print 'OES_CROES'
		return self.oes_cynghanedd_gytsain( llinell, dosbarthiadau=['CRO', 'COG'] )
	
	
	# traws
	def oes_traws(self, llinell):
		'''
		ffwythiant: oes_traws
		mewnbwn: llinell
		allbwn: adroddiad neu None
		'''
		out.info('prawf traws')
		if debug:
			print '=============================='
			print llinell
			print 'OES_TRAWS'
		return self.oes_cynghanedd_gytsain( llinell, dosbarthiadau=['TRA', 'TRF'] )
	

	# cynghanedd gytsain (croes neu draws)
	def oes_cynghanedd_gytsain(self, llinell, dosbarthiadau=[]):
		'''
		ffwythiant: oes_cynghanedd_gytsain
		mewnbwn:	llinell
		allbwn:		adroddiad neu None
		sylwadau:
			safle eithaf yr orffwysfa (AYG tud. 27):
				os gorffwysfa acenog (CAC ADI): pwyslais ar sill 1-4
				os gorffwysfa ddiacen (CDI, ADY): pwyslais ar sill 1-3 
			yn gyffredinol, rhaid cael o leiaf tri sill yn yr ail ran.
				e.g. llinell nawsill => gorffwysfa sill 1-6 etc.
			
		'''
		ybrifodl = llinell.geiriau[-1]
		
		cyfanswm_sillau = llinell.nifer_sillau()

		ch_geiriau = []
		dd_geiriau = list(llinell.geiriau)
		
		if debug:
			print [ [ g.llinyn() for g in ch_geiriau ], [ g.llinyn() for g in dd_geiriau ] ]
		
		nifer_sillau = 0
		while dd_geiriau:
			dd_geiriau.reverse()
			yrorffwysfa = dd_geiriau.pop()
			dd_geiriau.reverse()
			ch_geiriau.append(yrorffwysfa)

			if debug:
				print '-------------------'
				print 'Gorffwysfa: ' + yrorffwysfa.llinyn()

			# gwirio nifer sillau
			nifer_sillau += yrorffwysfa.nifer_sillau()

			if debug:
				print 'Cyfanswm sillau: %d' % nifer_sillau

			if nifer_sillau > llinell.nifer_sillau() - 3:
				break
			# ace = aceniad( yrorffwysfa, ybrifodl )
			# if debug:
			# 	print nifer_sillau
			# 	print ace
			# if ace in ['CAC','ADI'] and nifer_sillau  > 4:
			# 	break
			# if ace in ['CDI','ADY'] and nifer_sillau  > 4:
			# 	break			
						

			# osgoi geiriau gwan
			if yrorffwysfa.llinyn() in cy.geiriau_gwan:
				continue

			if debug:
				print [ [ g.llinyn() for g in ch_geiriau ], [ g.llinyn() for g in dd_geiriau ] ]
				# print ace
		
			
			dosb, bai, data = oes_cytseinedd( ch_geiriau , dd_geiriau)			
			if debug:
				if dosb:
					print 'Dosbarth cytseined: ' + dosb
				else:
					print 'Dim cytseinedd'
			
			# dianc os oes cytseinedd o fath derbyniol
			if dosb in dosbarthiadau:
				data['gorffwysfa'] = (yrorffwysfa),
				return Adroddiad(
					llinell = llinell,
					cynghanedd = dosb,
					bai = bai,
					aceniad = aceniad( yrorffwysfa, ybrifodl ),
					data = data,
				)
		return None
	

	# lusg
	def oes_llusg(self, llinell):
		'''
		ffwythiant: oes_llusg
		mewnbwn: llinell
		allbwn: adroddiad
		sylwadau:
			Rhaid i'r orffwysfa odli gyda pen blaen y brifodl
			Rhaid i'r brifodl fod yn air lluosill
			Bai trwm-ac-ysgafn yn amhosib
		'''
		out.info('prawf llusg')
		if debug:
			print '=============================='
			print llinell
			print 'OES_LUSG'

		ybrifodl = llinell.geiriau[-1]
		
		# rhaid i'r brifodl for yn air lluosill
		if ybrifodl.nifer_sillau() < 2:
			if debug:
				print 'oes_llusg: rhaid i\'r brifodl fod yn air lluosill'
			return None
			
		# iteru dros eiriau'r linell i ddarganfod yr orffwysfa
		for i in range( len(llinell.geiriau)-1 ):
			yrorffwysfa = llinell.geiriau[i]
			yrolynydd = llinell.geiriau[i+1]
			if debug:
				print yrorffwysfa.llinyn() + '+' + yrolynydd.llinyn() + '/' + ybrifodl.llinyn()

			# osgoi geiriau gwan
			if yrorffwysfa.llinyn() in cy.geiriau_gwan:
				continue
			
			# profi am odl lusg
			# print "Helo"
			odl, syl = oes_odl_lusg( yrorffwysfa, ybrifodl, olynydd=yrolynydd)
			# odl, syl = oes_odl_lusg( yrorffwysfa, ybrifodl )
			if odl and not any(nod.iscytsain() for nod in odl[0]):
				dosb = 'LLL'
			else:
				dosb = 'LLU'

			# dianc os oes odl lusg 
			if odl:
				return Adroddiad(
					llinell = llinell,
					cynghanedd = dosb,
					data = {
						'gorffwysfa': (yrorffwysfa,),
						'odl': odl,
						'sylwadau': syl,
					},
				)
		return None 
	
	# sain gadwynog
	def oes_sain_gadwynog(self, llinell):
		'''
		ffwythiant: oes_sain_gadwynog
		mewnbwn: llinell
		allbwn: adroddiad		
		'''
		out.info('prawf sain gadwynog')
		if debug:
			print '=============================='
			print llinell
			print 'OES_SAIN_GADWYNOG'
		
		ybrifodl = llinell.geiriau[-1]
		# iteru er mwyn darganfod yr orffwysfa gyntaf
		for i in range( len(llinell.geiriau)-3 ):
			yr_orffwysfa_gyntaf = llinell.geiriau[i]
			if yr_orffwysfa_gyntaf.llinyn() in cy.geiriau_gwan:
				continue
		
			# iteru er mwyn darganfod yr ail orffwysfa
			for j in range( i+1, len(llinell.geiriau)-2 ):
				yr_ail_orffwysfa = llinell.geiriau[j]
				if yr_ail_orffwysfa.llinyn() in cy.geiriau_gwan:
					continue

				# iteru er mwyn darganfod yr ail orffwysfa
				for k in range( j+1, len(llinell.geiriau)-1 ):
					y_drydedd_orffwysfa = llinell.geiriau[k]
					if y_drydedd_orffwysfa.llinyn() in cy.geiriau_gwan:
						continue

					if debug:
						print yr_orffwysfa_gyntaf.llinyn() + '/' + yr_ail_orffwysfa.llinyn() + '/' + y_drydedd_orffwysfa.llinyn() + '/' + ybrifodl.llinyn()

					# gwirio am odl rhwng yr orffwysfa gyntaf a'r drydedd orffwysfa
					odl,syl = oes_odl( yr_orffwysfa_gyntaf, y_drydedd_orffwysfa )
					if odl:	
						dosb = None
						# print yr_orffwysfa_gyntaf.llinyn()
						# print y_drydedd_orffwysfa.llinyn()
						# print i,j,k
						# print [gair.llinyn() for gair in llinell.geiriau[i+1:j+1]]
						# print [gair.llinyn() for gair in llinell.geiriau[k+1:]]
						dosb_cyts, bai, data = oes_cytseinedd( llinell.geiriau[i+1:j+1], llinell.geiriau[k+1:] )
						if dosb_cyts and dosb_cyts[0] in ['C','T']:
							dosb = 'SAG'
						# dianc os oes angen		
						if dosb:
							data['gorffwysfa'] = (yr_orffwysfa_gyntaf,yr_ail_orffwysfa,y_drydedd_orffwysfa)
							data['odl'] = odl
							return Adroddiad(
								llinell = llinell,
								cynghanedd = dosb,
								aceniad = aceniad( yr_ail_orffwysfa, ybrifodl ),
								data = data
							)
		return None
				




	# sain
	def oes_sain(self, llinell):
		'''
		ffwythiant: oes_sain
		mewnbwn: llinell
		allbwn: adroddiad		
		'''
		out.info('prawf sain')
		if debug:
			print '=============================='
			print llinell
			print 'OES_SAIN'
		
		ybrifodl = llinell.geiriau[-1]
		
		# iteru er mwyn darganfod yr orffwysfa gyntaf
		for j in range( len(llinell.geiriau)-2 ):
			yr_orffwysfa_gyntaf = llinell.geiriau[j]
			if yr_orffwysfa_gyntaf.llinyn() in cy.geiriau_gwan:
				continue
		
			# iteru er mwyn darganfod yr ail orffwysfa
			for k in range( j+1, len(llinell.geiriau)-1 ):			
				yr_ail_orffwysfa = llinell.geiriau[k]
				if yr_ail_orffwysfa.llinyn() in cy.geiriau_gwan:
					continue

				if debug:
					print yr_orffwysfa_gyntaf.llinyn() + '/' + yr_ail_orffwysfa.llinyn() + '/' + ybrifodl.llinyn()
				
				# gwirio am odl rhwng yr orffwysfa gyntaf a'r ail orffwysfa
				# odl, syl = oes_odl( yr_orffwysfa_gyntaf, yr_ail_orffwysfa )
				yrolynydd = llinell.geiriau[j+1]
				odl, syl = oes_odl( yr_orffwysfa_gyntaf, yr_ail_orffwysfa, olynydd=yrolynydd)
				# if yrolynydd.nifer_sillau() > 1 or (k > j + 1):
				# 	odl, syl = oes_odl( yr_orffwysfa_gyntaf, yr_ail_orffwysfa, olynydd=yrolynydd)
				# else:
				# 	odl, syl = oes_odl( yr_orffwysfa_gyntaf, yr_ail_orffwysfa)
				if not odl:
					yrolynydd = llinell.geiriau[k+1]
					# print yrolynydd
					# print yrolynydd.nifer_sillau()
					# print k
					# print len(llinell.geiriau) -1
					# if yrolynydd.nifer_sillau() > 1 or (k < len(llinell.geiriau)-2):
					odl, syl = oes_odl( yr_ail_orffwysfa, yr_orffwysfa_gyntaf, olynydd=yrolynydd)
					
				if odl:	
					# print 'DING'				
					dosb = None
					dosb_cyts, bai, data = oes_cytseinedd( yr_ail_orffwysfa, llinell.geiriau[k+1:] )
					if dosb_cyts == 'LLA':
						dosb = 'SAL'
					elif data and data.has_key('parau'):
						if data['parau']:
							if dosb_cyts == 'COG':
								dosb = 'SOG'
							else:
								dosb = 'SAI'
					# print 'dosb = ' + str(dosb)
					# print 'dosb_cyts = ' + str(dosb_cyts)
					# dianc os oes angen		
					if dosb:
						data['gorffwysfa'] = (yr_orffwysfa_gyntaf,yr_ail_orffwysfa)
						data['odl'] = odl
						data['sylwadau'] = syl
						return Adroddiad(
							llinell = llinell,
							cynghanedd = dosb,
							aceniad = aceniad( yr_ail_orffwysfa, ybrifodl ),
							data = data
						)
		return None
	

	# y cyfan
	def oes_cynghanedd(self, llinell):
		
		# if llinell.geiriau[-1].llinyn in cy.geiriau_gwan:
		# 	return 	Adroddiad( llinell=llinell, cynghanedd='DIM' )
		out.info('prawf cynghanedd: %s', llinell.llinyn() )
		if debug:
			print '==============================XXX'
			print llinell

		adro_sain	= self.oes_sain(llinell)
		adro_croes	= self.oes_croes(llinell)
		adro_llusg	= self.oes_llusg(llinell)
		adro_traws = self.oes_traws(llinell)
		
		sain = True if adro_sain and adro_sain.cynghanedd else False
		croes = True if adro_croes and adro_croes.cynghanedd else False
		llusg = True if adro_llusg and adro_llusg.cynghanedd else False
		traws = True if adro_traws and adro_traws.cynghanedd else False

		# if debug:
		# 	print sain
		# 	print croes
		# 	print llusg
		# 	print traws
				
		if sain:
			adro = adro_sain
			if adro.cynghanedd in ['SOG','SAG']:
				pass
			elif croes and not llusg and not traws :
				adro.cynghanedd = 'SEG'
				adro.data['adro_croes'] = adro_croes
			elif llusg and not croes and not traws :
				adro.cynghanedd = 'SEL'
				adro.data['adro_llusg'] = adro_llusg
			elif traws and not croes and not llusg :
				adro.cynghanedd = 'SED'
				adro.data['adro_traws'] = adro_traws
			else:
				pass							
		elif croes:
			adro = adro_croes
			if adro.cynghanedd == 'COG':
				pass
			elif llusg and not traws:
				adro.cynghanedd = 'CRL'
				adro.data['adro_llusg'] = adro_llusg
			else:
				pass
		elif llusg:
			adro = adro_llusg
			if traws:
				adro.cynghanedd = 'TRL'
				adro.data['adro_traws'] = adro_traws
			else:
				pass
		elif traws:
			adro = adro_traws
		else:
			adro = Adroddiad( llinell=llinell, cynghanedd='DIM' )

		# data ychwanegol
		adro.data['llinell'] = llinell
		adro.data['nifer_sillau'] = llinell.nifer_sillau()
		adro.data['nodau_acenog'] = llinell.nodau_acenog()

		return adro
	

#------------------------------------------------
def main():
	pe = Peiriant()
	s = None
	# s = "Gwr enwog yw o ran gwaith"		# methiant: croes-o-gyswllt (hefyd yn traws-fantach)
	# s = "Si'r oerwynt a sêr araul"		# cdi
	# s = "Ochain cloch a chanu clir"
	# s = "Awdur mad a dramodydd"
	# s = "Beiddgar yw geiriau cariad"
	# s = "Un distaw ei wrandawiad"
	# s = "Gwynt y rhew yn distewi"
	# s = "Y mae arogl yn goglais"
	# s = "Pell ydyw coed yr ellyll"
	s = "Y mae Morfudd yn cuddio"
	# s = "Yr haul ar dawel heli"
	# s = "Y brawd o bellafion bro"
	# s = "Awdur mad yw'r dramodydd"
	# s = "Gwynt y rhew yn distewra"
	# s = "Y mae Morfudd yn cuddio"
	# s = "Heddychwr gŵr rhagorol"
	# s = "Cân ddiddig ar frig y fron"
	# s = "Ochain cloch a chanu clir"
	# s = "canlyniad cariad yw cosb"
	# s = "Ni all lladd ond ennyn llid"
	# s = "Cân hardd croyw fardd Caerfyrddin"
	# s = "Mae'n gas gennyf dras y dref"
	# s = "Dy fab rhad O! Dad yw ef"		# methiant!
	# s = "Galarnad groch a chloch leddf"
	# s = "Bydd sug i'r grug a'r egin"
	# s = "Fe ddaeth pob croes i'w oes ef"
	# s = "Canlyniad cariad yw cosb"
	# s = "Ymysg y bedw yn ddedwydd"
	# s = "da oedd bardwn dydd bwrdais,"
	# s = "cloch y ffair ciliwch o'i ffordd."
	# s = "dwyglust feinion aflonydd"
	# s = "ail y carw olwg gorwyllt"
	# s = "y cawn ar lan Conwy'r wledd"
	# s = "Wele rith fel ymyl rhod"
	# s = "o'n cwmpas, campwaith"
	# s = "Hen derfyn nad yw'n darfod."
	# s = "Trech wyt na Christ yng ngwlad y Cristion"
	# s = "Hyd yr êl yr hylithr awelon,"
	# s = "Hyd y tywyn haul, duw wyt yn hon."
	# s = "Talog, boed law, boed heulwen"
	# s = "Ond hiroes yw braint derwen"
	# s = "Hel a didoli diadell"
	# s = "Trydar mwyn yr adar mynydd"
	# s = "Un dydd gwelais brydydd gwiw"
	# s = "Gweled y pren aeddfed, praff"
	# s = "Ac yma bu cydnabod"
	# s = "Gwr amhur yn sur ei sen"
	# s = "Fe ddaeth pob croes i'w oes ef"
	# s = "Golud a gwae Gwlad y Gân" # CYFATEBIAETH GAIR-AM-AIR = GWENDID
	# s = "Nid â dy gariad o gof"
	# s = "Eu plaid yw duw rhai drwy'u hoes"
	if s:
		print '++++++++++++++++++++++++++++++'
		print s
		# ad  = pe.oes_croes( Llinell(s) )
		ll = Llinell(s)
		# print ll.nodau()
		# print ll.clymau()
		ad	= pe.oes_cynghanedd( ll )
		# ad	= pe.oes_sain_gadwynog( Llinell(s) )
		# ad	= pe.oes_llusg( Llinell(s) )
		print ad
		# for key, val in ad.data.items():
		# 	print key
		# 	print val
			# print key + ':\t\t' + ' '.join([ nod.llinyn for nod in val ])
		return
if __name__ == '__main__': main()



		
