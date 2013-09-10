#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.etree.ElementTree import ElementTree
from llinell import Llinell, Cwpled, Cerdd
import os

debug = True

#------------------------------------------------
# ffwythiant: darllen_casgliad
#------------------------------------------------
def darllen_casgliad(filename):
    tree = ElementTree()
    tree.parse(filename)
	
    if tree.getroot().tag != 'casgliad':
        raise CerddException("Error: nid <casgliad> yw'r elfen uchaf")

    casgliad = tree.getroot()
    for k in casgliad.keys(): 
        print k + ':\t' +  casgliad.attrib[k]
    print ''
    if casgliad.find('llinell') is not None:
        rhestr_llinellau = []
        cit = casgliad.getiterator('llinell')
        for llinell in cit:
            s = llinell.text.strip()
            print 'Llinell:\t' + s
            for k in llinell.keys(): 
                print k + ':\t' +  llinell.attrib[k]
            print ''
            rhestr_llinellau.append(Llinell(s))
	return rhestr_llinellau

#------------------------------------------------
# ffwythiant: darllen_cerdd
#------------------------------------------------
def darllen_cerdd(filename):
    tree = ElementTree()
    tree.parse(filename)
	
    if tree.getroot().tag != 'cerdd':
        raise CerddException("camffurf xml: nid <cerdd> yw'r elfen uchaf")

    cerdd = tree.getroot()
    for k in cerdd.keys(): 
        print k + ':\t' +  cerdd.attrib[k]
    dilyniant = []
    if cerdd.find('cwpled') is not None:
        cit = cerdd.getiterator('cwpled')
        for cwpled in cit:
            s1 = cwpled[0].text.strip()
            print s1
            s2 = cwpled[1].text.strip()
            print s2
            dilyniant.append(Cwpled(s1,s2))

	return Cerdd(dilyniant)

class CerddException(Exception):
	def __init__(self, neges):
		self.neges = neges
	def __str__(self):
		return self.neges


cerdd = darllen_cerdd('cerddi/cywydd_tudur_aled.xml')
llinellau = darllen_casgliad('llinellau_profi.xml')

#------------------------------------------------
# main
#------------------------------------------------
#def main():
#filename = 'cywydd_tudur_aled.xml'
#cerdd = darllen_xml(filename)
#print cerdd

#if __name__ == '__main__': main()


'''
print os.getcwd()
print os.listdir(os.getcwd())
filename = 'cyfatebiaeth_seinegol.txt'
#filename = 'cysonion.py'
#for line in open(filename):
#    li=line.strip()
#    if not li.startswith("#"):
#        print line.rstrip()

import re
IPA_table = dict()
for line in open(filename):
    line = line.partition('#')[0]
    line = line.rstrip()
    if line:
        parts = re.split(r'\t+', line)
        key = parts[0].decode('utf-8')
        val = parts[1].decode('utf-8')
        IPA_table[key] = val
'''


