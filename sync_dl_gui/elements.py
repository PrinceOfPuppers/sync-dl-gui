import logging


import kivy

from kivy.app import App

from kivy.clock import Clock

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import DragBehavior


import os
import threading
from queue import Queue

import sync_dl.config as cfg

from sync_dl.helpers import getLocalSongs

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

class SongList(GridLayout):
    def __init__(self, **kwargs):
        super(SongList, self).__init__(**kwargs)

    def getOrder(self):
        '''
        gets newOrder to be passed to editPlaylist function in sync_dl, format is (None,newIndex)
        None is a placeholder, if the song had to be downloaded this would be where the id would go
        '''
        newOrder=[]

        for i in reversed(range(len(self.children))): # we iterate in reverse because grid layout behaves
                                                      # like a stack, 0 index is last
            newOrder.append((None,self.children[i].initalIndex))

        return newOrder

    def updateSongs(self,plPath):
        self.clear_widgets()
        localSongs = getLocalSongs(plPath)

        for i,song in enumerate(localSongs):
            self.add_widget(DragLabel(self,i,text=song))


class DragLabel(DragBehavior, Label):

    def __init__(self,grid,initalIndex, **kwargs):
        super(DragLabel, self).__init__(**kwargs)
        
        self.moving = False
        self.grid = grid
        self.initalIndex = initalIndex


    def findNearestSlot(self):
        for i,element in enumerate(self.grid.children):
            if element.y > self.y:
                return i

        return len(self.grid.children)

    def on_touch_up(self,touch):
        super().on_touch_up(touch)
        if self.moving and self.collide_point(touch.x,touch.y):
            self.grid.remove_widget(self)
            index = self.findNearestSlot()
            self.grid.add_widget(self,index)


    def on_touch_move(self,touch):
        super().on_touch_move(touch)

    def on_touch_down(self,touch):
        super().on_touch_down(touch)

        if self.collide_point(touch.x,touch.y):
            self.moving = True



