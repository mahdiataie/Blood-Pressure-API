from typing import Any
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class WithingsMeasureType(models.Model):
    measuretype = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'withings_measuretype'

    def __str__(self):
        return self.description


class WithingsMeasure(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    uuid = models.CharField(max_length=100)
    deviceID = models.CharField(max_length=100)
    measuretype_withings = models.ForeignKey(
        WithingsMeasureType, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)

    class Meta:
        db_table = 'withings_measures'

    def __str__(self):
        return self.id


class BloodPressureWarning(models.Model):
    WARNING_CHOICES = [
        ('YELLOW', 'Code Yellow'),
        ('RED', 'Code Red')
    ]
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    uuid = models.CharField(max_length=255)
    deviceID = models.CharField(max_length=255)
    measuretype_withings = models.IntegerField()
    value = models.FloatField()
    unit = models.IntegerField()
    warning_code = models.CharField(max_length=10, choices=WARNING_CHOICES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'bloodpressurewarning'

    def __str__(self):
        return f"{self.uuid} - {self.timestamp}"
