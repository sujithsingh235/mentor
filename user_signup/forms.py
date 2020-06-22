from django import forms
from django.db.models import Q
from .models import *

class mentee_signup_form(forms.ModelForm):
	confirm_password = forms.CharField()
	class Meta:
		model = mentee_model
		fields = ['name','email','dob','gender','mobile','username','password','confirm_password','field','sub_field',
		'startup','company_name','company_description']

	def __init__(self,*args,**kwargs):
		super().__init__(*args, **kwargs)
		self.fields['sub_field'].queryset = sub_field.objects.none()

		if 'field' in self.data:
	 		try:
	 			print('came here')
	 			field_id = int(self.data.get('field'))
	 			self.fields['sub_field'].queryset = sub_field.objects.filter(field_id=field_id).order_by('sub_field_name')
	 		except (ValueError, TypeError):
		 		pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			print('else block')
			self.fields['sub_field'].queryset = self.instance.field.sub_field_set.order_by('name')

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if mentee_model.objects.filter(email=email,verified=True):
			raise forms.ValidationError("Email already exists")
		return email

	def clean_mobile(self,*args,**kwargs):
		mobile = self.cleaned_data.get('mobile')
		if not (mobile>=1000000000 and mobile<=9999999999):
			raise forms.ValidationError("This is not a valid mobile number")
		if mentee_model.objects.filter(mobile=mobile, mobile_verified=True):
			raise forms.ValidationError("User Already Exist")
		return mobile

	def clean_username(self,*args,**kwargs):
		username = self.cleaned_data.get('username')
		if mentee_model.objects.filter(username=username).exists():
			raise forms.ValidationError("Username Already Taken! Try Something else.")
		if '@' in username:
			raise forms.ValidationError('Sorry! Username should not have @ in it')
		return username

	def clean_confirm_password(self,*args,**kwargs):
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if not password == confirm_password:
			raise forms.ValidationError('Password did not match')

	def clean_company_name(self,*args,**kwargs):
		is_startup = self.cleaned_data.get('startup')
		company_name = self.cleaned_data.get('company_name')
		if is_startup:
			if not company_name:
				raise forms.ValidationError('This Field is required')
		return company_name

	def clean_company_description(self,*args,**kwargs):
		is_startup = self.cleaned_data.get('startup')
		company_description = self.cleaned_data.get('company_description')
		if is_startup:
			if not company_description:
				raise forms.ValidationError('This Field is required')
		return company_description


#email verify form : 
class email_verify_form(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'readonly':True}))
	otp = forms.IntegerField()
	role = forms.CharField(widget=forms.HiddenInput())

# All users login form :
class login_form(forms.Form):
	CHOICES = (('mentee','Mentee'),('mentor','Mentor'),('others','others'))
	role = forms.ChoiceField(choices=CHOICES)
	username = forms.CharField()
	password = forms.CharField()

	def clean_username(self,*args,**kwargs):
		username = self.cleaned_data.get('username')
		role = self.cleaned_data.get('role')
		if role=='mentee':
			if not mentee_model.objects.filter(Q(username=username)|Q(email=username)).exists():
				raise forms.ValidationError('User Does Not Exist')
		if role=='mentor':
			if not mentor_model.objects.filter(Q(username=username)|Q(email=username)).exists():
				raise forms.ValidationError('User Does Not Exist')
		if role=='others':
			pass
		return username

# NEEDS TO BE UPDATED
class mentor_signup_form(forms.ModelForm):
	confirm_password = forms.CharField()

	class Meta:
		model = mentor_model
		fields = ['name','email','dob','gender','mobile','username','password','confirm_password','field','sub_field',
		'occupation','company_name','pay_per_month']

	def __init__(self,*args,**kwargs):
		super().__init__(*args, **kwargs)
		self.fields['sub_field'].queryset = sub_field.objects.none()

		if 'field' in self.data:
	 		try:
	 			print('came here')
	 			field_id = int(self.data.get('field'))
	 			self.fields['sub_field'].queryset = sub_field.objects.filter(field_id=field_id).order_by('sub_field_name')
	 		except (ValueError, TypeError):
		 		pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			print('else block')
			self.fields['sub_field'].queryset = self.instance.field.sub_field_set.order_by('name')

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if mentor_model.objects.filter(email=email,verified=True):
			raise forms.ValidationError("User already exists")
		return email

	def clean_mobile(self,*args,**kwargs):
		mobile = self.cleaned_data.get('mobile')
		if not (mobile>=1000000000 and mobile<=9999999999):
			raise forms.ValidationError("This is not a valid mobile number")
		if mentor_model.objects.filter(mobile=mobile, mobile_verified=True):
			raise forms.ValidationError("mobile Already Exist")
		return mobile

	def clean_username(self,*args,**kwargs):
		username = self.cleaned_data.get('username')
		if mentor_model.objects.filter(username=username).exists():
			raise forms.ValidationError("Username Already Taken! Try Something else.")
		if '@' in username:
			raise forms.ValidationError('Sorry! Username should not have @ in it')
		return username

	def clean_confirm_password(self,*args,**kwargs):
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if not password == confirm_password:
			raise forms.ValidationError('Password did not match')