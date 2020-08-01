from django.db import models

# Create your models here.
class questions(models.Model): #questions in the public forum
    user = models.CharField(max_length=25)
    name = models.CharField(max_length=25)
    posted_time = models.DateTimeField()
    question = models.CharField(max_length=30)
    description = models.CharField(max_length=100,blank=True)
    report = models.IntegerField()

class answers(models.Model): #Answers for the questions in the public forum
    question_id = models.IntegerField()
    user = models.CharField(max_length=25)
    name = models.CharField(max_length=25)
    posted_time = models.DateTimeField()
    answer = models.TextField()
    like = models.IntegerField()
    report = models.IntegerField()

class comments(models.Model):  # Comments for the answers in the public forum
    answer_id = models.IntegerField()
    user = models.CharField(max_length=25)
    name = models.CharField(max_length=25)
    posted_time = models.DateTimeField()
    comment = models.CharField(max_length=100)

class like(models.Model): # To Generate the like status of particular user and count the number of likes for an answer
    user = models.CharField(max_length=25)
    answer_id = models.IntegerField()

class favourite(models.Model):
    user = models.CharField(max_length=25)
    question_id = models.IntegerField()

class report(models.Model):
    user = models.CharField(max_length=25)
    QorA = models.CharField(max_length=10)
    QorA_id = models.IntegerField()
 
class tag(models.Model):
    tag_name = models.CharField(max_length=20)

class tag_with_question_id(models.Model):
    question_id = models.IntegerField()
    tag = models.CharField(max_length=30)
