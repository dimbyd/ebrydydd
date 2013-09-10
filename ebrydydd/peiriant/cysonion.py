# cysonion.py
# -*- coding: utf-8 -*-

#------------------------------------------------
# cysonion
#------------------------------------------------
a = u',.\'\"\\/!?-;:_@()*^%~{}[]+=|'
b = u'b,c,ch,d,dd,f,ff,g,ng,h,j,l,ll,m,n,p,ph,r,rh,s,t,th,k,q,v,x,z'
b2 = u'Ch,Dd,Ff,Ng,Ll,Ph,Rh,Th'
c = u'aeiouwy'
d = u'âêëîïôûŵŷ'

atalnodau = list(a)
cytseiniaid = b.rsplit(',') + b.upper().rsplit(',') + b2.rsplit(',')
llafariaid_ysgafn = list(c + c.upper())
llafariaid_trwm   = list(d + d.upper())
llafariaid = llafariaid_ysgafn + llafariaid_trwm

#------------------------------------------------
# dosbarth deuseuniaid
#------------------------------------------------
talgron         = '0'
lleddf_cyntaf   = '1'
lleddf_ail      = '2'
lleddf_trydydd  = '3'
lleddf_arall    = '4'

dosbarth_deuseiniaid = {
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


