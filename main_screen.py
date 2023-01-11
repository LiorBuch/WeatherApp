import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField


class MainScreen(Screen):
    def __init__(self, **kw):
        self.api_key = "a4Gsee6jhV2Klc89Prvsh34"
        super().__init__(**kw)
        self.name = "main_screen"
        self.main_layout = FloatLayout()
        self.stats_layout = BoxLayout(size_hint=(0.5, 0.2), orientation="vertical", pos_hint={'top': 0.7})
        self.sky_icon = AsyncImage(size_hint=(0.2, 0.2), pos_hint={'center_x': 0.7, 'center_y': 0.7})
        self.search_box = MDTextField(hint_text="Enter City Name", size_hint=(0.3, 1),
                                      pos_hint={'top': 0.95, 'left': 0.1})
        self.search_btn = MDFlatButton(text="Search Weather", on_press=self.search_btn_click,
                                       pos_hint={'right': 0.95, 'bottom': 0.95})
        self.city_name = MDLabel(text="")
        self.temp = MDLabel(text="0")
        self.sky_status = MDLabel(text="sky state")
        self.description = MDLabel(text="description")
        self.min_temp = MDLabel(text="0")
        self.max_temp = MDLabel(text="0")

        self.main_layout.add_widget(self.stats_layout)
        self.stats_layout.add_widget(self.city_name)
        self.stats_layout.add_widget(self.sky_status)
        self.stats_layout.add_widget(self.description)
        self.stats_layout.add_widget(self.temp)
        self.stats_layout.add_widget(self.max_temp)
        self.stats_layout.add_widget(self.min_temp)
        self.main_layout.add_widget(self.sky_icon)
        self.main_layout.add_widget(self.search_box)
        self.main_layout.add_widget(self.search_btn)
        self.add_widget(self.main_layout)

    def search_btn_click(self, instance):
        if self.search_box.text == "" or self.search_box.text is None:
            pop = Popup(size_hint=(0.4, 0.4))
            pop.title = "City name cant be blank!"
            self.search_box.error = True
            pop.open()
            return
        try:
            city_name = self.search_box.text
            weather_pack = requests.get(
                url=f"https://gittester.azurewebsites.net/weather/city={city_name}&key={self.api_key}")
            if weather_pack.status_code == 200:
                data = weather_pack.json()
                self.sky_icon.source = f'http://openweathermap.org/img/wn/{str(data["state"]["sky_icon"])}@2x.png'
                self.temp.text = "Current Temperature:" + str(data['temp']['current'])
                self.min_temp.text = "Minimum Temperature Today:" + str(data['temp']['min'])
                self.max_temp.text = "Maximum Temperature Today:" + str(data['temp']['max'])
                self.city_name.text = str(data['city_name'])
                self.sky_status.text = str(data['state']['sky'])
                self.description.text = str(data['state']['sky_info'])
            else:
                pop = Popup(title="Connection Error")
                pop.open(size_hint=(0.4, 0.4))
        except Exception as e:
            print(f"error , error log is:{e}")
