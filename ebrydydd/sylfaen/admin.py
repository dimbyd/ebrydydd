from django.contrib import admin
from ebrydydd.sylfaen.models import Cynghanedd, Llinell, Dadansoddiad

class CynghaneddAdmin(admin.ModelAdmin):
	list_display = ('enw', 'dosbarth')
	ordering = ('enw', 'dosbarth')

class LlinellAdmin(admin.ModelAdmin):
	list_display = ('llinyn', 'awdur')
	ordering = ('llinyn',)

class DadansoddiadAdmin(admin.ModelAdmin):
	list_display = ('llinell', 'cynghanedd', 'dadansoddwr')
	ordering = ('llinell',)

admin.site.register(Cynghanedd, CynghaneddAdmin)
admin.site.register(Llinell, LlinellAdmin)
admin.site.register(Dadansoddiad, DadansoddiadAdmin)

