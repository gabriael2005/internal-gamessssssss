from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal

class StartingPage(QDialog):
    counter_finished = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Create main vertical layout
        main_layout = QVBoxLayout()

        # Create the counter label
        self.counter_label = QLabel("3", self)
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setStyleSheet("color: white; font: bold 100px; background-color: #6fa8dc; border-radius: 20px; padding: 20px;")

        # Add the counter label to the layout
        main_layout.addWidget(self.counter_label, alignment=Qt.AlignCenter)

        # Set the main layout as the main layout for the dialog
        self.setLayout(main_layout)

        # Set the size of the QDialog
        self.resize(300, 400)

    def update_counter(self):
        if self.counter > 0:
            self.counter_label.setText(str(self.counter))
            self.counter -= 1
        else:
            self.timer.stop()
            self.counter_label.setText("Go")
            self.counter_finished.emit()
    
    def start(self):
        self.counter = 3
        self.counter_label.setText(str(self.counter))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_counter)
        self.timer.start(1000)  # Timer interval in milliseconds

        # Use a custom font for the counter label (You'll need to have the font file in your project directory)
        font = QFont()
        font.setFamily("Open Sans")
        font.setPointSize(100)
        font.setWeight(QFont.Bold)
        self.counter_label.setFont(font)