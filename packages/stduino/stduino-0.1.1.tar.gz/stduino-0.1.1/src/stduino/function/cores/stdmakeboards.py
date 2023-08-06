# import sys
from PyQt5.QtWidgets import QWidget, QComboBox, QLabel,QPushButton,QGridLayout
from PyQt5.QtCore import Qt
import threading
from function.cores.stdedit import stdinit
class StdMakeBoard(QWidget):
    def __init__(self):
        super().__init__()
        try:
            # 设置标题
            # self.setWindowTitle('ComBox例子')
            # # 设置初始界面大小
            # self.resize(300, 200)
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            # self.setWindowIcon(QIcon("appearance/img/st.PNG"))
            self.setStyleSheet('background: DimGrey')

            # 实例化QComBox对象

            self.cb = QComboBox(self)
            self.make_sec=1
            # self.cb.move(100, 20)
            self.tip_text = QLabel("该示例中含有多个芯片型号\n\n请选择目标芯片型号")

            # 单个添加条目
            # self.cb.addItem('C')
            # self.cb.addItem('C++')
            # self.cb.addItem('Python')
            # 多个添加条目

            # wlayout = QVBoxLayout()

            # 局部布局：水平，垂直，网格，表单
            glayout = QGridLayout()
            # line edit
            # LineEdit1 = QLineEdit()
            sec_board = QPushButton("确定")
            sec_board.clicked.connect(self.print_value)
            no_board = QPushButton("取消")
            no_board.clicked.connect(self.cancel)

            glayout.addWidget(self.tip_text, 1, 0)  # name platform board fromwork  下载方式
            glayout.addWidget(self.cb, 2, 0)

            glayout.addWidget(sec_board, 11, 0)
            glayout.addWidget(no_board, 11, 1)
            # 准备四个控件
            # gwg = QWidget()
            # # 使用四个控件设置局部布局
            # gwg.setLayout(glayout)
            # # 将四个控件添加到全局布局中
            # wlayout.addWidget(gwg)
            self.setLayout(glayout)
        except:
            stdinit.std_signal_gobal.stdprintln()
        #self.init_cores()

        # 信号
        # self.cb.currentIndexChanged[str].connect(self.print_value) # 条目发生改变，发射信号，传递条目内容
        # self.cb.currentIndexChanged[int].connect(self.print_value)  # 条目发生改变，发射信号，传递条目索引
        # self.cb.highlighted[str].connect(self.print_value)  # 在下拉列表中，鼠标移动到某个条目时发出信号，传递条目内容
        # self.cb.highlighted[int].connect(self.print_value)  # 在下拉列表中，鼠标移动到某个条目时发出信号，传递条目索引
    # def init_cores(self):
    #     self.cb.addItems(['Java', 'C#', 'PHP'])

    def make_run(self):
        try:
            if self.make_sec==1:
                stdinit.Std_Make.std_run()
            elif self.make_sec==2:
                stdinit.Std_Make.std_upload()
            elif self.make_sec==3:
                stdinit.Std_Make.std_upload()
            elif self.make_sec==4:
                stdinit.Std_Make.std_clean()


        except:
            stdinit.std_signal_gobal.stdprintln()

    def print_value(self):
        try:
            stdinit.std_make_board = self.cb.currentText()
            t1 = threading.Thread(target=self.make_run, name='make_run')
            t1.setDaemon(True)
            t1.start()
            self.close()

        except:
            stdinit.std_signal_gobal.stdprintln()

    def cancel(self):
        try:

            self.close()
            stdinit.std_signal_gobal.std_make_signal(0)
        except:
            stdinit.std_signal_gobal.stdprintln()




# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     comboxDemo = StdMakeBoard()
#     comboxDemo.show()
#     sys.exit(app.exec_())