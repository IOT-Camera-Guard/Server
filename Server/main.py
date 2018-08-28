from kivy.properties import get_color_from_hex
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.gridlayout import GridLayout

from kivy.app import App
from kivy.uix.button import Button
from glob import glob
import os
from os.path import join, dirname
from kivy.logger import Logger
from kivy.uix.image import Image
from kivy.uix.popup import Popup
import shutil

rem = False


class ImageButton(ButtonBehavior, Image):
    pass


class MyApp(App):
    screen = GridLayout(cols=2)
    bot = None
    fac = None

    def ref(self):
        parent = GridLayout(cols=3)
        curdir = dirname(__file__)
        for filename in glob(join(curdir, "Registered Users", '*')):
            try:
                b = ImageButton()
                b.source = filename
                b.bind(on_press=self.photoclick)
                parent.add_widget(b)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)
        self.screen.remove_widget(self.fac)
        self.fac = parent
        self.screen.add_widget(self.fac)

    def aded(self, filechooser, selection):
        print selection
        shutil.copy( selection[0] ,"Registered Users")
        self.ref()

    def ad(self, instance):
        chos = FileChooserIconView(path="./", )
        chos.bind(selection=self.aded)
        popup = Popup(title='Test popup',
                      content=chos,
                      size_hint=(None, None), size=(400, 400))
        popup.open()

    def rm(self, instance):
        global rem
        rem = not rem
        if rem:
            instance.background_color = get_color_from_hex('#0bc907')
        else:
            instance.background_color = get_color_from_hex('#e0080d')

    def photoclick(self, instance):
        if rem:
            self.fac.remove_widget(instance)
            os.remove(instance.source)

    def buttons(self):
        parent = GridLayout(rows=2)
        button1 = Button(text='add photo')
        button1.bind(on_press=self.ad)
        button2 = Button(text='remove photo')
        button2.background_color = get_color_from_hex('#e0080d')
        button2.bind(on_press=self.rm)
        parent.add_widget(button1)
        parent.add_widget(button2)
        self.bot = parent
    #    return parent

    def faces(self):
        parent = GridLayout(cols=3)
        curdir = dirname(__file__)
        for filename in glob(join(curdir, "Registered Users", '*')):
            try:
                b = ImageButton()
                b.source = filename
                b.bind(on_press=self.photoclick)
                parent.add_widget(b)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)

        self.fac = parent
    #    return parent

    def build(self):
       # parent =
        self.buttons()
        self.screen.add_widget(self.bot)

      #  parent2 =
        self.faces()
        self.screen.add_widget(self.fac)
        return self.screen


if __name__ == '__main__':
    MyApp().run()
