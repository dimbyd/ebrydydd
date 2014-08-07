#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
cysonion.py
	nodau:		llafariaid, cytseiniaid, atalnodau, deuseiniaid, 
	cytseinedd: parau ceseilio, cytseiniaid meddalu, cyfuniadau trychben, 
	odl: 		cyfuniadau gwyrdro
	dosbarthu:	llythrenwau
'''

#------------------------------------------------
# nodau
#------------------------------------------------
a = u',.\'\"\\/!?-;:_@()*^%~{}[]+=|'
b = u'b,c,ch,d,dd,f,ff,g,ng,h,j,l,ll,m,n,p,ph,r,rh,s,sh,t,th,k,q,v,x,z'
b2 = u'Ch,Dd,Ff,Ng,Ll,Ph,Rh,Th'
c = u'aeiouwyẙ'
d = u'âáêëîïôûúŵẃŷý'
atalnodau = list(a)
cytseiniaid = b.rsplit(',') + b.upper().rsplit(',') + b2.rsplit(',')
llafariaid_byr = list(c + c.upper())
llafariaid_hir   = list(d + d.upper())
llafariaid = llafariaid_byr + llafariaid_hir
llythrennau = cytseiniaid + llafariaid

#------------------------------------------------
# llythrenwau (dosbarthiadau)
# llinell: cynghanedd, aceniad, bai
# pennill: mesur
#------------------------------------------------
LLYTHRENWAU = {
	'cynghanedd': (
		('DIM', 'Dim cynghanedd'),
		('CRO', 'Croes'),
		('COG', 'Croes o gyswllt'),
		('CRD', 'Croes drychben'),
		('CRG', 'Croes gysylltben'),
		('CRL', 'Croeslusg'),
		('TRA', 'Traws'),
		('TRD', 'Traws drychben'),
		('TRG', 'Traws gysylltben'),
		('TRF', 'Traws fantach'),
		('TFD', 'Traws fantach drychben'),
		('TFG', 'Traws fantach gysylltben'),
		('TGR', 'Trawsgroes'),
		('TRL', 'Trawslusg'),
		('LLU', 'Llusg'),
		('LLL', 'Llusg lafarog'),
		('SAI', 'Sain'),
		('SAD', 'Traws drychben'),
		('SAG', 'Traws gysylltben'),
		('SOG', 'Sain o gyswllt'),
		('SAG', 'Sain gadwynog'),
		('SAL', 'Sain lafarog'),
		('SEG', 'Seingroes'),
		('SED', 'Seindraws'),
		('SEL', 'Seinlusg'),
	),
	'aceniad': (
		('CAC', 'cytbwys acennog'),
		('CDI', 'cytbwys ddiacen'),
		('ADI', 'anghytbwys ddisgynedig'),
		('ADY', 'anghytbwys ddyrchafedig'),
	),
	'bai': (
		('GOR',	'Gormod o odl'),
		('PRO',	'Proest i\'r odl'),
		('CRY',	'Crych a llyfn'),
		('TRW',	'Trwm ac ysgafn'),
		('LLE',	'Lleddf a thalgron'),
		('TOR',	'Tor mesur'),
	),
	'mesur': (
		('ENG', 'Englyn unodl union'),
		('CYW', 'Cywydd deuair hirion'),
		('CWC', 'Cwpled cywydd'),
		('TOB', 'Toddaid byr'),
		('TOD', 'Toddaid'),
		('TOH', 'Toddaid hir'),
		('CYH', 'Cyhydedd nawban'),
		('HAT', 'Hir-a-thoddaid'),
	),

}

#------------------------------------------------
# geiriau gwan (AYG tud. 28)
#------------------------------------------------
geiriau_gwan = [
	# bannod (article)
	'y','yn',
	# rhagenwau (pronouns)
	'fy','dy', 'di', 'ein', 'eich', 'eu',
	# cysyllteiriau (conjunctions)
	'a', 'ac', 'neu', 'na', 'yn', 'yw', 'ar',
	# eraill
	# 'o', 
]


#------------------------------------------------
# ceseilio
#------------------------------------------------
ceseiliaid = {
	'p': [ ('b','h'), ('b','b'), ('b','p'), ('p','b') ],
	't': [ ('d','h'), ('d','d'), ('d','t'), ('t','d') ],
	'c': [ ('g','h'), ('g','g'), ('g','c'), ('c','g') ],
	'ff': [ ('f','ff'), ('ff','f') ],
	'll': [ ('l','ll'), ('ll','l') ],
	'th': [ ('th','dd'), ('') ],
}
dosbarth_ceseiliad = dict([ (z,key) for key in ceseiliaid.keys() for z in ceseiliaid[key] ])
		
#------------------------------------------------
# meddalu
#------------------------------------------------
cytseiniaid_meddalu = ('c','ch','ff','ll','s')


#------------------------------------------------
# cyfuniadau gwyrdro (rhaid i'r ei/eu ddod yn yr ail odl)
#------------------------------------------------
cyfuniadau_gwyrdro = (
	('aith', 'eith'),
	('ain', 'ein'),
	('aur', 'eur'),
	('au', 'eu'),
)

#------------------------------------------------
# trychben (trych = truncated)
#------------------------------------------------
cyfuniadau_trychben = (
	'br', 'bl', 'dr', 'dl', 'dn', 'fl', 'fn', 'fr', 'ffr', 'ffl', 
	'gr', 'gl', 'gn', 'ls', 'lm', 'ml', 'nt', 'pl', 'pr', 'tl',
)

#------------------------------------------------
# deuseuniaid (Clywed Cynghanedd: tud. 23)
#------------------------------------------------
deuseiniaid = {
	'talgron': 			['ia', 'ie', 'io',  'iw', 'iy', 'ua', 'wa', 'we', 'wi', 'wo',  'wy'],
	'lleddf_cyntaf':	['aw', 'ew', 'iw', 'ow', 'uw', 'yw'],
	'lleddf_ail':		['ae', 'ai', 'ei', 'oe', 'oi', 'Wy'],
    'lleddf_trydydd':	['au', 'eu', 'ou', 'ey', 'oy'],
	'deusill':			['uo', 'eo', 'ea', 'oa' ,'ee'], 	# duon, eos, cread, credoau, deellir
	'eraill':			['ay', 'ue', 'ya'],
}
dosbarth_deusain = dict([ (z,key) for key in deuseiniaid.keys() for z in deuseiniaid[key] ])
deuseiniaid['lleddf'] = deuseiniaid['lleddf_cyntaf'] + deuseiniaid['lleddf_ail'] + deuseiniaid['lleddf_trydydd']

