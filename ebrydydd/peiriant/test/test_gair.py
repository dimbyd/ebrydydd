#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
filename: test_gair.py 
author: scmde
created: 28/06/2013
'''

import unittest
import gair

class TestGairFunctions(unittest.TestCase):
    def setUp(self):
        self.w = Gair('chwaethus')
    
    def test_nifer_sillau(self):
        self.assertEquals(self.w.nifer_sillau(),7)

if __name__ == '__main__':
    unittest.main()

