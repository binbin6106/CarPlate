from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import serial
import serial.tools.list_ports
import binascii


class SerPortTools:
    def __init__(self):
        super(SerPortTools, self).__init__()
        self.is_open = False
        self.ser = serial.Serial()
        self.ui = QUiLoader().load('../Gui/SerPortSet.ui')

        #定义属性
        self.ser_port_name = ''
        self.port_bps = ''

        # 定义选择下拉框
        self.port_name_items = []
        self.bps_items = ['600', '1200', '2400', '4800', '9600', '19200', '38400']
        for i in range(1, 20):
            self.port_name_items.append('COM{}'.format(str(i)))
        self.ui.comboBox.addItems(self.port_name_items)
        self.ui.comboBox_2.addItems(self.bps_items)

        # 定义按钮
        self.ui.pushButton.clicked.connect(self.open_ser)
        self.ui.pushButton_2.clicked.connect(self.close_windows)

    def __del__(self):
        if self.ser.is_open:
            self.close_port()
            # self.is_open = self.ser.is_open

    def get_port_name_and_bps(self):
        self.ser_port_name = self.ui.comboBox.currentText()
        self.port_bps = self.ui.comboBox_2.currentText()

    def open_ser(self):
        self.get_port_name_and_bps()
        self.ser.baudrate = int(self.port_bps)
        self.ser.port = self.ser_port_name

        try:
            self.ser.open()
            self.is_open = self.ser.is_open
            QMessageBox.information(self.ui, '提示', '串口打开成功!')
        except Exception as e:
            QMessageBox.information(self.ui, '提示', '串口打开失败，请检查!原因{}'.format(e))
            return

    @staticmethod
    def list_ports():
        plist = serial.tools.list_ports.comports()
        return plist

    def send_mess(self, info):
        #hex_info = binascii.b2a_hex(info)
        self.ser.write(info)

    def recieve_mess(self):
        res = self.ser.read()
        return res

    def close_windows(self):
        self.ui.close()

    def close_port(self):
        self.ser.close()
        self.is_open = self.ser.is_open
