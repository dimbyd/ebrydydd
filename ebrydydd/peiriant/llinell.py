#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
llinell.py
	craidd: rhestr o wrthrychau gair
'''

import sys
import cysonion as cy
import llinyn as ll
from lliwiau import coch
from gair import Gair

global debug

class Llinell:
	'''
	class Llinell:
	'''
	def __init__(self, s, awdur=None): 
		# self.llinyn = s.decode('utf-8')
		self.llinyn = s
		self.awdur = awdur
		self.nodau = ll.nodau(self.llinyn)
		self.geiriau = [Gair(w) for w in s.split(' ')]
		self.ybrifodl = self.geiriau[-1]

	def __unicode__(self):
		return self.llinyn
	
	def awdur(self):
		return self.awdur

	def nifer_geiriau(self):
		return len(self.geiriau)

	def nifer_sillau(self):
		return sum([g.nifer_sillau() for g in self.geiriau])

	def clymau(self):
		return [g.clymau for g in self.geiriau]
	
	def llinyn_acenion(self):
		return ' '.join([g.llinyn_acenion() for g in self.geiriau])
	
	def llinyn_cytseiniaid(self):
		return ' '.join([g.llinyn_cytseiniaid() for g in self.geiriau])

	def llinyn_llafariaid(self):
		return ' '.join([g.llinyn_llafariaid() for g in self.geiriau])

	
class CwpledCywydd(object):
	'''
	class CwpledCywydd:
		mewnbwn: dau linyn (yn y drefn gywir)
	'''
	def __init__(self, s1, s2):
		self.cyntaf = Llinell(s1)
		self.ail =	Llinell(s2)
		if not self.cyntaf.nifer_sillau == 7 or not self.ail.nifer_sillau() == 7:
			sys.stderr.write('TORR MESUR: Cwpled Cywydd: llinellau seithsill yn unig')
			return False
		if self.cyntaf.prifodl.nifer_sillau() == 1 and self.ail.prifodl.nifer_sillau() == 1:
			sys.stderr.write('TORR MESUR: Cwpled Cywydd: dau brifodl acenog')
			return False
		if self.cyntaf.prifodl.nifer_sillau() > 1 and self.ail.prifodl.nifer_sillau() > 1:
			sys.stderr.write('TORR MESUR: Cwpled Cywydd: dau brifodl diacen')
			return False

class ToddaidByr(object):
	'''
	class ToddaidByr:
		mewnbwn: dau linyn (yn y drefn gywir)
	'''
	def __init__(self, s1, s2):
		pass

class Englyn(object):
	'''
	class Englyn:
		mewnbwn: 
			toddaid byr a chwpled cywydd
	'''
	def __init__(self, tb, cc):
		self.toddaid_byr = ToddaidByr(tb)
		self.cwpled_cywydd = CwpledCywydd(cc)

class Cywydd(object):
	'''
	class Cywydd:
		mewnbwn: 
			rhestr cwpledau cywydd
	'''
	def __init__(self, rhestr_cc):
		self.rhestr_cc = [ CwpledCywydd(cc) for cc in rhestr_cc ]


#------------------------------------------------
def main():

	rhestr_llinynnau = (
		u"Taw â'th sôn, gad fi'n llonydd",
		u"Ochain cloch a chanu clir",
		u"Si'r oerwynt a sêr araul",
		u"Awdur mad a dramodydd",
		u"Ei awen gref yn ei grym",	  	
	)
	for s in rhestr_llinynnau:
		ll = Llinell(s)

		print '--------------------'
		print ll.llinyn_acenion()
		print ll.llinyn
		print ll.llinyn_cytseiniaid()
		print ll.nifer_sillau()

#	 cwpled = Cwpled(s1,s2)

if __name__ == '__main__': main()


