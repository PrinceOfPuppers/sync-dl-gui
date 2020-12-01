import kivy

from kivy.app import App

from kivy.lang import Builder
from kivy.core.window import Window

from screens import SManager,MainScreen,NewPlScreen,ExistingPlScreen
from kivy.config import Config 
  
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
    

if __name__ == "__main__":
    Main().run()