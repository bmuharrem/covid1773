import json 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Line 
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.uix.image import Image
from PIL import Image
import requests
import cv2
from urllib.request import urlopen
import webbrowser

# ARKA PLAN RENGİ

Window.clearcolor = 34/255, 38/255, 41/255, 1

# GENİŞLİK AYARLAMA

SPACE = 0.025
UCH = (1 - 4*SPACE) / 2
LENG = .1




# HABERLER VE GENEL İSTATİSTİKLER

# Asia Statistics

f = open("continentdata.json", "r")

readedasia = json.load(f)

ASİADATA= readedasia["result"][1]

f.close()


# ALL DATA

f = open("totaldata.json", "r")

readedall = json.load(f)

ALLDATA= readedall["result"]

f.close()


# TURKEY DATA

f = open("statistics.json", "r")

readedturkey = json.load(f)

TURKEYDATA = {}

for i in range(len(readedturkey["result"])):
    if readedturkey["result"][i]["country"] == "Turkey":
        TURKEYDATA = readedturkey["result"][i]

        
f.close()


# NEWS

f = open("news.json", "r")

readednews = json.load(f)

NEWS = readednews["result"]

f.close()






# Screeens :


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "detailed"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""



class DetailedForm(Screen):
    job = ObjectProperty(None)
    transportation = ObjectProperty(None)
    exercise = ObjectProperty(None)
    
    def submit(self):
        if self.transportation.text != "" and self.job.text != "" and self.exercise.text != "" :
            db.add_user(self.transportation.text, self.job.text, self.exercise.text)
            
            self.reset()
            
            sm.current = "login"
        
        else:
            invalidForm()
    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.transportation.text = ""
        self.job.text = ""
        self.exercise.text = ""
            
            

class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""



class MainWindow(Screen):
# =============================================================================
#     n = ObjectProperty(None)
#     created = ObjectProperty(None)
#     email = ObjectProperty(None)
#     current = ""
# 
#     def logOut(self):
#         sm.current = "login"
# 
#     def on_enter(self, *args):
#         password, name, created = db.get_user(self.current)
#         self.n.text = "Account Name: " + name
#         self.email.text = "Email: " + self.current
#         self.created.text = "Created On: " + created
# =============================================================================

    space = SPACE
    space_variable = SPACE
    uch = UCH
    leng = LENG
    pass
    def switch_to(self, to):
        sm.current = to



class HealthMSWindow(Screen):
    space = SPACE
    space_variable = SPACE
    uch = UCH
    leng = LENG

    turkey_recovery = TURKEYDATA["totalRecovered"]
    turkey_total_cases = TURKEYDATA["totalCases"]
    turkey_death = TURKEYDATA["totalDeaths"]
    global_recovery = ALLDATA["totalRecovered"]
    global_total_cases = ALLDATA["totalCases"]
    global_death = ALLDATA["totalDeaths"]

    def switch_to(self, to):
        sm.current = to



class RiskyConditionsWindow(Screen):
    space = SPACE
    space_variable = SPACE
    uch = UCH
    leng = LENG

    def switch_to(self, to):
        sm.current = to



class NewsWindow(Screen):
    space = SPACE
    space_variable = SPACE
    uch = UCH
    leng = LENG
    news_1_des = NEWS[0]["description"]
    # news_2_des = NEWS[1]["description"]
    # news_3_des = NEWS[2]["description"]

    def switch_to(self, to):
        sm.current = to



class SuggestionsWindow(Screen):
    space = SPACE
    space_variable = SPACE
    uch = UCH
    leng = LENG
    def switch_to(self, to):
        sm.current = to
        


class WindowManager(ScreenManager):
    pass




# functions

def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()



def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()




# Main operations

kv = Builder.load_file("covid1773.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main"),DetailedForm(name="detailed"),HealthMSWindow(name="health"), RiskyConditionsWindow(name="risk"), NewsWindow(name="news"), SuggestionsWindow(name="suggestions")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm

    def on_start(self):
        gps.configure(on_location=self.on_gps_location)
        gps.start()

    def on_gps_location(self, **kwargs):
        f = open("positions.txt", "a")
        f.write(kwargs)
        f.close()

if __name__ == "__main__":
    MyMainApp().run()