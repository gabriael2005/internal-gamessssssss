from PyQt5.QtWidgets import QVBoxLayout, QDialog, QPushButton
from PyQt5.QtCore import Qt, QEvent, pyqtSignal

from database.TimerManager import get_time_by_mode, update_timer_by_mode

class SpeedModeDialog(QDialog):
    def __init__(self, screen_width, screen_height, mode):
        super().__init__()
        self.current_time = get_time_by_mode(mode)
        self.mode = mode
        # Hide the title bar
        self.setWindowFlags(Qt.FramelessWindowHint)

        layout = QVBoxLayout(self)

        # Create buttons
        self.create_button('10', screen_width, screen_height, layout)
        self.create_button('15', screen_width, screen_height, layout)
        self.create_button('30', screen_width, screen_height, layout)
        self.create_button('45', screen_width, screen_height, layout)
        self.create_button('60', screen_width, screen_height, layout)
        self.create_button('Close', screen_width, screen_height, layout)

    def close_dialog(self):
        self.deleteLater()

    def create_button(self, time_text, screen_width, screen_height, layout):
        if time_text != 'Close':
            button_text = f"{time_text} seconds"
        else:
            button_text = time_text
        button = HoverButton(button_text, self)  # Use the HoverButton instead of QPushButton
        button.setStyleSheet("QPushButton { border: none; font: normal bold 30px/1 'Open Sans', sans-serif; color: #ffffff; background: #15d798; border-radius: 11px; padding: 30px 70px; }")
        layout.addWidget(button)
        start_x = int(screen_width * 0.5 - button.width() * 0.5)

        
        if time_text == str(self.current_time):
            button.setProperty("current_time", True)
            button.setStyleSheet("QPushButton { border: none; font: normal bold 30px/1 'Open Sans', sans-serif; color: #ffffff; background: #6fa8dc; border-radius: 11px; padding: 30px 70px; }")

        if time_text == '10':
            start_y = int(screen_height * 0.1 - button.height() * 0.1)
        elif time_text == '15':
            start_y = int(screen_height * 0.25 - button.height() * 0.25)
        elif time_text == '30':
            start_y = int(screen_height * 0.4 - button.height() * 0.4)
        elif time_text == '45':
            start_y = int(screen_height * 0.55 - button.height() * 0.55)
        elif time_text == '60':
            start_y = int(screen_height * 0.6 - button.height() * 0.6)
        else:
            start_y = int(screen_height * 0.75 - button.height() * 0.75)
        
        button.clicked.connect(self.close_dialog)

        button.move(start_x, start_y)


        # Connect the time_clicked signal to the update_time function
        button.time_clicked.connect(self.update_time)

    def update_time(self, time):
        update_timer_by_mode(int(time.split(' ')[0]), self.mode)


# Custom HoverButton widget to handle hover events and signals
class HoverButton(QPushButton):
    time_clicked = pyqtSignal(str)

    def __init__(self, text, parent):
        super().__init__(text, parent)
        self.hovered = False
        self.update_background()
        self.setMouseTracking(True)
        self.is_current_time = False  # Flag to indicate if it's the current time button

    def set_current_time(self, is_current):
        self.is_current_time = is_current
        self.update_background()

    def event(self, event):
        if event.type() == QEvent.HoverEnter:
            self.hovered = True
            self.update_background()
        elif event.type() == QEvent.HoverLeave:
            self.hovered = False
            self.update_background()
        return super().event(event)

    def update_background(self):
        if self.hovered and not self.property("current_time"):
            self.setStyleSheet("background: #6fa8dc; border-radius: 11px; padding: 30px 70px; color: #ffffff; font: normal bold 30px/1 'Open Sans', sans-serif;")
        elif self.property("current_time"):
            self.setStyleSheet("background: #6fa8dc; border-radius: 11px; padding: 30px 70px; color: #ffffff; font: normal bold 30px/1 'Open Sans', sans-serif;")
        else:
            self.setStyleSheet("background: #15d798; border-radius: 11px; padding: 30px 70px; color: #ffffff; font: normal bold 30px/1 'Open Sans', sans-serif;")

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.text() != 'Close':
            if not self.property("current_time"):  # If it's the current time button, emit the signal
                self.time_clicked.emit(self.text())
