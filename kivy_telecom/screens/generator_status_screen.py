from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class GeneratorStatusScreen(Screen):
    def __init__(self, **kwargs):
        super(GeneratorStatusScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Generator Status Page", font_size='20sp'))

        # Home Button
        home_button = Button(text="Home", size_hint=(None, None), size=(100, 50))
        home_button.bind(on_release=self.go_home)
        layout.add_widget(home_button)

        self.add_widget(layout)

    def go_home(self, instance):
        self.manager.current = 'home'
