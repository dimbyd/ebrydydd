#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
eithriadau.py 
	rhestri o eiriau afreolus (llinynnau)

1. lluosill_acennog
 	Geiriau lluosill sydd a'r pwyslais ar y sill olaf
		Nid oes angen cynnwys geiriau sydd yn dangos acen: caniatâu, nesáu

2. deusill 
	Geiriau yn cynnwys parau o lafariaid sydd fel arfer yn ddeuseiniaid (unsill)
	ond sydd yn ddeusill mewn gwirionedd

3. llafariaid_hir
	Geiriau yn cynnwys llafariaid hir ond heb acen grom echblyg

'''


# geiriau lluosill acennog
lluosill_acennog = (
	'caniatâu',
	'mawrhad',
	'nesáu',
	'prinhau',
	'rhyddhad',	
	'cymraeg',
	'anabl',
)

# deuseiniaid deusill
deusill = {
	'ia': (
		'dianc',
		'diadell',
		'rhiant',
		'Rhian'
	),
	'ie': (
		'rhieni',
	),
	'iw': (
		'diwair',
		'diwyd',
	),
	'ya': (
		'lletya',
	),
}

# llafariaid hir heb acen grom echblyg
llafariad_hir = (
	'mud',
	'mab',
	'tad',
	'tir',
)
