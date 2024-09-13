from django.db import models

from django.db import models

class PowerUsageData(models.Model):
    timestamp = models.DateTimeField()
    power_usage = models.FloatField()

class PredictionResult(models.Model):
    timestamp = models.DateTimeField()
    predicted_usage = models.CharField(max_length = 100)
