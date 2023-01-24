from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

import main_screen


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = None
        self.main_screen = None

    def build(self):
        self.sm = ScreenManager()
        self.main_screen = main_screen.MainScreen()
        self.sm.add_widget(self.main_screen)
        self.sm.current = "main_screen"
        return self.sm


MainApp().run()
