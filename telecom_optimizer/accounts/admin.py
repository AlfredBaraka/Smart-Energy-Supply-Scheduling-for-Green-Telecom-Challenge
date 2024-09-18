from django.contrib import admin

from .models import PredictedPowerUsage, ActualPowerUsage

admin.site.register([PredictedPowerUsage, ActualPowerUsage])
