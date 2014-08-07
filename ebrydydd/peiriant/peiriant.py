#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
peiriant.py
	peiriant dadansoddi cynghanedd (main)
'''

import os, re, sys, getopt, csv, codecs, time
from optparse import OptionParser

import cysonion as cy
import lliwiau as lliw

from gair import Gair
from llinell import Llinell
from pennill import Pennill

from dadansoddwr import Dadansoddwr
from dadansoddwr_pennill import DadansoddwrPennill

import logging
log = logging.getLogger()


def main(args=None):
	
	# dechrau
	log.info('peiriant: dechrau')


	# parser = OptionParser(usage="%prog [-v] [-q] [-d] [llinyn] [-i infile] [-o outfile]", version="%prog: fersiwn 1.0", add_help_option=False)
	parser = OptionParser(usage="%prog [-v] [-q] [-d] [-p] [-r] [llinyn] [-i infile]", version="%prog: fersiwn 0.1", add_help_option=False)

	parser.add_option("-d", "--demo", action="store_true", dest="demo", help="showan off")
	parser.add_option("-p", "--penillion", action="store_true", dest="demo_penillion", help="mwy o showan off")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="allbwn amleiriog")
	parser.add_option("-q", "--quiet", action="store_false", dest="verbose", help="allbwn cryno")
	parser.add_option("-r", "--rhyddiaith", action="store_true", dest="rhyddiaith", help="mewnbwn rhyddiaith")
	parser.add_option("-i", "--input", dest="infile", help="ffeil mewnbwn")
	parser.add_option("-h", "--help", action="help", help="cymorth")
	parser.set_defaults(verbose=True, demo=False, rhyddiaith=False)

	(options, args) = parser.parse_args()
	
	# dosrannu'r dewisiadau
	llinyn = ''
	if not args:
		args = sys.argv[1:]
	else:
		llinyn = args[0]
	
	# 1. llinyn unigol neu demos
	if llinyn:
		dad = Dadansoddwr()
		adro = dad.oes_cynghanedd( Llinell( llinyn ) )
		if options.verbose:
			print adro
		else:
			print lliw.magenta(adro.cynghanedd) + ': ' + llinyn.strip()
		return

	# 2. demos
	if options.demo:
		import demo
		demo.run_demo(verbose=options.verbose)
		return

	if options.demo_penillion:
		import demo_penillion
		demo_penillion.run_demo(verbose=options.verbose)
		return

	# 3. darllen o ffeil
	if options.infile:
		
		# rhyddiaith (hac, ond ok)
		if options.rhyddiaith:
			with codecs.open(options.infile, "r", "utf-8") as f:
				s = f.read()
			br = s.split('.')
			br = [b.strip() for b in br]
			brawddegau = []
			for b in br:
				if len(b) > 0:
					brawddegau.append( b + u'.')
			print('----------------------------------------')
			
			dad = Dadansoddwr()

			for b in brawddegau:
				geiriau = [Gair(s) for s in b.split(' ')]
				ns = 0
				idx_ch = 0
				idx_dd = 1
				rhestr = []
				llinellau = []
				while idx_dd < len(geiriau):
					while idx_dd < len(geiriau) and sum([ g.nifer_sillau() for g in geiriau[idx_ch:idx_dd] ]) < 7:
						rhestr.append( geiriau[idx_dd] )
						idx_dd = idx_dd + 1
					while sum([ g.nifer_sillau() for g in geiriau[idx_ch:idx_dd] ]) > 7:
						rhestr.reverse()
						rhestr.pop()
						rhestr.reverse()
						idx_ch = idx_ch + 1
					if geiriau[idx_dd-1].llinyn() not in cy.geiriau_gwan:
						llinellau.append( Llinell( geiriau[idx_ch:idx_dd] ) )
					idx_ch = idx_ch + 1
				for llinell in llinellau:
					adro = dad.oes_cynghanedd( llinell )
					if not adro.cynghanedd in ['DIM','SAL']:
						if options.verbose:
							print adro
						else:
							print lliw.magenta(adro.cynghanedd) + '\t' + adro.llinell.llinyn()
			print('----------------------------------------')
			return

		# cerdd
		with open(options.infile) as f:
			rhestr_llinynnau = f.readlines()
			
		# creu rhestr llinellau
		llinellau = []
		for s in rhestr_llinynnau:
			s.strip()
			if re.search(r'^#', s) or re.search(r'^\s*$', s):
				continue
			llinellau.append( Llinell(s) )
		
		# allbwn
		# if options.verbose:
		# 	print('========================================')
		# 	for llinell in llinellau:
		# 		print llinell.llinyn()
		# 	print('========================================')

		# dadansoddi pob llinell yn unigol (beth am doddeidiau? Mae angen darganfod cysylltnod)
		dad = Dadansoddwr()
		adro_llinellau_unigol = []
		for llinell in llinellau:
			adro = dad.oes_cynghanedd( llinell )
			adro_llinellau_unigol.append(adro)

		# profi mesurau
		dad = DadansoddwrPennill()
		pennill = Pennill(llinellau)
		cyw = dad.oes_cywydd( pennill )
		eng = dad.oes_englyn( pennill )
		cyh = dad.oes_cyhydedd_nawban( pennill )
		hat = dad.oes_hir_a_thoddaid( pennill )
		
		dosb = None
		if cyw[0]:
			dosb = 'CYW'
			adro = cyw[1]
		elif eng[0]:
			dosb = 'ENG'
			adro = eng[1]
		elif cyh[0]:
			dosb = 'CYH'
			adro = cyh[1]
		elif hat[0]:
			dosb = 'HAT'
			adro = hat[1]
		else:
			dosb = 'DIM'
			adro = adro_llinellau_unigol
		
		# allbwn
		print('----------------------------------------')
		if dosb:
			print lliw.cyan( dosb )
		if adro:
			for ad in adro:
				if options.verbose:
					if ad.cynghanedd == 'DIM':
						print lliw.magenta( ad.cynghanedd )
						print ad.llinyn_acenion()
						print ad.llinell.llinyn()
					else:
						print ad
				else:
					ss = ad.cynghanedd + ': ' + ad.llinell.llinyn().strip()
					if ad.cynghanedd == 'DIM':
						print lliw.magenta( ss )
					else:
						print ss
		print('----------------------------------------')

	# diwedd
	print "hwyl fawr...\n"
	time_str = time.strftime("%Y.%m.%d.%H.%M.%S")
	log.info('peiriant: diwedd')
		
if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
	main()





		
