from django.db import models
from django.utils import timezone


# Create your models here.


class locations_data(models.Model):
    id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=255, null=False)
    latitude = models.CharField(max_length=255, null=False)
    longitude = models.CharField(max_length=255, null=False)
    remarks = models.CharField(max_length=255, null=True)
    group = models.CharField(max_length=255, null=True)
    temp_location = models.CharField(max_length=255, default='False')
    Active = models.CharField(max_length=255, default='True')
    user_permission = models.CharField(max_length=255, default='all')
    time_stamp = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=255, default='')

    def __str__(self):
        return f"{self.location_name} | {self.temp_location}"


class checklist(models.Model):
    id = models.AutoField(primary_key=True)
    list_name = models.CharField(max_length=255, null=False)
    status  = models.CharField(max_length=255 , default = '1')
    item = models.CharField(max_length=255, null=False)
    time_stamp = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=255, default='')

    def __str__(self):
        return f"{self.list_name} | {self.item}"