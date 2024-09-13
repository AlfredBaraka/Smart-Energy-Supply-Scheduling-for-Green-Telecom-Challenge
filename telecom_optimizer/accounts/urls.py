from django.urls import path
from .views import RegisterUserView, LoginUserView, UserDetailView, predict_power_usage

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('data/power', predict_power_usage, name='data')
]
