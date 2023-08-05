# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

# from six.moves import urllib  # 下载文件
import json
#import zipfile  # 解压文件
# import shutil  # 用于压缩
# import subprocess
import os,stat
import sys
import re
# import socket
#
# import zipfile

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel,pyqtSignal,QThread
# from function.conf import res
from function.cores.stdmsg import reso

from PyQt5.QtWidgets import QMessageBox

import threading
from function.cores.stdedit import stdinit
import time

# fo = open("./appearance/stduino_json/library.json", mode='r', encoding='UTF-8')
# st = fo.read()
# fo.close()
# libraries = json.loads(st)

class stdthread(QThread):
    std_signal = pyqtSignal(str)
    def __init__(self):
        super(stdthread, self).__init__()
    def run(self):
        try:
            # a = (1, 2)
            # self.mysignal.emit(a)  # 发射自定义信号
            if stdinit.callch == 1:
                self.install_pio()
            elif stdinit.callch == 2:
                self.install_p()
        except:
            stdinit.std_signal_gobal.stdprintln()

    def install_pio(self):
        try:
            if stdinit.Pio_install.is_installed_pio():
                stdinit.std_signal_gobal.std_process(1, reso.package_uninstall)

                if stdinit.Pio_install.pio_uninstall():
                    self.std_signal.emit(reso.install_lib)
                    # self.install.setText(reso.install_lib)
                    stdinit.std_signal_gobal.std_process(0, reso.package_uninstall)
                    stdinit.std_signal_gobal.std_echo_msg(0, "卸载" + stdinit.package_choose_name + "成功！")
                else:
                    self.std_signal.emit(reso.install_lib)
                    stdinit.std_signal_gobal.std_process(0, reso.package_uninstall)
                    stdinit.std_signal_gobal.std_echo_msg(0, "卸载" + stdinit.package_choose_name + "失败！")


            else:
                stdinit.std_signal_gobal.std_process(1, reso.downloading)
                if stdinit.Pio_install.pio_install():
                    # self.install.setText(reso.package_uninstall)
                    self.std_signal.emit(reso.package_uninstall)
                    stdinit.std_signal_gobal.std_process(0, reso.downloading)
                    stdinit.std_signal_gobal.std_echo_msg(0, "安装" + stdinit.package_choose_name + "成功！")
                else:
                    self.std_signal.emit(reso.install_lib)
                    stdinit.std_signal_gobal.std_process(0, reso.downloading)
                    stdinit.std_signal_gobal.std_echo_msg(0, "安装" + stdinit.package_choose_name + "失败！")
        except:
            stdinit.std_signal_gobal.stdprintln()

    def install_p(self):
        try:
            for i in range(0, 5):

                time.sleep(1)

        except:
            stdinit.std_signal_gobal.stdprintln()


class StdAddPackages(QWidget):  # 安装库文件

    add_lib_s = pyqtSignal(int,int,str)
    def __init__(self):
        try:
            super(StdAddPackages, self).__init__()
            self.add_lib_s_load_f = 0
            self.find_more_p = 1
            self.pio_libs = []
            self.pio_libs.append(0)
            self.lib_list = []
            self.initUi()
        except:
            stdinit.std_signal_gobal.stdprintln()

    def initUi(self):
        try:
            self.bigEditor = QTextEdit()
            self.bigEditor.setReadOnly(True)


            #self.createGridGroupBox()
            self.createGridGroupBox2()
            self.creatVboxGroupBox()
            self.creatVboxGroupBox2()
            mainLayout = QVBoxLayout()
            hboxLayout = QHBoxLayout()
            hboxLayout.addWidget(self.vboxGroupBox2)
            hboxLayout.addWidget(self.vboxGroupBox)

            #the_window.add_lib_s_load.connect(self.libr_load)



            self.find_more = QPushButton(reso.lib_find_more, self)
            self.find_more.clicked.connect(self.find_mores)
            self.find_more.setEnabled(False)
            self.install = QPushButton(reso.install_lib, self)
            self.install.setDisabled(True)
            self.install.clicked.connect(self.install_url)
            self.install_return = QPushButton(reso.library_installer, self)
            self.install_return.clicked.connect(self.install_ret)
            #self.install.setFixedWidth(120)
            #self.pro1 = QProgressBar(self)
            # self.pro1.setOrientation(Qt.Horizontal)
            # self.pro1.setMinimum(0)
            # self.pro1.setMaximum(0)
            #self.pro1.setVisible(False)

            glayout = QGridLayout()
            glayout.addWidget(self.install, 0, 0)
            glayout.addWidget(self.find_more, 0, 1)
            glayout.addWidget(self.install_return, 0, 2)


            # 准备四个控件
            gwg = QWidget()
            # 使用四个控件设置局部布局
            gwg.setLayout(glayout)
            # 将四个控件添加到全局布局中


            #mainLayout.addWidget(self.gridGroupBox)
            mainLayout.addLayout(hboxLayout)
            mainLayout.addWidget(self.gridGroupBox2)
            #mainLayout.addWidget(self.pro1)
            mainLayout.addWidget(gwg)
            #mainLayout.addWidget(self.install_return)
            self.setLayout(mainLayout)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def libr_load(self):
        try:
            if self.add_lib_s_load_f == 0:
                self.add_lib_s_load_f = 1
                t1 = threading.Thread(target=self.library_load, name='li_load1')
                t1.setDaemon(True)
                t1.start()

        except:
            stdinit.std_signal_gobal.stdprintln()




    def createGridGroupBox2(self):
        try:
            self.gridGroupBox2 = QGroupBox(reso.lib_version)
            self.layout = QGridLayout()
            # nameLabel = QLabel("发布版本时间")
            self.vsion = QCheckBox(reso.select_version, self)
            self.vsion.setChecked(True)
            self.vsion.setEnabled(False)
            # self.vsion.stateChanged.connect(self.check_vsion)
            self.combobox_1 = QComboBox(self)
            self.combobox_1.setDisabled(True)
            self.layout.setSpacing(10)
            self.layout.addWidget(self.vsion, 1, 0)
            self.combobox_1.addItem("")
            self.layout.addWidget(self.combobox_1, 1, 1)
            self.layout.setColumnStretch(1, 10)
            self.gridGroupBox2.setLayout(self.layout)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def creatVboxGroupBox(self):
        try:
            self.vboxGroupBox = QGroupBox(reso.lib_detail)
            layout = QVBoxLayout()
            self.bigEditor.setPlainText(reso.lib_select)
            layout.addWidget(self.bigEditor)
            self.vboxGroupBox.setLayout(layout)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def creatVboxGroupBox2(self):

        try:
            self.vboxGroupBox2 = QGroupBox(reso.package_list)
            layout = QVBoxLayout()
            self.model_1 = QStringListModel(self)
            self.listview_1 = QListView(self)  # python3
            self.model_1.setStringList(self.lib_list)
            self.listview_1.setModel(self.model_1)

            self.listview_1.setEditTriggers(QAbstractItemView.NoEditTriggers)
            #self.listview_1.setFixedWidth(600)
            #self.listview_1.setFixedHeight(400)
            self.listview_1.clicked.connect(self.clicked)
            layout.addWidget(self.listview_1)
            self.vboxGroupBox2.setLayout(layout)
                    # self.listview_1.doubleClicked.connect(lambda: self.change_func(self.listview_1))
                    # self.listview_1.doubleClicked.connect(self.cs)

                    #self.listview_1.clicked.connect(self.clicked)
        except:
            self.lib_list = [reso.no_net]
            self.model_1 = QStringListModel(self)
            self.listview_1 = QListView(self)  # python3


            self.model_1.setStringList(self.lib_list)
            self.listview_1.setModel(self.model_1)
            self.listview_1.setEditTriggers(QAbstractItemView.NoEditTriggers)
            #self.listview_1.setFixedWidth(600)
            #self.listview_1.setFixedHeight(400)

            # self.item_list = ['item %s' % i for i in range(51)]  # 1
            stdinit.std_signal_gobal.stdprintln()

    def library_load(self):
        try:
            self.install_return.setText("Finding Library File...")
            lib_show = "PlatformIO\nby platformio    |    License:Apache 2.0"
            self.lib_list.append(lib_show + "\n")
            self.model_1.setStringList(self.lib_list)

            self.listview_1.setModel(self.model_1)
            self.install_return.setText(reso.library_installer)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def thread_return(self,strin):
        try:
            self.install.setText(strin)
            self.install.setEnabled(True)
            self.listview_1.setEnabled(True)
        except:
            stdinit.std_signal_gobal.stdprintln()



    def install_ret(self):#退出安装界面
        try:
            stdinit.std_signal_gobal.std_main_ui_change(3)
            # the_window.m_stackedLayout.setCurrentIndex(0)
            # the_window.liAct2.setEnabled(True)
        except:
            stdinit.std_signal_gobal.stdprintln()
    def clicked(self):#(self, qModelIndex):
        #self.my_thread.mysignal.connect(self.zhi)  # 自定义信号连接
        try:
            #n_lin=qModelIndex.row()
            descrabe = "A professional collaborative platform for embedded development. Cross-platform IDE and Unified Debugger. Static Code Analyzer and Remote Unit Testing. Multi-platform and Multi-architecture Build System. Firmware File Explorer and Memory Inspection. IoT, Arduino, CMSIS, ESP-IDF, FreeRTOS, libOpenCM3, mbedOS, Pulp OS, SPL, STM32Cube, Zephyr RTOS, ARM, AVR, Espressif (ESP8266/ESP32), FPGA, MCS-51 (8051), MSP430, Nordic (nRF51/nRF52), NXP i.MX RT, PIC32, RISC-V, STMicroelectronics (STM8/STM32), Teensy."#self.pio_libs[n_lib]["items"][n_lin]['description']+ "\n\nTag:"
            descrabe=descrabe+"\n\nHomepage:https://platformio.org"
            self.combobox_1.clear()
            stdinit.package_choose_name= "platformio"
            self.combobox_1.addItem("5.1.0")
            if stdinit.Pio_install.is_installed_pio():
                self.install.setDisabled(False)
                self.install.setText(reso.package_uninstall)
                pass
            else:
                self.install.setDisabled(False)
                self.install.setText(reso.install_lib)

            self.bigEditor.setText(descrabe)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def remove_readonly(self,func, path, _):
        try:
            # "Clear the readonly bit and reattempt the removal"
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def install_url(self):

        try:
            self.install.setEnabled(False)
            self.listview_1.setEnabled(False)
            if stdinit.Pio_install.is_installed_pio():
                ok = QMessageBox.information(self,
                                             "提示",
                                             "确认要卸载" + stdinit.package_choose_name + "？",
                                             QMessageBox.Yes, QMessageBox.No)
                if ok == QMessageBox.No:
                    return 0
            self.my_thread = stdthread()  # 步骤2. 主线程连接子线,同时传递一个值给子线程
            self.my_thread.std_signal.connect(self.thread_return)
            stdinit.callch = 1
            self.my_thread.start()  # 步骤3 子线程开始执行run函数
        except:
            stdinit.std_signal_gobal.stdprintln()
        #t1 = threading.Thread(target=pay_ticket, name='th1')



    def schedule(self,blocknum, blocksize, totalsize):
        try:
            # """
            #         blocknum:当前已经下载的块
            #         blocksize:每次传输的块大小
            #         totalsize:网页文件总大小
            #         """
            per = 100 * blocknum * blocksize / totalsize

            if per > 100:
                per = 100
                self.install_return.setText("Installing Package...")

            self.add_lib_s.emit(2, int(per), "")  # 2进度条数值
        except:
            stdinit.std_signal_gobal.stdprintln()

    def find_mores(self):
        try:
            self.install_return.setText("Finding File...")
            self.find_more_p = self.find_more_p + 1
            self.pio_libs.append(self.lib.lib_search(self.find_more_p))
            ii = len(self.pio_libs[self.find_more_p]['items'])
            i = 0
            while i < ii:
                self.lib_list.append(self.pio_libs[self.find_more_p]['items'][i]['name'] + "\ndescription:" +
                                     self.pio_libs[self.find_more_p]['items'][i]['description'] + "\n")  #
                i = i + 1
            self.model_1.setStringList(self.lib_list)

            self.listview_1.setModel(self.model_1)
            self.install_return.setText(reso.library_installer)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def check_vsion(self):
        try:
            if self.vsion.isChecked():
                self.combobox_1.setDisabled(False)
            else:
                self.combobox_1.setDisabled(True)
        except:
            stdinit.std_signal_gobal.stdprintln()





# class Model(object):
#     def logic(self):
#         data = "Got it"
#         print("Model: Crunching data as per business logic")
#         return data
#
#
# class View(object):
#     def updata(self, data):
#         print("View:Updating the view with results: ", data)
#
#
# class Controller(object):
#     def __init__(self):
#         self.model = Model()
#         self.view = View()
#
#     def interface(self):
#         print("Controller: Relayed the Client asks")
#         data = self.model.logic()
#         self.view.updata(data)

if __name__ == '__main__':  # main函数
    app = QApplication(sys.argv)

    try:


        d = StdAddPackages()
        d.show()

        # the_window.fileName = reso.lastfile
        # the_window.loadFile(reso.lastfile)



    except:
        pass
    sys.exit(app.exec_())


