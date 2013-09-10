# cysonion.py
# -*- coding: utf-8 -*-

#------------------------------------------------
# cysonion byd-eang 
#------------------------------------------------
a = list(u',.\'\"\\/!?-;:_@()*^%~{}[]+=|')
b = u'b,c,ch,d,dd,f,ff,g,ng,h,j,l,ll,m,n,p,ph,r,rh,s,t,th,k,q,v,x,z'
c = u'aeiouwy'
d = u'âêëîïôûŵuŷ'

atalnodau = list(a)
cytseiniaid = list(b + b.upper())
llafariaid_ysgafn = list(c + c.upper())
llafariaid_trwm   = list(d + d.upper())
llafariaid = llafariaid_ysgafn + llafariaid_trwm

#------------------------------------------------
# dosbarth deuseuniaid
#------------------------------------------------
talgron         = 0
lleddf_cyntaf   = 1
lleddf_ail      = 2
lleddf_trydydd  = 3
lleddf_arall    = 4

deuseiniaid_list = {
    'ia': talgron,
    'ie': talgron,
    'io': talgron,
    'iw': talgron,
    'iy': talgron,
    'wa': lleddf_cyntaf,
    'we': lleddf_cyntaf,
    'wi': lleddf_cyntaf,
    'wo': lleddf_cyntaf,
    'wy': lleddf_cyntaf,
    'aw': lleddf_ail,
    'ew': lleddf_ail,
    'iw': lleddf_ail,
    'ow': lleddf_ail,
    'uw': lleddf_ail,
    'yw': lleddf_ail,
    'ae': lleddf_trydydd,
    'oe': lleddf_trydydd,
    'Wy': lleddf_trydydd,
    'ei': lleddf_trydydd,
    'ai': lleddf_trydydd,
    'oi': lleddf_trydydd,
    'au': lleddf_arall,
    'eu': lleddf_arall,
    'ou': lleddf_arall,
    'ey': lleddf_arall,
}

deuseiniaid_dict = {
    'a': {
        'a': -1,
        'e': 3,
        'i': 3,
        'o': None,
        'u': 4,
        'w': 2,
        'y': None,
    },
    'e': {
        'a': None,
        'e': -1,
        'i': 3,
        'o': None,
        'u': 4,
        'w': 2,
        'y': 4,
    },
    'i': {
        'a': 0,
        'e': 0,
        'i': -1,
        'o': 0,
        'u': None,
        'w': 0,
        'y': 0,
    },
    'o': {
        'a': None,
        'e': 3,
        'i': 3,
        'o': -1,
        'u': 4,
        'w': 2,
        'y': None,
    },
    'u': {
        'a': None,
        'e': None,
        'i': None,
        'o': None,
        'u': -1,
        'w': 2,
        'y': None,
    },
    'w': {
        'a': 1,
        'e': 1,
        'i': 1,
        'o': 1,
        'u': None,
        'w': -1,
        'y': 1,
    },
    'y': {
        'a': None,
        'e': None,
        'i': None,
        'o': None,
        'u': None,
        'w': 2,
        'y': -1,
    },
}


#------------------------------------------------
# odl 
#------------------------------------------------
class Odl(object):
    
    def __init__(self, s1, s2):
        self.dosbarth_cynradd = 'odl'     # None, odl, proest
        self.dosbarth_eilradd = 'cyflawn' # None, cyflawn, llafarog
 
#------------------------------------------------
# cydbwysedd
#------------------------------------------------
class Cydbwysedd(object):

    def __init__(self, s1, s2):
        self.dosbarth_cynradd = 'cytbwys'   # None, cytbwys, anghytbwys
        self.dosbarth_eilradd = 'acennog'   # None, acennog, diacen

#------------------------------------------------
# bai
#------------------------------------------------
class Bai(object):

    def __init__(self, s1, s2):
        self.dosbarth_cynradd = 'odl'     # None, odl, proest
        self.enw = 'cyflawn' # None, cyflawn, llafarog


beiau = {
    'odli': {
        'TAY': "Trwm ac ysgafn",
        'LLE': "Lleddf a thalgron",
        'TWY': "Twyll odl",
        'GWE': "Gwestodl"
    },
    'prifodl': {
        'GOR': "Gormod o odlau",
        'PRO': "Proest i\'r odl",
        'DYB': "Dybryd sain",
        'RHY': "Rhy debyg",
        'YMS': "Ymsathr odlau",
        'HAN': "Hanner proest"
    },
    'cyfateb': {
        'TWY': "Twyll gynghanedd",
        'COS': "Camosodiad",
        'CRY': "Crych a llyfn",
        'CAM': "Camacennu"
    },
    'barddonol': {
        'LLY': "Llysiant llusg",
        'CAG': "Camosodiad gorffwysfa",
        'CAR': "Carnymorddiwes",
        'TIN': "Tin ab",
        'TOR': "Tor mesur"
    }
}

#-----------------------------------------
# geiriau afreolus (llwytho) 
#-----------------------------------------
#afreolaidd = dict()

#afreolaidd['geiriau_llafariaid_ysgafn_heb_acen'] = list()
#for line in open('afreolaidd/geiriau_llafariaid_ysgafn_heb_acen.txt'):
#    line = line.partition('#')[0]
#    line = line.rstrip()
#    if line:
#        afreolaidd['geiriau_llafariaid_ysgafn_heb_acen'].append(line)
#
#afreolaidd['geiriau_acen_sill_olaf'] = list()
#for line in open('afreolaidd/geiriau_acen_sill_olaf.txt'):
#    line = line.partition('#')[0]
#    line = line.rstrip()
#    if line:
#        afreolaidd['geiriau_acen_sill_olaf'].append(line)
#
#afreolaidd['geiriau_wy_leddf'] = list()
#for line in open('afreolaidd/geiriau_wy_leddf.txt'):
#    line = line.partition('#')[0]
#    line = line.rstrip()
#    if line:
#        afreolaidd['geiriau_wy_leddf'].append(line)


