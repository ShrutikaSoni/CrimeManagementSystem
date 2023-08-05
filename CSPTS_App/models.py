from django.db import models
from datetime import datetime

class Crime_Reports(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    location = models.CharField(max_length=100)
    mobile = models.IntegerField()
    victim = models.CharField(max_length=100)
    crime_date = models.CharField(max_length=30)
    report_date = models.CharField(max_length=100,default=datetime.now())
    status = models.CharField(max_length=20, default="blue")


class Fir(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)  
    location = models.CharField(max_length=100)
    mobile = models.IntegerField()
    image = models.ImageField(upload_to="FIR_Files")
    upload_date = models.CharField(max_length=100,default=datetime.now())

