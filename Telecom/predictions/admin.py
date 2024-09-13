from django.contrib import admin

from .models import PowerUsageData, PredictionResult

admin.site.register([PowerUsageData, PredictionResult])
