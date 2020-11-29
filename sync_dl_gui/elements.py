import logging


import kivy

from kivy.app import App

from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
import os
import threading
from queue import Queue

import sync_dl.config as cfg

class ConsoleHandler(logging.Handler):

    def __init__(self, console, level=logging.NOTSET):
        logging.Handler.__init__(self, level=level)
        self.console = console

    def emit(self, record):
        Clock.schedule_once(lambda x:self.console.append(self.format(record)))

class Console(TextInput):
    def __init__(self, **kwargs):
        super(Console, self).__init__(**kwargs)
        #self.keyboard_mode= 'managed'
        self.cursor=False

        cfg.logger.addHandler(ConsoleHandler(self))

    def append(self,text):
        self.readonly=False
        self.insert_text(f' ~ {text}\n')
        self.readonly=True



class PlaylistList(GridLayout):
    def __init__(self, **kwargs):
        super(PlaylistList, self).__init__(**kwargs)

        self.updateList()

    def updateList(self):
        '''
        Populates list of existing playlists as buttons
        '''
        self.clear_widgets()
        playlists = os.listdir(cfg.musicDir)
        for playlist in playlists:
            if os.path.exists(f"{cfg.musicDir}/{playlist}/{cfg.metaDataName}"):
                button = Button(
                    text=playlist,
                    on_press = self.playlistClicked
                    #on_release = test
                )
                self.add_widget(button)
    
    def playlistClicked(self,button):
        manager = App.get_running_app().root

        existingPlScreen = manager.get_screen('existingPlScreen')
        existingPlScreen.plName = button.text
        manager.current ='existingPlScreen'
        manager.transition.direction = "left"
