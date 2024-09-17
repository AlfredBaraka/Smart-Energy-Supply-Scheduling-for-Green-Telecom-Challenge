from django.urls import path
from .views import RegisterUserView, MainView, index

urlpatterns = [
    path('', index, name="intro" ),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('home', MainView.as_view(), name='home'),
]
