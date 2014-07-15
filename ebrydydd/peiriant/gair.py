#!/usr/bin/python
# coding=utf-8
'''
clymau: 
	dechrau a gorffen gyda cwlwm cytseiniaid (gwag o bosib)
		ffurf: [CC,CL,....,CL,CC]
	mae'n bosib cael dau gwlwm llafariaid cyfagos (e.e. duon, eos)
'''
global debug

import cysonion as cy
import llinyn as ll
import acen as ac

from lliwiau import coch, piws

#------------------------------------------------
# Gair class
#------------------------------------------------
class Gair(object):
	'''
	class: Gair
		 mewnbwn: llinyn (utf8)
	 ''' 
	def __init__(self, s):
		# self.llinyn = s.decode('utf-8')
		self.llinyn = s
		self.nodau = ll.nodau(self.llinyn)
		self.clymau = ll.clymau(self.llinyn)
		self.acenion = ac.acenion(self.llinyn)
		self.pwyslais = ac.pwyslais(self.llinyn)
 
	def __unicode__(self):
		return self.llinyn

	def nifer_sillau(self):
		return len(self.acenion)

	def nifer_clymau(self):
		return len(self.clymau)
   
	def llinyn_llafariaid(self):
		return ll.llinyn_llafariaid(self.llinyn)

	def llinyn_cytseiniaid(self):
		return ll.llinyn_cytseiniaid(self.llinyn)

	def llinyn_acenion(self, blanksymbol=' '):
		return ac.llinyn_acenion(self.llinyn, blanksymbol=blanksymbol)

	def llinyn_acen_colon(self, blanksymbol=' '):
		b = [blanksymbol]*len(self.llinyn)
		b[self.acenion[-1]] = ':'
		if self.pwyslais == -2:
			b[self.acenion[-2]] = ':'
		return ''.join(b)

	def	clymau_llafariaid(self):
		return filter(None, self.clymau[::2])
	
	def clymau_cytseiniaid(self):
		return filter(None, self.clymau[1::2])


#------------------------------------------------
def main():
	print 'gair.py'

	llinynnau = (
		'anifeiliaid',
		'cuddio',
		u'rhôm',
		u"â'th",
		'duon',			# deusain ddeusill
		'eos',			# deusain ddeusill
		'dramodydd',
		'cymraeg',
		'awen',
	)
	for s in llinynnau:
		g = Gair(s)
		print '-------------------'
		print g.llinyn_acenion()
		print g.llinyn
		print g.llinyn_cytseiniaid()
		print g.llinyn_acen_colon()

if __name__ == '__main__': 
	main()

		
