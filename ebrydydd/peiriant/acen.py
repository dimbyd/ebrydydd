#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' 
acen.py
	adnoddau darganfod dosbarth aceniad
		CAC: cytbwys acennog
		CDI: cytbwys ddiacen
		ADI: angytbwys ddisgynedig
		ADY: angytbwys ddyrchafedig
'''

from gair import Gair

global debug
debug = False

def aceniad(g1, g2):
	'''
	ffwythiant:	darganfod dosbarth aceniad dau aid
	mewnbwn:	dau air (yr orffwysfa a'r brifodl)
	allbwn:		llinyn dosbarth aceniad (CAC,CDI,ADI,ADY)
	'''
	pwy1 = g1.pwyslais()
	pwy2 = g2.pwyslais()
	if pwy1 == -1 and pwy2 == -1:
		return 'CAC'
	elif pwy1 == -1 and pwy2 != -1:
		return 'ADI'
	elif pwy1 != -1 and pwy2 == -1:
		return 'ADY'
	else:
		return 'CDI'

#------------------------------------------------
# TEST
def main():
	print 'aceniad.py'
	parau = (
		('ci','drwg'),			# CAC
		('ci','drewllyd'),		# ADI
		('blodyn','pert'),		# ADY
		('blodyn','banana'),	# CDI
	)
	for a,b in parau:
		print '-------------------'
		print a + '|' + b
		print aceniad( Gair(a),Gair(b) )


if __name__ == '__main__': 
	main()