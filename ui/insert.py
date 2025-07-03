from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout,
    QStackedWidget, QFormLayout, QLineEdit, QTextEdit, QMessageBox
)
from database.data_loader import DataLoader
from database.database import Database
from validators import Validators


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

        self.ca_form_widget, self.ca_form_fields = self.client_account_form()
        self.client_form_widget, self.client_form_fields = self.create_client_form()
        self.account_form_widget, self.account_form_fields = self.create_account_form()
        self.tariff_form_widget, self.tariff_form_fields = self.create_tariff_form()
        self.transaction_from_widget, self.transaction_form_fields = self.create_transaction_form()


        self.stacked.addWidget(QWidget())
        self.stacked.addWidget(self.ca_form_widget)
        self.stacked.addWidget(self.client_form_widget)
        self.stacked.addWidget(self.account_form_widget)
        self.stacked.addWidget(self.tariff_form_widget)
        self.stacked.addWidget(self.transaction_from_widget)


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

    def client_account_form(self):
        widget = QWidget()
        layout = QFormLayout(widget)

        full_name = QLineEdit()
        full_name.setValidator(Validators.get_validator('full_name'))
        layout.addRow("ФИО клиента:", full_name)

        phone = QLineEdit()
        phone.setValidator(Validators.get_validator('phone'))
        layout.addRow("Телефон:", phone)

        client_type = QComboBox()
        client_type.addItems(['private', 'legal'])
        layout.addRow("Тип клиента:", client_type)

        tariff = QComboBox()
        layout.addRow("Тариф:", tariff)

        balance = QLineEdit()
        balance.setText('0.00')
        balance.setValidator(Validators.get_validator("balance"))
        layout.addRow("Баланс:", balance)

        company_info = QTextEdit()
        layout.addRow("О компании:", company_info)

        client_type.currentTextChanged.connect(
            lambda: self.load_tariffs_by_client_type(client_type, tariff)
        )
        client_type.currentTextChanged.connect(
            lambda: self.on_client_type_changed(client_type, company_info))

        client_account_fields = {
            'full_name': full_name,
            'phone': phone,
            'client_type': client_type,
            'tariff': tariff,
            'balance': balance,
            'company_info': company_info,
        }

        return widget, client_account_fields


    def load_tariffs_by_client_type(self, client_type_field: QComboBox, tariffs_field):
        if client_type_field.currentData():
            client_type = client_type_field.currentData()[1]
        else:
            client_type = client_type_field.currentText().strip()
        if not client_type:
            tariffs_field.clear()
            tariffs_field.addItem('')
            return
        tariffs_field.clear()
        tariffs_field.addItem('')
        for tariff_id, tariff_name, tariff_type in self.data_loader.tariffs:
            if tariff_type == client_type:
                tariffs_field.addItem(f'{tariff_name}', tariff_id)



    def create_client_form(self):
        widget = QWidget()
        layout = QFormLayout(widget)

        full_name = QLineEdit()
        full_name.setValidator(Validators.get_validator("full_name"))
        layout.addRow("ФИО клиента:", full_name)

        phone = QLineEdit()
        phone.setValidator(Validators.get_validator("phone"))
        layout.addRow("Телефон:", phone)

        client_type = QComboBox()
        client_type.addItems(['', 'private','legal'])
        layout.addRow("Тип клиента:", client_type)

        company_info = QTextEdit()
        layout.addRow("О компании:", company_info)

        client_type.currentTextChanged.connect(
            lambda: self.on_client_type_changed(client_type, company_info))

        client_fields = {
            'full_name': full_name,
            'phone': phone,
            'client_type': client_type,
            'company_info': company_info
        }

        return widget, client_fields

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

        client = QComboBox()
        client.addItem('')
        for client_id, full_name, phone, client_type in self.data_loader.users:
            client.addItem(f'{full_name} ({phone})', (client_id, client_type))
        layout.addRow("Клиент:", client)


        tariff = QComboBox()
        layout.addRow("Тариф:", tariff)

        client.currentIndexChanged.connect(
            lambda: self.load_tariffs_by_client_type(client, tariff))

        balance = QLineEdit()
        balance.setText('0.00')
        balance.setValidator(Validators.get_validator('balance'))
        layout.addRow("Баланс:", balance)

        account_fields = {
            'client': client,
            'tariff': tariff,
            'balance': balance
        }

        return widget, account_fields


    def create_tariff_form(self):
        widget = QWidget()
        layout = QFormLayout(widget)

        tariff_name = QLineEdit()
        tariff_name.setValidator(Validators.get_validator('tariff_name'))
        layout.addRow("Название тарифа:", tariff_name)

        tariff_type = QComboBox()
        tariff_type.addItems(['private', 'legal'])
        layout.addRow("Тип тарифа:", tariff_type)

        tariff_price = QLineEdit()

        tariff_price.setValidator(Validators.get_validator('tariff_price'))
        layout.addRow("Стоимость:", tariff_price)

        tariff_description = QTextEdit()
        layout.addRow("Описание:", tariff_description)

        tariff_fields = {
            'tariff_name': tariff_name,
            'tariff_type': tariff_type,
            'tariff_price': tariff_price,
            'tariff_description': tariff_description,
        }

        return widget, tariff_fields

    def create_transaction_form(self):
        widget = QWidget()
        layout = QFormLayout(widget)

        account = QComboBox()
        account.addItem('')
        for account_id, full_name, phone in self.data_loader.accounts:
            account.addItem(f'{full_name} ({phone})', account_id)
        layout.addRow('Клиент:',account)

        transaction_type = QComboBox()
        transaction_type.addItems(['deposit', 'debit'])
        layout.addRow('Тип транзакции: ', transaction_type)

        amount = QLineEdit()
        amount.setValidator(Validators.get_validator('amount'))
        layout.addRow("Сумма:", amount)

        transaction_description = QTextEdit()
        layout.addRow("Описание:", transaction_description)

        transaction_fields = {
            'account': account,
            'transaction_type': transaction_type,
            'amount': amount,
            'transaction_description': transaction_description
        }


        return widget, transaction_fields

    def on_insert_clicked(self):
        selected_table = self.combo.currentText()

        if selected_table == 'Клиент-Аккаунт':
            full_name = self.ca_form_fields['full_name'].text().strip()
            phone = self.ca_form_fields['phone'].text().strip()
            client_type = self.ca_form_fields['client_type'].currentText().strip()
            company_info = self.ca_form_fields['company_info'].toPlainText().strip()
            tariff = self.ca_form_fields['tariff'].currentData()
            balance = self.ca_form_fields['balance'].text().strip()

            fields_to_validate = [
                (not full_name or not self.ca_form_fields['full_name'].hasAcceptableInput(), 'Некорректное ФИО'),
                (not phone or not self.ca_form_fields['phone'].hasAcceptableInput(), 'Некорректный номер телефона'),
                (not client_type, "Не указан тип обслуживания клиента"),
                (client_type == 'legal' and not company_info, 'Отсутствуют данные о компании'),
                (not tariff, 'Не указан тариф'),
                (not balance, "Укажите корректный баланс")
            ]
            if not self.validate_fields(fields_to_validate):
                return
            if client_type == 'private':
                company_info = None
            query = 'SELECT create_client_with_account(%s, %s, %s, %s, %s, %s,%s)'
            if self.db.execute_query(query,(full_name,phone,client_type,tariff,company_info,balance,None)):
                QMessageBox.information(self, 'Успех', 'Клиент с аккаунтом добавлен')
                self.data_loader.load_accounts()
                self.clear_current_form_fields()



        if selected_table == 'Клиенты':
            full_name = self.client_form_fields["full_name"].text().strip()
            phone = self.client_form_fields["phone"].text().strip()
            client_type = self.client_form_fields["client_type"].currentText().strip()
            company_info = self.client_form_fields["company_info"].toPlainText().strip()

            fields_to_validate = [
                (not full_name or not self.client_form_fields["full_name"].hasAcceptableInput(), 'Некорректное ФИО'),
                (not phone or not self.client_form_fields["phone"].hasAcceptableInput(),'Некорректный номер телефона'),
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
            client = self.account_form_fields['client'].currentData()[0]
            tariff = self.account_form_fields['tariff'].currentData()
            balance = self.account_form_fields['balance'].text().strip()

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
            tariff_name = self.tariff_form_fields['tariff_name'].text().strip()
            tariff_type = self.tariff_form_fields['tariff_type'].currentText().strip()
            tariff_price = self.tariff_form_fields['tariff_price'].text().strip()
            descr = self.tariff_form_fields['tariff_description'].toPlainText().strip()

            fields_to_validate = [
                (not tariff_name or not self.tariff_form_fields['tariff_name'].hasAcceptableInput(), 'Некорректное название тарифа'),
                (not tariff_type, 'Не указан тип тарифа'),
                (not tariff_price or not self.tariff_form_fields['tariff_price'].hasAcceptableInput(), "Некорректная стоимость тарифа"),
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
            account = self.transaction_form_fields['account'].currentData()
            transaction_type = self.transaction_form_fields['transaction_type'].currentText().strip()
            amount = self.transaction_form_fields['amount'].text().strip()
            descr = self.transaction_form_fields['transaction_description'].toPlainText().strip() or None

            fields_to_validate = [
                (not account, 'Не указан клиент'),
                (not transaction_type, 'Не указан тип операции'),
                (not amount or not self.transaction_form_fields['amount'].hasAcceptableInput(), "Некорректная сумма операции")
            ]
            if not self.validate_fields(fields_to_validate):
                return

            query = "SELECT FROM insert_transaction(%s, %s, %s, %s)"
            if self.db.execute_query(query,(account, transaction_type, amount, descr)):
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
    db = Database()
    db.connect('postgres',79230)
    app = QApplication([])
    window = InsertWindow()
    window.show()
    app.exec()
