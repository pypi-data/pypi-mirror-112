# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
__author__ = 'Su Jin Qiang'

from function.cores.stdedit import stdinit

from PyQt5.QtWidgets import QHBoxLayout,QGridLayout,QPushButton,QCheckBox,QColorDialog,QFontDialog,QComboBox,QMessageBox,QLabel,QWidget

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os
from function.conf import res, setup
from function.cores.stdmsg import reso


#import tempfile
# 开发本软件消耗了太多时间精力，一路走来，太不容易，写下此行留为纪念，尤其感谢几位学弟（林鉴波、梁莅、房杰、刘席鸣等一直以来的各方面支持）。——2019.10.22晚


my_sender = 'sam9661@qq.com'  # 发件人邮箱账号sam9661@qq.com  stduino@foxmail.com
my_pass = 'jrtuhtpsukpocjii'  # 发件人邮箱密码   squxhquxrlalbaae
my_user = 'service001@stduino.com'  # 收件人邮箱账号，我这边发送给自己

#pos = os.path.abspath('.')
#path = pos + "\\tool\msy"

#os.chdir("C:\stwork\stdemo2019827\dist\Stduinodebug\main")  # 通过更改当前运行目录F:\BaiduNetdiskDownload\stpython\stdemo\main

class StdBackColor(QWidget):
    def __init__(self):
        try:
            super(StdBackColor, self).__init__()
            self.setWindowOpacity(0.7)
            self.setGeometry(800, 200, 520, 280)
            # self.setFixedSize(420, 220)
            self.setWindowTitle('Background Setting')
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.setWindowIcon(QIcon("appearance/img/st.PNG"))
            self.init_path = stdinit.session_dir + "/mainconfig.cfg"

            # 全局布局（2中）：这里选择水平布局
            wlayout = QHBoxLayout()

            # 局部布局：水平，垂直，网格，表单

            glayout = QGridLayout()

            # 下拉框
            #
            self.combo = QComboBox(self)
            self.combo.addItem(reso.day_model)
            self.combo.addItem(reso.night_model)
            self.combo.addItem(reso.person_model)
            self.combo.setCurrentIndex(res.default_c)
            self.combo.currentIndexChanged.connect(self.toggle)

            # Qlabel

            lbl = QLabel(reso.person_setting, self)
            # lbl1 = QLabel("是否确认更改", self)

            # self.set1_button = QPushButton("字体更改")
            # 绑定传参方式
            # self.set1_button.clicked.connect(lambda: self.c_font(0))
            # 1.编辑栏背景 2.正常文字背景 python3.注释背景颜色 4.主关键字背景 5.函数关键字背景 6.括号背景
            self.set2_button = QPushButton(reso.edit_back_color)
            self.set2_button.clicked.connect(lambda: self.c_color(1))
            self.set3_button = QPushButton(reso.main_back_color)
            self.set3_button.clicked.connect(lambda: self.c_color(2))
            self.set4_button = QPushButton(reso.commenter_back_color)
            self.set4_button.clicked.connect(lambda: self.c_color(3))

            self.set15_button = QPushButton("主关键字背景")
            self.set15_button.clicked.connect(lambda: self.c_color(4))
            self.set16_button = QPushButton("函数关键字背景")
            self.set16_button.clicked.connect(lambda: self.c_color(5))
            self.set17_button = QPushButton("括号分号背景")
            self.set17_button.clicked.connect(lambda: self.c_color(6))
            self.set18_button = QPushButton("汉字背景")
            self.set18_button.clicked.connect(lambda: self.c_color(7))
            self.set19_button = QPushButton("数字背景")
            self.set19_button.clicked.connect(lambda: self.c_color(8))
            self.set20_button = QPushButton("预编译背景")
            self.set20_button.clicked.connect(lambda: self.c_color(9))
            self.stdauto_complete=QCheckBox("括号引号自动完成")
            self.stdauto_complete.clicked.connect(self.stdauto_action)
            self.stdauto_complete.setChecked(res.std_auto)

            self.set5_button = QPushButton(reso.confirm_change)
            self.set5_button.clicked.connect(self.confirm)
            self.set6_button = QPushButton(reso.concle_change)
            self.set6_button.clicked.connect(self.concel)
            self.set7_button = QPushButton(reso.exit_this)
            self.set7_button.clicked.connect(self.close)
            self.set6_button.setEnabled(False)
            self.set5_button.setEnabled(False)

            if res.default_c < 2:
                self.set2_button.setEnabled(False)
                self.set3_button.setEnabled(False)
                self.set4_button.setEnabled(False)
                self.set15_button.setEnabled(False)
                self.set16_button.setEnabled(False)
                self.set17_button.setEnabled(False)
                self.set18_button.setEnabled(False)
                self.set19_button.setEnabled(False)
                self.set20_button.setEnabled(False)

                pass
            else:
                self.set2_button.setEnabled(True)
                self.set3_button.setEnabled(True)
                self.set4_button.setEnabled(True)
                self.set15_button.setEnabled(True)
                self.set16_button.setEnabled(True)
                self.set17_button.setEnabled(True)
                self.set18_button.setEnabled(True)
                self.set19_button.setEnabled(True)
                self.set20_button.setEnabled(True)
                pass

            # line edit
            # LineEdit1 = QLineEdit()

            glayout.addWidget(lbl, 1, 0)
            # glayout.addWidget(LineEdit1, 1, 0)
            # glayout.addWidget(lbl1,1,1)

            # glayout.addWidget(lbl,0,1)
            glayout.addWidget(self.combo, 2, 0)
            # glayout.addWidget(QPushButton("确认"),2,1)
            # glayout.addWidget(QPushButton("取消"),2,2)

            glayout.addWidget(self.set2_button, 3, 0)
            glayout.addWidget(self.set3_button, 4, 0)

            glayout.addWidget(self.set4_button, 5, 0)
            glayout.addWidget(self.set18_button, 2, 1)
            glayout.addWidget(self.set15_button, 3, 1)
            glayout.addWidget(self.set16_button, 4, 1)

            glayout.addWidget(self.set17_button, 5, 1)
            glayout.addWidget(self.set19_button, 2, 2)
            glayout.addWidget(self.set20_button, 3, 2)
            glayout.addWidget(self.stdauto_complete, 4, 2)

            # glayout.addWidget("cd", 6, 0)

            glayout.addWidget(self.set5_button, 7, 1)
            glayout.addWidget(self.set6_button, 7, 2)
            glayout.addWidget(self.set7_button, 7, 3)
            # 准备四个控件
            gwg = QWidget()
            # 使用四个控件设置局部布局
            gwg.setLayout(glayout)
            # 将四个控件添加到全局布局中
            wlayout.addWidget(gwg)
            # 将窗口本身设置为全局布局
            self.setLayout(wlayout)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def stdauto_action(self):
        try:

            if os.path.exists(self.init_path):
                stdinit.pro_conf.clear()
                if res.std_auto==1:
                    res.std_auto=0
                else:
                    res.std_auto = 1
                stdinit.pro_conf.read(self.init_path, encoding="utf-8")  # python3
                stdinit.pro_conf.set("std_type", "std_auto", str(res.std_auto))
                stdinit.pro_conf.write(open(self.init_path, 'w'))

        except:
            stdinit.std_signal_gobal.stdprintln()




    def c_color(self, idd):
        try:
            self.set5_button.setEnabled(True)
            self.set6_button.setEnabled(True)
            # print(121)
            color = QColorDialog.getColor(Qt.blue, self, "Select Color")
            # 1.编辑栏背景 2.正常文字背景 python3.注释背景颜色 4.主关键字背景 5.函数关键字背景 6.括号背景
            if color.isValid():
                # return color.name()
                # the_window.setcolor_all(color.name(), idd)
                stdinit.std_signal_gobal.std_back_color(color.name(), idd)
                if idd == 1:
                    self.set2_button.setStyleSheet("background-color:" + color.name() + ";")  ########## 串口查找按钮
                elif idd == 2:
                    self.set3_button.setStyleSheet("background-color:" + color.name() + ";")  ########## 串口查找按钮
                elif idd == 3:
                    self.set4_button.setStyleSheet("background-color:" + color.name() + ";")  ########## 串口查找按钮
                elif idd == 4:
                    self.set15_button.setStyleSheet("background-color:" + color.name() + ";")  ########## 串口查找按钮
                elif idd == 5:
                    self.set16_button.setStyleSheet("background-color:" + color.name() + ";")  ########## 串口查找按钮
                elif idd == 6:
                    self.set17_button.setStyleSheet("background-color:" + color.name() + ";")  ########## 串口查找按钮
                elif idd == 7:
                    self.set18_button.setStyleSheet("background-color:" + color.name() + ";")  ########## 串口查找按钮
                elif idd == 8:
                    self.set19_button.setStyleSheet("background-color:" + color.name() + ";")  ########## 串口查找按钮
                else:
                    self.set20_button.setStyleSheet("background-color:" + color.name() + ";")  ########## 串口查找按钮
        except:
            stdinit.std_signal_gobal.stdprintln()



            # QsciLexerC.__lexer.setColor(QColor(color.name()), QsciLexerCPP.CommentLine)  # 注释 #66CDAA  #1C1C1C  黑
            # print(color.name(), color)
            # self.myButton.setPalette(QPalette(color))  # 给按钮填充背景色
            # self.myButton.setAutoFillBackground(True)

    def c_font(self, idd):
        try:
            font, ok = QFontDialog.getFont()
            if ok:
                # the_window.setcolor_all(font, idd)
                stdinit.std_signal_gobal.std_back_color(font, idd)
                # print(font)
        except:
            stdinit.std_signal_gobal.stdprintln()



    def confirm(self, event):
        try:
            self.set6_button.setEnabled(True)
            self.set5_button.setEnabled(False)

            reply = QMessageBox.question(self, reso.tip, reso.reset_up,
                                         QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                setup.save_confirm(str(self.combo.currentIndex()))
                # event.accept()
            else:
                pass
        except:
            stdinit.std_signal_gobal.stdprintln()




    def concel(self):
        try:
            self.set6_button.setEnabled(False)
            setup.save_confirm(str(res.default_c))
        except:
            stdinit.std_signal_gobal.stdprintln()


        # setup.save_mstyle(res.default_main)
        # setup.save_mstyle(res.default_text)
        # setup.save_cstyle(res.default_comment)

    def toggle(self, state):
        try:
            self.set5_button.setEnabled(True)
            # setup.save_confirm(state)
            if state < 2:
                self.set2_button.setEnabled(False)
                self.set3_button.setEnabled(False)
                self.set4_button.setEnabled(False)
                self.set15_button.setEnabled(False)
                self.set16_button.setEnabled(False)
                self.set17_button.setEnabled(False)
                self.set18_button.setEnabled(False)
                self.set19_button.setEnabled(False)
                self.set20_button.setEnabled(False)
                pass
            else:
                self.set2_button.setEnabled(True)
                self.set3_button.setEnabled(True)
                self.set4_button.setEnabled(True)
                self.set15_button.setEnabled(True)
                self.set16_button.setEnabled(True)
                self.set17_button.setEnabled(True)
                self.set18_button.setEnabled(True)
                self.set19_button.setEnabled(True)
                self.set20_button.setEnabled(True)
                pass
        except:
            stdinit.std_signal_gobal.stdprintln()


