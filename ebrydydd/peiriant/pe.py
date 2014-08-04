#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
eb.py
	peiriant dadansoddi cynghanedd (*nix)
'''

import os, re, sys, getopt, csv, codecs, time
from optparse import OptionParser

import cysonion as cy
import lliwiau as lliw

from mesur import Cerdd
from peiriant import Peiriant
from llinell import Llinell
from gair import Gair

import logging
PEIRIANT_ROOT = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(PEIRIANT_ROOT, 'peiriant.log')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)-10.8s - %(levelname)s - %(message)s',
                    filename=filename)

out = logging.getLogger(__name__)
# out.setLevel(logging.DEBUG)
# 
# # logger.setLevel(logging.DEBUG)
# fh = logging.FileHandler(filename)
# fh.setLevel(logging.DEBUG)
# # create console handler with a higher log level
# ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)
# # create formatter and add it to the handlers
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# ch.setFormatter(formatter)
# # add the handlers to the logger
# out.addHandler(fh)
# out.addHandler(ch)


def main(args=None):
	
	# opening
	time_str = time.strftime("%Y.%m.%d.%H.%M.%S")
	out.info('eb: dechrau: %s', time_str)


	# parser = OptionParser()
	# parser = OptionParser(usage="%prog [-f] [-q]", version="%prog 1.0")
	# parser = OptionParser(usage="%prog [-v] [-q] [-d] [llinyn] [-i infile] [-o outfile]", version="%prog: fersiwn 1.0", add_help_option=False)
	parser = OptionParser(usage="%prog [-v] [-q] [-d] [llinyn] [-i infile] [-o outfile]", add_help_option=False)

	parser.add_option("-d", "--demo", action="store_true", dest="demo", help="arddangosfa")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="allbwn amleiriog")
	parser.add_option("-q", "--quiet", action="store_false", dest="verbose", help="allbwn cryno")
	parser.add_option("-r", "--rhyddiaith", action="store_true", dest="rhyddiaith", help="mewnbwn rhyddiaith")
	parser.add_option("-i", "--input", dest="infile", help="ffeil mewnbwn")
	parser.add_option("-o", "--ouput", dest="outfile", help="ffeil allbwn")
	parser.add_option("-h", "--help", action="help", help="cymorth")
	parser.add_option("", "--version", action="version", help="fersiwn")
	parser.set_defaults(verbose=True, demo=False, rhyddiaith=False)

	# args = ["-o", "mypoints.csv"]
	(options, args) = parser.parse_args()
	
	# print '-----'
	# print options
	# print args
	# print '-----'
	# 
	# parse arguments
	s = ''
	if not args:
		args = sys.argv[1:]
	else:
		s = args[0]
	#	args = sys.argv[1:]
	# try:
	#	opts = getopt.getopt(args, "k:mdhs:v")
	# except getopt.GetoptError as err:
	#	print(err)
	#	sys.exit(2)
	
	# opts = getopt.getopt(args, "k:mdhs:v")
	# print opts

	pe = Peiriant()
	
	if s:
		ad = pe.oes_cynghanedd( Llinell(s) )
		if options.verbose:
			print ad
		else:
			print ad.cynghanedd + ': ' + s.strip()

	elif options.demo:
		import demo
		demo.run_demo(verbose=options.verbose)


	if options.infile:
		
		# rhyddiaith
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
			for b in brawddegau:
				geiriau = [Gair(s) for s in b.split(' ')]
				# print '|'.join([ gair.llinyn() for gair in geiriau ])
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
					# print llinell.llinyn()
					ad = pe.oes_cynghanedd( llinell )
					# if not ad.cynghanedd in ['DIM']:
					if not ad.cynghanedd in ['DIM','SAL']:
						if options.verbose:
							print ad
						else:
							print lliw.magenta(ad.cynghanedd) + '\t' + ad.llinell.llinyn()

			print('----------------------------------------')
			return

		# darllen ffeil
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
		if options.verbose:
			print('========================================')
			for llinell in llinellau:
				print llinell.llinyn()
			print('========================================')

		# dadansoddi pob llinell yn unigol (beth am toddaid byr/hir? Mae angen darganfod cysylltnod)
		adro_llinellau = []
		for llinell in llinellau:
			ad = pe.oes_cynghanedd( llinell )
			adro_llinellau.append(ad)

		# profi mesurau
		cerdd = Cerdd(llinellau)
		ateb_cyw, adro_cyw, syl_cyw = cerdd.oes_cywydd()
		ateb_eng, adro_eng, syl_eng = cerdd.oes_englyn()
		ateb_cyh, adro_cyh, syl_cyh = cerdd.oes_cyhydedd_nawban()
		ateb_hir, adro_hir, syl_hir = cerdd.oes_hir_a_thoddaid()
		
		# adro = None
		if ateb_cyw:
			dosb = 'CYWYDD'
			adro = adro_cyw
		elif ateb_eng:
			dosb = 'ENGLYN'
			adro = adro_eng
		elif ateb_cyh:
			dosb = 'CYHYDEDD NAWBAN'
			adro = adro_cyh
		elif ateb_hir:
			dosb = 'HiR-A-THODDAID'
			adro = adro_hir
		else:
			dosb = 'U'
			adro = adro_llinellau
		
		# allbwn
		print('----------------------------------------')
		if dosb:
			print lliw.cyan( dosb )
		if adro:
			for j in range( len(adro) ):
				ad = adro[j]
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
		# print ateb_eng
		# print syl_eng
		# for ad in adro_eng:
		# 	print ad

	# llwyddiant

	# diweddeb
	print "hwyl fawr...eb\n"
	time_str = time.strftime("%Y.%m.%d.%H.%M.%S")
	out.info('eb: diwedd: %s', time_str)
		
if __name__ == '__main__':
	sys.exit( main() )
		
