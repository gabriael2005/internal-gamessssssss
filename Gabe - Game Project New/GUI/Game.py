import os
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QPushButton, QVBoxLayout, QScrollArea, QLineEdit
from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal

from database.TimerManager import get_time_by_mode
from database.WordManager import get_words_list_in_range

class Game(QWidget):
    counter_finished = pyqtSignal(list, list)
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.timer_label = QLabel("0", self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("color: white; font: bold 100px; background-color: #6fa8dc; border-radius: 20px; padding: 20px;")
        self.timer_label.setFixedSize(200, 150)

        # Create the restart button
        self.restart_button = QPushButton("Restart", self)
        self.restart_button.setStyleSheet("color: white; font: bold 30px; background-color: #6fa8dc; border-radius: 20px; padding: 20px;")
        self.restart_button.setFixedSize(200, 80)
        self.restart_button.clicked.connect(self.restart_game)

        self.layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)
        # Add restart button to the layout in the top-left corner
        self.layout.addWidget(self.restart_button, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Create the scroll area
        scroll_area = QScrollArea()
        self.layout.addWidget(scroll_area)

        # Create a widget to hold the buttons
        widget = QWidget()
        scroll_area.setWidgetResizable(True)  # Allow the widget to resize with the scroll area
        scroll_area.setWidget(widget)

        inner_layout = QGridLayout()
        inner_layout.setHorizontalSpacing(2)  # Set the horizontal spacing between buttons
        inner_layout.setVerticalSpacing(2)    # Set the vertical spacing between buttons
        widget.setLayout(inner_layout)

        # Create the input field for the user
        self.input_field = QLineEdit(self)
        font = QFont()
        font.setFamily("Open Sans")
        font.setPointSize(24)
        font.setBold(True)
        self.input_field.setFont(font)
        self.input_field.setStyleSheet("QLineEdit { background: #f3f3f3; border: 2px solid #e3e3e3; border-radius: 11px; padding: 15px; }")
        self.input_field.setPlaceholderText("Type here...")
        self.input_field.setAlignment(Qt.AlignCenter)
        self.input_field.setFixedSize(800, 100)
        self.input_field.returnPressed.connect(self.check_input)
        # Add input field to the layout
        self.layout.addWidget(self.input_field, alignment=Qt.AlignCenter)


        

    def start(self,difficulty,words_range):
        self.seconds = get_time_by_mode(difficulty)
        self.timer_label.setText("0")
        self.timer = QTimer(self)
        self.counter = int(self.seconds)
        self.timer.timeout.connect(self.update_counter)
        self.timer.start(1000)  # Timer interval in milliseconds
        min_letters = words_range.split(" - ")[0]
        max_letters = words_range.split(" - ")[1].split(' ')[0]

        print(min_letters)
        print(max_letters)

        self.words_array = get_words_list_in_range(int(min_letters),int(max_letters))

        self.original_words = self.words_array.copy()  # Store the original word list for comparison

        # Common style for the buttons
        self.button_style = "background: #15d798; border-radius: 11px; padding: 30px 70px; color: #ffffff; font: normal bold 30px/1 'Open Sans', sans-serif;"

        if self.words_array:
            # Calculate the maximum width of the buttons based on the length of the longest word
            max_word_length = max(len(word) for word in self.words_array)
            self.max_button_width = 250 + (max_word_length - 4) * 20  # Increase width for longer words

        # Create buttons
        self.create_buttons()

        # Move the widget to the center of the screen
        start_x = int(self.screen_width * 0.5 - self.width() * 0.5)
        start_y = int(self.screen_height * 0.45 - self.height() * 0.45)
        self.move(start_x, start_y)

      
    def create_buttons(self):
        # Clear the existing buttons from the layout
        self.inner_layout = self.findChild(QGridLayout)
        for i in reversed(range(self.inner_layout.count())):
            self.inner_layout.itemAt(i).widget().setParent(None)

        # Create buttons with the updated words_array
        row = 0
        col = 0
        for label_text in self.words_array:
            button = self.create_button(label_text, self.button_style, self.max_button_width)
            self.inner_layout.addWidget(button, row, col, Qt.AlignCenter)  # Center the text inside the QLabel

            col += 1
            if col >= 3:  # Number of buttons in each row
                col = 0
                row += 1

    def create_button(self, label_text, style, width):
        button = HoverButton(self)  # Use the custom HoverButton instead of QLabel
        button.setStyleSheet(style)
        button.setFixedSize(width, 100)  # Adjust the size as needed
        button.setText(label_text)
        return button

    def update_counter(self):
        if self.counter > 0:
            self.timer_label.setText(str(self.counter))
            self.counter -= 1
        else:
            self.timer.stop()
            self.timer_label.setText("Go")
            print("Finished")
            self.show_results()

    def restart_game(self):
        self.timer_label.setText(str(self.seconds))
        self.timer.start()
        # Reset the words array to the original list
        self.words_array = self.original_words.copy()
        # Create buttons with the original list
        self.create_buttons()

    def check_input(self):
        user_input = self.input_field.text().lower()
        matched_words = [word for word in self.words_array if user_input == word.lower()]
        if matched_words:
            for word in matched_words:
                self.words_array.remove(word)
                self.remove_word_button(word)
       
        if not self.words_array:
            self.show_results()

        self.input_field.clear()

    def remove_word_button(self, word):
        for button in self.findChildren(HoverButton):
            if button.text().lower() == word.lower():
                button.setParent(None)

    def show_results(self):
        correct_words = [word for word in self.original_words if word not in self.words_array]
        missed_words = [word for word in self.original_words if word in self.words_array]
        self.counter_finished.emit(correct_words,missed_words)

# Custom HoverButton class to handle hover events
class HoverButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.hovered = False
        self.update_background()
        self.setMouseTracking(True)

    def event(self, event):
        if event.type() == QEvent.HoverEnter:
            self.hovered = True
            self.update_background()
        elif event.type() == QEvent.HoverLeave:
            self.hovered = False
            self.update_background()
        return super().event(event)

    def update_background(self):
        if self.hovered:
            self.setStyleSheet("background: #6fa8dc; border-radius: 11px; padding: 30px 70px; color: #ffffff; font: normal bold 30px/1 'Open Sans', sans-serif;")
        else:
            self.setStyleSheet("background: #15d798; border-radius: 11px; padding: 30px 70px; color: #ffffff; font: normal bold 30px/1 'Open Sans', sans-serif;")
