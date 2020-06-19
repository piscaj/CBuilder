import os
import kivy
from kivy.clock import Clock
from kivymd.utils import asynckivy
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition, CardTransition, NoTransition
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.toolbar import MDBottomAppBar, MDToolbar
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget, IRightBodyTouch, MDList
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFlatButton
from fileOps import FileOperation
from kivymd.icon_definitions import md_icons

f = FileOperation()
fileData = {}

class ConfirmDelete(BoxLayout):
    pass

class CList(MDList):
    pass

class ListItemDelete(IconLeftWidget):
    dialog = None

    def deleteItem(self, inst):
        f.deleteFromFile("Number", self.list_item.id)
        self.list_item.parent.remove_widget(self.list_item)
        self.dialog.dismiss()

    def closeDialog(self, inst):
        self.dialog.dismiss()

    def show_confirmation_dialog(self, _name):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Delete item?",
                size_hint=(None, None),
                size=(600, 500),
                type="alert",
                #theme_text_color= "Custom",
                #text_color= self.theme_cls.disabled_hint_text_color,
                text=_name+" will permanintly be removed.",
                # content_cls=ConfirmDelete(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=self.closeDialog
                    ),
                    MDFlatButton(
                        text="ACCEPT", text_color=self.theme_cls.primary_color, on_release=self.deleteItem
                    ),
                ],
            )
        self.dialog.set_normal_height()
        self.dialog.open()

    def on_release(self):
        self.show_confirmation_dialog(self.list_item.text)

class MenuScreen(Screen):
    pass


class CLScreen(Screen):
    def updateList(self):
        async def updateList():
            global fileData
            fileData = f.readFile()
            data = fileData["Config"]
            for name in data:
                await asynckivy.sleep(0)
                self.manager.get_screen('cl_screen').cList.add_widget(
                    ListItemWithEdit(id=str(name.get("Number")), text=name.get(
                        "RoomName"), icon="minus-circle-outline", secondary_text=name.get(
                        "Description"))
                )
        asynckivy.start(updateList())

    def listItemSelected(self):
        print(self.manager.get_screen('cl_screen').cList.text)

    def refresh(self, *args):
        def refresh(interval):
            self.manager.get_screen('cl_screen').cList.clear_widgets()
            self.updateList()
            self.manager.get_screen('cl_screen').cScroll.refresh_done()
            self.tick = 0

        Clock.schedule_once(refresh, 1)

    def on_enter(self, *args):
        if self.transition_progress == 1.0:
            self.refresh()

class EditScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class ListItemWithEdit(TwoLineIconListItem):
    icon = StringProperty()

    def on_release(self):
        print(self.text, self.id)
        self.parent.cScreen.manager.transition = CardTransition(
            duration=0.6, direction="left")
        self.parent.cScreen.manager.current = 'e_screen'

class CLBottomToolbar(MDBottomAppBar):
    def goSettings(self):
        self.cScreen.manager.transition = CardTransition(
            duration=0.6, direction="up")
        self.cScreen.manager.current = 's_screen'

    def addItem(self):
        itemAdded = f.addToFile()
        f.readFile()
        if itemAdded:
            self.cList.add_widget(
                ListItemWithEdit(id=str(f.numberOfItems()),
                                 text="New Room", icon="minus-circle-outline", secondary_text="No description")
            )

class EditBottomToolbar(MDToolbar):
    def goBack(self):
        self.eScreen.manager.transition = CardTransition(
            duration=0.6, direction="right")
        self.eScreen.manager.current = 'cl_screen'

class SettingsBottomToolbar(MDToolbar):
    def goBack(self):
        self.sScreen.manager.transition = NoTransition()
        self.sScreen.manager.current = 'cl_screen'

class ManagerScreen(ScreenManager):
    pass

class CBuilderApp(MDApp):

    global fileData

    def build(self):
        #self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        return Builder.load_file("main.kv")

    def on_start(self):
        fileData = f.readFile()

    def on_stop(self):
        print("CBuilder Closing....")

if __name__ == "__main__":
    CBuilderApp().run()
