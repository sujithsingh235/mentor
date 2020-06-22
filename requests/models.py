from django.db import models

from user_signup.models import *
# Create your models here.

class requests_model(models.Model):
	mentee_id = models.ForeignKey(mentee_model,on_delete=models.CASCADE)
	mentor_id = models.ForeignKey(mentor_model,on_delete=models.CASCADE)
	choices = (('pending','pending'),('accepted','accepted'),('rejected','rejected'),('expired','expired'))
	status = models.CharField(max_length=30,choices=choices,default="pending")
	requ_date = models.DateTimeField(auto_now_add=True)
	repl_date = models.DateTimeField(auto_now=True)
	duration = models.IntegerField()
	pay = models.PositiveIntegerField()