#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
dadansoddwr.py - chwilio am odl a chytseinedd er mwyn dosbarthu llinynnau
'''

import cysonion as cy

from acen import aceniad
from odl import oes_odl, oes_odl_lusg
from cytseinedd import oes_cytseinedd

from llinell import Llinell
from adroddiad import Adroddiad

import logging
log = logging.getLogger(__name__)

global debug
debug = False


class Dadansoddwr(object):
	'''
	class Dadansoddwr:
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
		log.info('prawf croes')
		return self.oes_cynghanedd_gytsain( llinell, dosbarth='C' )
	
	
	# traws
	def oes_traws(self, llinell):
		'''
		ffwythiant: oes_traws
		mewnbwn: llinell
		allbwn: adroddiad neu None
		'''
		log.info('prawf traws')
		return self.oes_cynghanedd_gytsain( llinell, dosbarth='T' )
	

	# cynghanedd gytsain (croes neu draws)
	def oes_cynghanedd_gytsain(self, llinell, dosbarth=''):
		'''
		ffwythiant: oes_cynghanedd_gytsain
		mewnbwn:	llinell
		allbwn:		adroddiad neu None
		sylwadau:
			safle eithaf yr orffwysfa (AYG tud. 27):
				os gorffwysfa acennog (CAC ADI): pwyslais ar sill 1-4
				os gorffwysfa ddiacen (CDI, ADY): pwyslais ar sill 1-3 
			yn gyffredinol, rhaid cael o leiaf tri sill yn yr ail ran.
				e.g. llinell nawsill => gorffwysfa sill 1-6 etc.
			
		'''
		ybrifodl = llinell.geiriau[-1]
		
		cyfanswm_sillau = llinell.nifer_sillau()

		ch_geiriau = []
		dd_geiriau = list(llinell.geiriau)
		
		nifer_sillau = 0
		while dd_geiriau:
			dd_geiriau.reverse()
			yrorffwysfa = dd_geiriau.pop()
			dd_geiriau.reverse()
			ch_geiriau.append(yrorffwysfa)

			log.debug('Gorffwysfa: ' + yrorffwysfa.llinyn())

			# gwirio nifer sillau
			nifer_sillau += yrorffwysfa.nifer_sillau()

			log.debug('Cyfanswm sillau: %d' % nifer_sillau)

			if nifer_sillau > 4:
				log.debug('Gorffwysfa wedi mynd yn rhy bell')
				break					

			# osgoi geiriau gwan
			if yrorffwysfa.llinyn() in cy.geiriau_gwan:
				continue

			dosb, bai, data = oes_cytseinedd( ch_geiriau , dd_geiriau)			

			llinyn_ch = ' '.join([ g.llinyn() for g in ch_geiriau ])
			llinyn_dd = ' '.join([ g.llinyn() for g in dd_geiriau ])
			llinyn_dosb = dosb if dosb else 'DIM'
			log.debug( '%s / %s : %s' % (llinyn_ch, llinyn_dd, llinyn_dosb) )	

			# dianc os oes cytseinedd o fath derbyniol
			if dosb and dosb[0] == dosbarth:
				data['gorffwysfeydd'] = (yrorffwysfa),
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
		log.info('prawf llusg')

		ybrifodl = llinell.geiriau[-1]
		
		# rhaid i'r brifodl for yn air lluosill
		if ybrifodl.nifer_sillau() < 2:
			log.debug('oes_llusg: rhaid i\'r brifodl fod yn air lluosill')
			return None
			
		# iteru dros eiriau'r linell i ddarganfod yr orffwysfa
		for i in range( len(llinell.geiriau)-1 ):
			yrorffwysfa = llinell.geiriau[i]
			yrolynydd = llinell.geiriau[i+1]
			log.debug( yrorffwysfa.llinyn() + '+' + yrolynydd.llinyn() + '/' + ybrifodl.llinyn() )

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
						'gorffwysfeydd': (yrorffwysfa,),
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
		log.info('prawf sain gadwynog')
		
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

					log.debug( yr_orffwysfa_gyntaf.llinyn() + '/' + yr_ail_orffwysfa.llinyn() + '/' + y_drydedd_orffwysfa.llinyn() + '/' + ybrifodl.llinyn() )

					# profi am odl rhwng yr orffwysfa gyntaf a'r drydedd 
					odl,syl = oes_odl( yr_orffwysfa_gyntaf, y_drydedd_orffwysfa )
					if odl:	
						dosb = None
						# os oes odl, profi an gytseinedd
						dosb_cyts, bai, data = oes_cytseinedd( llinell.geiriau[i+1:j+1], llinell.geiriau[k+1:] )
						if dosb_cyts and dosb_cyts[0] in ['C','T']:
							dosb = 'SAG'
						# dianc os oes angen		
						if dosb:
							data['gorffwysfeydd'] = (yr_orffwysfa_gyntaf,yr_ail_orffwysfa,y_drydedd_orffwysfa)
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
		log.info('prawf sain')
		
		# sain gadwynog
		adro_sain_gadwynog = self.oes_sain_gadwynog(llinell)
		if adro_sain_gadwynog:
			return adro_sain_gadwynog

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

				log.debug(yr_orffwysfa_gyntaf.llinyn() + '/' + yr_ail_orffwysfa.llinyn() + '/' + ybrifodl.llinyn())
				
				# profi am odl
				yrolynydd = llinell.geiriau[j+1]
				odl, syl = oes_odl( yr_orffwysfa_gyntaf, yr_ail_orffwysfa, olynydd=yrolynydd)
				if not odl:
					yrolynydd = llinell.geiriau[k+1]
					odl, syl = oes_odl( yr_ail_orffwysfa, yr_orffwysfa_gyntaf, olynydd=yrolynydd)
				
				# os oes odl, profi am gytseinedd
				if odl:	
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

					# dianc os oes angen		
					if dosb:
						data['gorffwysfeydd'] = (yr_orffwysfa_gyntaf,yr_ail_orffwysfa)
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
		log.info('prawf cynghanedd: %s', llinell.llinyn() )

		adro_sain	= self.oes_sain(llinell)
		adro_croes	= self.oes_croes(llinell)
		adro_llusg	= self.oes_llusg(llinell)
		adro_traws = self.oes_traws(llinell)
		
		sain = True if adro_sain and adro_sain.cynghanedd else False
		croes = True if adro_croes and adro_croes.cynghanedd else False
		llusg = True if adro_llusg and adro_llusg.cynghanedd else False
		traws = True if adro_traws and adro_traws.cynghanedd else False
		
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
		adro.data['nodau_acennog'] = llinell.nodau_acennog()

		if adro.data.has_key('sylwadau'):
			if adro.sylwadau:
				adro.sylwadau.append( '\n'.join(adro.data['sylwadau']) )
			else:
				adro.sylwadau = '\n'.join(adro.data['sylwadau'])
		

		return adro
	

#------------------------------------------------
def main():
	dad = Dadansoddwr()
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
	# s = "Y mae Morfudd yn cuddio"
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
	# s = "Wedi blwng ymosod blin"
	s = "Rhwydd gamwr, hawdd ei gymell"
	s = "i'r mynydd a'r mannau"
	s = "Cain yw awen cân eos"
	if s:
		print '++++++++++++++++++++++++++++++'
		print s
		ll = Llinell(s)
		print dad.oes_cynghanedd( ll )


if __name__ == '__main__': 
	import logging.config
	logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
	main()



		
