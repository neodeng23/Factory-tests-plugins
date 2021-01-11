# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *  # PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from main_ui import *  # 导入designer工具生成的login模块
from check_log import *

run_test_cmd = """
        osascript -e '
        tell application "System Events"
	        tell process "Hyperion"
		        click button "Start" of window 1 of application process "Hyperion" of application "System Events"
	        end tell
        end tell
        '
      """


# class EmittingStream(QtCore.QObject):
#     textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号
#
#     def write(self, data):
#         self.textWritten.emit(str(data))


class BackendThread(QThread):
    update_date = pyqtSignal(str)  # 通过类成员对象定义信号

    # 处理业务逻辑
    def run(self):
        now_size = getdirsize(monitor_dir)
        while True:
            data = QDateTime.currentDateTime()
            currTime = data.toString("yyyy-MM-dd hh:mm:ss")
            new_size = getdirsize(monitor_dir)
            if now_size != new_size:
                time.sleep(1)
                SN, res = get_newlog_res()
                test_res = SN + " : " + res
                if res == "PASS":
                    myWin.label.setStyleSheet(m_green_SheetStyle)
                    self.update_date.emit(str(currTime + " " + test_res))
                else:
                    myWin.label.setStyleSheet(m_red_SheetStyle)
                    self.update_date.emit(str(currTime + " " + test_res))
                time.sleep(5)
            else:
                myWin.label.setStyleSheet(m_yellow_SheetStyle)
                time.sleep(1)
                pass
            now_size = new_size


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setWindowTitle("MainWindow")
        self.setupUi(self)
        self.pushButton.clicked.connect(self.onClick_Button)

    def initUI(self):
        self.backend = BackendThread()  # 创建线程
        self.backend.update_date.connect(self.handleDisplay)  # 连接信号
        self.backend.start()  # 开始线程

    def handleDisplay(self, data):
        cursor = self.QTextEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        # self.textEdit.setText(data)
        cursor.insertText(data + '\n')
        self.QTextEdit.setTextCursor(cursor)
        self.QTextEdit.ensureCursorVisible()

    def onClick_Button(self):
        os.system(run_test_cmd)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    myWin = MyMainForm()
    myWin.initUI()
    myWin.show()
    sys.exit(app.exec())
