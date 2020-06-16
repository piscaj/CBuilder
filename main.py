import kivy
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, IconRightWidget, IRightBodyTouch, MDList
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivymd.uix.screen import Screen
from kivymd.icon_definitions import md_icons
            
class CList(MDList):
    pass
class CActionButton(MDFloatingActionButtonSpeedDial):
    def callback(self, instance):
        print(instance.icon)
    
class ListItemWithEdit(OneLineIconListItem):
    icon = StringProperty()

class MenuScreen(Screen):
   pass

class CLScreen(Screen):
    def updateList(self):
        print("It Worked")
        for i in range(30):
            self.manager.get_screen('cl_screen').cList.add_widget(
            ListItemWithEdit(text=f"Item {i}", icon="minus-circle-outline")
            )
class EditScreen(Screen):
    pass
    
class ManagerScreen(ScreenManager):
   pass

class CBuilderApp(MDApp):
    
    def build(self):
        #self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("main.kv")
    def on_start(self):
        pass
    
if __name__ == "__main__":
    CBuilderApp().run() 