# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

# from six.moves import urllib  # 下载文件

#import zipfile  # 解压文件
# import shutil  # 用于压缩
# import subprocess
import os,stat

# import re
# import socket
#
# import zipfile


from PyQt5.QtWidgets import QMessageBox,QWidget,QPushButton,QVBoxLayout,QGridLayout,QTextEdit,QHBoxLayout,QGroupBox,QAbstractItemView,QListView

from PyQt5.QtCore import QStringListModel

# from function.conf import res
from function.cores.stdmsg import reso

from function.cores.stdedit import stdinit
import threading
from function.piobuilder.piopltinstall import PioPlatformInstall
from shutil import copytree,rmtree
# fo = open("./appearance/stduino_json/library.json", mode='r', encoding='UTF-8')
# st = fo.read()
# fo.close()
# libraries = json.loads(st)



class StdOpenExamples(QWidget):  # 安装库文件


    def __init__(self):
        try:
            super(StdOpenExamples, self).__init__()

            self.plat = PioPlatformInstall()
            self.add_lib_s_load_f = 0
            self.find_more_p = 1
            self.pio_libs = []
            self.pio_libs.append(0)
            self.lib_list = []
            self.example_list=[]
            self.platform_sec=None
            self.example_sec = None
            self.example_name=None
            self.examp_path=None

            self.initUi()
        except:
            stdinit.std_signal_gobal.stdprintln()


    def initUi(self):
        try:
            self.bigEditor = QTextEdit()
            self.bigEditor.setReadOnly(True)

            #self.createGridGroupBox()
            #self.createGridGroupBox2()
            self.creatVboxGroupBox()
            self.creatVboxGroupBox2()
            mainLayout = QVBoxLayout()
            hboxLayout = QHBoxLayout()
            hboxLayout.addWidget(self.vboxGroupBox2)
            hboxLayout.addWidget(self.vboxGroupBox)

            #the_window.add_lib_s_load.connect(self.libr_load)

            self.install = QPushButton("请选择具体示例文件", self)
            self.install_return = QPushButton("退出当前界面", self)

            # self.find_more.setDisabled(True)
            self.install.setDisabled(True)
            self.install.clicked.connect(self.install_url)
            self.install_return.clicked.connect(self.install_ret)
            #self.install.setFixedWidth(120)
            #self.pro1 = QProgressBar(self)
            # self.pro1.setOrientation(Qt.Horizontal)
            # self.pro1.setMinimum(0)
            # self.pro1.setMaximum(0)
            #self.pro1.setVisible(False)

            glayout = QGridLayout()
            glayout.addWidget(self.install, 0, 0)

            glayout.addWidget(self.install_return, 0, 2)
            # 准备四个控件
            gwg = QWidget()
            # 使用四个控件设置局部布局
            gwg.setLayout(glayout)
            # 将四个控件添加到全局布局中


            #mainLayout.addWidget(self.gridGroupBox)
            mainLayout.addLayout(hboxLayout)
            #mainLayout.addWidget(self.gridGroupBox2)
            #mainLayout.addWidget(self.pro1)
            mainLayout.addWidget(gwg)
            #mainLayout.addWidget(self.install_return)
            self.setLayout(mainLayout)
        except:
            stdinit.std_signal_gobal.stdprintln()
    def libr_load(self):
        try:

            t1 = threading.Thread(target=self.library_load, name='li_load1')
            t1.setDaemon(True)
            t1.start()

        except:
            stdinit.std_signal_gobal.stdprintln()




    # def createGridGroupBox2(self):
    #     try:
    #         self.gridGroupBox2 = QGroupBox(reso.lib_version)
    #         self.layout = QGridLayout()
    #         # nameLabel = QLabel("发布版本时间")
    #         # self.vsion = QCheckBox(reso.select_version, self)
    #         # self.vsion.setChecked(True)
    #         # self.vsion.setEnabled(False)
    #         # self.vsion.stateChanged.connect(self.check_vsion)
    #         # self.combobox_1 = QComboBox(self)
    #         # self.combobox_1.setDisabled(True)
    #         self.layout.setSpacing(10)
    #         #self.layout.addWidget(self.vsion, 1, 0)
    #         #self.combobox_1.addItem("")
    #         #self.layout.addWidget(self.combobox_1, 1, 1)
    #         self.layout.setColumnStretch(1, 10)
    #         self.gridGroupBox2.setLayout(self.layout)
    #     except:
    #         stdinit.std_signal_gobal.stdprintln()


    def creatVboxGroupBox(self):
        try:
            self.vboxGroupBox = QGroupBox("对应平台示例项目")
            layout = QVBoxLayout()
            self.model_2 = QStringListModel(self)
            self.listview_2 = QListView(self)  # python3
            self.example_list = ["请先单击已安装平台"]
            self.model_2.setStringList(self.example_list)
            self.listview_2.setModel(self.model_2)

            self.listview_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
            # self.listview_1.setFixedWidth(600)
            # self.listview_1.setFixedHeight(400)
            self.listview_2.clicked.connect(self.example_clicked)

            #self.bigEditor.setPlainText("请先单击选择已安装平台")
            layout.addWidget(self.listview_2)
            self.vboxGroupBox.setLayout(layout)

        except:
            stdinit.std_signal_gobal.stdprintln()


    def creatVboxGroupBox2(self):

        try:
            self.vboxGroupBox2 = QGroupBox("已安装平台")
            layout = QVBoxLayout()

            self.model_1 = QStringListModel(self)
            self.listview_1 = QListView(self)  # python3
            self.lib_list=["正在加载文件夹"]
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

            # print(libraries)
            example_path=stdinit.stdenv+"/.platformio/platforms"
            if os.path.exists(example_path):
                self.lib_list = os.listdir(example_path)
                self.install_return.setText("Finding Platforms File...")
                if len(self.lib_list) > 0:
                    self.model_1.setStringList(self.lib_list)
                    self.listview_1.setModel(self.model_1)
                    self.install_return.setText(reso.library_installer)
                else:
                    self.lib_list = ["暂未安装任何平台"]
                    self.model_1.setStringList(self.lib_list)
                    self.listview_1.setModel(self.model_1)
                    self.install_return.setText(reso.library_installer)
            else:
                self.lib_list = ["暂未安装任何平台"]
                self.model_1.setStringList(self.lib_list)
                self.listview_1.setModel(self.model_1)
                self.install_return.setText(reso.library_installer)

        except:
            stdinit.std_signal_gobal.stdprintln()

    def install_ret(self):
        try:

            stdinit.std_signal_gobal.std_main_ui_change(4)
            # the_window.m_stackedLayout.setCurrentIndex(0)
            # the_window.liAct2.setEnabled(True)

        except:
            stdinit.std_signal_gobal.stdprintln()
    def example_clicked(self,qModelIndex):
        try:

            n_lin=qModelIndex.row()
            self.example_sec = self.example_list[n_lin]#self.pio_plts[n_lin]['description']

            if self.platform_sec==None:
                return 0
            self.examp_path=stdinit.stdenv+"/.platformio/platforms/"+self.platform_sec+"/examples/"+self.example_sec
            if os.path.exists(self.examp_path):
                self.install.setDisabled(False)
                self.install.setText("打开该示例")
            else:
                self.install.setDisabled(True)
                self.install.setText("该示例不存在")

                #self.install_return.setText(reso.library_installer)
            # for i in
            # self.combobox_1.clear()
            #self.pio_libs[self.find_more_p]['items'][i]['name']
            # stdinit.plat_choose_name=self.pio_plts[n_lin]['name']
            # self.combobox_1.addItem(self.pio_plts[n_lin]['versions'][0])

            # if self.find_more.isEnabled() == False:
            #     self.find_more.setDisabled(False)


        except:
            stdinit.std_signal_gobal.stdprintln()
    def clicked(self, qModelIndex):

        try:
            self.install.setDisabled(True)
            self.install.setText("请选择具体示例")
            n_lin=qModelIndex.row()
            self.platform_sec = self.lib_list[n_lin]#self.pio_plts[n_lin]['description']
            examp_path=stdinit.stdenv+"/.platformio/platforms/"+self.platform_sec+"/examples"
            if os.path.exists(examp_path):
                self.example_list.clear()
                self.example_list=os.listdir(examp_path)
                self.model_2.setStringList(self.example_list)
                self.listview_2.setModel(self.model_2)
            else:
                self.example_list.clear()
                self.example_list.append("暂无示例")
                self.model_2.setStringList(self.example_list)
                self.listview_2.setModel(self.model_2)
                #self.install_return.setText(reso.library_installer)
            # for i in
            # self.combobox_1.clear()
            #self.pio_libs[self.find_more_p]['items'][i]['name']
            # stdinit.plat_choose_name=self.pio_plts[n_lin]['name']
            # self.combobox_1.addItem(self.pio_plts[n_lin]['versions'][0])

            # if self.find_more.isEnabled() == False:
            #     self.find_more.setDisabled(False)


        except:
            stdinit.std_signal_gobal.stdprintln()

    def remove_readonly(self, func, path, _):
        try:
            # "Clear the readonly bit and reattempt the removal"
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def delete_file(self, path):
        try:
            if os.path.isdir(path):
                try:
                    rmtree(path, onerror=self.remove_readonly)
                except:
                    stdinit.std_signal_gobal.stdprintln()
                    # self.listwidget.append("Delete error:" + "\n 请手动至该文件夹处删除\nPlease manually delete to this folder")
                    # self.add_lib_si(python3, 0, "Unexpected error:" + "\n 请手动至该文件夹处删除\nPlease manually delete to this folder")
                    # QMessageBox.warning(self, "Delete error",
                    #                     "Unexpected error:" + "\n 请手动至该文件夹处删除\nPlease manually delete to this folder",
                    #                     QMessageBox.Yes)
                    pass
            else:
                try:
                    os.remove(path)
                except:
                    try:
                        # shutil.rmtree(path, onerror=self.remove_readonly)
                        os.chmod(path, stat.S_IWRITE)
                        os.remove(path)
                    except:
                        stdinit.std_signal_gobal.stdprintln()
                pass
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()
    def thread_return(self,strin):
        self.install.setText(strin)
        self.install.setEnabled(True)
        self.listview_1.setEnabled(True)
    def open_example(self):
        try:
            if os.path.exists(self.example_name):
                self.delete_file(self.example_name)
                #os.makedirs(self.example_name)
                copytree(self.examp_path, self.example_name)
                stdinit.std_signal_gobal.std_main_ui_change(4)
                stdinit.std_signal_gobal.std_echo_msg(0,"示例文件已拷贝至项目文件夹下，请手动进行切换当前工作空间！")
            else:
                #os.makedirs(self.example_name)
                copytree(self.examp_path, self.example_name)
                stdinit.std_signal_gobal.std_main_ui_change(4)
                stdinit.std_signal_gobal.std_echo_msg(0, "示例文件已拷贝至项目文件夹下，请手动进行切换当前工作空间！")

        except:
            stdinit.std_signal_gobal.stdprintln()



    def install_url(self):

        # from multiprocessing import Process
        # p = Process(target=self.install_url1, args=(1,))
        # print(1)
        try:

            self.install.setEnabled(False)
            # self.listview_1.setEnabled(False)
            example_nam=self.platform_sec + "-" + self.example_sec

            self.example_name=stdinit.projects_dir+self.platform_sec+"-"+self.example_sec
            if os.path.exists(self.example_name):
                ok = QMessageBox.information(self,
                                             "提示",
                                             "该示例文件:"+example_nam+"已打开是否重新打开?" ,
                                             QMessageBox.Yes, QMessageBox.No)
                if ok == QMessageBox.No:
                    return 0

            t1 = threading.Thread(target=self.open_example, name='open_example')
            t1.setDaemon(True)
            t1.start()  # File_tree_init
            # self.my_thread = stdthread()  # 步骤2. 主线程连接子线,同时传递一个值给子线程
            # self.my_thread.std_signal.connect(self.thread_return)
            # stdinit.callch = 1
            # self.my_thread.start()  # 步骤3 子线程开始执行run函数

        except:
            stdinit.std_signal_gobal.stdprintln()
        #t1 = threading.Thread(target=pay_ticket, name='th1')



    def schedule(self,blocknum, blocksize, totalsize):
        try:
            # """
            # blocknum:当前已经下载的块
            # blocksize:每次传输的块大小
            # totalsize:网页文件总大小
            # """
            per = 100 * blocknum * blocksize / totalsize

            if per > 100:
                per = 100
                self.install_return.setText("Installing Library...")

            #self.add_lib_s.emit(2, int(per), "")  # 2进度条数值
        except:
            stdinit.std_signal_gobal.stdprintln()







