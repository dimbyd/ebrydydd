# cysonion.py
# -*- coding: utf-8 -*-

#------------------------------------------------
# cysonion
#------------------------------------------------
a = u',.\'\"\\/!?-;:_@()*^%~{}[]+=|'
b = u'b,c,ch,d,dd,f,ff,g,ng,h,j,l,ll,m,n,p,ph,r,rh,s,sh,t,th,k,q,v,x,z'
b2 = u'Ch,Dd,Ff,Ng,Ll,Ph,Rh,Th'
c = u'aeiouwy'
d = u'âáêëîïôûŵŷ'

atalnodau = list(a)
cytseiniaid = b.rsplit(',') + b.upper().rsplit(',') + b2.rsplit(',')
llafariaid_byr = list(c + c.upper())
llafariaid_hir   = list(d + d.upper())
llafariaid = llafariaid_byr + llafariaid_hir
llythrennau = cytseiniaid + llafariaid
#------------------------------------------------
# dewisiadau a llythrenwau
#------------------------------------------------
LLYTHRENWAU = {
	'cynghanedd': (
		('CRO', 'Croes'),
		('TRA', 'Traws'),
		('SAI', 'Sain'),
		('LLU', 'Llusg'),
		('LLA', 'Llusg lafarog'),
		('COG', 'Croes o gyswllt'),
		('TRF', 'Traws fantach'),
		('SAL', 'Sain lafarog'),
	),
	'aceniad': (
		('CAC', 'Cytbwys Acenog'),
		('CDI', 'Cytbwys Ddiacen'),
		('ADI', 'Anghytbwys Ddisgynedig'),
		('ADY', 'Anghytbwys Ddyrchafedig'),
		# ('CAC', 'Cyt. Acenog'),
		# ('CDI', 'Cyt. Ddiacen'),
		# ('ADI', 'Ang. Ddisgynedig'),
		# ('ADY', 'Ang. Ddyrchafedig'),
	),
	'odl': (
		('OGY', 'Odl Gyflawn'),
		('PGY', 'Proest Gyflawn'),
		('OLA', 'Odl Lafarog'),
		('PLA', 'Proest Lafarog'),
	),
	'bai': (
		('TWG',	'Twyll gynghanedd'),
		('GOR',	'Gormod o odl'),
		('PRO',	'Proest i\'r odl'),
		('CRY',	'Crych a llyfn'),
		('TRW',	'Trwm ac ysgafn'),
		('LLE',	'Lleddf a thalgron'),
		('TWO',	'Twyll odl'),
		('GWE',	'Gwestodl'),
		('DYB',	'Dybryd sain'),
		('RHY',	'Rhy debyg'),
		('YMS',	'Ymsathr odlau'),
		('HAN',	'Hanner proest'),
		('CAM',	'Camacennu'),
		('LLY',	'Llysiant llusg'),
		('CAG',	'Camosodiad gorffwysffa'),	# llinell bendrom
		('CAR',	'Carnymorddiwes'),
		('TIN',	'Tin ab'),
		('TOR',	'Tor mesur'),
	),
	'statws': (
		('TEC', 'Technegydd'),
		('MYF', 'Myfyriwr'),
		('PRY', 'Prydydd'),
		('BAR', 'Bardd'),
		('PRI', 'Prifardd'),
	),
}
#------------------------------------------------
# deuseuniaid
#------------------------------------------------
'''
CC tud 23: 
	deuseiniaid talgron 
		cynnwys i neu w fel elfen gyntaf
			ia (cariad), ie (colier), io (cerfio), iw (cerfiwr), iy (faliym)
			wa (gwaun), we (gweld), wi (gwin), wy (gwyn), wo (gweddwon)
		pwyslais ar yr ail elfen
		odli gyda llafariaid unigol (gwlad, cariad)
		proestio gyda llafariaid unigol (gwas, nes)
		proestio gyda'u gilydd (gweithiwr, marwor)
	deuseiniaid lleddf
		dosbarth 1: aw, ew, iw, ow, uw, yw
		dosbarth 2: ae, oe, wy, ei, oi, 
		dosbarth 3: au, eu, ou, ey
		
CC: talgron = pwyslais ar yr ail elfen
DE: lleddf = pwyslais ar yr elfen gyntaf (?)

Mae rhai ar goll or rhestri uchod:
aa, ai, ao, ay
ea, ee, eo, 
ii, iu
oa, oo, oy
ua, ue, ui, uo, uu, uy
wu, ww
ya, ye, yi, yo, yu

Mae rhai clymau o lafariaid yn ddeusill:
eos	
duon,
'''
# talgron         = '0'
# lleddf_cyntaf   = '1'
# lleddf_ail      = '2'
# lleddf_trydydd  = '3'
# deusill 		= 'D'
# arall			= 'A'
# dosbarth_deusain = {
#     'ia': talgron,
#     'ie': talgron,
#     'io': talgron,
#     'iw': talgron,
#     'iy': talgron,
#     'wa': talgron,
#     'we': talgron,
#     'wi': talgron,
#     'wo': talgron,
#     'wy': talgron,
#     'aw': lleddf_cyntaf,
#     'ew': lleddf_cyntaf,
#     'iw': lleddf_cyntaf,
#     'ow': lleddf_cyntaf,
#     'uw': lleddf_cyntaf,
#     'yw': lleddf_cyntaf,
#     'ae': lleddf_ail,
#     'oe': lleddf_ail,
#     'Wy': lleddf_ail,
#     'ei': lleddf_ail,
#     'ai': lleddf_ail,
#     'oi': lleddf_ail,
#     'au': lleddf_trydydd,
#     'eu': lleddf_trydydd,
#     'ou': lleddf_trydydd,
#     'ey': lleddf_trydydd,
# 	# deuseiniaid heb eu rhestru yn y llyfrau (DE)
#     'uo': deusill,		# duon
# 	'eo': deusill,		# eos
# 	'ea': deusill,		# cread
# 	'oa': deusill,		# credoau
#     'oy': lleddf_trydydd,	
#     'ua': talgron,			
# }

deuseiniaid = {
	'talgron': 			['ia', 'ie', 'io',  'iw', 'iy', 'ua', 'wa', 'we', 'wi', 'wo',  'wy'],
	'lleddf_cyntaf':	['aw', 'ew', 'iw', 'ow', 'uw', 'yw'],
	'lleddf_ail':		['ae', 'ai', 'ei', 'oe', 'oi', 'Wy'],
    'lleddf_trydydd':	['au', 'eu', 'ou', 'ey', 'oy'],
	'deusill':			['uo', 'eo', 'ea', 'oa'], 	# duon, eos, cread, credodau
}

dosbarth_deusain = dict([ (z,key) for key in deuseiniaid.keys() for z in deuseiniaid[key] ])

# DEWISIADAU_CYNGHANEDD = (
# 	('DIM', 'Dim'),
# 	('CRO', 'Croes'),
# 	('TRA', 'Traws'),
# 	('SAI', 'Sain'),
# 	('LLU', 'Llusg'),
# 	('LLA', 'Llusg lafarog'),
# 	('COG', 'Croes o gyswllt'),
# 	('TRF', 'Traws fantach'),
# 	('SAL', 'Sain lafarog'),
# )
# DEWISIADAU_ACENIAD = (
# 	('CAC', 'Cytbwys Acenog'),
# 	('CDI', 'Cytbwys Ddiacen'),
# 	('ADI', 'Anghytbwys Ddisgynedig'),
# 	('ADY', 'Anghytbwys Ddyrchafedig'),
# )
# DEWISIADAU_ODL = (
# 	('OGY', 'Odl Gyflawn'),
# 	('PGY', 'Proest Gyflawn'),
# 	('OLA', 'Odl Lafarog'),
# 	('PLA', 'Proest Lafarog'),
# )	
# DEWISIADAU_BAI = (
# 	('TWG',	'Twyll gynghanedd'),
# 	('GOR',	'Gormod o odl'),
# 	('PRO',	'Proest i\'r odl'),
# 	('CRY',	'Crych a llyfn'),
# 	('TRW',	'Trwm ac ysgafn'),
# 	('LLE',	'Lleddf a thalgron'),
# 	('TWO',	'Twyll odl'),
# 	('GWE',	'Gwestodl'),
# 	('DYB',	'Dybryd sain'),
# 	('RHY',	'Rhy debyg'),
# 	('YMS',	'Ymsathr odlau'),
# 	('HAN',	'Hanner proest'),
# 	('CAM',	'Camacennu'),
# 	('LLY',	'Llysiant llusg'),
# 	('CAG',	'Camosodiad gorffwysffa'),	# llinell bendrom
# 	('CAR',	'Carnymorddiwes'),
# 	('TIN',	'Tin ab'),
# 	('TOR',	'Tor mesur'),
# )
# DEWISIADAU_STATWS = (
# 	('MYF', 'Myfyriwr'),
# 	('PRY', 'Prydydd'),
# 	('BAR', 'Bardd'),
# 	('PRI', 'Prifardd'),
# )

