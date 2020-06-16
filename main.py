import kivy
from kivy.clock import Clock
from kivymd.utils import asynckivy
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget, IRightBodyTouch, MDList
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDFloatingActionButtonSpeedDial,MDFlatButton
from kivymd.uix.screen import Screen
from kivymd.icon_definitions import md_icons
            
class CList(MDList):
    pass

class CActionButton(MDFloatingActionButtonSpeedDial):
    def addItem(self):
        self.cList.add_widget(
            ListItemWithEdit(text="Item", icon="minus-circle-outline")
            )
    
    def callback(self, instance):
        if instance.icon == "code-braces":
            self.addItem()
        
class ListItemDelete(IconLeftWidget):
    dialog = None
    
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Delete item?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color
                    ),
                    MDFlatButton(
                        text="DELETE", text_color=self.theme_cls.primary_color
                    ),
                ],
            )
        self.dialog.open()
        
    def on_release(self):
        ok = self.show_alert_dialog()
        #if ok:        
        #    self.list_item.parent.remove_widget(self.list_item)
    
class ListItemWithEdit(OneLineIconListItem):
    icon = StringProperty()
    
    def on_release(self):
        print(self.text)
 
class MenuScreen(Screen):
   pass

class CLScreen(Screen):
    def updateList(self):
        async def updateList():
            for i in range(15):
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