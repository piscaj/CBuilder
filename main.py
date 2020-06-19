import json
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

from kivymd.icon_definitions import md_icons

fileData = {}


def numberOfItems():
    with open("config.json", "r") as read_file:
        obj = json.load(read_file)
        objNum = len(obj["Config"])
        return objNum


def deleteFromFile(_key, _value):
    with open("config.json", "r") as read_file:
        obj = json.load(read_file)
        print("Searching", _key, _value)
        for i in range(len(obj["Config"])):
            print(i)
            if obj["Config"][i][_key] == int(_value):
                print("Found the entry!!!!!!")
                obj["Config"].pop(i)
                break

    with open("config.json", "w") as file_write:
        file_write.write(json.dumps(obj, sort_keys=True,
                                    indent=4, separators=(',', ': ')))


def addToFile():
    with open("config.json", "r") as read_file:
        obj = json.load(read_file)
        objNum = len(obj["Config"])
        obj["Config"].append({
            'Command': 'No device command',
            'Description': 'No description',
            'Number': objNum,
            'RoomName': 'New Room'
        })

    with open("config.json", "w") as file_write:
        file_write.write(json.dumps(obj, sort_keys=True,
                                    indent=4, separators=(',', ': ')))
        print("New item added to file...")
        return True


def makeFile():
    data = {}
    data['Config'] = []
    data['Config'].append({
        'Command': 'No device command',
        'Description': 'No description',
        'Number': 0,
        'RoomName': 'Room Name'
    })
    with open('config.json', 'w') as write_file:
        json.dump(data, write_file)
        print("New file added...")
    readFile()


def readFile():
    global fileData
    try:
        print("Trying Reading JSON file")
        with open("config.json", "r") as read_file:
            print("Converting JSON encoded data into Python dictionary")
            fileData = json.load(read_file)

            print("Decoded JSON Data From File")
            for key, value in fileData.items():
                print(key, ":", value)
            print("Done reading json file")
    except FileNotFoundError:
        print("File not found...")
        makeFile()


def editListItem():
    pass


class ConfirmDelete(BoxLayout):
    pass


class CList(MDList):
    pass


class ListItemDelete(IconLeftWidget):
    dialog = None

    def deleteItem(self, inst):
        deleteFromFile("Number", self.list_item.id)
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


class ListItemWithEdit(TwoLineIconListItem):
    icon = StringProperty()

    def on_release(self):
        print(self.text, self.id)
        self.parent.cScreen.manager.transition = SlideTransition(
            duration=0.6, direction="left")
        self.parent.cScreen.manager.current = 'e_screen'


class MenuScreen(Screen):
    pass


class CLScreen(Screen):
    def updateList(self):
        async def updateList():
            readFile()
            global fileData
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


class CLBottomToolbar(MDBottomAppBar):
    def goSettings(self):
        self.cScreen.manager.transition = CardTransition(
            duration=0.6, direction="up")
        self.cScreen.manager.current = 's_screen'

    def addItem(self):
        itemAdded = addToFile()
        readFile()
        if itemAdded:
            self.cList.add_widget(
                ListItemWithEdit(id=str(numberOfItems()),
                                 text="New Room", icon="minus-circle-outline", secondary_text="No description")
            )


class EditScreen(Screen):
    pass


class EditBottomToolbar(MDToolbar):
    def goBack(self):
        self.eScreen.manager.transition = SlideTransition(
            duration=0.6, direction="right")
        self.eScreen.manager.current = 'cl_screen'


class SettingsScreen(Screen):
    pass


class SettingsBottomToolbar(MDToolbar):
    def goBack(self):
        self.sScreen.manager.transition = NoTransition()
        self.sScreen.manager.current = 'cl_screen'


class ManagerScreen(ScreenManager):
    pass


class CBuilderApp(MDApp):

    def build(self):
        #self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        return Builder.load_file("main.kv")

    def on_start(self):
        readFile()

    def on_stop(self):
        print("CBuilder Closing....")


if __name__ == "__main__":
    CBuilderApp().run()
