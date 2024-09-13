from django.urls import path
from .views import predict_power_usage

urlpatterns = [
    path('predict/', predict_power_usage, name='predict_power_usage'),
]
