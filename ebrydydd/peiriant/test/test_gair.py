#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
filename: test_gair.py 
author: scmde
created: 28/06/2013
'''

import unittest
from ebrydydd.peiriant.gair import Gair

class TestCroes(unittest.TestCase):
    def setUp(self):
        Llinell.objects.create(llinyn="Am eu hawr yn ymaros", awdur="Dic Jones")
    
    def test_nifer_sillau(self):
        self.assertEquals(self.w.nifer_sillau(),7)

if __name__ == '__main__':
    unittest.main()

