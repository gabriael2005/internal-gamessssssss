import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import  QPixmap,QPainter
from PyQt5.QtCore import Qt
from GUI.Game import Game
from GUI.GameWords import GameWords
from GUI.HomePage import HomePage
from GUI.ResultsPage import ResultsPage
from GUI.SelectDifficulty import SelectDifficulty
from GUI.SelectWordRange import SelectWorldRange
from GUI.SettingsPage import SettingsPage
from GUI.SpeedModePage import SpeedModePage
from GUI.StartingPage import StartingPage

from GUI.TitleBar import TitleBar
from GUI.WordRanges import WordRanges

script_directory = os.path.dirname(os.path.abspath(__file__))

class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bg_image = QPixmap(os.path.join(script_directory, '../images/shared/Monkey.png'))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.bg_image)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_page = 0
        self.difficulty = ''
        self.word_range = ''
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove the title bar
        self.setWindowState(Qt.WindowFullScreen)  # Set the application to fullscreen

        self.title_bar = TitleBar(self)
        self.title_bar.exit_button.clicked.connect(self.close_application)
        self.setMenuWidget(self.title_bar)

        # Get the screen dimensions
        screen = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen.width(), screen.height()

        self.home_page = HomePage(screen_width, screen_height)
        self.settings_page = SettingsPage(screen_width, screen_height)
        self.speed_mode_page = SpeedModePage(screen_width, screen_height)
        self.word_ranges_page = WordRanges(screen_width, screen_height)
        self.game_words_page = GameWords(screen_width, screen_height)
        self.select_difficulty_page = SelectDifficulty(screen_width, screen_height)
        self.select_word_range_page = SelectWorldRange(screen_width, screen_height)
        self.starting_page = StartingPage()
        self.results_page = ResultsPage()
        self.game_page = Game(screen_width, screen_height)
        self.initUI()
        

    def initUI(self):
        # Create QColor instances for the background colors
        self.central_widget = BackgroundWidget(self)
        self.setCentralWidget(self.central_widget)

        self.stack_layout = QVBoxLayout(self.central_widget)
        
        self.stack_layout.addWidget(self.speed_mode_page)
        self.stack_layout.addWidget(self.home_page)
        self.stack_layout.addWidget(self.settings_page)
        self.stack_layout.addWidget(self.word_ranges_page)
        self.stack_layout.addWidget(self.game_words_page)
        self.stack_layout.addWidget(self.select_difficulty_page)
        self.stack_layout.addWidget(self.select_word_range_page)
        self.stack_layout.addWidget(self.starting_page)
        self.stack_layout.addWidget(self.game_page)
        self.stack_layout.addWidget(self.results_page)

        self.home_page.settings_button.clicked.connect(self.show_settings_page)
        self.settings_page.speed_mode_clicked.connect(self.show_speed_mode_page)
        self.settings_page.word_ranges_clicked.connect(self.show_word_ranges_page)
        self.settings_page.game_words_clicked.connect(self.show_game_words_page)
        self.home_page.start_button.clicked.connect(self.show_select_difficuly_page)
        self.select_difficulty_page.difficulty_clicked.connect(self.difficulty_clicked)
        self.select_word_range_page.buttonClicked.connect(self.range_selected)
        self.starting_page.counter_finished.connect(self.show_game_page)
        self.game_page.counter_finished.connect(self.show_results_page)
        self.results_page.restart_clicked.connect(self.restart_clicked)

        self.show_home_page()

        self.title_bar.back_button_clicked.connect(self.go_back)
        self.title_bar.add_button_clicked.connect(self.show_add)

    def restart_clicked(self):
        self.current_page = 7
        self.title_bar.back_button.show()
        self.game_page.start(self.difficulty,self.word_range)
        self.game_page.show()
        self.results_page.close()

    def show_add(self):
        if self.current_page == 3:
            self.word_ranges_page.show_add_word_range()
        else:
            self.game_words_page.show_add_widget()

    def go_back(self):
        if self.current_page == 1: 
            self.current_page = 0
            self.show_home_page()
        elif self.current_page == 2:
            self.speed_mode_page.close()
            self.current_page = 1
            self.settings_page.show()
        elif self.current_page == 3:
            self.title_bar.add_button.hide()
            self.current_page = 1
            self.word_ranges_page.close()
            self.settings_page.show()
        elif self.current_page == 4:
            self.current_page = 1
            self.title_bar.add_button.hide()
            self.game_words_page.close()
            self.settings_page.show()
        elif self.current_page == 5:
            self.current_page = 0
            self.show_home_page()
        elif self.current_page == 6:
            self.current_page = 5
            self.select_word_range_page.close()
            self.show_select_difficuly_page()
        elif self.current_page == 7 :
            self.current_page = 6
            self.game_page.timer.deleteLater()
            self.game_page.close()
            self.select_word_range_page.show()
        elif self.current_page == 8:
            self.current_page = 6
            self.results_page.close()
            self.select_word_range_page.show()

    def show_word_ranges_page(self):
        self.current_page = 3
        self.title_bar.add_button.show()
        self.settings_page.hide()
        self.word_ranges_page.show()
    
    def show_game_words_page(self):
        self.current_page = 4
        self.settings_page.hide()
        self.title_bar.add_button.show()
        self.game_words_page.show()

    def show_speed_mode_page(self):
        self.current_page = 2
        self.speed_mode_page.show()
        self.settings_page.hide()

    def show_home_page(self):
        self.current_page = 0
        self.home_page.show()
        self.title_bar.back_button.hide()
        self.settings_page.close()
        self.word_ranges_page.close()
        self.speed_mode_page.close()
        self.game_words_page.close()
        self.select_difficulty_page.close()
        self.select_word_range_page.close()
        self.starting_page.close()
        self.game_page.close()
        self.results_page.close()

    def show_settings_page(self):
        self.current_page = 1
        self.title_bar.back_button.show()
        self.settings_page.show()
        self.home_page.close()

    def show_select_difficuly_page(self):
        self.current_page = 5
        self.home_page.close()
        self.title_bar.back_button.show()
        self.select_difficulty_page.show()
    
    def show_select_word_range_page(self):
        self.select_difficulty_page.close()
        self.current_page = 6
        self.select_word_range_page.restart_ui()
        self.select_word_range_page.show()

    def difficulty_clicked(self,text):
        self.difficulty = text
        self.show_select_word_range_page()

    def show_starting_page(self):
        self.select_word_range_page.close()
        self.starting_page.start()
        self.starting_page.show()
    
    def range_selected(self,text):
        self.word_range = text
        self.title_bar.back_button.close()
        self.show_starting_page()

    def show_game_page(self):
        self.current_page = 7
        self.title_bar.back_button.show()
        self.game_page.start(self.difficulty,self.word_range)
        self.game_page.show()
        self.starting_page.close()

    def show_results_page(self,correct_words,missed_words):
        self.game_page.timer.deleteLater()
        self.game_page.close()
        self.current_page = 8 
        self.results_page.init_ui(correct_words,missed_words)
        self.results_page.show()

    def close_application(self):
        QApplication.quit()
