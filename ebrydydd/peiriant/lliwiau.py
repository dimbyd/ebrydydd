# lliwiau.py
# -*- coding: utf-8 -*-
'''
lliwiau.py: 
'''
class lliwiau:
	DIM 	= '\033[0m'
	DU	 	= '\033[30m'
	COCH 	= '\033[31m'
	GWYRDD 	= '\033[32m'
	MELYN 	= '\033[33m'
	GLAS 	= '\033[34m'
	MAGENTA	= '\033[35m'
	CYAN 	= '\033[36m'
	GWYN 	= '\033[37m'

	def disable(self):
		self.DIM = ''
		self.DU = ''
		self.COCH = ''
		self.GWYRDD = ''
		self.MELYN = ''
		self.GLAS = ''
		self.MAGENTA = ''
		self.CYAN = ''
		self.GWYN = ''

def coch(s):
	return lliwiau.COCH + s + lliwiau.DIM

def gwyrdd(s):
	return lliwiau.GWYRDD + s + lliwiau.DIM

def melyn(s):
	return lliwiau.MELYN + s + lliwiau.DIM

def glas(s):
	return lliwiau.GLAS + s + lliwiau.DIM

def magenta(s):
	return lliwiau.MAGENTA + s + lliwiau.DIM

def cyan(s):
	return lliwiau.CYAN + s + lliwiau.DIM

def gwyn(s):
	return lliwiau.GWYN + s + lliwiau.DIM

#------------------------------------------------
def main():
	s = 'cranc'
	print coch(s)
	print gwyrdd(s)
	print melyn(s)
	print glas(s)
	print magenta(s)
	print cyan(s)
	
if __name__ == '__main__': main()


