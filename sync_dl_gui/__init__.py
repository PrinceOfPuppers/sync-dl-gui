import kivy

from kivy.app import App

from kivy.lang import Builder


from screens import SManager,MainScreen,NewPlScreen,ExistingPlScreen

class Main(App):
    def build(self):

        layout = Builder.load_file('main.kv')
        return layout

    

if __name__ == "__main__":
    Main().run()