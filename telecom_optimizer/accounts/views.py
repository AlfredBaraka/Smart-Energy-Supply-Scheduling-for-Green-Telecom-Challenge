from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from .models import CustomUser, ActualPowerUsage, PredictedPowerUsage
from .forms import CustomUserCreationForm, LoginForm
from .predictor import TimeSequenceModel
import numpy as np
from django.utils import timezone
from django.db.models import Q
import numpy as np
from datetime import timedelta

def index(request):
    return render(request, 'intro.html')


class RegisterUserView(View):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
        return render(request, 'register.html', {'form': form})
    
    

class LoginUserView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('user-detail')
            else:
                form.add_error(None, 'Invalid credentials')
        return render(request, 'login.html', {'form': form})







class MainView(View):
    def get(self, request, *args, **kwargs):
        user = request.user

        current_time = timezone.now().replace(minute=0, second=0, microsecond=0)

    
        actual_usage = 4.29  

        
        actual_entry, created = ActualPowerUsage.objects.update_or_create(
            user=user,
            timestamp=current_time, 
            defaults={'usage': actual_usage}
        )


        past_18_hours = ActualPowerUsage.objects.filter(
            user=user,
            timestamp__gte=current_time - timedelta(hours=17),
            timestamp__lte=current_time
        ).order_by('timestamp')

        model_path = '/home/egovridc/Desktop/Smart-Energy-Supply-Scheduling-for-Green-Telecom-Challenge/data/energy_lstm_model_better2.pth'
        model = TimeSequenceModel(model_path)


        past_data = np.array([entry.usage for entry in past_18_hours])


        predicted_usage = np.array(model.predict(6, past_data))  

        for i, predicted_value in enumerate(predicted_usage):
            future_timestamp = current_time + timedelta(hours=(i + 1))
            PredictedPowerUsage.objects.update_or_create(
                user=user,
                timestamp=future_timestamp,
                defaults={'predicted_usage': predicted_value}
            )

        combined_data = np.concatenate((past_data, predicted_usage))

     
        context = {
            'user': user,
            'past_data': past_data.tolist(), 
            'predicted_usage': predicted_usage.tolist(), 
            'combined_data': combined_data.tolist(), 
        }

        return render(request, 'main.html', context)


