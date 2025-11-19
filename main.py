import os

from dotenv import load_dotenv

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

import threading

import networker

load_dotenv()

class MessagesUI(BoxLayout):
    
    def __init__(self,text,user = True, **argument):
        super().__init__(**argument)
        self.oreitation = 'horizontal'
        self.horizontalSize = dp(600)
        self.padding = [dp(10),dp(10)]
        
        if user:
            alignment='right'
            bgcolor = (0,200,0,1)
        else:
            alignment='left'
            bgcolor = (0,0,200,1)
        
        with self.canvas.before:
            Color(*bgcolor)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect,size=self.update_rect)
        
        textContainer=BoxLayout(orientation='vertical', size_hint_x=20)
        messageLabel=Label(text=text, text_size=(Window.width * 0.5, None), size_hint_y=None,height=dp(70), halign=alignment, valign='middle', color="#69EC1DEF",markup=True)
        messageLabel.bind(texture_size=messageLabel.setter('size'))
        textContainer.add_widget(messageLabel)
        if alignment=='right':
            self.add_widget(Label(size_hint_x=0.1))
            self.add_widget(textContainer)
            self.add_widget(Label(size_hint_x=0.1))
        else:
            self.add_widget(Label(size_hint_x=0.1))
            self.add_widget(textContainer)
            self.add_widget(Label(size_hint_x=0.1))
        
    def update(self,*args):
        self.rect.pos=self.pos
        self.rect.size=self.size
        
class AppUI(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading=True
        self.chatbotAPI=networker.Networker()
    def frame(self):
        self.title='НейроГрам'
        mainLayout=BoxLayout(orientation='vertical',spacing=0.1)
        header=Label(text='НейроГрам 1.0 (Networker Client)', size_hint_y=None,height=dp(50), font_size=20,bold=True, color='#D7D7D7D7')
        
        mainLayout.add_widget(header)
        
        self.scroll = ScrollView(size_hint=(1,0.5), do_scroll_x=False)
        self.chatLayout=BoxLayout(orientation='vertical',size_hint_y=None,spacing=dp(5))
        self.chatLayout.bind(minimum_height=self.chatLayout.setter('height'))
        
        self.scroll.add_widget(self.chatLayout)
        mainLayout.add_widget(self.scroll)
        
        self.indicatorBar = ProgressBar(size_hint_y=None,height=dp(5),max=100,value=30)
        self.indicatorBar.opacity=0
        mainLayout.add_widget(self.indicatorBar)
        
        self.inputLayout=BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        self.messageInput=TextInput(hint_text='Напишите что нибудь...', size_hint_x=0.7,multiline=False)
        self.messageInput.bind(on_text_validate=self.sendMessage)
        
        self.sendBtn=Button(text='Отправить',size_hint_x=0.2,background_color="#186DAA")
        self.sendBtn.bind(on_press=self.sendMessage)     
        
        self.clearBtn=Button(text='Очистить чат',size_hint_x=0.2,background_color="#AA1F18")
        self.clearBtn.bind(on_press=self.clear_chat)    
        
        self.inputLayout.add_widget(self.messageInput)
        self.inputLayout.add_widget(self.clearBtn)
        self.inputLayout.add_widget(self.sendBtn)
        
        mainLayout.add_widget(self.inputLayout)
    
    def sendMessage(self):
        text=self.input.text
        if not text:
            return
        self.add_message_label(text)
        self.input.text=''
        threading.Thread(target=self.get_response,args=(text,)).start()
        
    def add_message_label(self,text):
        message=Label(text=text, size_hint_y=None, height=dp(40), halign='left', markup=True, text_size=(None, None))
        self.chatLayout.add_widget(message)
        
    def get_response(self,text):
        try:
            response=self.chatbotAPI.message(text)
            def updateUI():
                self.add_message_label(response)
            Clock.schedule_once(lambda dt: updateUI())
        except Exception as e:
            def errorUI():
                self.add_message_label(f"[color=ff0000]Ошибка: {str(e)}[/color]")
            Clock.schedule_once(lambda dt: errorUI())
            
if __name__ == '__main__':
    Window.size = (400,400)
    Window.minimum_width = 300
    Window.minimum_height = 400
    AppUI().run()
        
        
        
        
        
