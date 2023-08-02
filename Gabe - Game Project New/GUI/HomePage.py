import os
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QIcon

script_directory = os.path.dirname(os.path.abspath(__file__))

class HomePage(QWidget):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        # Set app title
        app_title_label = QLabel("Gabe Spelling Game", self)
        app_title_label.setStyleSheet("font-size: 60px; font-weight: bold;")
        title_x = int(screen_width * 0.46 - app_title_label.width() * 0.4)
        title_y = int(screen_height * 0.1)
        app_title_label.move(title_x, title_y)

        # Create buttons
        start_button_image = QPixmap(os.path.join(script_directory, '../images/home/start.png'))
        self.start_button = QPushButton(self)
        self.start_button.setIcon(QIcon(start_button_image))
        self.start_button.setIconSize(start_button_image.size())
        self.start_button.setFixedSize(start_button_image.size())
        self.start_button.setStyleSheet("QPushButton { border: none; }")
        start_x = int(screen_width * 0.5 - start_button_image.width() * 0.5)
        start_y = int(screen_height * 0.3 - start_button_image.height() * 0.3)
        self.start_button.move(start_x, start_y)
        self.start_button.clicked.connect(self.start_button_clicked)

        settings_button_image = QPixmap(os.path.join(script_directory, '../images/home/settings.png'))
        self.settings_button = QPushButton(self)
        self.settings_button.setIcon(QIcon(settings_button_image))
        self.settings_button.setIconSize(settings_button_image.size())
        self.settings_button.setFixedSize(settings_button_image.size())
        self.settings_button.setStyleSheet("QPushButton { border: none; }")
        settings_x = int(screen_width * 0.5 - settings_button_image.width() * 0.5)
        settings_y = int(screen_height * 0.45 - settings_button_image.height() * 0.45)
        self.settings_button.move(settings_x, settings_y)
        self.settings_button.clicked.connect(self.settings_clicked)

    def settings_clicked(self):
        print("Settings button clicked!")

    def start_button_clicked(self):
        print("Start button clicked!")
