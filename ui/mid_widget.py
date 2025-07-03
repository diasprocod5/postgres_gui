from  PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QStackedLayout
from PySide6.QtCore import Signal

from database.queries import query_dict

class MidWidget(QWidget):
    TABLE_BUTTON_CLICKED = Signal(str)

    def __init__(self):
        super().__init__()

        self.queries = query_dict

        self.layout = QStackedLayout(self)

        self.widget_tables = QWidget()
        self.widget_queries = QWidget()

        self.layout_tables = QHBoxLayout(self.widget_tables)
        self.layout_queries = QHBoxLayout(self.widget_queries)

        self.layout.addWidget(self.widget_tables)
        self.layout.addWidget(self.widget_queries)

        self.layout.setCurrentIndex(0)

        self.btn_general = QPushButton("Основная таблица")
        self.btn_clients = QPushButton('Клиенты')
        self.btn_debtors = QPushButton('Должники')
        self.btn_transactions = QPushButton('Транзакции')
        self.btn_tariffs = QPushButton('Тарифы')

        self.btn_query_1 = QPushButton('1')
        self.btn_query_2 = QPushButton('2')
        self.btn_query_3 = QPushButton('3')
        self.btn_query_4 = QPushButton('4')
        self.btn_query_5 = QPushButton('5')

        self.layout_tables.addWidget(self.btn_general)
        self.layout_tables.addWidget(self.btn_clients)
        self.layout_tables.addWidget(self.btn_debtors)
        self.layout_tables.addWidget(self.btn_transactions)
        self.layout_tables.addWidget(self.btn_tariffs)
        self.layout_tables.addStretch(1)

        self.layout_queries.addWidget(self.btn_query_1)
        self.layout_queries.addWidget(self.btn_query_2)
        self.layout_queries.addWidget(self.btn_query_3)
        self.layout_queries.addWidget(self.btn_query_4)
        self.layout_queries.addWidget(self.btn_query_5)
        self.layout_queries.addStretch(1)

        self.btn_tariffs.clicked.connect(lambda: self.TABLE_BUTTON_CLICKED.emit(self.queries['tariffs']))
        self.btn_general.clicked.connect(lambda: self.TABLE_BUTTON_CLICKED.emit(self.queries['general']))




    def switch_layout(self, index):
        self.layout.setCurrentIndex(index)




