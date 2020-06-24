from django import forms

class answers_form(forms.Form):
    ans = forms.CharField(label="Enter your answer:" ,widget = forms.Textarea())