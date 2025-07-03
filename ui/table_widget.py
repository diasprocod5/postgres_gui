from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit,QTableView,
                               QPushButton, QHBoxLayout, QMessageBox, QLabel)
from PySide6.QtCore import QModelIndex, Qt, QAbstractTableModel,Signal
from database.database import Database




class TableModel(QAbstractTableModel):
    def __init__(self, data: list[list], headers: list[str], parent=None):
        super().__init__(parent)
        self._data = data
        self._headers = headers

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and index.isValid():
            return str(self._data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
            else:
                return str(section + 1)
        return None


class TableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.table = QTableView()
        self.layout.addWidget(self.table)

        self.model = None
        self.database = Database()
        self.current_query = None
        self.current_params = None

    def load_data(self, query: str, params: tuple = None):
        """Загружает данные по SQL-запросу"""
        self.current_query = query
        self.current_params = params
        try:
            data, headers = self.database.execute_query(query, params)
            self.model = TableModel(data, headers)
            self.table.setModel(self.model)
            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке данных:\n{e}")

    def reload_data(self):
        """Повторная загрузка тех же данных"""
        if self.current_query:
            self.load_data(self.current_query, self.current_params)




class ExtendedTableWidget(TableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_column = -1

        self.search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")

        self.search_button = QPushButton("Найти")
        self.search_button.clicked.connect(self._on_search_clicked)

        self.reset_button = QPushButton("Сброс")
        self.reset_button.clicked.connect(self._on_reset_clicked)

        self.search_column_label = QLabel("Поиск по: Все поля")

        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.addWidget(self.reset_button)
        self.search_layout.addWidget(self.search_column_label)

        self.layout.insertLayout(0, self.search_layout)

        self.table.doubleClicked.connect(self._on_row_double_clicked)

        header = self.table.horizontalHeader()
        header.sectionClicked.connect(self._on_header_clicked)

    def _on_header_clicked(self, logicalIndex: int):
        """Обработка клика по заголовку столбца для выбора поля поиска"""
        headers = self.model._headers if self.model else []
        if logicalIndex < 0 or logicalIndex >= len(headers):
            return

        if self.search_column == logicalIndex:
            self.search_column = -1
            self.search_column_label.setText("Поиск по: Все поля")
        else:
            self.search_column = logicalIndex
            self.search_column_label.setText(f"Поиск по: {headers[logicalIndex]}")

        self._on_search_clicked()

    def _on_search_clicked(self):
        if not self.model:
            return

        text = self.search_input.text().lower().strip()
        if not text:
            self.table.setModel(self.model)
            self.table.resizeColumnsToContents()
            return

        if self.search_column == -1:
            filtered_data = [
                row for row in self.model._data
                if any(text in str(cell).lower() for cell in row)
            ]
        else:
            filtered_data = [
                row for row in self.model._data
                if text in str(row[self.search_column]).lower()
            ]

        filtered_model = self.model.__class__(filtered_data, self.model._headers)
        self.table.setModel(filtered_model)
        self.table.resizeColumnsToContents()

    def _on_reset_clicked(self):
        self.search_input.clear()
        self.search_column = -1
        self.search_column_label.setText("Поиск по: Все поля")
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

    def _on_row_double_clicked(self, index: QModelIndex):
        if not index.isValid() or self.model is None:
            return

        row = index.row()
        record = {
            self.model._headers[col]: self.model.data(self.model.index(row, col))
            for col in range(self.model.columnCount())
        }

        print("Выбрана запись:", record)
