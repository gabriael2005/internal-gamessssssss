import os
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout,QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt,pyqtSignal
from utils.SoundManager import SoundManager

script_directory = os.path.dirname(os.path.abspath(__file__))

class TitleBar(QWidget):
    back_button_clicked = pyqtSignal()
    add_button_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(TitleBar, self).__init__(parent)
        SoundManager.play_sound()
        self.setObjectName("TitleBar")
        self.layout = QHBoxLayout()

        # Load the image and resize it to the desired size
        self.muted = False 
        close_button_image = QPixmap(os.path.join(script_directory,'../images/shared/exit.png'))

        # Create a close button using a QPushButton
        self.exit_button = QPushButton(self)
        self.exit_button.setIcon(QIcon(close_button_image))
        self.exit_button.setIconSize(close_button_image.size())
        self.exit_button.setFixedSize(close_button_image.size())
        self.exit_button.setStyleSheet("QPushButton { border: none; }")
        

        # Create a back button using a QPushButton
        back_button_image = QPixmap(os.path.join(script_directory,'../images/shared/back.png'))
        self.back_button = QPushButton(self)
        self.back_button.setIcon(QIcon(back_button_image))
        self.back_button.setIconSize(back_button_image.size())
        self.back_button.setFixedSize(back_button_image.size())
        self.back_button.setStyleSheet("QPushButton { border: none; }")

        add_button_image = QPixmap(os.path.join(script_directory, '../images/shared/add.png'))
        self.add_button = QPushButton(self)
        self.add_button.setIcon(QIcon(add_button_image))
        self.add_button.setIconSize(add_button_image.size())
        self.add_button.setFixedSize(add_button_image.size())
        self.add_button.setStyleSheet("QPushButton { border: none; }")
        self.add_button.move(10,0)

        mute_button_image = QPixmap(os.path.join(script_directory,'../images/shared/icons8-mute-100.png'))
        self.mute_button = QPushButton(self)
        self.mute_button.setIcon(QIcon(mute_button_image))
        self.mute_button.setIconSize(mute_button_image.size())
        self.mute_button.setFixedSize(mute_button_image.size())
        self.mute_button.setStyleSheet("QPushButton { border: none; }")
        # Add the buttons and spacer to the layout
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.mute_button, alignment=Qt.AlignLeft)
        self.layout.addStretch(1)  # Add stretchable space at the bottom to push buttons up
        self.layout.addWidget(self.add_button, alignment=Qt.AlignRight)

        self.layout.addItem(spacer_item)
        self.layout.addWidget(self.exit_button, alignment=Qt.AlignRight)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.back_button.hide()
        self.add_button.hide()

        self.mute_button.clicked.connect(self.mute)

        self.back_button.clicked.connect(self.go_back)
        self.add_button.clicked.connect(self.show_add)

    def show_add(self):
        self.add_button_clicked.emit()

    def go_back(self):
        self.back_button_clicked.emit()

    def mute(self):
        if not self.muted:
            muted_button_image = QPixmap(os.path.join(script_directory,'../images/shared/icons8-mute-101.png'))
            self.mute_button.setIcon(QIcon(muted_button_image))
            self.muted = True
            SoundManager.mute()
        else :
            mute_button_image = QPixmap(os.path.join(script_directory,'../images/shared/icons8-mute-100.png'))
            self.mute_button.setIcon(QIcon(mute_button_image))
            self.muted = False
            SoundManager.unmute()