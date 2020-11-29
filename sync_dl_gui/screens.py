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
from sync_dl.plManagement import editPlaylist
from sync_dl import noInterrupt
import sync_dl.config as cfg
import time

from elements import Console,PlaylistList

class Runner:
    '''
    Used to run a single command at a time without locking up the UI
    Does not buffer Commands 

    '''
    def __init__(self):
        self.jobQueue = Queue(1)

        self.working=False

        self.t=threading.Thread(target = self.start)
        self.t.start()

    def addJob(self,job,plPath,*args):
        if self.working:
            cfg.logger.info("Command Currently Running")
        else:
            self.jobQueue.put((job,plPath,args))


    def start(self):
        while threading.main_thread().is_alive():
            try:
                package = self.jobQueue.get(timeout=3)
            except:
                continue

            self.working=True

            job,plPath,args=package
            try:
                job(plPath,*args)
                cfg.logger.info("Done!")
            except:
                sync_dl.plManagement.correctStateCorruption(plPath)
                cfg.logger.info("Cancelled")
            
            self.working=False


runner=Runner()


class SManager(ScreenManager):
    def __init__(self,**kwargs):
        super(SManager, self).__init__(**kwargs)
        cfg.logger.setLevel(logging.INFO)


class MainScreen(Screen):
    playlists = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
    
    def on_pre_enter(self):
        if self.playlists:
            self.playlists.updateList()

    
class NewPlScreen(Screen):
    url = ObjectProperty(None)
    plName = ObjectProperty(None)
    console = ObjectProperty(Console)


    def create(self):
        runner.addJob(cmds.newPlaylist,f"{cfg.musicDir}/{self.plName.text}",self.url.text)

    def cancel(self):
        noInterrupt.simulateSigint()


class ExistingPlScreen(Screen):
    plName = ''
    plLabel = ObjectProperty(None)
    console = ObjectProperty(None)

    def on_pre_enter(self):
        self.plLabel.text = self.plName

        self.console.bind()


    def smartSync(self):
        runner.addJob(cmds.smartSync,f"{cfg.musicDir}/{self.plName}")
    
    def appendNew(self):
        runner.addJob(cmds.appendNew,f"{cfg.musicDir}/{self.plName}")
    
    def reOrder(self):
        manager = self.manager

        reOrderScreen = manager.get_screen('reOrderScreen')
        reOrderScreen.plName = self.plName
        manager.current ='reOrderScreen'
        manager.transition.direction = "left"
    
    def cancel(self):
        noInterrupt.simulateSigint()
    
    def info(self):
        runner.addJob(cmds.compareMetaData,f"{cfg.musicDir}/{self.plName}")
        runner.addJob(cmds.showPlaylist,f"{cfg.musicDir}/{self.plName}",'')

class ReOrderScreen(Screen):
    plName = ''
    plLabel = ObjectProperty(None)
    songList = ObjectProperty(None)

    def on_pre_enter(self):
        self.plLabel.text = self.plName

        self.songList.updateSongs(f"{cfg.musicDir}/{self.plName}")


    def apply(self):
        newOrder = self.songList.getOrder()
        runner.addJob(editPlaylist,f"{cfg.musicDir}/{self.plName}",newOrder)
        
        time.sleep(0.1)
        while runner.working:
            time.sleep(0.1)

        self.songList.updateSongs(f"{cfg.musicDir}/{self.plName}")