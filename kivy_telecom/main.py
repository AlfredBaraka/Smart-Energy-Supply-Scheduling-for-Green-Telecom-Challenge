from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen
from screens.battery_status_screen import BatteryStatusScreen
from screens.generator_status_screen import GeneratorStatusScreen
from screens.outage_plan_screen import OutagePlanScreen

class TelecomApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(BatteryStatusScreen(name='battery_status'))
        sm.add_widget(GeneratorStatusScreen(name='generator_status'))
        sm.add_widget(OutagePlanScreen(name='outage_plan'))
        return sm

if __name__ == '__main__':
    TelecomApp().run()
