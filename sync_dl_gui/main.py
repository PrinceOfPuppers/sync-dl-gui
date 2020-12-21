import kivy

from kivy.app import App

from kivy.lang import Builder
from kivy.core.window import Window

from screens import SManager,MainScreen,NewPlScreen,ExistingPlScreen
from kivy.config import Config 

import sync_dl.config as cfg
import os

import youtube_dl
import shutil
import certifi
from time import sleep
from sync_dl import noInterrupt

from runner import runner

class Main(App):
    def build(self):

        layout = Builder.load_file('main.kv')

        if kivy.utils.platform == "android":
            from android.runnable import run_on_ui_thread
            @run_on_ui_thread
            def changeBarColor():
                if kivy.utils.platform == "android":

                    from jnius import autoclass


                    Color = autoclass("android.graphics.Color")
                    WindowManager = autoclass('android.view.WindowManager$LayoutParams')
                    activity = autoclass('org.kivy.android.PythonActivity').mActivity

                    window = activity.getWindow()
                    window.clearFlags(WindowManager.FLAG_TRANSLUCENT_STATUS)
                    window.addFlags(WindowManager.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
                    window.setStatusBarColor(Color.parseColor("#000000")) 
                    window.setNavigationBarColor(Color.parseColor("#000000"))
                    
            changeBarColor()
        return layout

    def on_pause(self):
        runner.cancel()
        return True

    def on_stop(self):
        runner.cancel()
        return True

    def on_start(self):
        runner.start()
        
    # methods used within kv scripts
    def relSize(self,x,y):
        '''converts size from proportion of screen to actual size'''
        return (2*Window.width*x,2*Window.height*y)




def permissionsGranted():
    return check_permission(Permission.READ_EXTERNAL_STORAGE) and check_permission(Permission.WRITE_EXTERNAL_STORAGE)

def getPermissions():
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

if __name__ == "__main__":
    if kivy.utils.platform == "android":

        from android.permissions import request_permissions,check_permission, Permission
    
        while not permissionsGranted():
            sleep(0.1)
            getPermissions()

        if not os.path.exists(cfg.musicDir):
            cfg.musicDir = '/storage/emulated/0/Music'
        if not os.path.exists(cfg.musicDir):
            raise Exception(f"{cfg.musicDir} Doesnt Exist")


            

    os.environ['SSL_CERT_FILE'] = certifi.where()

    cfg.params['quiet'] = True

    cfg.params['no_warnings'] = True
    cfg.params['ignoreerrors'] = True
    #cfg.params['logger'] = cfg.logger
    cfg.params['postprocessors'] = []
    


    Main().run()
