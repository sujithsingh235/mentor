from django import forms

class question_form(forms.Form):
	question = forms.CharField()
	CHOICES = ((1,'a'),(2,'b'),(3,'a'))
	unnknown = forms.MultipleChoiceField(choices=CHOICES)