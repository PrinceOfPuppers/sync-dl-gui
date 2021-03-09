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

from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.clock import Clock

import os


from io import StringIO
import pkg_resources
import sync_dl
import sync_dl.commands as cmds
from sync_dl.plManagement import editPlaylist

import sync_dl.config as cfg
import time
import sys
import webbrowser

from elements import Console,PlaylistList

from runner import runner



class SManager(ScreenManager):
    def __init__(self,**kwargs):
        super(SManager, self).__init__(**kwargs)
        cfg.logger.setLevel(logging.INFO)
        Window.bind(on_keyboard=self.hook_keyboard)
 

    def hook_keyboard(self, window, key, *largs):
        if key == 27:

            if(self.current=='mainScreen'):
                App.get_running_app().stop()
            self.current='mainScreen'
            self.transition.direction = 'right'
            return True 

class MainScreen(Screen):
    playlists = ObjectProperty(None)
    console = ObjectProperty(None)
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
        runner.cancel()


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
        runner.cancel()
    
    def info(self):
        #runner.addJob(cmds.compareMetaData,f"{cfg.musicDir}/{self.plName}")
        runner.addJob(cmds.showPlaylist,f"{cfg.musicDir}/{self.plName}",'\n')

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
    
    def cancel(self):
        self.songList.updateSongs(f"{cfg.musicDir}/{self.plName}")

class SettingsScreen(Screen):
    musicDir = ObjectProperty(None)
    console =  ObjectProperty(None)

    def getSyncDlVersion(self):
        return pkg_resources.require("sync_dl")[0].version

    def getMusicDir(self):
        return cfg.musicDir
    
    def setMusicDir(self):
        path = self.musicDir.text.strip()
        if not os.path.exists(path):
            cfg.logger.info(f"{path} Does Not Exist")
            return
        
        cfg.writeToConfig('musicDir',self.musicDir.text.strip())

        cfg.logger.info(f"Music Directory Changed")
    
    def FrontEndLink(self):
        webbrowser.open('https://github.com/PrinceOfPuppers/sync-dl-gui')
    
    def backEndLink(self):
        webbrowser.open('https://github.com/PrinceOfPuppers/sync-dl')
    
    def bgArtLink(self):
        webbrowser.open('https://sonyakat.com')
    
    def onForceM4aClick(self):
        if self.forceM4aCheckbox.active:
            cfg.params["format"] = 'm4a'
            cfg.writeToConfig('format','m4a')
            cfg.logger.info(f"All Downloads Will Be in m4a Format")
        else:
            cfg.params["format"] = 'bestaudio'
            cfg.writeToConfig('format','bestaudio')
            cfg.logger.info(f"All Downloads Will Be in best audio Format")

    def m4aForced(self):
        '''used to set the inital state of the force m4a checkbox'''
        if cfg.params["format"] == 'm4a':
            return True
        return False