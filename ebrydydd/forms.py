'''
ebrydydd: forms.py
'''

from django import forms
from django.contrib.auth.models import User

from ebrydydd.models import Llinell, Dadansoddiad, Aelod
from ebrydydd.peiriant import Adroddiad

# # llinell law
# class LlinellNewyddForm(forms.Form):
# 	llinyn = forms.CharField( widget=forms.TextInput( attrs={'size': '100'} ), required=False )
# 
# # llinell ddewis
# class LlinellCronfaForm(forms.Form):
# 	llinell = forms.ModelChoiceField(
# 		queryset = Llinell.objects.all().order_by('llinyn'),
# 		initial = '1',
# 	)

# llinell
class LlinellForm(forms.Form):
	llinyn = forms.CharField( widget=forms.TextInput( attrs={'size': '100'} ), required=False )
	llinell_ddewis = forms.ModelChoiceField(
		queryset = Llinell.objects.all().order_by('llinyn'),
		initial = '1',
	)

# cwis
class DadansoddiadForm(forms.ModelForm):
	class Meta:
		model = Dadansoddiad
		fields = ['llinell', 'cynghanedd', 'aceniad', 'bai', 'sylwadau', 'dadansoddwr']

# defnyddiwr
class UserForm(forms.ModelForm):
	password = forms.CharField( widget=forms.PasswordInput() )
	class Meta:
		model = User
		fields = ('username', 'email', 'password')

# aelod
class AelodForm(forms.ModelForm):
	class Meta:
		model = Aelod
		fields = ( 'user', 'ffugenw', 'statws', )

