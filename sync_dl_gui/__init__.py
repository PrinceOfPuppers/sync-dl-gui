import kivy

from kivy.app import App

from kivy.lang import Builder
from screens import ScreenManager,MainScreen,NewPlScreen,ExistingPlScreen

class Main(App):
    def build(self):

        layout = Builder.load_file('main.kv')
        return layout

    

if __name__ == "__main__":
    Main().run()