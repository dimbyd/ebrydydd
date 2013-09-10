#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from gair import *

global debug
class Llinell:
    '''
    class Llinell:
    mewnbwn: llinyn yn y ffurf safonol 
    '''

    def __init__(self, s):
      
        self.llinyn = s.encode('utf-8')
        self.llythrennau = rhestr_llythrennau(self.llinyn)
        self.geiriau = [Gair(w) for w in s.split(' ')]
        self.ybrifodl = self.geiriau[-1]

        self.clymau_llafariaid, self.clymau_cytseiniaid = clymau(self.llinyn)

        self.bylchau = [pos for pos in range(len(self.llythrennau)) if self.llythrennau[pos] == ' ']
        self.collnodau = [pos for pos in range(len(self.llythrennau)) if self.llythrennau[pos] == "'"]
        self.atalnodau = [pos for pos in range(len(self.llythrennau)) if self.llythrennau[pos] == ","]
        self.atalnodau_llawn = [pos for pos in range(len(self.llythrennau)) if self.llythrennau[pos] == "."]

        # mae angen rhoi'r brifodl a'r orffwysfa fel index i gwlwm llafariaid

        self.cynghanedd = None
        self.pwysau = None
        self.odl = None

    def __str__(self):
        return self.llinyn

    def __unicode__(self):
        return self.llinyn
    
    def nifer_geiriau(self):
        return len(self.geiriau)

    def nifer_sillau(self):
        return sum([g.nifer_sillau() for g in self.geiriau])

    def clymau(self):
        return [c for g in self.geiriau for c in g.clymau]
    
    def llinyn_acenion(self):
        return ' '.join([g.llinyn_acenion() for g in self.geiriau])
    
    def llinyn_cytseiniaid(self, gorffwysfa=None):
        s = []
        for c in self.llythrennau:
            if c in cy.cytseiniaid:
                s.append(c)
            else:
                s.append(' '*len(c))
        if gorffwysfa and isinstance(gorffwysfa,int) and gorffwysfa > -1 and gorffwysfa < len(self.llythrennau):
            s[gorffwysfa] = '|'
        return ''.join(s)

    def llinyn_llafariaid(self):
        s = []
        for c in self.llythrennau:
            if c in cy.llafariaid:
                s.append(c)
            else:
                s.append(' '*len(c))
        return ''.join(s)

    
class Cwpled:
    '''
    class Cwpled:
    mewnbwn: dau linyn safonol yn y drefn gywir 
    '''
    
    def __init__(self, s1, s2):
        self.cyntaf = Llinell(s1)
        self.ail =  Llinell(s2)
        
    def is_cwpled_cywydd(self):
        if self.cyntaf.nifer_sillau != 7 or self.ail.nifer_sillau() != 7:
            sys.stderr.write('TORR MESUR: cwpled cywydd (llinellau seithsill yn unig')
            return False
        if self.cyntaf.prifodl.pwyslais == self.ail.prifodl.pwyslais:
            sys.stderr.write('TORR MESUR: cwpled cywydd (llinellau seithsill yn unig')
            return False

class Cerdd:
    '''
    class Cerdd:
    '''

    def __init__(self, dilyniant):
        self.dilyniant = dilyniant

#------------------------------------------------
#def main():
if True:
    s1 = "Drwy eu sain a'u hystyr sydd"
    s2 = "Yn galw ar ei gilydd."
    #s2 = u'Amodau, rhwymau oedd rhôm'

    e1 = Llinell(s1)
    e2 = Llinell(s2)
    
    print e1.llinyn_acenion()
    print e1
    print e2.llinyn_acenion()
    print e2

#    cwpled = Cwpled(s1,s2)

#if __name__ == '__main__': main()


