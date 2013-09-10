#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
filename: peiriant.py 
author: scmde
created: 28/08/2013

functions:
    cydbwysedd
    oes_odl 
    oes_groes
    oes_draws 
    oes_lusg 
    oes_sain 
'''

import cysonion as cy
from llinell import *
from gair import *

import io

global debug
debug = True


#-----------------------------------------
# cydbwysedd
#-----------------------------------------
def cydbwysedd(s1,s2):
    '''
    ffwythiant: cydbwysedd
        pwrpas: darganfod dosbarth cydbwysedd 
        mewn:   dau air
        allan:  dosbarth cydbwysedd
    '''

    n1 = Gair(s1).nifer_sillau()
    n2 = Gair(s2).nifer_sillau()
    s = ''
    if n1 == n2:
        if n1 == 1:
            s =  'cytbwys_acennog'
        else:
            s =  'cytbwys_ddiacen'
    else:
        if n1 > n2: 
            s =  'anghytbwys_ddisgynedig'
        else:
            s = 'anghytbyws_ddyrchafedig'
    if debug: 
        print s
    return s

#-----------------------------------------
# oes_odli
#-----------------------------------------

def oes_odli(s1,s2):
    '''
    ffwythiant: odl_odli
        pwrpas: darganfod a didoli odl neu broest rhwng dau air
        mewn:   dau linyn
        allan:  llinyn odl (e.g. WCH/WCH, RO/TO etc.)

    dosbarthiadau:
        odl gyflawn
        proest cyflawn
        odl lafarog
        proest lafarog
    
    nodiant:
        aa - cwlwm llafariad
        bb - cwlwm cytseiniaid
        ds - deusain
    
    rheolau:

    odl gyflawn:
        cwlwm olaf:         bb yn cyfateb
        cwlwm olaf-ond-un:  aa yn cyfateb, ac o'r un pwysau os ydy'r ddau yn acennog (e.e. cath/math, pren/llen)

    proest gyflawn:
        cwlwm olaf:         bb yn cyfateb
        cwlwm olaf-ond-un:  aa o'r un pwysau (e.e. hen/dyn)
                        ds lleddf o'r un dosbarth  (e.e. llawn/mewn)
    odl lafarog:
        cwlwm olaf: aa yn cyfateb (e.e. tro/llo/bro)

    proest lafarog:
        cwlwm olaf: aa o'r un pwysau (e.e. bro/da/ci/te/du) 
                    ds lleddf o'r un dosbarth (e.e. tew/byw)
    
    deuseiniaid talgron:
        odl:    gyda'r llafariaid unigol priodol (e.e. cariad/gwlad)
        proest: gyda sillau sy'n cynnwys unrhyw lafariaid unigol (e.e gwas/nes, creithiog/golwg)

    deuseiniaid lleddf:
        odl:    gyda'r un ddeusain
        proest: gyda deusain o'r un dosbarth    (e.e. tew/byw, llawn/mewn, dewr/awr)
        
        
    patrwm_odl: C=cytsain, Y=llafariaid_ysgafn, T=llafariaid_trwm, 0,1,2,3,A
    '''
    g1 = Gair(s1)
    g2 = Gair(s2)

    dosbarth = 'dim'
    odl = ''

    # trwm ac ysgafn yn amhosib os oes gair lluosill (felly troi pob trwm yn ysgafn)
    if g1.nifer_sillau() > 1 or g2.nifer_sillau() > 1:
        g1.patrwm = g1.patrwm.replace('T','Y')
        g2.patrwm = g2.patrwm.replace('T','Y')
    
    cynffon1 = ''.join(g1.clymau[-1])
    cynffon2 = ''.join(g2.clymau[-1])
    if len(g1.clymau) > 1:
        cynffon1 = ''.join(g1.clymau[-2]) + cynffon1
    if len(g2.clymau) > 1:
        cynffon2 = ''.join(g2.clymau[-2]) + cynffon2
    odl_str = '['+ cynffon1 + '/' + cynffon2 + ']' 

    if debug:
        print odl_str
        
    # clymau olaf yn cyfateb
    if g1.clymau[-1] == g2.clymau[-1]:
        if debug: 
            print 'clymau olaf yn cyfateb:'
            
        # clymau olaf cytseinaidd
        if g1.patrwm[-1] == 'C':
            if debug: 
                print '  clymau olaf cytseinaidd:'
            
            if len(g1.clymau) > 1 and len(g1.clymau) > 1:
                if g1.clymau[-2] == g2.clymau[-2]:
                    if debug: 
                        print '    clymau olaf-ond-un yn cyfatab.'
                        print '      <ODL GYFLAWN> ' + odl_str
                    dosbarth = 'odl_gyflawn'
                    odl = (cynffon1, cynffon2)           
                else:
                    if g1.patrwm[-2] == g2.patrwm[-2]:
                        if debug: 
                            print '    clymau olaf-ond-un o\'r un dosbarth.'
                            print '        <PROEST GYFLAWN> ' + odl_str
                        dosbarth = 'proest_gyflawn'
                        odl = (cynffon1, cynffon2)
    
        # clymau olaf llafaraidd
        else:
            if debug: 
                print '  clymau olaf llafaraidd:'               
                print '    <ODL LAFAROG> ' + odl_str 
            dosbarth = 'odl_lafarog'
            odl = (cynffon1, cynffon2)
    
    # clymau olaf ddim yn gyfateb
    else:
        if debug: 
            print 'clymau olaf DDIM yn cyfateb' 
    
        # clymau olaf yn llafaraidd
        if g1.patrwm[-1] != 'C' and g2.patrwm[-1] != 'C':
            if debug:
                print '  clymau olaf yn llafaraidd'
                
            if g1.patrwm[-1] == g2.patrwm[-1]:

                if len(g1.clymau[-1]) == 1 and len(g2.clymau[-1]) == 1:
                    if debug: 
                        print '    clymau olaf yn llafariaid sengl o\'r un dosbarth.'
                        print '      <PROEST LAFAROG> ' + odl_str
                    dosbarth = 'proest_lafarog'
                    odl = (cynffon1, cynffon2)

                elif len(g1.clymau[-1]) > 1 and len(g2.clymau[-1] ) > 1:
                    if debug: 
                        print '    clymau olaf yn ddeuseiniaid o\'r un dosbarth.'
                        print '      <PROEST LAFAROG> '+ odl_str
                    dosbarth = 'proest_lafarog'
                    odl = (cynffon1, cynffon2)
                else:
                    if debug:
                        print '    clymau olaf yn DDIM o\'r un dosbarth.'
                        print '    <DIM ODL>.'
                    dosbarth = 'dim_odl'
                    odl = None
            
        # clymau olaf ddim yn llafaraidd
        else:
            if debug: 
                print '  clymau olaf ddim yn llafaraidd.'
                print '  <DIM ODL> ' + odl_str
                dosbarth = 'dim_odl'
                odl = None

    return dosbarth, odl



#-----------------------------------------
# oes_lusg
#-----------------------------------------
    
def oes_lusg(s):
    '''
    ffwythiant: oes_lusg
    '''

    cynghanedd_lusg = False
    ylinell = Llinell(s)
    
    # rhaid i'r brifodl for yn air lluosill
    if ylinell.ybrifodl.nifer_sillau() == 1:
        return False

    # hollti'r brifodl
    pen_ybrifodl, cwt_ybrifodl = ylinell.ybrifodl.pen_a_chynffon()
    if debug:
        print ''.join(pen_ybrifodl), ''.join(cwt_ybrifodl)

    # iteru dros eiriau'r linell i ddarganfod yr orffwysfa
    for yrorffwysfa in ylinell.geiriau:
        if yrorffwysfa == ylinell.ybrifodl:
            continue

        # darganfod a didoli odl
        o_str = yrorffwysfa.llinyn
        print ''
        print '[' + yrorffwysfa.llinyn + '/' + pb_str + ']'
        
        dosbarth, odl = oes_odli(o_str, pb_str)
        if dosbarth == 'odl_gyflawn': 
            cynghanedd_lusg = True
            print '\nCynghanedd LUSG: [' + yrorffwysfa.llinyn + '/' + llinell.ybrifodl.llinyn + ']'
            break

    return cynghanedd_lusg, odl

#-----------------------------------------
# oes_cytseinio
#-----------------------------------------

def oes_cytseinio(s0,s1):
    '''
    ffwythiant: oes_cystseinio
        darganfod a didoli cytseinio rhwng dau linyn
    '''


#-----------------------------------------
# oes_seithsill
#-----------------------------------------
def oes_seithsill(s):
    '''
    ffwythiant: oes_seithsill
    '''
    ll = Llinell(s)
    if ll.nifer_sillau() == 7:
        return True
    return False

#-----------------------------------------
# oes_groes
#-----------------------------------------
def oes_groes(s):
    '''
    ffwythiant: oes_groes
    '''
    
    cynghanedd_groes = False
    n_wreiddgoll = False
    n_ganolgoll  = False
    
    ll = Llinell(s)
    if debug:
        print ll
    
    # llinellau seithsill yn unig
    if not oes_seithsill(s):
        return False

    # hollti'r brifodl
    pb, ab, cb = ll.ybrifodl.pen_acen_cwt()
    if debug:
        print pb, ab, cb

    # iteru dros eiriau'r linell i ddarganfod yr orffwysfa
    # NA: iteru dros y sillau
    
    print ll.clymau_llafariaid
    k=0
    while k < 4:
        idx_chw = ll.clymau_llafariaid[k][0]   
        idx_dde = ll.clymau_llafariaid[k][-1]
        chw = ll.llythrennau[:idx_chw]
        can = ll.llythrennau[idx_chw:idx_dde+1]
        dde = ll.llythrennau[idx_dde+1:]
        if debug: 
            print '\nk = %d' % k
            print ''.join(chw)
            print ''.join(can)
            print ''.join(dde)
        k = k + 1

    k = 0
    n = ll.nifer_geiriau()
    while k < n-1:
        print '\nk = %d' % k
        yrorffwysfa = ll.geiriau[k]    

# Angen defnyddio RHESTRAU CLYMAU fan hyn (er mwyn darganfod toriadau o fewn gair)
        
        # hollti'r orffwysfa (tri rhestr llythrennau)
        po, ao, co = yrorffwysfa.pen_acen_cwt()
        if debug:
            print po, ao, co
        
        pen_chw =  [c for g in ll.geiriau[:k] for c in g.llythrennau] + po
        cwt_chw = co 
        pen_dde =  [c for g in ll.geiriau[k+1:-1] for c in g.llythrennau] + pb
        cwt_dde = cb


        if debug: 
            print pen_chw, cwt_chw
            print pen_dde, cwt_dde

        c_chw = []
        for cwlwm in pen_chw:
            for c in cwlwm:
                if c in cy.cytseiniaid:
                    c_chw.append(c)
        c_dde = []
        for cwlwm in pen_dde:
            for c in cwlwm:
                if c in cy.cytseiniaid:
                    c_dde.append(c)
        if debug:
            print '[' + ''.join(c_chw) + '/' + ''.join(c_dde) + ']'
        
        if c_chw == c_dde:
            cynghanedd_groes = True
            break
        elif len(c_chw) > 1 and c_chw[0] == 'n' and c_chw[1:] == c_dde:
            cynghanedd_groes = True
            n_wreiddgoll = True

        k = k + 1

    if cynghanedd_groes:
        print '\nCynghanedd GROES: [' + ''.join(c_chw) + '/' + ''.join(c_dde) + ']'
        print 'yr orffwysfa: ' + yrorffwysfa.llinyn
        chw_str = ' '.join([g.llinyn for g in ll.geiriau[:k+1]])
        dde_str = ' '.join([g.llinyn for g in ll.geiriau[k+1:]])
        print ll.llinyn_acenion()
        print ll 
        print ll.print_cytseiniaid()
        if n_wreiddgoll:
            print '>>> n wreiddgoll'

    return cynghanedd_groes

#------------------------------------------------
# testing
#------------------------------------------------
llinellau = dict()
llinellau['groes']= [
        "Ochain cloch a chanu clir",
        "Si'r oerwynt a sêr araul",
        "Awdur mad a dramodydd",
        "Ei awen gref yn ei grym",
    ]
llinellau['draws'] = [
        "Ochain cloch a gwreichion clir",
        "Si'r oerwynt dan sêr araul",
        "Awdur mad yw'r dramodydd",
    ]
llinellau['lusg'] = [
        "Beiddgar yw geiriau cariad",
        "Y mae arogl yn goglais",
        "Pell ydyw coed yr ellyll",
        "Y mae Morfudd yn cuddio",
        "Yr haul ar dawel heli",
#        "Taw â'th sôn, gad fi'n llonydd",
    ]
llinellau['sain'] = [
        "Cân ddiddig ar frig y fron",
        "Gŵr amhur yn sur ei sen",
        "Bydd y dolydd yn deilio",
        "Canlyniad cariad yw cosb",
        "Cân hardd croyw fardd Caerfyrddin",
        "Gŵr o ystryw ydyw ef",
        "Mae'n gas gennyf dras y dref",
        "Heddychwr gwr rhagorol",
    ]

odlau = dict()
odlau['cyflawn'] = [
    ('cath','math'),
    ('pren','llen'),
]
odlau['llafarog'] = [
    ('tro','llo'),
]

proestau = dict()
proestau['cyflawn'] = [
    ('hen','dyn'),
    ('llawn','mewn'),
]
proestau['llafarog'] = [
    ('tew','byw'),
]


def test_oes_lusg():
    print '\n------------------------------'
    print 'LUSG'
    print '------------------------------'
    for s in llinellau['lusg']:
        print s
        oes_lusg(s)
        print '\n------------------------------'
        


def test_oes_odli():
    print '\n------------------------------'
    print 'ODL GYFLAWN'
    print '------------------------------'
    for pair in odlau['cyflawn']:
        print pair
        oes_odli(pair[0],pair[1])
        print '---------------'

    print '\n------------------------------'
    print 'PROEST CYFLAWN'
    print '------------------------------'
    for pair in proestau['cyflawn']:
        print pair
        oes_odli(pair[0],pair[1])
        print '---------------'

    print '\n------------------------------'
    print 'ODL LAFAROG'
    print '------------------------------'
    for pair in odlau['llafarog']:
        print pair
        oes_odli(pair[0],pair[1])
        print '---------------'

    print '\n------------------------------'
    print 'PROEST LAFAROG'
    print '------------------------------'
    for pair in proestau['llafarog']:
        print pair
        oes_odli(pair[0],pair[1])
        print '---------------'

#------------------------------------------------
#def main():
if True:

    # test
    #test_oes_odli()
    #test_oes_lusg()

    s = "Och finnau, o chaf einioes"
    oes_groes(s)

'''
    s = "Beiddgar yw geiriau cariad"dd
    print '\n' + s
    oes_lusg(s)

    rhestr_llinellau = io.darllen_casgliad('llinellau_profi.xml')
    for ll in rhestr_llinellau:
        print ll

# test GROES
test_groes = True
if test_groes:
    for s in trysorfa['groes']:
        print '------------------------------'
        print '<' + s + '>'
        oes_groes(s)
        print '------------------------------'

# test LUSG
test_lusg = False
if test_lusg:
    for s in trysorfa['lusg']:
        print '------------------------------'
        print '<' + s + '>'
        oes_lusg(s)
        print '------------------------------'
'''

#if __name__ == '__main__': main()


        
