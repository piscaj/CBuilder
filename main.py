from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior

class CBuilderApp(MDApp):
	
	data = {
		'code-braces': 'New',
		'send': 'Send',
		'settings': 'Settings',
      	}
     
	column = [
		('#', 'dp(30)'),
		('Name','dp(30)'),
		]
      	
	row = [
		('1','2'),
      	]
      	
	def build(self):#
        #self.theme_cls.primary_palette = "Red"
		self.theme_cls.theme_style = "Dark"
		return Builder.load_file("main.kv")

if __name__ == "__main__":
    CBuilderApp().run