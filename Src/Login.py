from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import *
from PySide2.QtCore import *
import sys
import os
import MainForm
import SqlTools
from threading import Thread
from PySide2.QtCore import Signal, QObject


class LoginForm:
    def __init__(self):
        super(LoginForm, self).__init__()
        self.ui = QUiLoader().load('../Gui/LoginForm.ui')
        self.ui.pushButton.clicked.connect(self.check_user)
        self.ui.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.ui.progressBar.setVisible(False)
        self.sql_name = 'userinfo'
        self.tools = SqlTools.Tools()
        self.tools.create_sql(self.sql_name, 'user')

    def load_main_form(self):

        mainform.ui.show()
        LoginForm.ui.close()

        #self.ui.close()

    def show_progress(self, info):
        self.ui.progressBar.setRange(0, 0)
        self.ui.progressBar.setVisible(True)
        # QMessageBox.information(self.ui, '提示', info)

    def check_user(self):
        user_name = self.ui.lineEdit.text()
        user_password = self.ui.lineEdit_2.text()
        if user_name == '' or user_password == '':
            QMessageBox.information(self.ui, '提示', '请输入用户名或密码！')
            return
        is_user = self.tools.check_user(user_name, user_password)
        if is_user[0]:
            # QMessageBox.information(self.ui, '提示', is_user[1])
            self.load_main_form()

        else:
            QMessageBox.information(self.ui, '提示', is_user[1])
            return

    def add_user(self):
        user_name = self.ui.lineEdit.text()
        user_password = self.ui.lineEdit_2.text()
        is_user = self.tools.add_user(user_name, user_password)
        QMessageBox.information(self.ui, '提示', is_user)

    def get_user_info(self):
        pass


if __name__ == '__main__':
    app = QApplication()
    LoginForm = LoginForm()
    mainform = MainForm.MainFormUI()
    LoginForm.ui.show()
    app.exec_()

