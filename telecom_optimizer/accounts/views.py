from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.utils import timezone
from datetime import timedelta, datetime
from .models import CustomUser, ActualPowerUsage, PredictedPowerUsage
from .forms import CustomUserCreationForm, LoginForm, SimulationForm
from .predictor import TimeSequenceModel
import numpy as np
import json
import random


def success_page(request):
    return render(request, 'success.html')


def index(request):
    return render(request, 'intro.html')


class RegisterUserView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
        return render(request, 'register.html', {'form': form})


class LoginUserView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('user-detail')
            form.add_error(None, 'Invalid credentials')
        return render(request, 'login.html', {'form': form})


class MainView(View):
    def get(self, request):
        user = request.user
        current_time = timezone.now().replace(minute=0, second=0, microsecond=0)

        # Fetch the past 18 hours of actual power usage
        past_18_hours = ActualPowerUsage.objects.filter(
            user=user,
            timestamp__range=(current_time - timedelta(hours=17), current_time)
        ).order_by('timestamp')

        if not past_18_hours:
            return render(request, 'main.html', {'message': 'No data available for the past 18 hours.'})

        if len(past_18_hours) < 10:
            return render(request, 'main.html', {'message': 'Not enough data for prediction. At least 10 hours of data is required.'})

        # Load and use the prediction model
        model_path = '/home/egovridc/Desktop/Smart-Energy-Supply-Scheduling-for-Green-Telecom-Challenge/data/energy_lstm_model_better2.pth'
        model = TimeSequenceModel(model_path)

        past_data = np.array([entry.usage for entry in past_18_hours])
        predicted_usage = np.array(model.predict(6, past_data))

        # Save predicted data
        for i, predicted_value in enumerate(predicted_usage):
            future_timestamp = current_time + timedelta(hours=(i + 1))
            PredictedPowerUsage.objects.update_or_create(
                user=user,
                timestamp=future_timestamp,
                defaults={'predicted_usage': predicted_value}
            )

        # Combine actual and predicted data
        combined_data = np.concatenate((past_data, predicted_usage))

        # Prepare timestamps for combined data
        timestamps = [entry.timestamp for entry in past_18_hours]
        timestamps += [current_time + timedelta(hours=(i + 1)) for i in range(len(predicted_usage))]

        context = {
            'user': user,
            'timestamps': [ts.isoformat() for ts in timestamps],  # Convert to ISO 8601 format
            'combined_data': combined_data.tolist(),
        }

        return render(request, 'main.html', context)


def simulate_data(request):
    if request.method == 'POST':
        form = SimulationForm(request.POST)
        if form.is_valid():
            min_value = form.cleaned_data['min_value']
            max_value = form.cleaned_data['max_value']
            simulate_hours = form.cleaned_data['simulate_hours']
            now = timezone.now()

            simulated_data = [
                (
                    now - timedelta(hours=(simulate_hours - i)).replace(minute=0, second=0, microsecond=0),
                    random.uniform(min_value, max_value)
                ) for i in range(simulate_hours)
            ]

            return render(request, 'review_simulation.html', {'simulated_data': simulated_data})

    else:
        form = SimulationForm()

    return render(request, 'simulate_data.html', {'form': form})


def save_simulated_data(request):
    if request.method == 'POST':
        simulated_data = request.POST.get('simulated_data')

        if simulated_data:
            simulated_data = json.loads(simulated_data)
            for entry in simulated_data:
                timestamp_str = entry['timestamp']
                usage = entry['usage']
                timestamp = timezone.make_aware(datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S'))
                ActualPowerUsage.objects.create(user=request.user, timestamp=timestamp, usage=usage)

        return redirect('success_page')

    return redirect('simulate_data')
