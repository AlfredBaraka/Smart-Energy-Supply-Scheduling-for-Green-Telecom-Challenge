from django.contrib import admin
from django import forms
from .models import PredictedPowerUsage, ActualPowerUsage

class ActualPowerUsageForm(forms.ModelForm):
    class Meta:
        model = ActualPowerUsage
        fields = ['user', 'timestamp', 'usage']

class PredictedPowerUsageForm(forms.ModelForm):
    class Meta:
        model = PredictedPowerUsage
        fields = ['user', 'timestamp', 'predicted_usage']

@admin.register(ActualPowerUsage)
class ActualPowerUsageAdmin(admin.ModelAdmin):
    form = ActualPowerUsageForm
    list_display = ('user', 'timestamp', 'usage')

@admin.register(PredictedPowerUsage)
class PredictedPowerUsageAdmin(admin.ModelAdmin):
    form = PredictedPowerUsageForm  # Corrected here
    list_display = ('user', 'timestamp', 'predicted_usage')
