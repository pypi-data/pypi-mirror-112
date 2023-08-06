# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
#
# from six.moves import urllib  # 下载文件
import json
#import zipfile  # 解压文件
# import shutil  # 用于压缩
# import subprocess
import os,stat
import sys
# import re
# import socket
#
# import zipfile
#
# import time

from PyQt5.QtWidgets import QComboBox,QTextEdit,QLabel,QVBoxLayout,QWidget,QHBoxLayout,QPushButton,QGridLayout,QGroupBox,QLineEdit,QCheckBox,QListView,QAbstractItemView

from PyQt5.QtCore import Qt,QStringListModel,pyqtSignal
from function.piobuilder.piolibinstall import PioLibInstall

# from function.conf import res
from function.cores.stdmsg import reso
from function.cores.stdedit import stdinit

import threading



# fo = open("./appearance/stduino_json/library.json", mode='r', encoding='UTF-8')
# st = fo.read()
# fo.close()
# libraries = json.loads(st)
class StdAddLibs(QWidget):  # 安装库文件

    add_lib_s = pyqtSignal(int,int,str)

    def __init__(self):

        super(StdAddLibs, self).__init__()
        try:
            self.lib = PioLibInstall()
            self.add_lib_s_load_f = 0
            self.lib_p = 1
            self.find_more_p = 1
            self.pio_libs = []
            self.pio_lib=[]
            self.pio_libs.append(0)
            self.search_more_p = 1
            self.lib_list = []
            self.choose_id = 0
            self.initUi()
        except:
            stdinit.std_signal_gobal.stdprintln()



    def initUi(self):
        try:
            self.bigEditor = QTextEdit()
            self.bigEditor.setReadOnly(True)

            self.createGridGroupBox()
            self.createGridGroupBox2()
            self.creatVboxGroupBox()
            self.creatVboxGroupBox2()
            mainLayout = QVBoxLayout()
            hboxLayout = QHBoxLayout()
            hboxLayout.addWidget(self.vboxGroupBox2)
            hboxLayout.addWidget(self.vboxGroupBox)

            self.find_more = QPushButton(reso.lib_find_more, self)
            self.find_more.clicked.connect(self.find_mores)
            self.install_return = QPushButton(reso.library_installer, self)
            self.install_return.clicked.connect(self.install_ret)
            self.install = QPushButton(reso.install_lib, self)
            self.install.setDisabled(True)
            self.install.clicked.connect(self.install_url)


            glayout = QGridLayout()
            glayout.addWidget(self.install, 0, 0)
            glayout.addWidget(self.find_more, 0, 1)
            glayout.addWidget(self.install_return, 0, 2)


            # 准备四个控件
            gwg = QWidget()
            # 使用四个控件设置局部布局
            gwg.setLayout(glayout)
            # 将四个控件添加到全局布局中


            mainLayout.addWidget(self.gridGroupBox)
            mainLayout.addLayout(hboxLayout)
            mainLayout.addWidget(self.gridGroupBox2)
            #mainLayout.addWidget(self.pro1)
            mainLayout.addWidget(gwg)
            #mainLayout.addWidget(self.install_return)
            self.setLayout(mainLayout)
        except:
            stdinit.std_signal_gobal.stdprintln()
    def check_net(self):
        try:
            return stdinit.std_signal_gobal.is_connected()

        except:
            return False
    def libr_load(self):
        try:
            if self.check_net()==False:
                return False
            if self.add_lib_s_load_f == 0:
                self.add_lib_s_load_f = 1
                t1 = threading.Thread(target=self.library_load, name='li_load1')
                t1.setDaemon(True)
                t1.start()

        except:
            stdinit.std_signal_gobal.stdprintln()


    def createGridGroupBox(self):
        try:
            self.gridGroupBox = QGroupBox(reso.search_lib)
            layout = QGridLayout()
            nameLabel = QLabel(reso.lib_search)
            self.nameLineEdit = QLineEdit("")
            # self.nameLineEdit.editingFinished.connect(self.find_lib)
            #self.nameLineEdit.textChanged.connect(self.find_lib)
            self.search_lib_button=QPushButton(reso.search)
            self.search_lib_button.clicked.connect(self.find_lib)
            layout.setSpacing(10)
            layout.addWidget(nameLabel, 1, 0)
            layout.addWidget(self.nameLineEdit, 1, 1)
            layout.addWidget(self.search_lib_button, 1,2)
            layout.setColumnStretch(1, 10)
            self.gridGroupBox.setLayout(layout)
            self.setWindowTitle(reso.stduino_lib_install)
            #self.setFixedWidth(955)
            #self.setWindowIcon(QIcon("appearance/img/st.PNG"))
            #self.setFixedHeight(684)
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
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
            #self.vsion.stateChanged.connect(self.check_vsion)
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
            self.vboxGroupBox2 = QGroupBox(reso.lib_list)
            layout = QVBoxLayout()

            self.model_1 = QStringListModel(self)
            self.listview_1 = QListView(self)  # python3
            self.lib_list = ["正在加载中~"]
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
            if self.check_net()==False:
                return False

            self.lib_list.clear()
            self.pio_lib = self.lib.lib_search(self.find_more_p)
            if self.pio_lib == None:

                target = stdinit.stdenv + "/.stduino/packages/pioenv/pioboards.json"  # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"
                if os.path.exists(target):
                    stdinit.std_signal_gobal.std_echo_msg(0, "请重启软件再次打开该界面若还存在该问题，请至插件安装界面卸载并重新安装Platformio！")
                else:
                    stdinit.std_signal_gobal.std_echo_msg(0, "当前插件安装存在文件缺失，请至插件安装界面卸载并重新安装Platformio！")
                return 0
            stdinit.std_signal_gobal.std_echo_msg(1, "Page:" + str(self.pio_lib['page']) + " | Total:" + str(
                self.pio_lib['total']))
            #self.pio_libs.append(self.pio_lib)

            ii = len(self.pio_lib['items'])
            if ii > 0:
                pass
            else:
                return 0
            i = 0
            while i < ii:
                try:  # libs['items'][0]['name']
                    lib_show = self.pio_lib['items'][i]['name'] + "\nby " + \
                               self.pio_lib['items'][i]['authornames'][
                                   0] + "    |    Downloads:" + str(
                        self.pio_lib['items'][i]['dllifetime']) + "\nSupported frameworks: "
                    i_lib = len(self.pio_lib['items'][i]['frameworks'])
                    i_li = 0
                    while i_li < i_lib:
                        if i_li > 0:
                            lib_show = lib_show + "," + self.pio_lib['items'][i]['frameworks'][i_li][
                                "title"]
                        else:
                            lib_show = lib_show + self.pio_lib['items'][i]['frameworks'][i_li][
                                "title"]
                        i_li = i_li + 1
                    self.lib_list.append(lib_show + "\n")
                except:
                    stdinit.std_signal_gobal.stdprintln()
                    break
                i = i + 1
            self.model_1.setStringList(self.lib_list)
            self.listview_1.setModel(self.model_1)

        except:
            stdinit.std_signal_gobal.stdprintln()




    def install_ret(self):
        try:

            #self.libui_change.emit()
            stdinit.std_signal_gobal.std_main_ui_change(1)
            # the_window.m_stackedLayout.setCurrentIndex(0)
            # the_window.liAct2.setEnabled(True)

        except:
            stdinit.std_signal_gobal.stdprintln()
    def clicked(self, qModelIndex):
        try:

            n_lin=qModelIndex.row()
            #n_lib = int(n_lin / 10)+1
            # if n_lin>9:
            #     n_lin = int(n_lin % 10)
            descrabe = self.pio_lib["items"][n_lin]['description']+ "\n\nTag:"
            i_lib = len(self.pio_lib['items'][n_lin]['keywords'])
            i_li = 0
            while i_li < i_lib:
                if i_li > 0:
                    descrabe = descrabe + "," + self.pio_lib['items'][n_lin]['keywords'][i_li]
                else:
                    descrabe = descrabe + self.pio_lib['items'][n_lin]['keywords'][i_li]

                i_li = i_li + 1
            descrabe=descrabe+"\n\nSupported platforms:"
            i_lib = len(self.pio_lib['items'][n_lin]['platforms'])
            i_li = 0
            while i_li < i_lib:
                if i_li > 0:
                    descrabe = descrabe + "," + self.pio_lib['items'][n_lin]['platforms'][i_li]['title']
                else:
                    descrabe = descrabe + self.pio_lib['items'][n_lin]['platforms'][i_li]['title']

                i_li = i_li + 1

            # for i in

            self.combobox_1.clear()
            #self.pio_libs[self.find_more_p]['items'][i]['name']

            self.choose_id=self.pio_lib['items'][n_lin]['id']

            self.combobox_1.addItem(self.pio_lib["items"][n_lin]['updated'])

            if self.install.isEnabled() == False:
                self.install.setDisabled(False)

            # if self.find_more.isEnabled() == False:
            #     self.find_more.setDisabled(False)

            self.bigEditor.setText(descrabe)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def remove_readonly(self,func, path, _):
        try:
            #"Clear the readonly bit and reattempt the removal"
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def install_lib(self):

        try:
            if self.check_net()==False:
                return False
            stdinit.std_signal_gobal.std_process(1,reso.downloading)
            self.lib.lib_install(str(self.choose_id))
            self.install.setDisabled(False)
            self.listview_1.setEnabled(True)
            stdinit.std_signal_gobal.std_process(0, reso.downloading)
        except:
            stdinit.std_signal_gobal.stdprintln()
            stdinit.std_signal_gobal.std_process(0, reso.downloading)

    def install_url(self):
        # from multiprocessing import Process
        # p = Process(target=self.install_url1, args=(1,))
        # print(1)
        try:
            if self.check_net()==False:
                return False
            self.install.setEnabled(False)
            self.listview_1.setEnabled(False)
            #self.my_thread = stdthread()  # 步骤2. 主线程连接子线,同时传递一个值给子线程
            # self.my_thread.std_signal.connect(self.thread_return)
            # stdinit.callch = 1
            # self.my_thread.start()  # 步骤3 子线程开始执行run函数
            t1 = threading.Thread(target=self.install_lib, name='th1', args=())
            t1.setDaemon(True)
            t1.start()

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
                self.install_return.setText("Installing Library...")

            self.add_lib_s.emit(2, int(per), "")  # 2进度条数值

        except:
            stdinit.std_signal_gobal.stdprintln()


    def find_more_lib(self):
        try:
            if self.check_net()==False:
                return False
            #self.install_return.setText("Finding Library File...")
            stdinit.std_signal_gobal.std_process(1,reso.search)
            self.find_more.setEnabled(False)
            self.find_more_p = self.find_more_p + 1
            self.lib_p= self.lib_p + 1
            self.lib_list.clear()
            self.pio_lib=self.lib.lib_search(self.find_more_p)
            if self.pio_lib == None:

                target = stdinit.stdenv + "/.stduino/packages/pioenv/pioboards.json"  # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"
                if os.path.exists(target):
                    stdinit.std_signal_gobal.std_echo_msg(0, "请重启软件再次打开该界面若还存在该问题，请至插件安装界面卸载并重新安装Platformio！")
                else:
                    stdinit.std_signal_gobal.std_echo_msg(0, "当前插件安装存在文件缺失，请至插件安装界面卸载并重新安装Platformio！")
                return 0
            #self.pio_libs.append(self.pio_lib)
            stdinit.std_signal_gobal.std_echo_msg(1, "Page:" + str(self.pio_lib['page']) + " | Total:" + str(self.pio_lib['total']))
            ii = len(self.pio_lib['items'])
            i = 0
            while i < ii:
                self.lib_list.append(self.pio_lib['items'][i]['name'] + "\ndescription:" +
                                     self.pio_lib['items'][i]['description'] + "\n")  #
                i = i + 1
            self.model_1.setStringList(self.lib_list)
            self.listview_1.setModel(self.model_1)
            self.find_more.setEnabled(True)
            stdinit.std_signal_gobal.std_process(0, reso.search)
            stdinit.std_signal_gobal.std_echo_msg(1,reso.search_sucess)
        except:
            self.find_more.setEnabled(True)
            stdinit.std_signal_gobal.std_process(0, reso.search)
            stdinit.std_signal_gobal.std_echo_msg(1, reso.download_failed)
            stdinit.std_signal_gobal.stdprintln()
            pass
    def find_mores(self):
        try:

            t1 = threading.Thread(target=self.find_more_lib, name='th1', args=())
            t1.setDaemon(True)
            t1.start()
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

    def search_load(self):
        try:
            if self.check_net()==False:
                return False
            self.lib_list.clear()
            self.pio_lib = self.lib.lib_search_k(self.nameLineEdit.text(),self.search_more_p)
            if self.pio_lib==None:

                target = stdinit.stdenv + "/.stduino/packages/pioenv/pioboards.json"  # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"
                if os.path.exists(target):
                    stdinit.std_signal_gobal.std_echo_msg(0, "请重启软件再次打开该界面若还存在该问题，请至插件安装界面卸载并重新安装Platformio！")
                else:
                    stdinit.std_signal_gobal.std_echo_msg(0, "当前插件安装存在文件缺失，请至插件安装界面卸载并重新安装Platformio！")
                return 0

            stdinit.std_signal_gobal.std_echo_msg(1, "Page:" + str(self.pio_lib['page']) + " | Total:" + str(self.pio_lib['total']))


            self.lib_p=self.lib_p+1
            self.search_more_p=self.search_more_p+1
            #self.pio_libs.append(self.pio_lib)
            try:

                ii = len(self.pio_lib['items'])
                if ii>0:
                    pass
                else:
                    return 0
                i = 0
                while i < ii:
                    try:  # libs['items'][0]['name']
                        lib_show = self.pio_lib['items'][i]['name'] + "\nby " + \
                                   self.pio_lib['items'][i]['authornames'][0] + "    |    Downloads:" + str(
                            self.pio_lib['items'][i]['dllifetime']) + "\nSupported frameworks: "
                        i_lib = len(self.pio_lib['items'][i]['frameworks'])
                        i_li = 0
                        while i_li < i_lib:
                            if i_li > 0:
                                lib_show = lib_show + "," + \
                                           self.pio_lib['items'][i]['frameworks'][i_li]["title"]
                            else:
                                lib_show = lib_show + self.pio_lib['items'][i]['frameworks'][i_li]["title"]
                            i_li = i_li + 1
                        self.lib_list.append(lib_show + "\n")
                    except:
                        stdinit.std_signal_gobal.stdprintln()
                        break
                    i = i + 1
                self.model_1.setStringList(self.lib_list)
                self.listview_1.setModel(self.model_1)

            except:
                stdinit.std_signal_gobal.stdprintln()
        except:
            stdinit.std_signal_gobal.stdprintln()
    def search_lib(self):#-k
        try:
            if self.check_net()==False:
                return False
            if self.search_more_p == 1:
                stdinit.std_signal_gobal.std_process(1, reso.search)
                self.search_load()
                stdinit.std_signal_gobal.std_process(0, reso.search)
                stdinit.std_signal_gobal.std_echo_msg(1, reso.search_sucess)
                self.search_lib_button.setText(reso.lib_find_more)

            else:
                stdinit.std_signal_gobal.std_process(1, reso.search)
                self.search_load()
                stdinit.std_signal_gobal.std_process(0, reso.search)
                stdinit.std_signal_gobal.std_echo_msg(1, reso.search_sucess)
            self.search_lib_button.setEnabled(True)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def find_lib(self):#最早实现方式看码云上的备份
        try:
            if self.check_net()==False:
                return False
            self.search_lib_button.setEnabled(False)
            t1 = threading.Thread(target=self.search_lib, name='th1', args=())
            t1.setDaemon(True)
            t1.start()
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