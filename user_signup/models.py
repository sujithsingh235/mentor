from django.db import models
from django import forms
# Create your models here.

class field(models.Model):
	field_name = models.CharField(max_length=50)
	def __str__(self):
		return self.field_name

class sub_field(models.Model):
	field = models.ForeignKey(field,on_delete=models.CASCADE)
	sub_field_name = models.CharField(max_length=50)
	def __str__(self):
		return self.sub_field_name

class mentee_model(models.Model):
	username = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=254)
	mobile = models.BigIntegerField()
	password = models.CharField(max_length=150)
	dob = models.DateField()
	choices = (('male','Male'),('female','Female'))
	gender = models.CharField(max_length=25,choices=choices)
	field = models.ForeignKey(field,on_delete=models.SET_NULL,null=True)
	sub_field = models.ForeignKey(sub_field,on_delete=models.SET_NULL,null=True)
	startup = models.BooleanField(default=False)
	company_name = models.CharField(max_length=100,blank=True)
	company_description = models.CharField(max_length=250,blank=True)
	otp = models.IntegerField()
	verified = models.BooleanField(default=False)
	mobile_verified = models.BooleanField(default=False)


class mentor_model(models.Model):
	username = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=254)
	mobile = models.BigIntegerField()
	password = models.CharField(max_length=150)
	dob = models.DateField()
	choices = (('male','Male'),('female','Female'))
	gender = models.CharField(max_length=25,choices=choices)
	field = models.ForeignKey(field,on_delete=models.SET_DEFAULT,default="others")
	sub_field = models.ForeignKey(sub_field,on_delete=models.SET_DEFAULT,default="others")
	occupation = models.CharField(max_length=50)
	company_name = models.CharField(max_length=100)
	pay_per_month = models.PositiveIntegerField(default=1000)
	otp = models.IntegerField()
	verified = models.BooleanField(default=False)
	mobile_verified = models.BooleanField(default=False)

