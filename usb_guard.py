from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
import os
import base64
import string
import shutil
import logging
import threading
import win32api

class USBGuardApp(App):
    def __init__(self):
        super().__init__()
        self.usb_path = None
        self.password = None
        self.options_shown = False
        self.prev_disks = set()
        self.theme_dark = True
        self.cancel_flag = False

    def build(self):
        self.apply_theme()
        Window.maximize()  # Разворачиваем окно на весь экран
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        self.header = Label(
            text='[b]USB Guard[/b] Шифрование данных. [color=#3500D3][i]Не для реальной защиты. программа создана в учебных целях[/i][/color]',
            markup=True,
            font_size='24sp',
            color=(1, 1, 1, 1) if self.theme_dark else (0, 0, 0, 1),
            size_hint_y=None,
            height=60
        )
        self.layout.add_widget(self.header)

        # Убираем status_label, он больше не нужен

        self.disk_spinner = Spinner(
            text='Выбрать диск',
            values=self.get_available_disks(),
            background_color=(0.14, 0, 0.56, 1),  # #240090
            background_normal='',
            color=(1, 1, 1, 1) if self.theme_dark else (0, 0, 0, 1),
            size_hint_y=None,
            height=60,
            font_size='18sp'
        )
        self.disk_spinner.bind(text=self.on_disk_selected)
        self.layout.add_widget(self.disk_spinner)

        self.process_label = Label(
            text='',
            font_size='20sp',
            color=(1, 1, 1, 1) if self.theme_dark else (0, 0, 0, 1),
            size_hint_y=None,
            height=60
        )
        self.layout.add_widget(self.process_label)

        self.progress_container = BoxLayout(orientation='vertical', size_hint_y=None, height=60)
        self.layout.add_widget(self.progress_container)

        self.options_container = BoxLayout(orientation='vertical', spacing=20)
        self.layout.add_widget(self.options_container)

        # Пустое пространство перед футером
        self.spacer = Label(
            text='',
            size_hint_y=None,
            height=60
        )
        self.layout.add_widget(self.spacer)

        self.footer = Label(
            text='[i]Создано с помощью Grok и narkomanchik228[/i]',
            markup=True,
            font_size='16sp',
            color=(1, 1, 1, 1) if self.theme_dark else (0, 0, 0, 1),
            size_hint_y=None,
            height=40
        )
        self.layout.add_widget(self.footer)

        Clock.schedule_interval(self.update_disk_list, 2.0)
        Clock.schedule_interval(self.check_usb_connection, 1.0)
        return self.layout

    def apply_theme(self):
        if self.theme_dark:
            Window.clearcolor = (0.16, 0.16, 0.16, 1)  # #282828
        else:
            Window.clearcolor = (1, 1, 1, 1)  # Белый фон

    def get_available_disks(self):
        drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:/"
            if os.path.exists(drive) and drive != "C:/":
                try:
                    name = win32api.GetVolumeInformation(drive)[0] or "Без имени"
                except:
                    name = "Без имени"
                drives.append(f"{drive} ({name})")
        return drives

    def update_disk_list(self, dt):
        new_values = self.get_available_disks()
        if set(new_values) != set(self.disk_spinner.values):
            self.disk_spinner.values = new_values
            if not self.usb_path or self.usb_path not in [v.split(' (')[0] for v in new_values]:
                self.clear_options()
                self.disk_spinner.text = 'Выбрать диск'
                self.process_label.text = ''

    def on_disk_selected(self, spinner, text):
        if text != 'Выбрать диск':
            self.usb_path = text.split(' (')[0]
            self.process_label.text = ''
            self.check_usb_connection(0)
            logging.basicConfig(filename=os.path.join(self.usb_path, 'usb_guard_log.txt'),
                                level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s')

    def check_usb_connection(self, dt):
        current_disks = set(self.get_available_disks())
        if current_disks != self.prev_disks:
            if len(current_disks) > len(self.prev_disks):
                self.show_popup('Флешка подключена', 'Обнаружен новый диск!')
            elif len(current_disks) < len(self.prev_disks):
                self.show_popup('Флешка отключена', 'Диск исчез...')
            self.prev_disks = current_disks
        if self.usb_path and os.path.exists(self.usb_path):
            if not self.options_shown:
                self.show_options()
        else:
            self.clear_options()
            self.process_label.text = ''

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message, color=(1, 1, 1, 1) if self.theme_dark else (0, 0, 0, 1)), size_hint=(0.8, 0.5))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 3)

    def show_options(self):
        self.options_shown = True
        self.options_container.clear_widgets()

        self.password_input = TextInput(
            hint_text='Введите пароль',
            multiline=False,
            background_color=(0.05, 0, 0.19, 1) if self.theme_dark else (0.53, 0.70, 0.82, 1),  # #0C0032 или #86B3D1
            foreground_color=(1, 1, 1, 1) if self.theme_dark else (0, 0, 0, 1),
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )
        self.encrypt_button = Button(
            text='Зашифровать',
            background_color=(0.20, 0, 0.83, 1),  # #3500D3
            background_normal='',
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )
        self.decrypt_button = Button(
            text='Расшифровать',
            background_color=(0.14, 0, 0.56, 1),  # #240090
            background_normal='',
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )
        self.theme_button = Button(
            text='Светлая тема' if self.theme_dark else 'Тёмная тема',
            background_color=(0.09, 0, 0.38, 1),  # #190061
            background_normal='',
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )
        self.back_button = Button(
            text='Назад',
            background_color=(0.53, 0.70, 0.82, 1),  # #86B3D1
            background_normal='',
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )

        self.encrypt_button.bind(on_press=self.encrypt_action)
        self.decrypt_button.bind(on_press=self.decrypt_action)
        self.theme_button.bind(on_press=self.toggle_theme)
        self.back_button.bind(on_press=self.return_to_disk_selection)

        for widget in [self.password_input, self.encrypt_button, self.decrypt_button, self.theme_button, self.back_button]:
            widget.opacity = 0
            self.options_container.add_widget(widget)
            anim = Animation(opacity=1, duration=0.5, t='out_quad') + Animation(opacity=0.8, duration=0.2)
            anim.start(widget)

        self.disk_spinner.disabled = True

    def toggle_theme(self, instance):
        self.theme_dark = not self.theme_dark
        self.apply_theme()
        self.header.color = (1, 1, 1, 1) if self.theme_dark else (0, 0, 0, 1)
        self.process_label.color = (1, 1, 1, 1) if self.theme_dark else (0, 0, 0, 1)
        self.password_input.background_color = (0.05, 0, 0.19, 1) if self.theme_dark else (0.53, 0.70, 0.82, 1)
        self.password_input.foreground_color = (1, 1, 1, 1) if self.theme_dark else (0, 0, 0, 1)
        self.disk_spinner.color = (1, 1, 1, 1) if self.theme_dark else (0, 0, 0, 1)
        self.theme_button.text = 'Светлая тема' if self.theme_dark else 'Тёмная тема'
        self.footer.color = (1, 1, 1, 1) if self.theme_dark else (0, 0, 0, 1)
        for widget in self.options_container.children:
            anim = Animation(opacity=1, duration=0.3, t='out_quad')
            anim.start(widget)

    def clear_options(self):
        if self.options_shown:
            self.options_container.clear_widgets()
            self.progress_container.clear_widgets()
            self.options_shown = False
            self.process_label.text = ''

    def show_task_complete(self, message):
        self.clear_options()
        self.process_label.text = f'{message}\n[b]Задача выполнена ✓[/b]'
        self.process_label.markup = True

        self.back_button = Button(
            text='Назад',
            background_color=(0.53, 0.70, 0.82, 1),  # #86B3D1
            background_normal='',
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )
        self.back_button.bind(on_press=self.return_to_disk_selection)
        self.options_container.add_widget(self.back_button)
        anim = Animation(opacity=1, duration=0.5, t='out_quad')
        anim.start(self.back_button)

    def return_to_disk_selection(self, instance):
        self.cancel_flag = True
        self.clear_options()
        self.usb_path = None
        self.disk_spinner.text = 'Выбрать диск'
        self.disk_spinner.disabled = False
        self.process_label.text = ''

    def show_progress(self, message):
        self.options_container.clear_widgets()
        self.progress_container.clear_widgets()
        self.process_label.text = message

        self.progress_bar = ProgressBar(max=100, value=0, size_hint_y=None, height=40)
        self.progress_container.add_widget(self.progress_bar)

        self.cancel_button = Button(
            text='Отмена',
            background_color=(0.20, 0, 0.83, 1),  # #3500D3
            background_normal='',
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )
        self.cancel_button.bind(on_press=self.return_to_disk_selection)
        self.progress_container.add_widget(self.cancel_button)

        return self.progress_bar

    def encrypt_action(self, instance):
        try:
            self.password = self.password_input.text.encode('utf-8')
            if not self.password:
                self.process_label.text = 'Введите пароль!'
                return
            logging.info("Создание резервной копии перед шифрованием")
            backup_dir = os.path.join(self.usb_path, 'Backup')
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            control_file = os.path.join(self.usb_path, 'control.txt')
            with open(control_file, 'w', encoding='utf-8') as f:
                f.write('ХУЙ')
            for root, _, files in os.walk(self.usb_path):
                for file in files:
                    src_path = os.path.join(root, file)
                    if 'Backup' not in src_path:
                        dst_path = os.path.join(backup_dir, os.path.relpath(src_path, self.usb_path))
                        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                        shutil.copy2(src_path, dst_path)
            logging.info(f"Резервная копия создана в {backup_dir}")
            files = [os.path.join(root, f) for root, _, fs in os.walk(self.usb_path) for f in fs if 'Backup' not in root]
            progress_bar = self.show_progress('Шифрование...')
            self.cancel_flag = False
            threading.Thread(target=self.encrypt_all_files_with_progress, args=(progress_bar, files)).start()
        except Exception as e:
            logging.error(f"Ошибка при создании резервной копии или шифровании: {str(e)}")
            self.process_label.text = f'Ошибка шифрования: {str(e)}'

    def decrypt_action(self, instance):
        try:
            self.password = self.password_input.text.encode('utf-8')
            if not self.password:
                self.process_label.text = 'Введите пароль!'
                return
            control_file = os.path.join(self.usb_path, 'control.txt')
            if not os.path.exists(control_file):
                self.process_label.text = 'Контрольный файл не найден!'
                return
            with open(control_file, 'rb') as f:
                encoded_data = f.read()
            try:
                encrypted_data = base64.b64decode(encoded_data)
                key = self.password * (len(encrypted_data) // len(self.password) + 1)
                key = key[:len(encrypted_data)]
                decrypted_data = bytes(a ^ b for a, b in zip(encrypted_data, key))
                if decrypted_data.decode('utf-8') != 'ХУЙ':
                    self.process_label.text = 'Неверный пароль!'
                    return
            except Exception:
                self.process_label.text = 'Неверный пароль!'
                return
            files = [os.path.join(root, f) for root, _, fs in os.walk(self.usb_path) for f in fs if 'Backup' not in root]
            progress_bar = self.show_progress('Расшифровка...')
            self.cancel_flag = False
            threading.Thread(target=self.decrypt_all_files_with_progress, args=(progress_bar, files)).start()
        except Exception as e:
            logging.error(f"Ошибка при запуске расшифровки: {str(e)}")
            self.process_label.text = f'Ошибка расшифровки: {str(e)}'

    def encrypt_all_files_with_progress(self, progress_bar, files):
        logging.info(f"Начало шифрования диска {self.usb_path}")
        total_files = len(files)
        if total_files == 0:
            logging.info("Нет файлов для шифрования")
            Clock.schedule_once(lambda dt: self.show_task_complete('Файлы зашифрованы'))
            return

        for i, file_path in enumerate(files):
            if self.cancel_flag:
                logging.info("Шифрование прервано пользователем")
                Clock.schedule_once(lambda dt: self.return_to_disk_selection(None))
                return
            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
                key = self.password * (len(data) // len(self.password) + 1)
                key = key[:len(data)]
                encrypted_data = bytes(a ^ b for a, b in zip(data, key))
                encoded_data = base64.b64encode(encrypted_data)
                with open(file_path, 'wb') as f:
                    f.write(encoded_data)
                logging.info(f"Успешно зашифрован файл: {file_path}")
            except Exception as e:
                logging.error(f"Ошибка шифрования файла {file_path}: {str(e)}")
                Clock.schedule_once(lambda dt: self.process_label.setter('text')(self, f'Ошибка шифрования файла {file_path}: {str(e)}'))
                Clock.schedule_once(lambda dt: self.return_to_disk_selection(None))
                return
            Clock.schedule_once(lambda dt: setattr(progress_bar, 'value', (i + 1) * 100 / total_files))

        backup_dir = os.path.join(self.usb_path, 'Backup')
        if os.path.exists(backup_dir):
            try:
                shutil.rmtree(backup_dir)
                logging.info(f"Папка Backup удалена: {backup_dir}")
            except Exception as e:
                logging.error(f"Ошибка при удалении папки Backup: {str(e)}")
                Clock.schedule_once(lambda dt: self.process_label.setter('text')(self, f'Ошибка удаления Backup: {str(e)}'))

        logging.info("Шифрование завершено")
        Clock.schedule_once(lambda dt: self.show_task_complete('Файлы зашифрованы'))

    def decrypt_all_files_with_progress(self, progress_bar, files):
        logging.info(f"Начало расшифровки диска {self.usb_path}")
        total_files = len(files)
        if total_files == 0:
            logging.info("Нет файлов для расшифровки")
            Clock.schedule_once(lambda dt: self.show_task_complete('Файлы расшифрованы'))
            return

        for i, file_path in enumerate(files):
            if self.cancel_flag:
                logging.info("Расшифровка прервана пользователем")
                Clock.schedule_once(lambda dt: self.return_to_disk_selection(None))
                return
            try:
                with open(file_path, 'rb') as f:
                    encoded_data = f.read()
                encrypted_data = base64.b64decode(encoded_data)
                key = self.password * (len(encrypted_data) // len(self.password) + 1)
                key = key[:len(encrypted_data)]
                original_data = bytes(a ^ b for a, b in zip(encrypted_data, key))
                with open(file_path, 'wb') as f:
                    f.write(original_data)
                logging.info(f"Успешно расшифрован файл: {file_path}")
            except Exception as e:
                logging.error(f"Ошибка расшифровки файла {file_path}: {str(e)}")
                Clock.schedule_once(lambda dt: self.process_label.setter('text')(self, f'Ошибка расшифровки файла {file_path}: {str(e)}'))
                Clock.schedule_once(lambda dt: self.return_to_disk_selection(None))
                return
            Clock.schedule_once(lambda dt: setattr(progress_bar, 'value', (i + 1) * 100 / total_files))

        control_file = os.path.join(self.usb_path, 'control.txt')
        if os.path.exists(control_file):
            try:
                os.remove(control_file)
                logging.info(f"Контрольный файл удалён: {control_file}")
            except Exception as e:
                logging.error(f"Ошибка при удалении контрольного файла: {str(e)}")
                Clock.schedule_once(lambda dt: self.process_label.setter('text')(self, f'Ошибка удаления контрольного файла: {str(e)}'))

        logging.info("Расшифровка завершена")
        Clock.schedule_once(lambda dt: self.show_task_complete('Файлы расшифрованы'))


if __name__ == '__main__':
    try:
        USBGuardApp().run()
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
        input("Нажмите Enter для выхода...")