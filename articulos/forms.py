from django import forms

class QuantityForm(forms.Form):
	cantidad = forms.IntegerField()