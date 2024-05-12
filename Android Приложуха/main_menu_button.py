from kivy.uix.button import Button

class MainMenuButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Back to Main Menu"
        self.size_hint = (None, None)
        self.width = 200
        self.height = 50
        self.pos_hint = {"center_x": 0.5, "center_y": 0.1}
        self.bind(on_press=self.go_to_main_menu)

    def go_to_main_menu(self, instance):
        self.manager.current = "instructions"
