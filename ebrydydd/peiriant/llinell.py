#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
llinell.py
	Llinell class: rhestr o wrthrychau Gair
'''

from gair import Gair

class Llinell(object):
	'''
	class Llinell:
	'''
	def __init__(self, s, awdur=None): 

		# gwirio am restr geiriau
		if type(s) == list and all( [type(x)==Gair for x in s] ):
			self.geiriau = s
		# gwirio am linyn unicode
		elif type(s) == str or type(s) == unicode:
			s = s.strip()
			if type(s) != unicode:
				s = s.decode('utf-8')
			self.geiriau = [Gair(ss) for ss in s.split(' ')]
		else:
			self.geiriau = None
		
		if self.geiriau:
			self.ybrifodl = self.geiriau[-1]
		else:
			self.ybrifodl = None

	def __unicode__(self):
		return u' '.join( [gair.__unicode__() for gair in self.geiriau] )
	
	def __str__(self):
		return self.__unicode__().encode('utf-8')

	# manion
	def nifer_geiriau(self):
		return len(self.geiriau)

	def nifer_sillau(self):
		return sum([ g.nifer_sillau() for g in self.geiriau ])

	# rhestri nodau a chlymau
	def nodau(self):
		return [g.nodau for g in self.geiriau]
		
	def clymau(self):
		return [g.nodau.rhestr_clymau() for g in self.geiriau]
	
	def nodau_acennog(self):
		return [nod for g in self.geiriau for nod in g.nodau_acennog()]
		
	# allbwn
	def llinyn(self):
		return ' '.join( [gair.llinyn() for gair in self.geiriau] )
		
	def llinyn_acenion(self):
		return ' '.join([g.llinyn_acenion() for g in self.geiriau])
	
	def llinyn_acenion_colon(self):
		return ' '.join([g.llinyn_acenion_colon() for g in self.geiriau])
	
	def llinyn_cytseiniaid(self):
		return ' '.join([g.llinyn_cytseiniaid() for g in self.geiriau])

	def llinyn_llafariaid(self):
		return ' '.join([g.llinyn_llafariaid() for g in self.geiriau])

	def llinyn_clymau(self):
		return ' '.join([ unicode(g.clymau) for g in self.geiriau ])
	

#------------------------------------------------
def main():

	# s = "Ymysg y bedw yn ddedwydd"
	s = "cloch y ffair ciliwch o'i ffordd."
	ll = Llinell(s)
	print ll.nodau()
	print ll.llinyn_acenion()
	print ll.llinyn()
	print ll.llinyn_clymau()
	return

	rhestr_llinynnau = (
		"Taw â'th sôn, gad fi'n llonydd",
		"Ochain cloch a chanu clir",
		"Si'r oerwynt a sêr araul",
		"Awdur mad a dramodydd",
		"Ei awen gref yn ei grym",	  	
	)
	for s in rhestr_llinynnau:
		ll = Llinell(s)

		print '--------------------'
		print ll.llinyn_acenion()
		print ll.llinyn()
		print ll.llinyn_llafariaid()
		print ll.llinyn_cytseiniaid()
		print ll.nifer_geiriau()
		print ll.nifer_sillau()
		nac = ll.nodau_acennog()
		print [nod.llinyn for nod in nac]

if __name__ == '__main__': main()


