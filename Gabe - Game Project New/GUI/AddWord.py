from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QDialog, QLineEdit, QHBoxLayout
import os
from PyQt5.QtCore import pyqtSignal
from database.WordManager import insert_word

script_directory = os.path.dirname(os.path.abspath(__file__))

class AddWord(QDialog):

    new_word_added = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.save_button = HoverButton(self, "Save", base_color="#6fa8dc", hover_color="#7fb7ed")
        self.save_button.setStyleSheet("background: #6fa8dc; border-radius: 11px; padding: 30px 70px; color: #ffffff; font: normal bold 30px/1 'Open Sans', sans-serif;")
        self.save_button.resize(50, 50)
        self.save_button.clicked.connect(self.add_new_word)

        self.close_button = HoverButton(self, "Close", base_color="#cc0000", hover_color="#ff0000")
        self.close_button.setStyleSheet("background: #cc0000; border-radius: 11px; padding: 30px 70px; color: #ffffff; font: normal bold 30px/1 'Open Sans', sans-serif;")
        self.close_button.clicked.connect(self.reject)  # Connect clicked signal to the reject method

        # Create the QLineEdit for the input
        self.input_lineedit = QLineEdit(self)
        self.input_lineedit.setPlaceholderText("Enter your new word")
        self.input_lineedit.setStyleSheet("QLineEdit { background: #f3f3f3; border: 2px solid #e3e3e3; border-radius: 11px; padding: 20px; font: 24px 'Open Sans', sans-serif; }")

        # Create a QHBoxLayout to arrange the buttons horizontally
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.close_button)

        # Create a QVBoxLayout to arrange the widgets
        main_layout = QVBoxLayout(self)  # Pass the parent to QVBoxLayout
        main_layout.addWidget(self.input_lineedit)
        main_layout.addLayout(buttons_layout)

        # Set the size of the QDialog
        self.resize(700, 200)

    def add_new_word(self):
        if self.input_lineedit.text():
            new_word = self.input_lineedit.text()
            insert_word(new_word)
            self.new_word_added.emit(new_word) 
            self.close()

class HoverButton(QPushButton):
    def __init__(self, parent, text, base_color, hover_color):
        super().__init__(text, parent)
        self.base_color = base_color
        self.hover_color = hover_color
        self.hovered = False
        self.update_background()
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.hovered = True
        self.update_background()

    def leaveEvent(self, event):
        self.hovered = False
        self.update_background()

    def update_background(self):
        if self.hovered:
            self.setStyleSheet(f"background: {self.hover_color}; border-radius: 11px; padding: 30px 70px; color: #ffffff; font: normal bold 30px/1 'Open Sans', sans-serif;")
        else:
            self.setStyleSheet(f"background: {self.base_color}; border-radius: 11px; padding: 30px 70px; color: #ffffff; font: normal bold 30px/1 'Open Sans', sans-serif;")

