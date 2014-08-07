#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
demo-penillion.py - mwy o showan off
'''

from subprocess import call

from llinell import Llinell
from pennill import Pennill
from dadansoddwr_pennill import DadansoddwrPennill

import lliwiau as lliw

penillion = {
	'cwpled_cywydd': (
		"Hen linell bell nad yw'n bod,\nHen derfyn nad yw'n darfod.",
	),
	'toddaid_byr': (
#		"Talog, boed law, boed heulwen, - y saif hi\nEr oes faith, anniben;",
		"Deunaw oed yn ei hyder, - deunaw oed\nYn ei holl ysblander,",
		"Rhwydd gamwr, hawdd ei gymell - i'r mynydd\nA'r mannau anghysbell;",
	),
	'toddaid': (
#		"Wedi blwng ymosod blin, - encilio:\nWedi'n creithio dianc i'r eithin.",
		"A'u gweld yn eu dillad gwaith - trwy'r oriau\nYn rhwygo o greigiau eu goreugwaith.",
	),
	'toddaid_hir': (
		# "Ac yn nyfnder y weryd - gwn y caf\nEi gusan olaf megis anwylyd.",
		"Mae antur dan y mintys - ac anial\nYw'r creithiau mâl lle bu'r crythau melys.",
	),
	'cywydd': (
		"Pa eisiau dim hapusach,\nNa byd yr aderyn bach?\nByd o hedfan a chanu\nA hwylio toc i gael tu.",
	),
	'englyn': (
		# "Talog, boed law, boed heulwen, - y saif hi\nEr oes faith, anniben;\nDaw ein byw sydyn i ben\nOnd hiroes yw braint derwen.",
#		"Deunaw oed yn ei hyder, - deunaw oed\nYn ei holl ysblander,\nDy ddeunaw oed boed yn bêr,\nYn baradwys ddibryder.",
		"Wele rith fel ymyl rhod - o'n cwmpas,\nCampwaith dewin hynod;\nHen linell bell nad yw'n bod,\nHen derfyn nad yw'n darfod.",
		"Rhwydd gamwr, hawdd ei gymell - i'r mynydd\nA'r mannau anghysbell;\nHel a didol diadell\nYw camp hwn yn y cwm pell.",
	),
	'cyhydedd_nawban': (
		"Cyfled yw dy gred â daear gron,\nTery ffiniau tir a phennod ton;\nHyd yr êl yr hylithr awelon,\nHyd y tywyn haul, duw wyt yn hon.",
	),
	'hir_a_thoddaid': (
		"A thwym ddwyfron y gwneuthum ddiofryd\nI garu fy mhau fel gwyrf fy mywyd;\nAnwylo gwylltineb tir fy mebyd,\nEi lwyn a'i afon a'i lynnau hefyd.\nAc yn nyfnder ei weryd - gwn y caf\nEi gusan olaf megis anwylyd."
	),
}

def run_demo(verbose=True):
	
	dad = DadansoddwrPennill()	
	for key in [
		'cwpled_cywydd', 
		'toddaid_byr', 
		'toddaid', 
		'toddaid_hir', 
		'cywydd',
		'englyn',
		'cyhydedd_nawban',
		# 'hir_a_thoddaid'
		]:
		val = penillion[key]
		for s in val:
			call(["clear"])
			print '========================================'
			print key.upper()
			print '========================================'
			llinynnau = s.split('\n')
			llinellau = [ Llinell(s) for s in llinynnau ]
			pennill = Pennill( llinellau )

			ateb = dad.oes_mesur( pennill )
			if ateb:
				print lliw.cyan( ateb[0] )
				for adro in ateb[1]:
					if verbose:
						print adro
					else:
						print lliw.magenta(adro.cynghanedd) + ': ' + adro.llinell.llinyn().strip()
			else:
				print lliw.magenta('DIM')
			print '========================================'
			print 
			try:
				aros = raw_input(">> bwrwch y dychwelwr i barhau ...")
			except KeyboardInterrupt:
				print
				return
			continue


#------------------------------------------------
def main():

	run_demo()

if __name__ == '__main__': main()


		
