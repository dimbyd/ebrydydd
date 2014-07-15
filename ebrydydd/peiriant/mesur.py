#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from gair import Gair
from llinell import Llinell
    
class Cwpled:
    '''
    class Cwpled:
    mewnbwn: dau linyn safonol yn y drefn gywir 
    '''
    
    def __init__(self, s1, s2):
        self.cyntaf = Llinell(s1)
        self.ail =  Llinell(s2)

    def __str__(self):
        return self.cyntaf.llinyn + '\n' + self.ail.llinyn
        
    def is_cwpled_cywydd(self):
        if self.cyntaf.nifer_sillau() != 7 or self.ail.nifer_sillau() != 7:
            print 'cwpled_cywydd: torr_mesur: llinell heb fod yn seithsill'
            return False
        if self.cyntaf.ybrifodl.sillaf_pwyslais == self.ail.ybrifodl.sillaf_pwyslais:
            print 'cwpled_cywydd: torr_mesur: acenion o\'r un fath'
            return False
        return True

#------------------------------------------------
#def main():
if True:
    s1 = "Drwy eu sain a'u hystyr sydd"
    s2 = "Yn galw ar ei gilydd."

    cwpled = Cwpled(s1,s2)
    
    print cwpled.cyntaf.llinyn_acenion()
    print cwpled.cyntaf.llinyn
    print cwpled.cyntaf.nifer_sillau()
    print cwpled.cyntaf.ybrifodl.safleoedd_acenion
    print cwpled.cyntaf.ybrifodl.sillaf_pwyslais
    print cwpled.ail.llinyn_acenion()
    print cwpled.ail.llinyn
    print cwpled.ail.nifer_sillau()
    print cwpled.ail.ybrifodl.safleoedd_acenion
    print cwpled.ail.ybrifodl.sillaf_pwyslais
    
    print 'Test <cwpled_cywydd>:' 
    print cwpled.is_cwpled_cywydd()

#if __name__ == '__main__': main()



