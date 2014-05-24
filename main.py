from datetime import timedelta

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.settings import Settings
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget


# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
#: import sys sys
#: import td datetime.timedelta

<Header@Label>:
    markup: True
    font_size: 24
    color: [0, 0, 0, 1]
    canvas.before:
        Color:
            rgba: .95, .95, .95, 1
        Rectangle:
            pos: self.pos
            size: self.size

<CountdownWidget>:
    seconds_left: 30*60
    canvas.before:
        Color:
            rgba: 1,1,1,0.5
        Rectangle:
            size: self.size
            pos: self.pos

<AlmostInput@TextInput>:
    font_size: 24

<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        
        Button:
            text: "WORK"
            font_size: 50
            #size_hint: (1, .25)
            on_press: root.manager.current = 'settings'
            canvas:
                Color:
                    
        Button:
            text: "HOME"
            font_size: 50
            #size_hint: (1, .25)
        Button:
            text: "+ ADD NEW"
            font_size: 50
            #size_hint: (1, .25)
        Label:
            size_hint: (1, .20)
        
<SettingsScreen>:    
    BoxLayout:
        padding: 3
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            spacing: '5sp'
            size_hint: (1, .8)
            Label:
                text: 'GET ME TO...'
                halign: 'left'
                font_size: 18
                bold: True
            AlmostInput:
                background_color: .8, .8, .8, .8
            Label:
                text: 'FROM...'
                font_size: 18
                bold: True
            AlmostInput:
                background_color: .8, .8, .8, .8
            Label:
                text: 'BY OR AFTER'
                bold: True
                font_size: 18
            AlmostInput:
                background_color: .8, .8, .8, .8
            BoxLayout:
                Label:
                    text: 'ALERTS'
                    bold: True
                Label:
                    text: 'ON / OFF'
            AlmostInput:
                background_color: .8, .8, .8, .8
            Label:
                text: 'MON TUE WED THU FRI SAT SUN'
                font_size: 18
                bold: True
                markup: True
                    
        Button:
            size_hint: (1, 0.1)
            text: 'Go'
            on_press: root.manager.current = 'when_to_leave'
            #disabled: True

<WhenToLeaveScreen>:
    id: countdown
    seconds_left: 30*24

    BoxLayout:
        #size_hint: (1, 0.8)
            
        orientation: 'vertical'
        Header:
            size_hint: (1, .1)
            text: 'Get me to [b]WORK[/b]'
            
        GridLayout:
            cols: 1
            size_hint: (1, .7)
            Label:
                text: ""
                size_hint_y: 0.2
            Label:
                font_size: '80dp'
                text: str(td(seconds=countdown.seconds_left)).split(":",1)[1]
                #size: self.texture_size
                size_hint_y: 0.4
                
                
            Label:
                font_size: '24dp'
                pos: (10, root.size[1]*0.4)
                text: countdown.message
                #size: self.texture_size
            Label:
                text: countdown.alert
                font_size: '24dp'

        #BoxLayout:
        #    orientation: 'horizontal'
        #    size_hint: (1, .2)
        #    
        #    Label:
        #        text: "Time now: 7:06am" 
        #        font_size: 18
        #    Label:
        #        text: "Time to walk: 7mins"
        #        font_size: 18
        #    Label:
        #        text: "Bus due: 7:30am"
        #        font_size: 18
        BoxLayout:
            orientation: 'horizontal'
            size_hint: (1, .1)
            
            Button:
                text: 'Home'
                on_press: root.manager.current = 'home'
            
""")


SETTINGS = """[
    {
        "type": "string",
        "title": "GET ME TO...",
        "key": "destination",
    },
    {
        "type": "string",
        "title": "FROM...",
        "key": "origin",
    },
    {
        "type": "options",
        "title": "BEFORE OR AFTER",
        "key": "before_or_after",
        "values": ["Before", "After"]
        "default": "after"
    },
    {
        "type": "string",
        "key": "when",
        "default: "now"
    },
    {
        "type": "options",
        "title": "ALERTS",
        "key": "destination",
    },
    {
        "type": "options",
        "title": "BEFORE OR AFTER",
        "key": "before_or_after",
        "values: ["MON", "TUE", "WED", "THU", "FRI", "SAT, "SUN"]
    },

    
    ]"""

# Declare both screens
class HomeScreen(Screen):
    pass

class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class LocationInputScreen(Screen):
    pass
    
class WhenToLeaveScreen(Screen):
    seconds_left = NumericProperty(30*60)
    message = StringProperty("minutes to go \nbefore you need to leave")
    alert   = StringProperty("")
    display = ObjectProperty(None)
    
    def __init__(self, seconds_left=30*60, *aa, **kw):
        super(WhenToLeaveScreen, self).__init__(*aa, **kw)
       
        Clock.schedule_interval(self._count_down, 1)
        
        self.display = Label(pos=self.pos, size=self.size)
        self.add_widget(self.display)

    def _count_down(self, dt):
        self.seconds_left -= 1
        if self.seconds_left < 60:
            self.message = ""
            self.alert = "TIME TO GO"
        elif self.seconds_left < 60*10:
            self.alert = "HAVE YOU GOT YOUR\nUNDERWEAR ON?"
    
    def _turbo(self, *args):
        Clock.schedule_interval(self._count_down, 0.02)
        Clock.schedule_once(lambda *args: self._count_down, 1)
        
    def on_touch(self, *args):
        self._turbo()
    
# Create the screen manager
sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(WhenToLeaveScreen(name='when_to_leave'))

class TestApp(App):
    def build_settings(self, settings):
        self.config = ConfigParser()
        self.settings = Settings()
        self.settings.add_json_panel('Preferences', self.config, data=SETTINGS)

    def build(self):
        return sm

if __name__ == '__main__':
    app = TestApp()
    app.run()