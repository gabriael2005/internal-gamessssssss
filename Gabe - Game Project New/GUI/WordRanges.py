import os
from PyQt5.QtWidgets import QGridLayout, QWidget, QPushButton, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt,QEvent
from PyQt5.QtCore import Qt,pyqtSignal

from GUI.AddWordRange import AddWordRange
from database.wordRangeManager import delete_word_range_by_id, get_word_ranges_list

script_directory = os.path.dirname(os.path.abspath(__file__))

class WordRanges(QWidget):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Create the scroll area
        scroll_area = QScrollArea()
        layout.addWidget(scroll_area)

        # Create a widget to hold the buttons
        widget = QWidget()
        scroll_area.setWidgetResizable(True)  # Allow the widget to resize with the scroll area
        scroll_area.setWidget(widget)

        self.inner_layout = QGridLayout()
        self.inner_layout.setHorizontalSpacing(2)  # Set the horizontal spacing between buttons
        self.inner_layout.setVerticalSpacing(2)    # Set the vertical spacing between buttons
        widget.setLayout(self.inner_layout)

        self.init_word_ranges()
        # Move the widget to the center of the screen
        start_x = int(self.screen_width * 0.5 - self.width() * 0.5)
        start_y = int(self.screen_width * 0.6 - self.height() * 0.6)
        self.move(start_x, start_y)

    def clear_inner_layout(self):
        while self.inner_layout.count():
            item = self.inner_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def init_word_ranges(self):
        # Common style for the buttons
        button_style = "background: #15d798; border-radius: 11px; padding: 30px 70px; color: #ffffff; font: normal bold 30px/1 'Open Sans', sans-serif;"
        self.words_ranges_array = get_word_ranges_list()
        self.ranges = [ f'{item[1]} - {item[0]} letter words'  for item in self.words_ranges_array ]

        if self.ranges:
            # Calculate the maximum width of the buttons based on the length of the longest word
            self.max_word_length = max(len(word) for word in self.ranges)
            self.max_button_width = 250 + (self.max_word_length - 4) * 20  # Increase width for longer words

        # Create buttons
        row = 0
        col = 0
        for label_text in self.ranges:
            button = self.create_button(label_text, button_style, self.max_button_width)
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
        button.word_range_clicked.connect(self.delete_word_range_from_list)  # Connect the word_clicked signal
        return button
    
    def delete_word_range_from_list(self,word_range_text):
        selected_id = None
        for item in self.words_ranges_array:
            if f'{item[1]} - {item[0]} letter words' == word_range_text:
                selected_id = item[2]
                delete_word_range_by_id(selected_id)
                break
        self.clear_inner_layout()
        self.init_word_ranges()

    def show_add_word_range(self):
        custom_dialog = AddWordRange()
        custom_dialog.new_word_range_added.connect(self.add_new_word_range_to_list)
        custom_dialog.exec_()

    def add_new_word_range_to_list(self):
        self.clear_inner_layout()
        self.init_word_ranges()

# Custom HoverButton class to handle hover events
class HoverButton(QPushButton):
    word_range_clicked = pyqtSignal(str)
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


    def mousePressEvent(self, event):
        self.word_range_clicked.emit(self.text())
        super().mousePressEvent(event)