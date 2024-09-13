from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .predictor import TimeSequenceModel
class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
import requests
import numpy as np
from django.contrib.auth import authenticate



class LoginUserView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'username': user.username,
            'email': user.email
        }
        return Response(data)


    
def predict_power_usage(request):
    # Load the model
    model_path = r'/home/egovridc/Desktop/Smart-Energy-Supply-Scheduling-for-Green-Telecom-Challenge/data/energy_lstm_model_better2.pth'
    model = TimeSequenceModel(model_path)

    # Example input sequence
    past_data = np.array([8.36, 6.56, 4.19, 3.98, 7.97, 8.21, 8.49, 8.51, 8.50, 8.77, 8.81, 8.67, 8.86, 8.90, 8.91], dtype=np.float32)

    # Make a prediction
    predicted_usage = model.predict(3, past_data)

    # Prepare the payload with both past_data and predicted_usage
    payload = {
        'past_data': past_data.tolist(),  # Convert numpy array to list
        'predicted_usage': predicted_usage
    }

    api_endpoint = 'http://localhost:8000/api/data/power'  
    try:
        response = requests.post(api_endpoint, json=payload)
        # Print response details for debugging
        print('API Response Status Code:', response.status_code)
        print('API Response Content:', response.text)  # Print raw response text

        # Attempt to decode the response JSON
        try:
            api_response_json = response.json()
        except ValueError as e:
            # Handle JSON decoding error
            print('JSON Decode Error:', e)
            api_response_json = {'error': 'Failed to decode JSON response'}

    except requests.RequestException as e:
        # Handle request exception
        print('Request Error:', e)
        api_response_json = {'error': 'Failed to make API request'}

    # Return JSON response
    return JsonResponse({
        'predicted_usage': predicted_usage,
        'past_data': past_data.tolist()
    })