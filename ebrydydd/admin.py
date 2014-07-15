'''
admin.py (sylfaen app)
'''
from django.contrib import admin
from ebrydydd.models import Llinell, Dadansoddiad, Aelod

class LlinellAdmin(admin.ModelAdmin):
	list_display = ('llinyn', 'awdur')
	ordering = ('llinyn',)

class DadansoddiadAdmin(admin.ModelAdmin):
	list_display = ('llinell','cynghanedd', 'aceniad', 'bai', 'dadansoddwr', 'sylwadau',)
	ordering = ('llinell', 'dadansoddwr',)
	
admin.site.register(Llinell, LlinellAdmin)
admin.site.register(Dadansoddiad, DadansoddiadAdmin)
admin.site.register(Aelod)

