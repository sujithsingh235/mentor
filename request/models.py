from django.db import models
from user_signup.models import mentor_model

# Create your models here.
class mentee_request_model(models.Model):
    mentor = models.ForeignKey(mentor_model,on_delete=models.CASCADE)
    mentee_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    hours_per_day = models.IntegerField()
    no_of_days = models.IntegerField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20)
    request_posted_time = models.DateTimeField()
    