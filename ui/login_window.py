from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QApplication
from PySide6.QtCore import Signal
from database.database import Database
from database.queries import get_user_roles

class LoginWindow(QWidget):

    LOGIN_SUCCESS = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setFixedSize(300,200)
        self.database = Database()

        self.layout = QVBoxLayout(self)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText('Логин')

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Пароль')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_layout = QHBoxLayout()
        self.btn_confirm = QPushButton('Подтвердить')
        self.btn_close = QPushButton('Выход')
        self.btn_layout.addWidget(self.btn_close,1)
        self.btn_layout.addWidget(self.btn_confirm,3)

        self.layout.addStretch(3)
        self.layout.addWidget(self.login_input)
        self.layout.addWidget(self.password_input)
        self.layout.addStretch(2)
        self.layout.addLayout(self.btn_layout)
        self.layout.addStretch(3)


        self.btn_close.clicked.connect(self.close_login_window)
        self.btn_confirm.clicked.connect(self.on_confirm_btn)



    def on_confirm_btn(self):
        login = self.login_input.text()
        password = self.password_input.text()
        if not login and not password:
            if self.database.connect('postgres',79230):
                self.LOGIN_SUCCESS.emit()
                # user_role = [role[0] for role in self.database.execute_query(get_user_roles)[0]]
                # print(user_role)
                # self.LOGIN_SUCCESS.emit(user_role)
            else:
                print('Что-то пошло не так как хотелось')
        else:
            print('Yamete kudasai')

    @staticmethod
    def close_login_window():
        QApplication.quit()



