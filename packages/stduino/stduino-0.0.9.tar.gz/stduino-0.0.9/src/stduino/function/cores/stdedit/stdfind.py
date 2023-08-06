# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
__author__ = 'Su Jin Qiang'

# from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget,QFormLayout,QPushButton,QLineEdit,QLabel
from PyQt5.QtGui import QIcon
from function.cores.stdmsg import reso
from PyQt5 import QtCore, QtWidgets
from function.cores.stdedit import stdinit

#import tempfile
# 开发本软件消耗了太多时间精力，一路走来，太不容易，写下此行留为纪念，尤其感谢几位学弟（林鉴波、梁莅、房杰、刘席鸣等一直以来的各方面支持）。——2019.10.22晚

#pos = os.path.abspath('.')
#path = pos + "\\tool\msy"

#os.chdir("C:\stwork\stdemo2019827\dist\Stduinodebug\main")  # 通过更改当前运行目录F:\BaiduNetdiskDownload\stpython\stdemo\main


class StdFind(QWidget):

    def __init__(self, parent=None):
        try:
            super(StdFind, self).__init__(parent)
            self.setGeometry(680, 300, 350, 100)
            self.setFixedSize(350, 130)
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.setWindowIcon(QIcon("appearance/img/st.PNG"))

            # 表单布局
            layout = QFormLayout()

            # 创建按钮，当行文本框并建立按钮点击与槽函数的联系，添加到布局中
            self.btn1 = QPushButton(reso.find_next)
            self.le1 = QLineEdit()
            self.le2 = QLineEdit()
            self.qfind = QtWidgets.QCheckBox()
            self.qfind.setChecked(True)
            self.btn1.clicked.connect(lambda: self.getItem(0))

            layout.addRow(self.le1, self.btn1)

            # 创建按钮，当行文本框并建立按钮点击与槽函数的联系，添加到布局中
            self.btn2 = QPushButton(reso.replace_next)
            self.btn2.clicked.connect(lambda: self.getItem(1))

            layout.addRow(self.le2, self.btn2)

            # 创建按钮，当行文本框并建立按钮点击与槽函数的联系，添加到布局中
            self.btn3 = QPushButton(reso.replace_all)
            self.btn3.clicked.connect(lambda: self.getItem(2))

            lbl = QLabel(reso.match, self)
            lbl.setGeometry(QtCore.QRect(30, 81, 90, 20))
            layout.addRow(self.qfind, self.btn3)

            # 设置主窗口的布局及标题
            self.setLayout(layout)
            self.setWindowTitle(reso.search)

        except:
            stdinit.std_signal_gobal.stdprintln()


    def getItem(self, id):
        try:
            idd = id
            findtext = self.le1.text()
            changetext = self.le2.text()
            afind = self.qfind.isChecked()
            stdinit.std_signal_gobal.std_find(idd, changetext, findtext, afind)

            # the_window.Tofind(idd, changetext, findtext, afind)

            # the_window.__editor.
            # to_find_text = 'delay'
            # ASt=the_window.__editor.findFirst(to_find_text,True,True,True,True)
            # self.__editor.replaceSelectedText('a')
            # self.__editor.#setAlignment()
            # while (self.__editor.find(to_find_text,QTextDocument.FindBackward)):#QTextDocument.FindBackward()
            # self.__editor.findFirst(to_find_text)
        except:
            stdinit.std_signal_gobal.stdprintln()


        # QMessageBox.critical(self, "Port Error", "此串口不能被打开！")


