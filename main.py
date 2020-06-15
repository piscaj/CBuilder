import kivy
from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineAvatarIconListItem, IconRightWidget, IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons



class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''

    icon = StringProperty("android")

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''

class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''

    icon = StringProperty("android")

class CBuilderApp(MDApp):
    
    data = {
		'code-braces': 'New',
		'send': 'Send',
		'settings': 'Settings'
      	}

    def build(self):
        #self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("main.kv")
    
    def on_start(self):
        icons = list(md_icons.keys())
        for i in range(30):
            self.root.ids.scroll.add_widget(
                ListItemWithCheckbox(text=f"Item {i}", icon=icons[i])
            )

if __name__ == "__main__":
    CBuilderApp().run()