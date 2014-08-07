#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
pennill.py - chwilio am linellau cynghenedd mewn cyfundrefn dilys
'''

from llinell import Llinell

class Cwpled(object):
	'''
	class Cwpled:
	mewnbwn: dau linyn safonol yn y drefn gywir 
	'''

	def __init__(self, llinell_1, llinell_2):
		self.cyntaf = llinell_1
		self.ail	= llinell_2

	def __unicode__(self):
		return self.cyntaf.llinyn() + '\n' + self.ail.llinyn()

	def __str__(self):
		return self.__unicode__().encode('utf-8')


class Pennill(object):
	'''
	class Pennill:
	'''
	def __init__(self, llinellau):
		self.llinellau = llinellau

	def __unicode__(self):
		return '\n'.join([ llinell.llinyn() for llinell in self.llinellau ])

	def __str__(self):
		return self.__unicode__().encode('utf-8')


if __name__ == '__main__': 
	main()

