from django import forms
from .models import *

class request_form(forms.ModelForm):
	class Meta:
		model = requests_model
		fields = ['mentor_id','duration']
		widgets = {
			'mentor_id' : forms.HiddenInput(),
		}