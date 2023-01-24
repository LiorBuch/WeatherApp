import json

from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from plyer import gps
from kivy.network.urlrequest import UrlRequest
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
        self.stats_layout = BoxLayout(size_hint=(0.7, 0.2), orientation="vertical", pos_hint={'top': 0.7},spacing = 10)
        self.sky_icon = AsyncImage(size_hint=(0.3, 0.3), pos_hint={'center_x': 0.7, 'center_y': 0.7})
        self.search_box_city = MDTextField(hint_text="Enter City Name", size_hint=(0.3, 1),
                                           pos_hint={'top': 0.95, 'left': 0.1})
        self.search_box_country = MDTextField(hint_text="Enter Country Name", size_hint=(0.3, 1),
                                              pos_hint={'top': 0.90, 'left': 0.1})
        self.search_btn = MDFlatButton(text="Search Weather", on_press=self.search_btn_click,
                                       pos_hint={'right': 0.95, 'bottom': 0.95})
        self.search_by_loc_btn = MDFlatButton(text="Search By GPS", pos_hint={'left': 0.95, 'bottom': 0.95},
                                              on_press=self.location_btn)
        self.city_name = MDLabel(text="")
        self.temp = MDLabel(text="0")
        self.sky_status = MDLabel(text="sky state")
        self.description = MDLabel(text="description")
        self.min_temp = MDLabel(text="0")
        self.max_temp = MDLabel(text="0")

        self.sky_icon.opacity=0

        self.main_layout.add_widget(self.stats_layout)
        self.main_layout.add_widget(self.sky_icon)
        self.stats_layout.add_widget(self.city_name)
        self.stats_layout.add_widget(self.sky_status)
        self.stats_layout.add_widget(self.description)
        self.stats_layout.add_widget(self.temp)
        self.stats_layout.add_widget(self.max_temp)
        self.stats_layout.add_widget(self.min_temp)
        self.main_layout.add_widget(self.search_box_city)
        self.main_layout.add_widget(self.search_box_country)
        self.main_layout.add_widget(self.search_btn)
        self.main_layout.add_widget(self.search_by_loc_btn)
        self.add_widget(self.main_layout)

        with self.canvas.before:
            Color(0.5,0.5,0.5,0.5)
            self.rect = Rectangle(size=Window.size)

    def search_btn_click(self, instance):
        if not self.search_box_city.text.isalpha() or self.search_box_city.text is None:
            pop = Popup(size_hint=(0.4, 0.2))
            pop.title = "Incorrect Format!"
            self.search_box_city.error = True
            pop.open()
            return
        try:
            city_name = self.search_box_city.text
            weather_pack = UrlRequest(
                url=f"https://gittester.azurewebsites.net/weather/city={city_name}/", req_headers={'api': self.api_key},
                timeout=10,
                on_success=self.prini, on_redirect=self.multi_country)
            weather_pack.wait()

        except Exception as e:
            pop = Popup(title="internal error", size_hint=(0.4, 0.2))
            pop.open()
            print(f"error , error log is:{e}")

    def prini(self, *args):
        self.sky_icon.opacity=1
        data = json.loads(args[1])
        self.sky_icon.source = f'http://openweathermap.org/img/wn/{str(data["state"]["sky_icon"])}@2x.png'
        self.temp.text = "Current Temperature:" + str(data['temp']['current'])
        self.min_temp.text = "Minimum Temperature Today:" + str(data['temp']['min'])
        self.max_temp.text = "Maximum Temperature Today:" + str(data['temp']['max'])
        self.city_name.text = str(data['city_name'])
        self.sky_status.text = str(data['state']['sky'])
        self.description.text = str(data['state']['sky_info'])

    def location_btn(self, instance):
        print("starting gps")
        gps.configure(on_location=self.send_loc)
        gps.start()
        gps.stop()

    def send_loc(self,**kwargs):
        print("go!")
        lat = kwargs["lat"]
        lon = kwargs["lon"]
        self.city_name.text = lat
        print(lat)
        print(lon)

    def multi_country(self, *args):
        pop = Popup(title="Problem with request")
        pop_label = MDLabel(text=json.loads(args[1])["info"])
        pop.content = pop_label
        pop.open()
