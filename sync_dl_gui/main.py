import kivy

from kivy.app import App

from kivy.lang import Builder
from kivy.core.window import Window

from screens import SManager,MainScreen,NewPlScreen,ExistingPlScreen
from kivy.config import Config 

import sync_dl.config as cfg
import os
  
# 0 being off 1 being on as in true / false 
# you can use 0 or 1 && True or False 

class Main(App):
    def build(self):

        layout = Builder.load_file('main.kv')

        return layout

    # methods used within kv scripts
    def relSize(self,x,y):
        '''converts size from proportion of screen to actual size'''
        return (2*Window.width*x,2*Window.height*y)
        


import youtube_dl
import shutil



if __name__ == "__main__":
    import certifi

    os.environ['SSL_CERT_FILE'] = certifi.where()

    
    if not os.path.exists(cfg.musicDir):
        cfg.musicDir = '/storage/emulated/0/Music'

    


    cfg.params['quiet'] = True

    cfg.params['no_warnings'] = True
    cfg.params['ignoreerrors'] = True
    #cfg.params['logger'] = cfg.logger
    cfg.params['postprocessors'] = []

    if not os.path.exists(cfg.musicDir):
        raise Exception(f"{cfg.musicDir} Doesnt Exist")


    Main().run()
