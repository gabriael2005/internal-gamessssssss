import os
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt,pyqtSignal


script_directory = os.path.dirname(os.path.abspath(__file__))

class SettingsPage(QWidget):
    speed_mode_clicked = pyqtSignal()
    word_ranges_clicked = pyqtSignal()
    game_words_clicked = pyqtSignal()
    
    def __init__(self, screen_width, screen_height):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create buttons
        speed_mode_image = QPixmap(os.path.join(script_directory,'../images/settings/speed_mode.png'))
        self.speed_mode_button = QPushButton(self)
        self.speed_mode_button.setIcon(QIcon(speed_mode_image))
        self.speed_mode_button.setIconSize(speed_mode_image.size())
        self.speed_mode_button.setFixedSize(speed_mode_image.size())
        self.speed_mode_button.setStyleSheet("QPushButton { border: none; }")
        start_x = int(screen_width * 0.5 - speed_mode_image.width() * 0.5)
        start_y = int(screen_height * 0.3 - speed_mode_image.height() * 0.3)
        self.speed_mode_button.move(start_x, start_y)
        self.speed_mode_button.clicked.connect(self.speed_mode)

        word_ranges_image = QPixmap(os.path.join(script_directory,'../images/settings/word_ranges.png'))
        self.word_ranges_button = QPushButton(self)
        self.word_ranges_button.setIcon(QIcon(word_ranges_image))
        self.word_ranges_button.setIconSize(word_ranges_image.size())
        self.word_ranges_button.setFixedSize(word_ranges_image.size())
        self.word_ranges_button.setStyleSheet("QPushButton { border: none; }")
        start_x =  int(screen_width * 0.5 - word_ranges_image.width() * 0.5)
        start_y = int(screen_height * 0.45 - word_ranges_image.height() * 0.45)
        self.word_ranges_button.move(start_x, start_y)
        self.word_ranges_button.clicked.connect(self.word_ranges)

        start_game_words_image = QPixmap(os.path.join(script_directory,'../images/settings/game_words.png'))
        self.game_words_button = QPushButton(self)
        self.game_words_button.setIcon(QIcon(start_game_words_image))
        self.game_words_button.setIconSize(start_game_words_image.size())
        self.game_words_button.setFixedSize(start_game_words_image.size())
        self.game_words_button.setStyleSheet("QPushButton { border: none; }")
        start_x = int(screen_width * 0.5 - start_game_words_image.width() * 0.5)
        start_y = int(screen_height * 0.6 - start_game_words_image.height() * 0.6)
        self.game_words_button.move(start_x, start_y)
        self.game_words_button.clicked.connect(self.game_words)

    def game_words(self):
        print("game words clicked!")
        self.game_words_clicked.emit()
    
    def speed_mode(self):
        print("speed mode clicked!")
        self.speed_mode_clicked.emit()
    
    def word_ranges(self):
        print("word ranges clicked!")
        self.word_ranges_clicked.emit()