import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.garden.graph import Graph, LinePlot
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        
        # Set minimum window size
        Window.size = (800, 600) 
        Window.minimum_width = 1400  
        Window.minimum_height = 980

        # Main layout using FloatLayout
        main_layout = FloatLayout()

        # Set background color
        with main_layout.canvas.before:
            Color(0.7, 0.9, 1, 1)  # Light Blue
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)

        main_layout.bind(size=self._update_rect, pos=self._update_rect)

        # Header
        # Header
        self.header_label = Label(
            text='TELECOM ENERGY OPTIMIZER',
            font_size='24sp',
            bold=True,
            color=(0, 0, 0, 1),  # Black color for text
            size_hint_y=None,
            height=50,
            pos_hint={'center_x': 0.5, 'top': 1}
        )
        main_layout.add_widget(self.header_label)


        # Top bar with username and email
        top_bar = GridLayout(cols=2, size_hint_y=None, height=50, spacing=10,
                             pos_hint={'x': 0, 'top': 0.95})
        self.username_label = Label(text='Username: ', font_size='18sp', color=(0, 0, 0, 1), halign='left', size_hint_x=None, width=250)
        self.email_label = Label(text='Email: ', font_size='18sp', color=(0, 0, 0, 1), halign='left', size_hint_x=None, width=250)
        
        top_bar.add_widget(self.username_label)
        top_bar.add_widget(self.email_label)

        # Buttons linking to different statuses
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10,
                                  pos_hint={'x': 0, 'top': 0.9})
        battery_button = Button(text='Battery Status', font_size='18sp', size_hint=(0.3, 1),
                                background_color=(0.1, 0.6, 0.3, 1))  # Bright green
        battery_button.bind(on_press=self.goto_battery_status)
        generator_button = Button(text='Generator Status', font_size='18sp', size_hint=(0.3, 1),
                                  background_color=(0.1, 0.6, 0.9, 1))  # Bright blue
        generator_button.bind(on_press=self.goto_generator_status)
        outage_button = Button(text='National Grid Outage Plan', font_size='18sp', size_hint=(0.4, 1),
                               background_color=(0.9, 0.6, 0.1, 1))  # Bright yellow
        outage_button.bind(on_press=self.goto_outage_plan)

        button_layout.add_widget(battery_button)
        button_layout.add_widget(generator_button)
        button_layout.add_widget(outage_button)

        # Add stylish "PREDICTION: USE BATTERY" BoxLayout
        prediction_box = BoxLayout(size_hint_y=None, height=50, padding=10, pos_hint={'x': 0, 'top': 0.85})
        prediction_label = Label(text='[b][i]PREDICTION: USE BATTERY[/i][/b]', font_size='20sp', markup=True,
                                 color=(0.2, 0.2, 0.6, 1), bold=True)
        prediction_box.add_widget(prediction_label)

        # Placeholder for the graph
        self.power_graph = Graph(
            xlabel='Time (hrs)',
            ylabel='Power (kW)',
            x_ticks_minor=1,
            x_ticks_major=1,
            y_ticks_minor=5,
            y_ticks_major=1,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            x_grid=True,
            y_grid=True,
            xmin=0,
            xmax=20,
            ymin=0,
            ymax=10,
            size_hint=(0.5, 0.5),
            pos_hint={'x': 0, 'y': 0},
            label_options={'color': [0, 0, 0, 1], 'bold': True}  # Black labels for numbers
        )
        # Create LinePlot instances for past data and predicted data
        self.past_plot = LinePlot(line_width=2, color=[0.2, 0.8, 0.2, 1])  # Light Green for past data
        self.predicted_plot = LinePlot(line_width=2, color=[1, 0.6, 0, 1])  # Dark Orange for predicted data

        self.power_graph.add_plot(self.past_plot)
        self.power_graph.add_plot(self.predicted_plot)

        # Add widgets to the main layout
        main_layout.add_widget(top_bar)
        main_layout.add_widget(button_layout)
        main_layout.add_widget(prediction_box)  # Add prediction box
        main_layout.add_widget(self.power_graph)

        self.add_widget(main_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_enter(self, *args):
        # Load user data and update the graph when the screen is entered
        self.load_user_data()
        self.update_graph()

    def load_user_data(self):
        try:
            # Retrieve the JWT token from file
            with open('token.txt', 'r') as f:
                token = f.read().strip()

            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get('http://localhost:8000/api/user/', headers=headers)

            if response.status_code == 200:
                user_data = response.json()
                # Update UI elements with user_data
                self.username_label.text = f'Username: {user_data.get("username", "N/A")}'
                self.email_label.text = f'Email: {user_data.get("email", "N/A")}'
            else:
                self.show_error_popup(f'Failed to load user data. Status code: {response.status_code}')
        except requests.RequestException as e:
            self.show_error_popup(f'An error occurred: {e}')

    def update_graph(self):
        try:
            response = requests.get('http://localhost:8000/api/data/power')
            if response.status_code == 200:
                data = response.json()
                past_data = data.get('past_data', [])
                predicted_usage = data.get('predicted_usage', [])

                # Combine past_data and predicted_usage
                x_past = list(range(len(past_data)))  # X-axis values for past data
                x_predicted = list(range(len(past_data), len(past_data) + len(predicted_usage)))  # X-axis values for predicted data

                # Update the graph data
                self.past_plot.points = [(x, y) for x, y in zip(x_past, past_data)]
                self.predicted_plot.points = [(x, y) for x, y in zip(x_predicted, predicted_usage)]

            else:
                self.show_error_popup(f'Failed to load power data. Status code: {response.status_code}')
        except requests.RequestException as e:
            self.show_error_popup(f'An error occurred: {e}')

    def show_error_popup(self, message):
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(0.6, 0.3),
            auto_dismiss=True
        )
        popup.open()

    def goto_battery_status(self, instance):
        # Navigate to the Battery Status screen
        self.manager.current = 'battery_status'

    def goto_generator_status(self, instance):
        # Navigate to the Generator Status screen
        self.manager.current = 'generator_status'

    def goto_outage_plan(self, instance):
        # Navigate to the National Grid Outage Plan screen
        self.manager.current = 'outage_plan'
