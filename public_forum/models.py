from django.db import models

# Create your models here.
class questions(models.Model): #questions in the public forum
    user = models.CharField(max_length=25)
    posted_time = models.DateTimeField()
    question = models.CharField(max_length=30)
    description = models.CharField(max_length=100)

class answers(models.Model): #Answers for the questions in the public forum
    question_id = models.IntegerField()
    user = models.CharField(max_length=25)
    posted_time = models.DateTimeField()
    answer = models.CharField(max_length=100)

class comments(models.Model):  # Comments for the answers in the public forum
    answer_id = models.IntegerField()
    user = models.CharField(max_length=25)
    posted_time = models.DateTimeField()
    comment = models.CharField(max_length=100)
