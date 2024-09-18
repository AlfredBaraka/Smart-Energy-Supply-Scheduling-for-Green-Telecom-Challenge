from django.urls import path
from .views import RegisterUserView, MainView, index, simulate_data, save_simulated_data, success_page

urlpatterns = [
    path('', index, name="intro" ),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('home', MainView.as_view(), name='home'),
    path('simulate/', simulate_data, name='simulate_data'),
    path('save_simulated_data/', save_simulated_data, name='save_simulated_data'),
    path('success/', success_page, name='success_page'),
]
