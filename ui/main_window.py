from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedLayout
from PySide6.QtCore import Qt, Signal
from ui.top_widget import TopWidget
from ui.mid_widget import MidWidget
from ui.table_widget import TableWidget, ExtendedTableWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('My application')
        self.setFixedSize(800, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        self.top_widget = TopWidget()
        self.mid_widget = MidWidget()
        self.table_widget = TableWidget()
        self.tab_widget = ExtendedTableWidget()

        self.layout.addWidget(self.top_widget)
        self.layout.addWidget(self.mid_widget)
        self.layout.addStretch(1)
        self.layout.addWidget(self.tab_widget,10)

        self.mid_widget.TABLE_BUTTON_CLICKED.connect(self.tab_widget.load_data)


