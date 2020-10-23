from django.db import models


# Create your models here.
class Shortcuts(models.Model):
    n_star = models.IntegerField(blank=True, null=True)
    short = models.CharField(max_length=400, blank=True, null=True)
    sentiment = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shortcuts'