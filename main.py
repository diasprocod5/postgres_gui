import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.login_window import LoginWindow
from ui.insert_window import InsertWindow
from database.database import Database
from typing import Optional


class Main:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window: Optional[MainWindow] = None
        self.login_window: Optional[LoginWindow] = None
        self.insert_window: Optional[InsertWindow] = None
        self.database = Database()


        self.init_login_window()


    def init_login_window(self):
        if self.insert_window:
            self.insert_window.close()
            self.insert_window.deleteLater()
            self.insert_window = None
        if self.main_window:
            self.main_window.close()
            self.main_window.deleteLater()
            self.main_window = None
            self.database.disconnect()

        self.login_window = LoginWindow()
        self.login_window.LOGIN_SUCCESS.connect(self.init_main_window)
        self.login_window.show()

    def init_main_window(self):
        if self.login_window:
            self.login_window.close()
            self.login_window.deleteLater()
            self.login_window = None

        self.main_window = MainWindow()
        self.main_window.top_widget.LOGOUT_BUTTON_CLICKED.connect(self.init_login_window)
        self.main_window.show()
        self.main_window.top_widget.INSERT_BUTTON_CLICKED.connect(self.init_insert_window)

    def init_insert_window(self):
        if not self.insert_window:
            self.insert_window = InsertWindow()
            self.insert_window.show()
        if not self.insert_window.isVisible():
            self.insert_window.show()
        self.insert_window.raise_()


    def run(self):
        sys.exit(self.app.exec())


if __name__=='__main__':
    app = Main()
    app.run()
