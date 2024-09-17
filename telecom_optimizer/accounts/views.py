from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from .models import CustomUser
from .forms import CustomUserCreationForm, LoginForm
from .predictor import TimeSequenceModel
import numpy as np

def index(request):
    return render(request, 'intro.html')

# Register User View
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
            return redirect('home')  # Redirect to a success page or home
        return render(request, 'register.html', {'form': form})
    
    
# Login User View
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
        # Fetch user details
        user = request.user

        # Simulate 24 hours of data from 5 to 7
        simulated_data = np.linspace(4, 6, 24)

        # Initialize the model
        model_path = '/home/egovridc/Desktop/Smart-Energy-Supply-Scheduling-for-Green-Telecom-Challenge/data/energy_lstm_model_better2.pth'
        model = TimeSequenceModel(model_path)

        # Predict the next 6 hours using the last 18 hours of simulated data
        past_data = [3.975, 3.975, 3.97, 3.99, 3.97, 3.98, 4, 4.16, 4.19, 4.2, 4.22, 4.2, 4.19, 4.2, 4.2, 4.19, 4.19, 4.19, 4.07]
        predicted_usage = model.predict(6, past_data)

        # Ensure predicted_usage is a NumPy array
        if isinstance(predicted_usage, list):
            predicted_usage = np.array(predicted_usage)

        # Combine the last 18 hours of actual data with the 6 hours of predicted data
        combined_data = np.concatenate((past_data, predicted_usage))

        # Prepare context for the template
        context = {
            'user': user,
            'past_data': past_data.tolist(),
            'predicted_usage': predicted_usage.tolist(),
            'combined_data': combined_data.tolist()  # Convert combined_data to list
        }

        return render(request, 'main.html', context)