import kivy
from kivy.clock import Clock
from kivymd.utils import asynckivy
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget, IRightBodyTouch, MDList
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivymd.uix.screen import Screen
from kivymd.icon_definitions import md_icons
            
class CList(MDList):
    pass

class CActionButton(MDFloatingActionButtonSpeedDial):
    def callback(self, instance):
        print(instance.icon)
        
class ListItemDelete(IconLeftWidget):
    def on_release(self):
        print("Delete: "+self.list_item.text)
    
class ListItemWithEdit(OneLineIconListItem):
    icon = StringProperty()
    
    def on_release(self):
        print(self.text)
 
class MenuScreen(Screen):
   pass

class CLScreen(Screen):
    def updateList(self):
        async def updateList():
            for i in range(30):
                await asynckivy.sleep(0)
                self.manager.get_screen('cl_screen').cList.add_widget(
                ListItemWithEdit(text=f"Item {i}", icon="minus-circle-outline")
                )
        asynckivy.start(updateList())
        
    def listItemSelected(self):
        print(self.manager.get_screen('cl_screen').cList.text)
    def refresh_callback(self, *args):
        '''A method that updates the state of your application
        while the spinner remains on the screen.'''
        def refresh_callback(interval):
            self.manager.get_screen('cl_screen').cList.clear_widgets()
            self.updateList()
            self.manager.get_screen('cl_screen').cScroll.refresh_done()
            self.tick = 0

        Clock.schedule_once(refresh_callback, 1)
    
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
    def on_stop(self):
        print("CBuilder Closing....")
    
if __name__ == "__main__":
    CBuilderApp().run() 