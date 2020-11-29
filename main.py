



import logging


import kivy

from kivy.app import App

from kivy.lang import Builder

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput

from kivy.properties import ObjectProperty

from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.clock import Clock

import os
import threading
from queue import Queue

from io import StringIO
import sync_dl
import sync_dl.commands as cmds
from sync_dl import noInterrupt
import sync_dl.config as cfg




class Runner:
    '''
    Used to run a single command at a time without locking up the UI
    Does not buffer Commands 

    '''
    def __init__(self):
        self.job = Queue(1)

        self.working=False

        self.t=threading.Thread(target = self.start)
        self.t.start()

    def addJob(self,job,args):
        if self.working:
            cfg.logger.info("Command Currently Running")
        else:
            self.job.put((job,args))


    def start(self):
        while threading.main_thread().is_alive():
            try:
                job = self.job.get(timeout=3)
            except:
                continue

            self.working=True

            try:
                job[0](*job[1])
                cfg.logger.info("Done!")
            except:
                cfg.logger.info("Cancelled")
            
            self.working=False


runner=Runner()

class ConsoleHandler(logging.Handler):

    def __init__(self, console, level=logging.NOTSET):
        logging.Handler.__init__(self, level=level)
        self.console = console

    def emit(self, record):
        Clock.schedule_once(lambda x:self.console.append(self.format(record)))


class WindowManager(ScreenManager):
    def __init__(self,**kwargs):

        super(WindowManager, self).__init__(**kwargs)
        cfg.logger.setLevel(logging.INFO)


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

        existingPlWindow = manager.get_screen('existingPlWindow')
        existingPlWindow.plName = button.text
        manager.current ='existingPlWindow'

        manager.transition.direction = "left"

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



class MainWindow(Screen):
    playlists = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
    
    def on_pre_enter(self):
        if self.playlists:
            self.playlists.updateList()



    
class NewPlWindow(Screen):
    url = ObjectProperty(None)
    plName = ObjectProperty(None)
    console = ObjectProperty(Console)


    def create(self):
        runner.addJob(cmds.newPlaylist,[f"{cfg.musicDir}/{self.plName.text}",self.url.text])

    def cancel(self):
        noInterrupt.simulateSigint()


class ExistingPlWindow(Screen):
    plName = ''
    plLabel = ObjectProperty(None)
    console = ObjectProperty(None)

    def on_pre_enter(self):
        self.plLabel.text = self.plName

        self.console.bind()


    def smartSync(self):
        runner.addJob(cmds.smartSync,[f"{cfg.musicDir}/{self.plName}"])
    
    def appendNew(self):
        runner.addJob(cmds.appendNew,[f"{cfg.musicDir}/{self.plName}"])
    
    def reorder(self):
        print(self.plName)
    
    def cancel(self):
        noInterrupt.simulateSigint()

    



class Main(App):
    def build(self):
        layout = Builder.load_file('kvMan.kv')
        return layout

    

if __name__ == "__main__":

    Main().run()