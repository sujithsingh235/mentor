from django.db import models

# Homepage Models
# Create your models here.

class req(models.Model):
	req_id = models.AutoField(primary_key=True)
	mentor_id = models.IntegerField()
	mentee_id = models.IntegerField()
	req_date = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=25,default='pending')