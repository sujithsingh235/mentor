from django.db import models

# Create your models here.
class news_model(models.Model):
    title = models.CharField(max_length=100,blank=True)
    author = models.CharField(max_length=100,blank=True)
    url = models.URLField(blank=True)
    url_to_image = models.URLField(blank=True)
    content = models.TextField(blank=True)
    published_at = models.DateTimeField(blank=True)
    type = models.CharField(max_length=20,blank=True)