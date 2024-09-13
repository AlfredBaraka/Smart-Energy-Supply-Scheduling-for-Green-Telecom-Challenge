from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import requests
import os

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        # Print current working directory for debugging
        print("Current working directory:", os.getcwd())
        
        # Create a layout to hold both the form and the image
        layout = FloatLayout()
        
        # Add the image
        try:
            image = Image(source='tower.jpg')  # Update to a valid local image path
            print("Image loaded successfully.")
        except Exception as e:
            print(f"Error loading image: {e}")
        
        image.size_hint = (0.5, 1)  # Set the image to take up half the width
        image.pos_hint = {'x': 0, 'y': 0}  # Position it on the left side
        layout.add_widget(image)
        
        # Create the form layout
        form_layout = BoxLayout(
            orientation='vertical', 
            size_hint=(0.375, None),  # Set to 75% of the default width
            pos_hint={'x': 0.625, 'y': 0.5},  # Centered vertically, on the right side
            padding=20,
            spacing=10
        )
        
        # Create and style text inputs
        self.email_input = TextInput(
            hint_text='Email', 
            multiline=False, 
            size_hint_y=None, 
            height=50,
            padding=[10, 10],
            background_normal='',
            background_color=(1, 1, 1, 1),  # White background
            foreground_color=(0, 0, 0, 1),  # Black text
            hint_text_color=(0.7, 0.7, 0.7, 1)  # Light gray placeholder
        )
        
        self.password_input = TextInput(
            hint_text='Password', 
            password=True, 
            multiline=False, 
            size_hint_y=None, 
            height=50,
            padding=[10, 10],
            background_normal='',
            background_color=(1, 1, 1, 1),  # White background
            foreground_color=(0, 0, 0, 1),  # Black text
            hint_text_color=(0.7, 0.7, 0.7, 1)  # Light gray placeholder
        )
        
        login_button = Button(
            text='Login',
            size_hint_y=None,
            height=50,
            background_color=(0.0, 0.7, 0.9, 1),  # Bright blue background
            color=(1, 1, 1, 1)  # White text
        )
        login_button.size_hint_x = 0.75  # Set width to 75% of default width
        login_button.bind(on_press=self.login)
        
        # Add widgets to the form layout
        form_layout.add_widget(self.email_input)
        form_layout.add_widget(self.password_input)
        form_layout.add_widget(login_button)
        
        # Add the form layout to the main layout
        layout.add_widget(form_layout)
        
        self.add_widget(layout)
    
    def login(self, instance):
        # Retrieve the text inputs correctly
        email = self.email_input.text
        password = self.password_input.text
        response = requests.post(
            'http://localhost:8000/api/login/', 
            data={'email': email, 'password': password}
        )
        if response.status_code == 200:
            data = response.json()
            refresh_token = data.get('refresh')
            access_token = data.get('access')
            if access_token:
                with open('token.txt', 'w') as f:
                    f.write(access_token)
                print('Login successful')
                self.manager.current = 'home'  # Switch to home screen
            else:
                print('Access token not received in response')
                self.show_login_failed_popup()
        else:
            self.show_login_failed_popup()

    def show_login_failed_popup(self):
        popup = Popup(
            title='Login Failed',
            content=Label(text='Invalid email or password. Please try again.'),
            size_hint=(0.6, 0.3),
            auto_dismiss=True
        )
        popup.open()
