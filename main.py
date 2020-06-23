import os
import json
import kivy
from kivy.clock import Clock
from kivymd.utils import asynckivy
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition, CardTransition, NoTransition
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.toolbar import MDBottomAppBar, MDToolbar
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget, IRightBodyTouch, MDList
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFlatButton, MDRaisedButton
from fileOps import FileOperation
from ftpOps import FtpOperation
from kivymd.icon_definitions import md_icons
from kivy.core.window import Window

Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"

f = FileOperation()
fileData = {}
sftp =  FtpOperation()

app_folder = os.path.dirname(os.path.abspath(__file__))

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
class FtpScreen(Screen,ThemableBehavior):
    dialog = None
    
    def saveEdits(self,inst):
        global fileData
        data = fileData
        for i in range(len(data["Connect"])):
            data["Connect"][i]["Host"] = self.fHost.text
            data["Connect"][i]["User"] = self.fUser.text
            data["Connect"][i]["Pass"] = self.fPass.text
            data["Connect"][i]["Directory"] = self.fPath.text
            break
        
        with open("config.json", "w") as file_write:
            file_write.write(json.dumps(data, sort_keys=True,
                                        indent=4, separators=(',', ': ')))
        self.dialog.dismiss()
    
    def uploadConfig(self,inst):
        global fileData
        data = fileData
        for i in range(len(data["Connect"])):
            _host = data["Connect"][i]["Host"]
            _user = data["Connect"][i]["User"]
            _pass = data["Connect"][i]["Pass"]
            _path = data["Connect"][i]["Directory"]
        
        sftp.writeFile(_host,_user,_pass,_path,"config.json")
        self.dialog.dismiss()
        
    def closeDialog(self, inst):
        self.dialog.dismiss()

    def show_confirmation_save(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Save settings?",
                size_hint=(None, None),
                size=(600, 500),
                type="alert",
                #theme_text_color= "Custom",
                #text_color= self.theme_cls.disabled_hint_text_color,
                text="This will update your SFTP settings.",
                # content_cls=ConfirmDelete(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=self.closeDialog
                    ),
                    MDFlatButton(
                        text="ACCEPT", text_color=self.theme_cls.primary_color, on_release=self.saveEdits
                    ),
                ],
            )
        self.dialog.set_normal_height()
        self.dialog.open()
    
    def show_confirmation_upload(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Upload configuration file?",
                size_hint=(None, None),
                size=(600, 500),
                type="alert",
                #theme_text_color= "Custom",
                #text_color= self.theme_cls.disabled_hint_text_color,
                text="This will transfer config.json to the remote path.",
                # content_cls=ConfirmDelete(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=self.closeDialog
                    ),
                    MDFlatButton(
                        text="ACCEPT", text_color=self.theme_cls.primary_color, on_release=self.uploadConfig
                    ),
                ],
            )
        self.dialog.set_normal_height()
        self.dialog.open()
    
    def on_enter(self):
        global fileData
        data = fileData
        for i in range(len(data["Connect"])):
            self.fHost.text = data["Connect"][i]["Host"]
            self.fUser.text = data["Connect"][i]["User"]
            self.fPass.text = data["Connect"][i]["Pass"]
            self.fPath.text = data["Connect"][i]["Directory"]
            break
                    
    def save(self):
        self.show_confirmation_save()
    
    def upload(self):
        self.show_confirmation_upload()
        
    def goBack(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'cl_screen' 
    
    
    
class EditScreen(Screen):
    passedId = StringProperty()
    
    def on_enter(self):
        global fileData
        data = fileData
        for i in range(len(data["Config"])):
                if data["Config"][i]["Number"] == int(self.manager.statedata):
                    self.eName.text = data["Config"][i]["RoomName"]
                    self.eDes.text = data["Config"][i]["Description"]
                    self.eCom.text = data["Config"][i]["Command"]
                    break
                
    def saveEdits(self):
        global fileData
        data = fileData
        for i in range(len(data["Config"])):
                if data["Config"][i]["Number"] == int(self.manager.statedata):
                    data["Config"][i]["RoomName"] = self.eName.text
                    data["Config"][i]["Description"] = self.eDes.text
                    data["Config"][i]["Command"] = self.eCom.text
                    break
        with open("config.json", "w") as file_write:
            file_write.write(json.dumps(data, sort_keys=True,
                                        indent=4, separators=(',', ': ')))            
class SettingsScreen(Screen):
    def goBack(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'cl_screen'
class ViewCodeScreen(Screen):
    def on_enter(self):
        global fileData
        data = fileData
        self.vLabel.text = json.dumps(data, indent=4, sort_keys=True)
    def goBack(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'cl_screen'  
class ListItemWithEdit(TwoLineIconListItem):
    icon = StringProperty()

    def on_release(self):
        print(self.text, self.id)
        self.parent.cScreen.manager.transition = SlideTransition(
            duration=0.6, direction="left")
        self.parent.cScreen.manager.current = 'e_screen'
        self.parent.cScreen.manager.statedata = self.id
class CLBottomToolbar(MDBottomAppBar):
    def goFTP(self):
        self.cScreen.manager.transition = CardTransition(
            duration=0.6, direction="up")
        self.cScreen.manager.current = 'f_screen'
    
    def goSettings(self):
        self.cScreen.manager.transition = CardTransition(
            duration=0.6, direction="up")
        self.cScreen.manager.current = 's_screen'
    
    def goViewCode(self):
        self.cScreen.manager.transition = CardTransition(
            duration=0.6, direction="up")
        self.cScreen.manager.current = 'v_screen'

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
        self.eScreen.manager.transition = SlideTransition(
            duration=0.6, direction="right")
        self.eScreen.manager.current = 'cl_screen'
class ManagerScreen(ScreenManager):
    statedata = ObjectProperty()
class CBuilderApp(MDApp):

    def build(self):
        #self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        return Builder.load_file("main.kv")

    def on_start(self):
        global fileData
        fileData = f.readFile()

    def on_stop(self):
        print("CBuilder Closing....")

if __name__ == "__main__":
    CBuilderApp().run()
