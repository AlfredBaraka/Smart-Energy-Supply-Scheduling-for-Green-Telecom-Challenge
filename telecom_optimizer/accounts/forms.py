from django import forms
from django.contrib.auth.models import User

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Password confirmation")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
            'password_confirmation': forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter email'})
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', "Passwords do not match.")





from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser  

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')



from django import forms

class SimulationForm(forms.Form):
    min_value = forms.FloatField(label='Min Value', min_value=0)
    max_value = forms.FloatField(label='Max Value', min_value=0)
    simulate_hours = forms.IntegerField(label='Hours to Simulate', min_value=1, max_value=24)
