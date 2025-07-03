from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal

class TopWidget(QWidget):
    LOGOUT_BUTTON_CLICKED = Signal()
    INSERT_BUTTON_CLICKED = Signal()

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)

        self.btn_tables = QPushButton("Таблицы")
        self.btn_queries = QPushButton("Запросы")
        self.btn_insert = QPushButton("Добавить")
        self.btn_exit = QPushButton('Выход')

        self.layout.addWidget(self.btn_tables)
        self.layout.addWidget(self.btn_queries)
        self.layout.addWidget(self.btn_insert)
        self.layout.addStretch(1)
        self.layout.addWidget(self.btn_exit)



        self.btn_exit.clicked.connect(self.LOGOUT_BUTTON_CLICKED.emit)
        self.btn_insert.clicked.connect(self.INSERT_BUTTON_CLICKED.emit)