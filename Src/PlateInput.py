from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import *
from PySide2.QtCore import *
import SqlTools


class PlateInputTools:
    def __init__(self):
        super(PlateInputTools, self).__init__()
        self.sql_name = 'plateinfo'
        self.tools = SqlTools.Tools()
        self.tools.create_sql(self.sql_name, 'plateinfo')
        self.ui = QUiLoader().load('../Gui/PlateInput.ui')
        self.ui.pushButton.clicked.connect(self.input)
        self.ui.pushButton_2.clicked.connect(self.cancel)

    def input(self):
        plate = self.ui.lineEdit.text()
        check_plate = self.tools.check_plate(plate)
        if check_plate[0]:
            QMessageBox.information(self.ui, '提示!', '车牌已存在，请勿重复录入!')
            return
        else:
            res = self.tools.input_plate(plate)
            if res[0]:
                QMessageBox.information(self.ui, '提示!', res[1])
            else:
                QMessageBox.information(self.ui, '提示!', res[1])
                return

    def cancel(self):
        self.ui.close()
