from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea
from PyQt5 import QtChart
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal


class ResultsPage(QWidget):
    restart_clicked = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

    def init_ui(self, correct_words, missed_words):
        # Clear existing widgets from layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Create a vertical layout for the results page
        main_layout = QVBoxLayout()

        # Add a restart button on top and make it bigger
        restart_button = QPushButton("Restart", self)
        restart_button.setStyleSheet("color: white; background-color: #6fa8dc; border-radius: 11px; padding: 10px;")
        restart_button.setFont(QFont("Open Sans", 15, QFont.Bold))
        restart_button.clicked.connect(self.restart_game)
        main_layout.addWidget(restart_button, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Create a chart to display the percentages
        chart = QtChart.QChart()
        series = QtChart.QPieSeries()
        correct_percentage = (len(correct_words) / (len(correct_words) + len(missed_words))) * 100
        missed_percentage = (len(missed_words) / (len(correct_words) + len(missed_words))) * 100

        correct_slice = series.append(f"Correct: {correct_percentage:.2f}%", correct_percentage)
        missed_slice = series.append(f"Missed: {missed_percentage:.2f}%", missed_percentage)

        # Customize colors of chart slices
        correct_color = QColor("#15d798")  # Green color for correct words
        missed_color = QColor("#c93b3b")   # Red color for missed words
        correct_slice.setBrush(correct_color)
        missed_slice.setBrush(missed_color)

        chart.addSeries(series)
        chart.setTitle("Performance Chart")
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart_view = QtChart.QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)  # Make the chart view look smoother
        main_layout.addWidget(chart_view)

        # Create a horizontal scroll area for the correct words
        correct_scroll_area = QScrollArea(self)
        correct_scroll_area.setWidgetResizable(True)
        correct_scroll_area.setFixedHeight(100)
        main_layout.addWidget(correct_scroll_area)

        # Create a widget to hold the correct words horizontally
        correct_widget = QWidget()
        correct_scroll_area.setWidget(correct_widget)

        correct_layout = QHBoxLayout(correct_widget)
        correct_layout.setAlignment(Qt.AlignLeft)

        # Create the label for "Correct Words:" and make it smaller
        correct_label = QLabel("Correct Words:", self)
        correct_label.setStyleSheet("color: white; font: bold 18px; padding-right: 10px; background-color: #6fa8dc; border-radius: 11px; padding: 10px;")
        correct_layout.addWidget(correct_label)

        for word in correct_words:
            label = QLabel(word, self)
            label.setStyleSheet("background-color: #15d798; color: white; font: bold 24px; padding: 5px 10px; border-radius: 5px;")
            correct_layout.addWidget(label)

        # Create a horizontal scroll area for the missed words
        missed_scroll_area = QScrollArea(self)
        missed_scroll_area.setWidgetResizable(True)
        missed_scroll_area.setFixedHeight(100)
        main_layout.addWidget(missed_scroll_area)

        # Create a widget to hold the missed words horizontally
        missed_widget = QWidget()
        missed_scroll_area.setWidget(missed_widget)

        missed_layout = QHBoxLayout(missed_widget)
        missed_layout.setAlignment(Qt.AlignLeft)

        # Create the label for "Missed Words:" and make it smaller
        missed_label = QLabel("Missed Words:", self)
        missed_label.setStyleSheet("color: white; font: bold 18px; padding-right: 10px; background-color: #6fa8dc; border-radius: 11px; padding: 10px;")
        missed_layout.addWidget(missed_label)

        for word in missed_words:
            label = QLabel(word, self)
            label.setStyleSheet("background-color: #c93b3b; color: white; font: bold 24px; padding: 5px 10px; border-radius: 5px;")
            missed_layout.addWidget(label)

        # Add some spacing between the correct and missed words
        main_layout.addSpacing(20)

        # Adjust the layout
        self.layout.addLayout(main_layout)

    def restart_game(self):
        self.restart_clicked.emit()
