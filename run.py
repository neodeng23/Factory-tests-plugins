# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow   # PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from main_ui import *  # 导入designer工具生成的login模块
from check_log import *


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        #self.status.showMessage("run_Test", 5000)
        self.setWindowTitle("MainWindow")
        self.setupUi(self)

        self.pushButton.clicked.connect(self.on_pushButton_clicked)    # 按键事件

    def on_pushButton_clicked(self):
        self.QLineEdit.append("开始监控测试")
        now_size = getdirsize(monitor_dir)
        while True:
            new_size = getdirsize(monitor_dir)
            if now_size != new_size:
                SN, res = get_newlog_res()
                self.QLineEdit.append(SN + " : " + res + "\n")
                if res == "PASS":
                    self.label.setStyleSheet(m_green_SheetStyle)
                else:
                    self.label.setStyleSheet(m_red_SheetStyle)
                time.sleep(5)
            else:
                self.label.setStyleSheet(m_yellow_SheetStyle)
                pass
            now_size = new_size


if __name__ == "__main__":
    app = QApplication(sys.argv)            # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec())

