from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import *
from PySide2.QtCore import *
import cv2
from threading import Thread
# from hyperlpr import pipline as pp
import SerPort
import time


class MainFormUI(QDialog):
    def __init__(self):
        # 从文件中加载UI定义
        super(MainFormUI, self).__init__()
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('../Gui/MainForm.ui')
        # 载入界面
        self.ser_config = SerPort.SerPortTools()
        self.ui.statusbar.addWidget(self.ui.label_3)

        # self.ui.pushButton_5.clicked.connect(self.button_clicked)
        self.ui.pushButton_5.clicked.connect(self.test)
        self.ui.action_8.triggered.connect(self.open_ser_config)

        # 创建线程
        self.thead = Thread(target=self.update_serial_info, name=None)
        self.thead.setDaemon(True) # 设置为守护线程
        self.thead.start() #启动串口监听

        # 创建定时器
        self.timer = QTimer() #显示时间
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

    def test(self):
        # print(test.list_ports())
        self.ser_config.close_port()
        #self.ser_config.send_mess(b'1')

    def open_ser_config(self):
        self.ser_config.ui.show()

    def openfile(self):
        openfile_name, _ = QFileDialog.getOpenFileName(self.ui, '选择文件', '', 'Jpeg files(*.jpg , *.jpeg)')
        return openfile_name

    def start_check(self, file):
        image = cv2.imread(file)
        image, res = pp.SimpleRecognizePlate(image)
        # print(res[0])
        self.ui.label.setText(res[0])
        self.ui.label.adjustSize()

    def button_clicked(self):
        filename = self.openfile()
        self.start_check(filename)

    def showTime(self):
        # 获取系统当前时间
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.ui.label_3.setText(now_time)

    def update_serial_info(self):
        while True:
            while self.ser_config.is_open:
                try:
                    serial_info = self.ser_config.recieve_mess()
                    if serial_info != '':
                        # self.ui.plainTextEdit.appendPlainText(serial_info)
                        print(serial_info)
                except Exception as e:
                    continue
            time.sleep(0.1)

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



if __name__ == '__main__':
    app = QApplication([])
    stats = MainFormUI()
    stats.ui.show()
    app.exec_()
