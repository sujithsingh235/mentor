from django.db import models

# Create your models here.
class scheme(models.Model):
    head = models.TextField()
    Launched_in = models.CharField(max_length=50)
    Headed_by = models.TextField()
    Industry_applicable = models.TextField()
    Eligible_for = models.TextField()
    Overview = models.TextField()
    Fiscal_incentives = models.TextField()
    Time_period = models.TextField()
    more_info_link = models.URLField(blank=True)