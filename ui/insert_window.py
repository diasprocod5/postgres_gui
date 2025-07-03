from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout,
    QStackedWidget, QFormLayout, QLabel, QLineEdit, QTextEdit, QMessageBox
)
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
from database.data_loader import DataLoader
from database.database import Database


class InsertWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Внести данные в БД')
        self.setFixedSize(800,600)
        self.db = Database()

        self.data_loader = DataLoader()
        self.data_loader.load_all()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50,50,50,50)


        self.top_form = QFormLayout()
        self.combo = QComboBox()
        self.combo.addItems(["","Клиент-Аккаунт", "Клиенты", "Аккаунты", "Тарифы","Транзакции"])
        self.top_form.addRow("Таблица: ", self.combo)
        main_layout.addLayout(self.top_form)

        self.stacked = QStackedWidget()
        main_layout.addWidget(self.stacked)


        self.stacked.addWidget(QWidget())
        self.stacked.addWidget(self.create_client_account_form())
        self.stacked.addWidget(self.create_client_form())
        self.stacked.addWidget(self.create_account_form())
        self.stacked.addWidget(self.create_tariff_form())
        self.stacked.addWidget(self.create_transaction_form())


        self.combo.currentIndexChanged.connect(self.stacked.setCurrentIndex)

        # buttons
        self.btn_layout = QHBoxLayout()
        self.btn_insert = QPushButton('INSERT')
        self.btn_cancel = QPushButton('CANCEL')
        self.btn_layout.addStretch(2)
        self.btn_layout.addWidget(self.btn_cancel,2)
        self.btn_layout.addWidget(self.btn_insert,2)
        self.btn_layout.addStretch(2)
        main_layout.addLayout(self.btn_layout)

        self.btn_insert.clicked.connect(self.on_insert_clicked)
        self.btn_cancel.clicked.connect(self.close)
        self.btn_cancel.clicked.connect(self.clear_current_form_fields)

    def create_client_account_form(self):
        widget = QWidget()
        layout = QFormLayout(widget)

        self.ca_full_name = QLineEdit()
        regex_full_name = QRegularExpression(r"^([А-ЯЁ][а-яё]{0,20}\s){2}[А-ЯЁ][а-яё]{0,20}$")
        full_name_validator = QRegularExpressionValidator(regex_full_name)
        self.ca_full_name.setValidator(full_name_validator)
        layout.addRow("ФИО клиента:", self.ca_full_name)

        self.ca_phone = QLineEdit()
        regex_phone = QRegularExpression(r"^9[0-9]{9}$")
        phone_validator = QRegularExpressionValidator(regex_phone)
        self.ca_phone.setValidator(phone_validator)
        layout.addRow("Телефон:", self.ca_phone)

        self.ca_client_type = QComboBox()
        self.ca_client_type.addItem('')
        self.ca_client_type.addItems(['private', 'legal'])
        layout.addRow("Тип клиента:", self.ca_client_type)
        self.ca_client_type.currentTextChanged.connect(self.ca_load_tariffs_by_client_type)

        self.ca_tariffs = QComboBox()
        layout.addRow("Тариф:", self.ca_tariffs)

        self.ca_balance = QLineEdit()
        self.ca_balance.setText('0.00')
        regex_balance = QRegularExpression(r"^[1-9][0-9]{0,5}(\.[0-9]{1,2})?$|^0\.[0-9]{1,2}$")
        balance_validator = QRegularExpressionValidator(regex_balance)
        self.ca_balance.setValidator(balance_validator)
        layout.addRow("Баланс:", self.ca_balance)

        self.ca_company_info = QTextEdit()
        layout.addRow("О компании:", self.ca_company_info)

        self.ca_client_type.currentTextChanged.connect(
            lambda: self.on_client_type_changed(self.ca_client_type, self.ca_company_info))


        return widget


    def ca_load_tariffs_by_client_type(self):
        client_type = self.ca_client_type.currentText().strip()
        if not client_type:
            self.ca_tariffs.clear()
            self.ca_tariffs.addItem('')
            return
        self.ca_tariffs.clear()
        self.ca_tariffs.addItem('')
        for tariff_id, tariff_name, tariff_type in self.data_loader.tariffs:
            if tariff_type == client_type:
                self.ca_tariffs.addItem(f'{tariff_name}', tariff_id)



    def create_client_form(self):
        widget = QWidget()
        layout = QFormLayout(widget)

        self.full_name = QLineEdit()
        regex_full_name = QRegularExpression(r"^([А-ЯЁ][а-яё]{0,20}\s){2}[А-ЯЁ][а-яё]{0,20}$")
        full_name_validator = QRegularExpressionValidator(regex_full_name)
        self.full_name.setValidator(full_name_validator)
        layout.addRow("ФИО клиента:", self.full_name)

        self.phone = QLineEdit()
        regex_phone = QRegularExpression(r"^9[0-9]{9}$")
        phone_validator = QRegularExpressionValidator(regex_phone)
        self.phone.setValidator(phone_validator)
        layout.addRow("Телефон:", self.phone)

        self.client_type = QComboBox()
        self.client_type.addItem('')
        self.client_type.addItems(['private','legal'])
        layout.addRow("Тип клиента:", self.client_type)

        self.company_info = QTextEdit()
        layout.addRow("О компании:", self.company_info)

        self.client_type.currentTextChanged.connect(
            lambda: self.on_client_type_changed(self.client_type, self.company_info))

        return widget

    @staticmethod
    def on_client_type_changed(type_field: QComboBox, text_field:QTextEdit):
        client_type = type_field.currentText()
        if client_type == 'private':
            text_field.clear()
            text_field.setDisabled(True)
        else:
            text_field.setDisabled(False)

    def create_account_form(self):
        widget = QWidget()
        layout = QFormLayout(widget)

        self.client_id = QComboBox()
        self.client_id.addItem('')
        for cl_id, cl_full_name, cl_phone, cl_type in self.data_loader.users:
            display_text = f'{cl_full_name} ({cl_phone})'
            self.client_id.addItem(display_text, (cl_id, cl_type))
        layout.addRow("Клиент:", self.client_id)
        self.client_id.currentIndexChanged.connect(self.load_tariffs_by_client_type)

        self.tariffs = QComboBox()
        layout.addRow("Тариф:", self.tariffs)

        self.balance = QLineEdit()
        self.balance.setText('0.00')
        regex_balance = QRegularExpression(r"^[1-9][0-9]{0,5}(\.[0-9]{1,2})?$|^0\.[0-9]{1,2}$")
        balance_validator = QRegularExpressionValidator(regex_balance)
        self.balance.setValidator(balance_validator)
        layout.addRow("Баланс:", self.balance)

        return widget

    def load_tariffs_by_client_type(self):
        client_data = self.client_id.currentData()
        if not client_data:
            self.tariffs.clear()
            self.tariffs.addItem('')
            return
        _, client_type = client_data
        self.tariffs.clear()
        self.tariffs.addItem('')
        for tariff_id, tariff_name, tariff_type in self.data_loader.tariffs:
            if tariff_type == client_type:
                self.tariffs.addItem(f'{tariff_name}', tariff_id)


    def create_tariff_form(self):
        widget = QWidget()
        layout = QFormLayout(widget)

        self.tariff_name = QLineEdit()
        regex_tariff_name = QRegularExpression(r'^.{5,25}$')
        tariff_name_validator = QRegularExpressionValidator(regex_tariff_name)
        self.tariff_name.setValidator(tariff_name_validator)
        layout.addRow("Название тарифа:", self.tariff_name)

        self.tariff_type = QComboBox()
        self.tariff_type.addItems(['private', 'legal'])
        layout.addRow("Тип тарифа:", self.tariff_type)

        self.tariff_price = QLineEdit()
        regex_price = QRegularExpression(r"^[1-9][0-9]{1,4}(\.[0-9]{1,2})?$")
        price_validator = QRegularExpressionValidator(regex_price)
        self.tariff_price.setValidator(price_validator)
        layout.addRow("Стоимость:", self.tariff_price)

        self.tariff_description = QTextEdit()
        layout.addRow("Описание:", self.tariff_description)

        return widget

    def create_transaction_form(self):
        widget = QWidget()
        layout = QFormLayout(widget)

        self.transaction_account_id = QComboBox()
        self.transaction_account_id.addItem('')
        for ac_id, cl_full_name, cl_phone in self.data_loader.accounts:
            self.transaction_account_id.addItem(f'{cl_full_name} ({cl_phone})', ac_id)
        layout.addRow('Клиент:',self.transaction_account_id)

        self.transaction_type = QComboBox()
        self.transaction_type.addItems(['deposit', 'debit'])
        layout.addRow('Тип транзакции: ', self.transaction_type)

        self.amount = QLineEdit()
        regex_amount = QRegularExpression(r"^[1-9][0-9]{0,5}(\.[0-9]{1,2})?$")
        amount_validator = QRegularExpressionValidator(regex_amount)
        self.amount.setValidator(amount_validator)
        layout.addRow("Сумма:", self.amount)

        self.transaction_description = QTextEdit()
        layout.addRow("Описание:", self.transaction_description)


        return widget

    def on_insert_clicked(self):
        selected_table = self.combo.currentText()

        if selected_table == 'Клиент-Аккаунт':
            full_name = self.ca_full_name.text().strip()
            phone = self.ca_phone.text().strip()
            client_type = self.ca_client_type.currentText().strip()
            company_info = self.ca_company_info.toPlainText().strip()
            tariff = self.ca_tariffs.currentData()
            balance = self.ca_balance.text().strip()

            fields_to_validate = [
                (not full_name or not self.ca_full_name.hasAcceptableInput(), 'Некорректное ФИО'),
                (not phone or not self.ca_phone.hasAcceptableInput(), 'Некорректный номер телефона'),
                (not client_type, "Не указан тип обслуживания клиента"),
                (client_type == 'legal' and not company_info, 'Отсутствуют данные о компании'),
                (not tariff, 'Не указан тариф'),
                (not balance, "Укажите корректный баланс")
            ]
            if not self.validate_fields(fields_to_validate):
                return
            if client_type == 'private':
                company_info = None
            print(full_name,phone,client_type,tariff,company_info,balance)
            query = 'SELECT create_client_with_account(%s, %s, %s, %s, %s, %s,%s)'
            if self.db.execute_query(query,(full_name,phone,client_type,tariff,company_info,balance,None)):
                QMessageBox.information(self, 'Успех', 'Клиент с аккаунтом добавлен')
                self.data_loader.load_accounts()
                self.clear_current_form_fields()



        if selected_table == 'Клиенты':
            full_name = self.full_name.text().strip()
            phone = self.phone.text().strip()
            client_type = self.client_type.currentText().strip()
            company_info = self.company_info.toPlainText().strip()

            fields_to_validate = [
                (not full_name or not self.full_name.hasAcceptableInput(), 'Некорректное ФИО'),
                (not phone or not self.phone.hasAcceptableInput(),'Некорректный номер телефона'),
                (not client_type, "Не указан тип обслуживания клиента"),
                (client_type == 'legal' and not company_info, 'Отсутствуют данные о компании')
            ]
            if not self.validate_fields(fields_to_validate):
                return
            if client_type == 'private':
                company_info = None

            query = "SELECT FROM insert_client(%s, %s, %s, %s)"
            if self.db.execute_query(query, (full_name,phone,client_type,company_info)):
                QMessageBox.information(self, 'Успех', 'Клиент добавлен')
                self.clear_current_form_fields()
                self.data_loader.load_users()

        if selected_table == 'Аккаунты':
            client = self.client_id.currentData()[0]
            tariff = self.tariffs.currentData()
            balance = self.balance.text().strip()

            fields_to_validate = [
                (not client, 'Нет данных о клиенте'),
                (not tariff, 'Не указан тариф'),
                (not balance, "Укажите корректный баланс")
            ]
            if not self.validate_fields(fields_to_validate):
                return

            query = "SELECT FROM insert_account(%s, %s, %s, %s, %s)"
            if self.db.execute_query(query,(client,tariff,'new',balance,None)):
                QMessageBox.information(self, 'Успех', 'Создан новый аккаунт')
                self.clear_current_form_fields()
                self.data_loader.load_users()
                self.data_loader.load_accounts()

        if selected_table == 'Тарифы':
            tariff_name = self.tariff_name.text().strip()
            tariff_type = self.tariff_type.currentText().strip()
            tariff_price = self.tariff_price.text().strip()
            descr = self.tariff_description.toPlainText().strip()

            fields_to_validate = [
                (not tariff_name or not self.tariff_name.hasAcceptableInput(), 'Некорректное название тарифа'),
                (not tariff_type, 'Не указан тип тарифа'),
                (not tariff_price or not self.tariff_price.hasAcceptableInput(), "Некорректная стоимость тарифа"),
                (not  descr, 'Отсутствует описание тарифа')
            ]
            if not self.validate_fields(fields_to_validate):
                return

            query = "SELECT FROM insert_tariff(%s, %s, %s, %s)"
            if self.db.execute_query(query,(tariff_name,tariff_price,tariff_type,descr)):
                QMessageBox.information(self, 'Успех', 'Новый тариф добавлен')
                self.clear_current_form_fields()
                self.data_loader.load_tariffs()

        if selected_table == "Транзакции":
            account_id = self.transaction_account_id.currentData()
            transaction_type = self.transaction_type.currentText().strip()
            amount = self.amount.text().strip()
            descr = self.transaction_description.toPlainText().strip() or None

            fields_to_validate = [
                (not account_id, 'Не указан клиент'),
                (not transaction_type, 'Не указан тип операции'),
                (not amount or not self.amount.hasAcceptableInput(), "Некорректная сумма операции")
            ]
            if not self.validate_fields(fields_to_validate):
                return

            query = "SELECT FROM insert_transaction(%s, %s, %s, %s)"
            if self.db.execute_query(query,(account_id, transaction_type, amount, descr)):
                QMessageBox.information(self,'Успех','Транзакция проведена')
                self.clear_current_form_fields()

    def validate_fields(self, fields):
        errors = [msg for condition, msg in fields if condition]
        if errors:
            QMessageBox.warning(self,'Ошибка валидации', '\n'.join(errors))
            return False
        return True

    def clear_current_form_fields(self):
        current_widget = self.stacked.currentWidget()

        if current_widget is None:
            return

        def clear_widget(widget):
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QTextEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
        for child in current_widget.findChildren(QWidget):
            clear_widget(child)


if __name__ == "__main__":
    app = QApplication([])
    window = InsertWindow()
    window.show()
    app.exec()
