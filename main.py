import os
import json
import kivy
from kivy.clock import Clock
import time
import threading
from kivymd.utils import asynckivy
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition, CardTransition, NoTransition
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.toolbar import MDBottomAppBar, MDToolbar
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.uix.floatlayout import FloatLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget,IRightBodyTouch,IconRightWidget, MDList
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFlatButton, MDRaisedButton
from fileOps import FileOperation
from ftpOps import FtpOperation
from kivymd.icon_definitions import md_icons
from kivy.core.window import Window
from kivymd.uix.card import MDCardSwipe

Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"

f = FileOperation()
fileData = {}
sftp = FtpOperation()

app_folder = os.path.dirname(os.path.abspath(__file__))

class Progress(FloatLayout):
    pass


class CList(MDList):
    pass


class ListItemCopy(IconRightWidget):
    dialog = None

    def deleteItem(self, inst):
        global fileData
        f.deleteFromFile("Number", self.list_item.id)
        self.list_item.parent.remove_widget(self.list_item)
        fileData = f.readFile()
        self.dialog.dismiss()

    def closeDialog(self, inst):
        self.dialog.dismiss()
    
    def show_confirmation_dialog(self, _name):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Make another like this?",
                size_hint=(None, None),
                size=(600, 500),
                type="alert",
                text=_name+" command will be duplicated.",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=self.closeDialog
                    ),
                    MDFlatButton(
                        text="ACCEPT", text_color=self.theme_cls.primary_color, on_release=self.deleteItem
                    ),
                ],
            )
        self.dialog.open()

    def on_release(self):
        self.show_confirmation_dialog(self.list_item.text)

class ListItemDelete(IconLeftWidget):
    dialog = None

    def deleteItem(self, inst):
        global fileData
        f.deleteFromFile("Number", self.list_item.id)
        self.list_item.parent.remove_widget(self.list_item)
        fileData = f.readFile()
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
                text=_name+" will permanintly be removed.",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=self.closeDialog
                    ),
                    MDFlatButton(
                        text="ACCEPT", text_color=self.theme_cls.primary_color, on_release=self.deleteItem
                    ),
                ],
            )
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
                        "Name"), iconL="trash-can-outline",iconR="clipboard-plus-outline", secondary_text=name.get(
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
            if self.manager.updateRequest:
                self.manager.updateRequest = False
                self.refresh()
    def on_kv_post(self, base_widget):
        global fileData
        fileData = f.readFile()
        self.refresh()


class FtpScreen(Screen, ThemableBehavior):
    dialogSave = None
    dialogUpload = None
    dialogDownload = None
    dialogUploading = None
    dialogDownloading = None
    dialogException = None

    def saveEdits(self, inst):
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
        self.dialogSave.dismiss()

    def uploadConfig(self):
        global fileData
        data = fileData
        for i in range(len(data["Connect"])):
            _host = data["Connect"][i]["Host"]
            _user = data["Connect"][i]["User"]
            _pass = data["Connect"][i]["Pass"]
            _path = data["Connect"][i]["Directory"]

        transfer = sftp.writeFile(_host, _user, _pass, _path, "config.json")
        if transfer == "Success":
            self.dialogUploading.dismiss()
        else:
            self.dialogUploading.dismiss()
            self.show_exception(str(transfer))

    def downloadConfig(self):
        global fileData
        data = fileData
        for i in range(len(data["Connect"])):
            _host = data["Connect"][i]["Host"]
            _user = data["Connect"][i]["User"]
            _pass = data["Connect"][i]["Pass"]
            _path = data["Connect"][i]["Directory"]

        download = sftp.getFile(_host, _user, _pass, _path, "config.json")
        if download == "Success":
            self.dialogDownloading.dismiss()
            self.manager.updateRequest = True
        else:
            self.dialogDownloading.dismiss()
            self.show_exception(str(download))

    def startUpload(self):
        thistime = time.time()
        while thistime + 2 > time.time():  # 5 seconds
            time.sleep(.5)
        self.uploadConfig()

    def startDownload(self):
        thistime = time.time()
        while thistime + 2 > time.time():  # 5 seconds
            time.sleep(.5)
        self.downloadConfig()

    def closeSaveDialog(self, inst):
        self.dialogSave.dismiss()

    def closeUploadDialog(self, inst):
        self.dialogUpload.dismiss()

    def closeDownloadDialog(self, inst):
        self.dialogDownload.dismiss()

    def closeUploadingDialog(self, inst):
        self.dialogUploading.dismiss()

    def closeDownloadingDialog(self, inst):
        self.dialogDownloading.dismiss()

    def closeExceptionDialog(self, inst):
        self.dialogException.dismiss()

    def show_confirmation_save(self):
        if not self.dialogSave:
            self.dialogSave = MDDialog(
                title="Save settings?",
                size_hint=(None, None),
                size=(600, 500),
                type="alert",
                text="This will update your SFTP settings.",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=self.closeSaveDialog
                    ),
                    MDFlatButton(
                        text="ACCEPT", text_color=self.theme_cls.primary_color, on_release=self.saveEdits
                    ),
                ],
            )
        self.dialogSave.open()

    def show_confirmation_upload(self):
        if not self.dialogUpload:
            self.dialogUpload = MDDialog(
                title="Upload configuration file?",
                size_hint=(None, None),
                size=(600, 500),
                type="alert",
                text="This will transfer config.json to the remote path.",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=self.closeUploadDialog
                    ),
                    MDFlatButton(
                        text="ACCEPT", text_color=self.theme_cls.primary_color, on_release=self.showUploadingDialog
                    ),
                ],
            )
        self.dialogUpload.open()

    def show_confirmation_download(self):
        if not self.dialogDownload:
            self.dialogDownload = MDDialog(
                title="Download configuration file?",
                size_hint=(None, None),
                size=(600, 500),
                type="alert",
                text="This will download the config.json from the remote path and overwrite the local copy on your device.",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=self.closeDownloadDialog
                    ),
                    MDFlatButton(
                        text="ACCEPT", text_color=self.theme_cls.primary_color, on_release=self.showDownloadingDialog
                    ),
                ],
            )
        self.dialogDownload.open()

    def showUploadingDialog(self, inst):
        self.closeUploadDialog(inst)
        if not self.dialogUploading:
            self.dialogUploading = MDDialog(
                title="Uploading configuration file?",
                size_hint=(None, None),
                size=(600, 500),
                type="custom",
                text="",
                content_cls=Progress()
            )
        self.dialogUploading.open()
        if self.dialogUploading:
            upload = threading.Thread(target=self.startUpload)
            upload.start()

    def showDownloadingDialog(self, inst):
        self.closeDownloadDialog(inst)
        if not self.dialogDownloading:
            self.dialogDownloading = MDDialog(
                title="Downloading configuration file?",
                size_hint=(None, None),
                size=(600, 500),
                type="custom",
                text="",
                content_cls=Progress()
            )
        self.dialogDownloading.open()
        if self.dialogDownloading:
            download = threading.Thread(target=self.startDownload)
            download.start()

    def show_exception(self, err):
        if not self.dialogException:
            self.dialogException = MDDialog(
                title="Ooops!?",
                size_hint=(None, None),
                size=(600, 500),
                type="alert",
                text=err,
                buttons=[
                    MDFlatButton(
                        text="DISMISS", text_color=self.theme_cls.primary_color, on_release=self.closeExceptionDialog
                    ),
                ],
            )
        self.dialogException.open()

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
        self.manager.transition =  CardTransition(duration=0.5, direction="down", mode="pop")
        self.manager.current = 'cl_screen'


class EditScreen(Screen,ThemableBehavior):
    #passedId = StringProperty()
    dialog = None
    def on_enter(self):
        global fileData
        data = fileData
        for i in range(len(data["Config"])):
            if data["Config"][i]["Number"] == int(self.manager.statedata):
                self.eName.text = data["Config"][i]["Name"]
                self.eDes.text = data["Config"][i]["Description"]
                self.eCom.text = data["Config"][i]["Command"]
                break

    def saveEdits(self,inst):
        global fileData
        data = fileData
        for i in range(len(data["Config"])):
            if data["Config"][i]["Number"] == int(self.manager.statedata):
                data["Config"][i]["Name"] = self.eName.text
                data["Config"][i]["Description"] = self.eDes.text
                data["Config"][i]["Command"] = self.eCom.text
                break
        with open("config.json", "w") as file_write:
            file_write.write(json.dumps(data, sort_keys=True,
                                        indent=4, separators=(',', ': ')))
            self.manager.updateRequest = True
            self.dialog.dismiss()

    def closeDialog(self, inst):
        self.dialog.dismiss()

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Save changes?",
                size_hint=(None, None),
                size=(600, 500),
                type="alert",
                text="This will update config.json.",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=self.closeDialog
                    ),
                    MDFlatButton(
                        text="ACCEPT", text_color=self.theme_cls.primary_color, on_release=self.saveEdits
                    ),
                ],
            )
        self.dialog.open()


class SettingsScreen(Screen):
    def goBack(self):
        self.manager.transition = CardTransition(duration=0.5, direction="down", mode="pop")
        self.manager.current = 'cl_screen'


class ViewCodeScreen(Screen):
    def on_enter(self):
        global fileData
        data = fileData
        self.vLabel.text = json.dumps(data, indent=4, sort_keys=True)

    def goBack(self):
        self.manager.transition =  CardTransition(duration=0.5, direction="down", mode="pop")
        self.manager.current = 'cl_screen'


class ListItemWithEdit(TwoLineAvatarIconListItem):
    iconL = StringProperty()
    iconR = StringProperty()

    def on_release(self):
        self.parent.cScreen.manager.statedata = self.id
        self.parent.cScreen.manager.transition = CardTransition(
            duration=0.5, direction="left", mode="push")
        self.parent.cScreen.manager.current = 'e_screen'


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
        global fileData
        itemAdded = f.addToFile()
        if itemAdded:
            self.cList.add_widget(
                ListItemWithEdit(id=str(itemAdded),
                                 text="My new command", iconL="minus", iconR="plus", secondary_text="No description")
            )
        fileData = f.readFile()


class EditBottomToolbar(MDToolbar):
    def goBack(self):
        self.eScreen.manager.transition = CardTransition(
            duration=0.5, direction="right", mode="pop")
        self.eScreen.manager.current = 'cl_screen'


class ManagerScreen(ScreenManager):
    statedata = ObjectProperty()
    updateRequest = ObjectProperty()


class CBuilderApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Lime"
        #self.theme_cls.primary_hue = "300"
        return Builder.load_file("main.kv")

    def on_start(self):
        pass

    def on_stop(self):
        print("CBuilder Closing....")


if __name__ == "__main__":
    CBuilderApp().run()
