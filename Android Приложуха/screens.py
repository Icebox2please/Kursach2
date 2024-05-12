from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from database import Database
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

class ActionSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(ActionSelectionScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text='Select Action', font_size=50))
        layout.add_widget(Button(text='Register', on_press=self.register_action))
        layout.add_widget(Button(text='Login', on_press=self.login_action))
        self.add_widget(layout)

    def register_action(self, instance):
        self.manager.current = 'register'

    def login_action(self, instance):
        self.manager.current = 'login'

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text='Register', font_size=50))
        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(Button(text='Register', on_press=self.register))
        self.add_widget(layout)

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if not username or not password:
            popup = Popup(title='Error', content=Label(text='Please enter both username and password.'), size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        db = Database("my_database.db")
        db.create_users_table()

        try:
            db.register_user(username, password)
            popup = Popup(title='Success', content=Label(text='Registration successful!'), size_hint=(None, None), size=(400, 200))
            popup.open()
            self.manager.current = 'login'
        except Exception as e:
            popup = Popup(title='Error', content=Label(text=str(e)), size_hint=(None, None), size=(400, 200))
            popup.open()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text='Login', font_size=50))
        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(Button(text='Login', on_press=self.login))
        self.add_widget(layout)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if not username or not password:
            popup = Popup(title='Error', content=Label(text='Please enter both username and password.'), size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        db = Database("my_database.db")
        db.create_users_table()

        if db.login_user(username, password):
            popup = Popup(title='Success', content=Label(text='Login successful!'), size_hint=(None, None), size=(400, 200))
            popup.open()
            self.manager.current = 'main_menu'
        else:
            popup = Popup(title='Error', content=Label(text='Invalid username or password.'), size_hint=(None, None), size=(400, 200))
            popup.open()

class InstructionsScreen(Screen):
    def __init__(self, **kwargs):
        super(InstructionsScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text='Instructions', font_size=50))
        layout.add_widget(Label(text='Welcome to our app!', font_size=20))
        layout.add_widget(Label(text='Instructions:'))
        layout.add_widget(Label(text='- To create a new test, press "Create Test" on the main menu.'))
        layout.add_widget(Label(text='- To start a test, press "Start Test" on the main menu.'))
        layout.add_widget(Label(text='- To view results, press "View Results" on the main menu.'))
        layout.add_widget(Button(text='Back to Main Menu', on_press=self.back_to_main_menu))
        self.add_widget(layout)

    def back_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text='Main Menu', font_size=50))
        layout.add_widget(Button(text='Start Test', on_press=self.show_test_selection))  # Изменено на вызов метода show_test_selection
        layout.add_widget(Button(text='View Results'))
        layout.add_widget(Button(text='Instructions', on_press=self.show_instructions))
        layout.add_widget(Button(text='Create Test', on_press=self.create_test))
        self.add_widget(layout)

    def show_test_selection(self, instance):
        self.manager.current = 'test_selection'  # Переходим на экран с выбором тестов

    def show_instructions(self, instance):
        self.manager.current = 'instructions'

    def create_test(self, instance):
        current_test_id = 1
        create_test_screen = CreateTestScreen(current_test_id=current_test_id)
        self.manager.current = 'create_test'


class TestSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(TestSelectionScreen, self).__init__(**kwargs)
        self.selected_test_id = None  # Атрибут для хранения выбранного test_id

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Button(text='Choose Test', on_press=self.show_test_selection))
        self.add_widget(layout)

    def show_test_selection(self, instance):
        db = Database("my_database.db")  # Путь к вашей базе данных
        available_tests = db.get_available_tests()

        if not available_tests:
            popup = Popup(title='No Tests Available', content=Label(text='There are no tests available.'), size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        popup_content = BoxLayout(orientation='vertical', padding=10)
        popup = Popup(title='Choose Test', content=popup_content, size_hint=(None, None), size=(400, 400))

        for test_id, test_name in available_tests:
            button = Button(text=test_name, size_hint=(1, None), height=40)
            button.bind(on_press=lambda instance, test_id=test_id: self.select_test(test_id, popup))
            popup_content.add_widget(button)

        popup.open()

    def select_test(self, test_id, popup):
        # Сохраняем выбранный test_id
        self.selected_test_id = test_id
        # Переходим на экран теста
        test_screen = TestScreen(name='test')
        test_screen.test_id = test_id
        self.manager.add_widget(test_screen)
        self.manager.current = 'test'
        popup.dismiss()


class TestScreen(Screen):
    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        self.test_id = kwargs.get('test_id')

    def on_enter(self):
        # Вызывается при входе на экран
        print("Test ID:", self.test_id)

    def on_leave(self):
        # Вызывается при выходе с экрана
        pass



class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        # результаты потом реализую

class CreateTestScreen(Screen):
    def __init__(self, current_test_id=None, **kwargs):
        super(CreateTestScreen, self).__init__(**kwargs)
        self.current_test_id = current_test_id
        layout = GridLayout(cols=1, padding=10)

        self.question_input = TextInput(hint_text='Enter question', multiline=False)
        self.answer_input = TextInput(hint_text='Enter answer', multiline=False)

        self.next_question_button = Button(text='Next Question', on_press=self.next_question)
        self.finish_button = Button(text='Finish Test', on_press=self.finish_test)
        self.back_to_main_menu_button = Button(text='Back to Main Menu', on_press=self.back_to_main_menu)

        layout.add_widget(Label(text='Create Test', font_size=50))
        layout.add_widget(self.question_input)
        layout.add_widget(self.answer_input)
        layout.add_widget(self.next_question_button)
        layout.add_widget(self.finish_button)
        layout.add_widget(self.back_to_main_menu_button)

        self.add_widget(layout)

        self.db = Database("my_database.db")  # Путь к вашей базе данных

        # Создание пустого списка вопросов при создании экрана
        self.questions_list = []

    def next_question(self, instance):
        question = self.question_input.text
        answer = self.answer_input.text

        # Добавляем вопрос и ответ в список вопросов
        self.questions_list.append((question, answer))

        # Очищаем поля ввода
        self.question_input.text = ''
        self.answer_input.text = ''

    def finish_test(self, instance):
        if self.questions_list:
            # Создаем всплывающее окно для ввода имени теста
            popup_content = GridLayout(cols=1, padding=10)
            test_name_input = TextInput(hint_text='Enter test name', multiline=False)
            ok_button = Button(text='OK', size_hint=(1, None), height=40)
            popup_content.add_widget(test_name_input)
            popup_content.add_widget(ok_button)
            popup = Popup(title='Enter Test Name', content=popup_content, size_hint=(None, None), size=(400, 200))
            ok_button.bind(on_press=lambda instance: self.save_test(test_name_input.text, popup))
            popup.open()
        else:
            # Предупреждение, если список вопросов пуст
            popup = Popup(title='Warning', content=Label(text='Please add at least one question.'), size_hint=(None, None), size=(400, 200))
            popup.open()

    def save_test(self, test_name, popup):
        # Вызываем метод save_test из базы данных, передавая имя теста и список вопросов
        self.db.save_test(test_name, self.questions_list)

        # Закрываем всплывающее окно
        popup.dismiss()

        # Переходим на главное меню
        self.manager.current = 'main_menu'

    def back_to_main_menu(self, instance):
        self.manager.current = 'main_menu'
