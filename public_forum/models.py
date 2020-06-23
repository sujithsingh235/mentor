from django.db import models

# Create your models here.
class question(models.Model):
    question = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
