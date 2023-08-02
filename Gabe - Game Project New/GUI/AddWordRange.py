from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QPushButton, QLabel, QDialog, QLineEdit, QVBoxLayout, QHBoxLayout
import os
from PyQt5.QtCore import pyqtSignal

from database.wordRangeManager import insert_word_range

script_directory = os.path.dirname(os.path.abspath(__file__))

class AddWordRange(QDialog):
    new_word_range_added = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Create main vertical layout
        main_layout = QVBoxLayout()

        # Create horizontal layout for minimum letters input
        min_letters_layout = QHBoxLayout()
        self.min_letters_input = QLineEdit(self)
        self.min_letters_input.setPlaceholderText("Min")
        self.min_letters_input.setStyleSheet("QLineEdit { background: #f3f3f3; border: 2px solid #e3e3e3; border-radius: 11px; padding: 15px; font: 24px 'Open Sans', sans-serif; }")
        self.min_letters_input.setFixedSize(180, 80)
        self.min_plus_button = HoverButton(self, "+", base_color="#6fa8dc", hover_color="#7fb7ed", fixed_size=True)
        self.min_plus_button.clicked.connect(self.increment_min_letters)
        self.min_minus_button = HoverButton(self, "-", base_color="#6fa8dc", hover_color="#7fb7ed", fixed_size=True)
        self.min_minus_button.clicked.connect(self.decrement_min_letters)

        min_letters_layout.addWidget(self.min_minus_button)
        min_letters_layout.addWidget(self.min_letters_input)
        min_letters_layout.addWidget(self.min_plus_button)

        # Create horizontal layout for maximum letters input
        max_letters_layout = QHBoxLayout()
        self.max_letters_input = QLineEdit(self)
        self.max_letters_input.setPlaceholderText("Max")
        self.max_letters_input.setStyleSheet("QLineEdit { background: #f3f3f3; border: 2px solid #e3e3e3; border-radius: 11px; padding: 15px; font: 24px 'Open Sans', sans-serif; }")
        self.max_letters_input.setFixedSize(180, 80)
        self.max_plus_button = HoverButton(self, "+", base_color="#6fa8dc", hover_color="#7fb7ed", fixed_size=True)
        self.max_plus_button.clicked.connect(self.increment_max_letters)
        self.max_minus_button = HoverButton(self, "-", base_color="#6fa8dc", hover_color="#7fb7ed", fixed_size=True)
        self.max_minus_button.clicked.connect(self.decrement_max_letters)

        max_letters_layout.addWidget(self.max_minus_button)
        max_letters_layout.addWidget(self.max_letters_input)
        max_letters_layout.addWidget(self.max_plus_button)

        # Create horizontal layout for buttons
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.save_button.setStyleSheet("background: #6fa8dc; border-radius: 11px; padding: 30px 70px; color: #ffffff; font: normal bold 25px/1 'Open Sans', sans-serif;")
        self.save_button.clicked.connect(self.save_data)
        self.close_button = QPushButton("Close", self)
        self.close_button.setStyleSheet("background: #cc0000; border-radius: 11px; padding: 30px 70px; color: #ffffff; font: normal bold 25px/1 'Open Sans', sans-serif;")
        self.close_button.clicked.connect(self.reject)

        buttons_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(self.close_button, alignment=Qt.AlignCenter)

        # Add layouts to the main layout
        main_layout.addLayout(min_letters_layout)
        main_layout.addLayout(max_letters_layout)
        main_layout.addLayout(buttons_layout)

        # Set the main layout as the main layout for the dialog
        self.setLayout(main_layout)

        # Set the size of the QDialog
        self.resize(500, 300)

    def increment_min_letters(self):
        self.current_min = int(self.min_letters_input.text() or 0)
        self.min_letters_input.setText(str(self.current_min + 1))

    def decrement_min_letters(self):
        self.current_min = int(self.min_letters_input.text() or 0)
        new_min = max(self.current_min - 1, 0)
        self.min_letters_input.setText(str(new_min))

    def increment_max_letters(self):
        self.current_max = int(self.max_letters_input.text() or 0)
        self.max_letters_input.setText(str(self.current_max + 1))

    def decrement_max_letters(self):
        self.current_max = int(self.max_letters_input.text() or 0)
        new_max = max(self.current_max - 1, 0)
        self.max_letters_input.setText(str(new_max))

    def save_data(self):
        try:
            min = int(self.min_letters_input.text())
            max = int(self.max_letters_input.text())
            if max > min:
                insert_word_range(min,max)
                self.new_word_range_added.emit() 
                self.accept()
        except:
            pass

class HoverButton(QPushButton):
    def __init__(self, parent, text, base_color, hover_color, fixed_size=False):
        super().__init__(text, parent)
        self.base_color = base_color
        self.hover_color = hover_color
        self.fixed_size = fixed_size
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
            self.setStyleSheet(f"background: {self.hover_color}; border-radius: 11px; padding: 5px; color: #ffffff; font: normal bold 25px/1 'Open Sans', sans-serif;")
        else:
            self.setStyleSheet(f"background: {self.base_color}; border-radius: 11px; padding: 5px; color: #ffffff; font: normal bold 25px/1 'Open Sans', sans-serif;")
        if self.fixed_size:
            self.setFixedSize(80, 80)
