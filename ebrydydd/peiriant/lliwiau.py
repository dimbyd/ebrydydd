# lliwiau.py
# -*- coding: utf-8 -*-
'''
lliwiau.py: 
'''
class bcolors:
	COCH 	= '\033[31m'
	GWYRDD 	= '\033[32m'
	MELYN 	= '\033[33m'
	GLAS 	= '\033[34m'
	PIWS 	= '\033[35m'
	DIM 	= '\033[0m'

	def disable(self):
		self.COCH = ''
		self.GLAS = ''
		self.DIM = ''
		self.A = ''
		self.B = ''
		self.C = ''
		self.D = ''
		self.E = ''

def coch(s):
	return bcolors.COCH + s + bcolors.DIM

def gwyrdd(s):
	return bcolors.GWYRDD + s + bcolors.DIM

def melyn(s):
	return bcolors.MELYN + s + bcolors.DIM

def glas(s):
	return bcolors.GLAS + s + bcolors.DIM

def piws(s):
	return bcolors.PIWS + s + bcolors.DIM

#------------------------------------------------
def main():
	s = 'cranc'
	print coch(s)
	print gwyrdd(s)
	print melyn(s)
	print glas(s)
	print piws(s)
	
if __name__ == '__main__': main()


