from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import *
from PySide2.QtCore import *
import cv2
from threading import Thread
from hyperlpr import pipline as pp
import SqlTools
import SerPort
import PlateInput
import time


class MainFormUI(QDialog):
    def __init__(self):
        # 从文件中加载UI定义
        super(MainFormUI, self).__init__()

        # 定义一些属性
        self.taken_photo_flag = 0
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('../Gui/MainForm.ui')
        # 载入子页面
        self.ser_config = SerPort.SerPortTools()
        self.plate_input = PlateInput.PlateInputTools()
        self.sql_tools = SqlTools.Tools()
        # 界面设置
        self.ui.statusbar.addWidget(self.ui.label_3)
        self.ui.statusbar.addWidget(self.ui.label_2)
        self.ui.label_2.setAutoFillBackground(True)  # 设置背景充满，为设置背景颜色的必要条件
        self.set_label_2_color('red')
        # 跳转相关界面
        self.ui.action_5.triggered.connect(self.open_plate_input)  # 录入车牌
        self.ui.action_8.triggered.connect(self.open_ser_config)  # 串口设置
        # 测试用
        # self.ui.pushButton_5.clicked.connect(self.button_clicked)
        self.ui.pushButton_5.clicked.connect(self.button_clicked)

        # 创建线程
        self.thead = Thread(target=self.update_serial_info, name=None)
        self.thead.setDaemon(True)  # 设置为守护线程
        self.thead.start()  # 启动串口监听

        # 创建定时器
        self.timer = QTimer()  # 显示时间
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

    def test(self):
        # print(test.list_ports())
        self.ser_config.close_port()
        #self.ser_config.send_mess(b'1')

    def open_ser_config(self):
        self.ser_config.ui.show()

    def open_plate_input(self):
        self.plate_input.ui.show()

    def openfile(self):
        openfile_name, _ = QFileDialog.getOpenFileName(self.ui, '选择文件', '', 'Jpeg files(*.jpg , *.jpeg)')
        return openfile_name

    def start_check(self, file):
        image = cv2.imread(file)
        image, res = pp.SimpleRecognizePlate(image)
        # print(res[0])
        self.ui.label.setText(res[0])
        self.ui.label.adjustSize()
        check_res = self.sql_tools.check_plate(res[0])
        # print(check_res)
        if check_res[0]:
            if check_res[1][4] == '0':
                now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                self.ui.plainTextEdit.appendPlainText('车牌号:{}, 进入时间{}'.format(check_res[1][1], now_time))
                self.sql_tools.update_intime_plate_info(now_time, check_res[1][0])
                self.ui.plainTextEdit.appendPlainText('匹配成功，正在下发抬杆指令...')
                time.sleep(0.01)
                self.ui.plainTextEdit.appendPlainText('下发成功，正在抬杆')
        else:
            self.ui.plainTextEdit.appendPlainText('外来车辆，不予抬杆...')

    def set_label_2_color(self, color):
        pe = QPalette()
        # pe.setColor(QPalette.WindowText, Qt.red)  # 设置字体颜色
        if color == 'red':
            pe.setColor(QPalette.Window, Qt.red)  # 设置背景颜色
            self.ui.label_2.setPalette(pe)
        else:
            pe.setColor(QPalette.Window, Qt.green)  # 设置背景颜色
            self.ui.label_2.setPalette(pe)

    def button_clicked(self):
        filename = self.openfile()
        self.start_check(filename)

    def showTime(self):
        # 获取系统当前时间
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.ui.label_3.setText('当前时间:{}'.format(now_time))
        if self.ser_config.is_open:
            self.set_label_2_color('green')
            self.ui.label_2.setText('设备状态:已连接')
        else:
            self.set_label_2_color('red')
            self.ui.label_2.setText('设备状态:未连接')

    def take_photo(self):
        pass

    def update_serial_info(self):
        while True:
            while self.ser_config.is_open:
                try:
                    serial_info = self.ser_config.recieve_mess()
                    if serial_info != '':
                        rec_mess = (str(serial_info, encoding='utf-8'))
                        if rec_mess:  # 下位机发来拍照信号
                            if self.taken_photo_flag == 0:
                                self.take_photo()
                                self.taken_photo_flag = 1
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
