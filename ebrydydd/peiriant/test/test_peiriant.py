#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
filename: test_peiriant.py 
author: scmde
created: 28/06/2013
'''

import unittest
from peiriant import oes_cynghanedd

global debug
debug = False

# --- croes ---
class TestCroes(unittest.TestCase):
	def setUp(self):
		self.llinellau = (
			"Ochain cloch a chanu clir",
			"Si'r oerwynt a sêr araul",
			"Awdur mad a dramodydd",
			"Ei awen gref yn ei grym",			# n-ganolgoll ac w-gytsain
		)
	def test_croes(self):
		for s in self.llinellau:
			dad = oes_cynghanedd(s)
			self.assertEqual(dad['cynghanedd', 'CRO')

# --- traws ---
class TestTraws(unittest.TestCase):
	def setUp(self):
		self.llinellau = (
			"Ochain cloch a gwreichion clir",
			"Ei awen brudd dros ein bro",		# w-gytsain
			"Si'r oerwynt dan sêr araul",
			"Awdur mad yw'r dramodydd",
		)
	def test_traws(self):
		for s in self.llinellau:
			dad = oes_cynghanedd(s)
			self.assertEqual(dad['cynghanedd', 'TRA')

# --- sain ---
class TestSain(unittest.TestCase):
	def setUp(self):
		self.llinellau = (
			"Cân ddiddig ar frig y fron",
			"Gŵr amhur yn sur ei sen",
			"Bydd y dolydd yn deilio",
			"Canlyniad cariad yw cosb",
			"Cân hardd croyw fardd Caerfyrddin",
			"Mae'n gas gennyf dras y dref",	  
			"Heddychwr gwr rhagorol",		  
		)
	def test_sain(self):
		for s in self.llinellau:
			cy, ac = oes_cynghanedd_sain(s)
			dad = oes_cynghanedd(s)
			self.assertEqual(dad['cynghanedd', 'SAI')

.
# --- llusg ---
class TestLlusg(unittest.TestCase):
	def setUp(self):
		self.llinellau = (
			"Beiddgar yw geiriau cariad",
			"Y mae arogl yn goglais",
			"Pell ydyw coed yr ellyll",
			"Y mae Morfudd yn cuddio",
			"Yr haul ar dawel heli",
			"Taw â'th sôn, gad fi'n llonydd",
			"Ymysg y bedw yn ddedwydd",				# methiant: w-ansillafog
			"Ac yma bu cydnabod",
			"Ac wele wychder Dewi",					# methiant
		)
	def test_llusg(self):
		for s in self.llinellau:
			dad = oes_cynghanedd(s)
			self.assertEqual(dad['cynghanedd', 'LLU')

# # --- llusg lafarog---
# class TestLlusgLafarog(unittest.TestCase):
# 	def setUp(self):
# 		self.llinellau = (
# 			"Un distaw ei wrandawiad",				# methiant: w-ansillafog
# 			"Gwynt y rhew yn distewi",				# methiant: w-ansillafog
# 			"Gwynt y rhew yn distewra"
# 		)
# 	def test_llusg_lafarog(self):
# 		for s in self.llinellau:
# 			dad = oes_cynghanedd(s)
# 			self.assertEqual(dad['cynghanedd', 'LLU')
# 			self.assertEqual(dad['odl', 'OL')


# --- main ---
if __name__ == '__main__':
	unittest.main()

