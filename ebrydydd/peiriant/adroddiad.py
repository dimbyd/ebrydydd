#!/usr/bin/python
# coding=utf8

'''
adroddiad.py 
'''

# from acen import aceniad, nifer_sillau, pwyslais, traeannu_cytseiniaid
# from odl import prawf_odl, prawf_odl_lusg
# from cytseinedd2 import prawf_cytseinedd

# import cysonion as cy
import llinyn as ll
import acen as ac
import odl as od

global debug
debug = False

# adroddiad
class Adroddiad(object):
	'''
	class Adroddiad:
		Yn cynnwys...
			(a) dosbarthiadau/sylwadau ar gyfer Dadansoddiad(cynghanedd, aceniad, bai, sylwadau, dadansoddwr=EBR)
			(b) data ychwanegol e.e. safle'r orrfwysfa, mynegrifau '
		Nodiadau:
			Mae'r mynegrifau yn cyfeirio at rhestr nodau y llinyn
	'''
	def __init__(self, llinyn, cynghanedd=None, aceniad=None, bai=None, sylwadau=None, data=dict()): 
		self.llinyn = llinyn
		self.cynghanedd = cynghanedd
		self.aceniad = aceniad
		self.bai = bai
		self.sylwadau = sylwadau
		self.data = data

	def __str__(self):
		# s = '-----\n'
		# s = '------------------------------\n'
		s = ''
		s += self.llinyn + '\n'
		if self.cynghanedd:
			s += 'CNG: ' + self.cynghanedd + '\n'
		# if self.aceniad:
		# 	s += 'ACE: ' + self.aceniad + '\n'
		# if self.bai:
		# 	s += 'BAI: ' + self.bai + '\n'
		# if self.sylwadau:
		# 	s += 'SYL: ' + self.sylwadau + '\n'
		if self.data:
			# for kk in self.data.iterkeys():
			# 	s += kk + '\t' + str(self.data[kk]) + '\n'
			s += self.llinyn_acenion() + '\n'
			s += self.llinyn + '\n'
			s += self.llinyn_gorffwysfa() + '\n'
			s += self.llinyn_sillau_colon() + '\n'
			if self.data.has_key('parau'):
				s += self.llinyn_cytseiniaid_cyfatebol() + '\n'
				s += self.llinyn_cytseiniaid_traws() + '\n'
			# s += self.llinyn_cytseiniaid_cynffon() + '\n'
			if self.data.has_key('odl'):
				s += self.llinyn_odl() + '\n'
			if self.data.has_key('sylwadau') and self.data['sylwadau']:
				s += str(self.data['sylwadau']) + '\n'
			s += '------------------------------'
			
		return s
	
	def llinyn_acenion(self):
		return ' '.join([ ac.llinyn_acenion(g) for g in self.llinyn.split(' ') ])


	# odl
	def llinyn_odl(self, html=False, blanksymbol=' '):
		nodau = ll.nodau(self.llinyn)
		ss = [' '*len(nodyn) for nodyn in nodau]
		if self.data.has_key('odl'):
			geiriau = self.llinyn.split(' ')
			for i,b in self.data['odl']:
				offset = 0
				for g in geiriau[:i]: 
					offset += len( ll.nodau(g) ) + 1
				for j in range(b[0],b[1]):
					ss[offset+j] = nodau[offset+j]
				if html:
					ss[offset+b[0]] = '<span class="odl">' + ss[ offset+b[0] ]
					ss[offset+b[1]-1] = ss[offset+b[1]-1] + '</span>'
		return ''.join(ss)
		
	def llinyn_gorffwysfa(self, html=False, blanksymbol=' '):
		nodau = ll.nodau(self.llinyn)
		ss = [' '*len(nodyn) for nodyn in nodau]
		if self.data.has_key('gorffwysfa'):
			geiriau = self.llinyn.split(' ')
			for i in self.data['gorffwysfa']:
				offset = 0
				for g in geiriau[:i+1]: 
					offset += len( ll.nodau(g) ) + 1
				idx = offset - 1
				if html:
					ss[idx] = '<span class="gorffwysfa">|</span>'
				else:
					ss[idx] = '|'
		return ''.join(ss)

	def llinyn_sillau_colon(self, html=False, blanksymbol=' '):
		nodau = ll.nodau(self.llinyn)
		ss = [' '*len(nodyn) for nodyn in nodau]
		# ss = list(blanksymbol*len(nodau))
		if self.data.has_key('gorffwysfa') and self.data.has_key('acenion'):
			acenion = self.data['acenion']
			geiriau = self.llinyn.split(' ')
			gorff = self.data['gorffwysfa'][-1]	# dewis yr ail orffwysfa yn y gynghanedd sain
			for i in [gorff, len(geiriau)-1]:
				offset = 0
				for g in geiriau[:i]: offset += len( ll.nodau(g) ) + 1
				ace = acenion[i][0]
				idx = offset + ace[-1]
				ss[idx] = ':'
				if len(ace) > 1:
					idx = offset + ace[-2]
					ss[idx] = ':'
		return ''.join(ss)

	def llinyn_cytseiniaid_cyfatebol(self, html=False, blanksymbol=' '):
		nodau = ll.nodau(self.llinyn)
		ss = [' '*len(nodyn) for nodyn in nodau]
		if self.data.has_key('parau'):
			for i,j in self.data['parau']:
				ss[i] = nodau[i]
				ss[j] = nodau[j]
		return ''.join(ss)

	def llinyn_cytseiniaid_traws(self, html=False, blanksymbol=' '):
		nodau = ll.nodau(self.llinyn)
		ss = [' '*len(nodyn) for nodyn in nodau]
		if self.data.has_key('pen_y'):
			mynegrifau = self.data['pen_y']
			for i in mynegrifau:
				ss[i] = nodau[i]
			# mi = min(mynegrifau)
			# mx = max(mynegrifau)
			# ss[mi-1] = '('
			# ss[mx+1] = ')'
		return ''.join(ss)

	def llinyn_cytseiniaid_cynffon(self, html=False, blanksymbol=' '):
		nodau = ll.nodau(self.llinyn)
		ss = [' '*len(nodyn) for nodyn in nodau]
		if self.data.has_key('cwt_x'):
			for i in self.data['cwt_x']: 
				# print 'cwt_x >> ' + str(i)
				ss[i] = nodau[i]
		if self.data.has_key('cwt_y'):
			for i in self.data['cwt_y']: 
				# print 'cwt_y >> ' + str(i)
				ss[i] = nodau[i]
		return ''.join(ss)

#------------------------------------------------
def main():
	print 'adroddiad.py'


if __name__ == '__main__': main()


		
