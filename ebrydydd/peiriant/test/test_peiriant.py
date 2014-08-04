#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
filename: test_peiriant.py 
author: scmde
created: 28/06/2013
'''

import unittest
from peiriant import Peiriant
from llinell import Llinell

global debug
debug = False

# data
llinellau = {
	'croes': (
		"Ochain cloch a chanu clir",
		"Si'r oerwynt a sêr araul",
		"Awdur mad a dramodydd",
		"Ei awen gref yn ei grym",	  		
		"Onid teg yw ein tud",				
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
		# "Ymysg y bedw yn ddedwydd",			# methiant
	),
	'llusg_lafarog': (
		"Un distaw ei wrandawiad",				
		"Gwynt y rhew yn distewi",				
	),
	'llusg_odl_gudd': (
		"Ac yma bu cydnabod",
		"Ac wele wychder Dewi",				# methiant
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

pe = Peiriant()

# --- croes ---
class TestCroes(unittest.TestCase):
	def setUp(self):
		self.llinellau = llinellau['croes']
	def test_croes(self):
		for s in self.llinellau:
			ad = pe.oes_cynghanedd( Llinell(s) )
			self.assertEqual(ad.cynghanedd, 'CRO')

# --- traws ---
class TestTraws(unittest.TestCase):
	def setUp(self):
		self.llinellau = llinellau['traws']
	def test_traws(self):
		for s in self.llinellau:
			ad = pe.oes_cynghanedd( Llinell(s) )
			self.assertEqual(ad.cynghanedd, 'TRA')

# --- sain ---
class TestSain(unittest.TestCase):
	def setUp(self):
		self.llinellau = llinellau['sain']
	def test_sain(self):
		for s in self.llinellau:
			ad = pe.oes_cynghanedd( Llinell(s) )
			self.assertEqual(ad.cynghanedd, 'SAI')


# --- llusg ---
class TestLlusg(unittest.TestCase):
	def setUp(self):
		self.llinellau = llinellau['llusg']
	def test_llusg(self):
		for s in self.llinellau:
			ad = pe.oes_cynghanedd( Llinell(s) )
			self.assertEqual(ad.cynghanedd, 'LLU')

# --- main ---
if __name__ == '__main__':
	unittest.main()

