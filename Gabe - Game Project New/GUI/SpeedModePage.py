import os
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QInputDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal

from GUI.SpeedModeDialog import SpeedModeDialog

script_directory = os.path.dirname(os.path.abspath(__file__))


class SpeedModePage(QWidget):
    speed_mode_clicked = pyqtSignal()

    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create buttons
        slow_mode_image = QPixmap(os.path.join(script_directory, '../images/speed_mode/slow_mode_time.png'))
        self.slow_mode_button = QPushButton(self)
        self.slow_mode_button.setIcon(QIcon(slow_mode_image))
        self.slow_mode_button.setIconSize(slow_mode_image.size())
        self.slow_mode_button.setFixedSize(slow_mode_image.size())
        self.slow_mode_button.setStyleSheet("QPushButton { border: none; }")
        start_x = int(screen_width * 0.5 - slow_mode_image.width() * 0.5)
        start_y = int(screen_height * 0.3 - slow_mode_image.height() * 0.3)
        self.slow_mode_button.move(start_x, start_y)
        self.slow_mode_button.clicked.connect(self.show_slow_mode_input)

        medium_mode_image = QPixmap(os.path.join(script_directory, '../images/speed_mode/medium_mode_time.png'))
        self.medium_mode_button = QPushButton(self)
        self.medium_mode_button.setIcon(QIcon(medium_mode_image))
        self.medium_mode_button.setIconSize(medium_mode_image.size())
        self.medium_mode_button.setFixedSize(medium_mode_image.size())
        self.medium_mode_button.setStyleSheet("QPushButton { border: none; }")
        start_x = int(screen_width * 0.5 - medium_mode_image.width() * 0.5)
        start_y = int(screen_height * 0.45 - medium_mode_image.height() * 0.45)
        self.medium_mode_button.move(start_x, start_y)
        self.medium_mode_button.clicked.connect(self.show_medium_mode_input)

        fast_mode_image = QPixmap(os.path.join(script_directory, '../images/speed_mode/fast_mode_time.png'))
        self.fast_mode_button = QPushButton(self)
        self.fast_mode_button.setIcon(QIcon(fast_mode_image))
        self.fast_mode_button.setIconSize(fast_mode_image.size())
        self.fast_mode_button.setFixedSize(fast_mode_image.size())
        self.fast_mode_button.setStyleSheet("QPushButton { border: none; }")
        start_x = int(screen_width * 0.5 - fast_mode_image.width() * 0.5)
        start_y = int(screen_height * 0.6 - fast_mode_image.height() * 0.6)
        self.fast_mode_button.move(start_x, start_y)
        self.fast_mode_button.clicked.connect(self.show_fast_mode_input)

    def show_slow_mode_input(self):
        self.show_custom_dialog('slow')

    def show_medium_mode_input(self):
        self.show_custom_dialog('medium')

    def show_fast_mode_input(self):
        self.show_custom_dialog('fast')

    def show_custom_dialog(self,mode):
        custom_dialog = SpeedModeDialog(self.screen_width, self.screen_height,mode)
        custom_dialog.exec_()