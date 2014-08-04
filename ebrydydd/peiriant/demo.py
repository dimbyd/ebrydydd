#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
demo.py - showan off
'''

from llinell import Llinell
from peiriant import Peiriant

global debug
debug = True

# data
llinellau = {
	'croes': (
		"Ochain cloch a chanu clir",
		"Si'r oerwynt a sêr araul",
		"Awdur mad a dramodydd",
		"Ei awen gref yn ei grym",	  		
	),
	'croes_o_gyswllt': (
		"Aderyn llwyd ar un llaw",
		"Daw geiriau Duw o'i gaer deg",		
		"Gwr enwog yw o ran gwaith",		# methiant
	),
	'traws': (
		"Ochain cloch a gwreichion clir",
		"Ei awen brudd dros ein bro",		
		"Si'r oerwynt dan sêr araul",
		"Awdur mad yw'r dramodydd",
		"Ni all lladd ond ennyn llid",		
		"Onid teg yw ein tud",				
	),
	'traws_fantach': (
		"Y gŵr aruchel ei gân",
		"Y brawd o bellafion bro",
		"Brwd yw aderyn brig",
		"Glaw ar ymylon y glyn",
	),
	'llusg': (
		"Beiddgar yw geiriau cariad",
		"Y mae arogl yn goglais",
		"Pell ydyw coed yr ellyll",
		"Y mae Morfudd yn cuddio",
		"Yr haul ar dawel heli",				
		"Taw â'th sôn, gad fi'n llonydd",
		"Ymysg y bedw yn ddedwydd",			# methiant
	),
	'llusg_lafarog': (
		"Un distaw ei wrandawiad",				
		"Gwynt y rhew yn distewi",				
	),
	'llusg_odl_gudd': (
		"Ac yma bu cydnabod",
		"Ac wedi d'awr godidog",
		"Ac wele lid y gelyn",
		"Gwn ddifa lawer calon",
		"Dacw wiw dyfiant liwdeg",
		"Ac wele wychder Dewi",
		"Y ddinas draw yn wastraff",
		"Esgor mae llid ar ormes",
		"Bu llawer ddoe yn cerdded",
		"Eto dring lethr Carn Ingli",
	),
	'llusg_odl_ewinog': (
		"Yn wyneb haul ar Epynt",
		"Yr esgob biau popeth",
		"Aeth fy nghariad hyd ato",
		"O'r garreg hon daeth eco",
		"I'r esgob pur rhoed popeth",
		"Fy nghariad troaf atat",
		"O'r garreg clywaid eco",
	),
	'sain': (
		"Cân ddiddig ar frig y fron",
		"Gŵr amhur yn sur ei sen",
		"Bydd y dolydd yn deilio",
		"Canlyniad cariad yw cosb",
		"Cân hardd croyw fardd Caerfyrddin",
		"Mae'n gas gennyf dras y dref",	  
		"Heddychwr gwr rhagorol",		  
	),
	'sain_odl_ewinog': (
		"Caf fynd draw ar hynt i'r rhos",
		"Rhoi het ar ei harffed hi",
		"Caf fynd tua'r helynt draw",
	),
	'sain_odl_gudd': (
		"Eu plaid yw duw rhai drwy'u hoes",
		"Llyfrdra dy wlad nid yw les",
		"A'i gord yn deffro'r dyffryn",
		"Aeth Idris draw'n drist gan drawster",
		"Nid â dy gariad o gof",
	),
	'sain_lafarog': (
		"Fe ddaeth pob croes i'w oes ef",
		"Didranc ieuanc ei awen",
		"Pren gwyrddliw o wiw wead",
		"Gŵr o ystryw ydyw ef",
	),
	'sain_o_gyswllt': (
		"Galarnad groch a chloch leddf",
		"Bydd sug i'r grug a'r egin",
		"Dy fab rhad O! Dad yw ef",			# methiant
	),
	'seingroes': (
		"Lleuad fad lleuad fedi",
		"Y cawr mawr yn curo myrdd",
		"Eos dlos yn deilio ir",
		"Gweled cur o glywed can",
	),
	'trawsgroes': (
		"Enaid unig a dinam",
		"Geiriau gwrol gor-gywrain",
	),
	'seindraws': (
		"Gwrol gwrol frawdgarwch",
		"Y feinwen fwynwen fanwallt",
	),
	'croeslusg': (
		"Duw ei hun a'u dihunodd",
		"Ein ceidwad eon cadarn",
	),
	'seinlusg': (
		"Gŵr o forwr a fwriwyd",
		"Gwyraf, yfaf o'r afon",
	),
	'trawslusg': (
		"Yr arwr mewn arwriaeth",
		"Y feinwen a gâr f'enaid",
	),
}

def run_demo(verbose=True):
	pe = Peiriant()
	for key in [
			# 'croes', 
			# 'croes_o_gyswllt', 
			# 'traws', 
			# 'traws_fantach', 
			'llusg', 
			'llusg_lafarog',
			'llusg_odl_gudd',
			'llusg_odl_ewinog',
			'sain', 
			'sain_odl_gudd',
			'sain_odl_ewinog',
			'sain_lafarog',
			# 'sain_o_gyswllt',
			# 'seingroes',
			# 'trawsgroes',
			# 'seindraws',
			# 'croeslusg',
			# 'seinlusg',
			# 'trawslusg',
		]:
		val = llinellau[key]
		print '=============================='
		print key.upper()
		print '=============================='
		for s in val:
			# if debug:
			# 	print '++++++++++++++++++++++++++++++'
			# 	print s
			# 	print '++++++++++++++++++++++++++++++'
			# print s
			ad = pe.oes_cynghanedd( Llinell(s) )
			if verbose:
				print ad
			else:
				print ad.cynghanedd + ': ' + s.strip()
		print

#------------------------------------------------
def main():

	run_demo()

if __name__ == '__main__': main()


		
