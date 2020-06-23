from django.db import models

# Create your models here.
class questions(models.Model):
    user = models.CharField(max_length=25)
    posted_time = models.DateTimeField()
    question = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
