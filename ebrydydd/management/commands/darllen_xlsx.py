'''
darllen_cronfa_xml.py (ebrydydd/management)

xlrd: cell types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
'''

import os, time, xlrd

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from django.contrib.auth.models import User
from ebrydydd.models import Awdur, Llinell, Cwpled, ToddaidByr, Englyn, Dadansoddiad, Aelod

DATA_ROOT  = getattr(settings, 'DATA_ROOT')


class Command(BaseCommand):
	'''
	oes angen dilysu data fan hyn?
	e.e. beth am wirio os oes awdur yn barod wedi ei gynnwys yn y gronfa?
	Oes posib dileu dyblygau o'r gronfa, nes ymlaen?
	'''
	args = 'enw_gweithlyfr.xlsx'
	help = 'colofnau: llinell, awdur, cynghanedd, aceniad, bai, dadansoddwr, sylwadau'

	def handle(self, *args, **options):		

		wb_file = os.path.join(DATA_ROOT, 'ebrydydd_data.xlsx')

		# open workbook
		wb = xlrd.open_workbook(wb_file)
		print wb.sheet_names()

		# iteru dros y dalenau
		sheet_names = wb.sheet_names()
		for sheet_name in sheet_names:
			ws = wb.sheet_by_name(sheet_name)

			if sheet_name in ['llythrenwau', 'englynion']:
				continue

			# defnyddwyr
			if sheet_name in ['aelodau']:
				print '>>>>>>>>>> ' + sheet_name
				curr_row = 0	
				while curr_row < ws.nrows - 1:
					curr_row += 1
					if ws.cell_type(curr_row, 0) == 1:
						s = ws.cell_value(curr_row, 0)
						u = User( username=s, email=s )
						if ws.cell_type(curr_row, 1) == 1:
							u.first_name = ws.cell_value(curr_row, 1)
						if ws.cell_type(curr_row, 2) == 1:
							u.last_name = ws.cell_value(curr_row, 2)
						u.save()
						a = Aelod( user=u )
						if ws.cell_type(curr_row, 3) == 1:
							a.ffugenw = ws.cell_value(curr_row, 3)
						if ws.cell_type(curr_row, 4) == 1:
							a.statws = ws.cell_value(curr_row, 4)
						a.save()

			# cwpledi
			if sheet_name in ['cwpledi']:
				print '>>>>>>>>>> ' + sheet_name
				curr_row = 0	
				while curr_row < ws.nrows - 1:
					curr_row += 1	
					# llinellau
					if ws.cell_type(curr_row, 0) == 1:
						s = ws.cell_value(curr_row, 0).split('\n')
						if len(s) == 2:
							cyntaf = Llinell( llinyn=s[0] )
							ail = Llinell( llinyn=s[1] ) 
							cyntaf.save()
							ail.save()
							c = Cwpled( cyntaf=cyntaf, ail=ail )
							# awdur
							if ws.cell_type(curr_row, 1) == 1:
								a = Awdur( enw = ws.cell_value(curr_row, 1) )
								a.save()
								c.awdur = a
							c.save()

			# llinellau
			if sheet_name in ['croes', 'traws', 'llusg', 'sain']:
				print '>>>>>>>>>> ' + sheet_name
				curr_row = 0	
				while curr_row < ws.nrows - 1:
					curr_row += 1
					# llinell (llinyn,	awdur)
					if ws.cell_type(curr_row, 0) == 1:
						s = ws.cell_value(curr_row, 0)
						ll = Llinell( llinyn=s )
						# awdur
						if ws.cell_type(curr_row, 1) == 1:
							a = Awdur( enw	= ws.cell_value(curr_row, 1) )
							a.save()
							ll.awdur = a
						ll.save()
						# dadansoddiad (llinell, cynghanedd, aceniad, bai, dadansoddwr, sylwadau)
						if ws.cell_type(curr_row, 2) == 1:
							dad = Dadansoddiad( llinell=ll )
							dad.cynghanedd = ws.cell_value(curr_row, 2)
							if ws.cell_type(curr_row, 3) == 1:
								dad.aceniad = ws.cell_value(curr_row, 3)
							if ws.cell_type(curr_row, 4) == 1:
								dad.bai = ws.cell_value(curr_row, 4)				
							if ws.cell_type(curr_row, 5) == 1:
								dad.dadansoddwr = ws.cell_value(curr_row, 5)				
							if ws.cell_type(curr_row, 6) == 1:
								dad.sylwadau = ws.cell_value(curr_row, 6)
							dad.save()
				
