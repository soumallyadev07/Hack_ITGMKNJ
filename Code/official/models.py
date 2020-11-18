from django.db import models

class Personality(models.Model):
    country     = models.CharField(max_length=100)
    title       = models.CharField(max_length=50,null=True)
    full_name   = models.CharField(max_length=150)
    first_name  = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True)
    last_name   = models.CharField(max_length=100, null=True)
    contact     = models.TextField(null=True)
    gender      = models.CharField(max_length=10, null=True)
    designation = models.CharField(max_length=200, null=True)
    images      = models.TextField(null=True)
    last_updated= models.CharField(max_length=30)
