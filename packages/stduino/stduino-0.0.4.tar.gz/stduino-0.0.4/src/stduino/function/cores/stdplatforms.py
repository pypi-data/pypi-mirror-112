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

import time

from PyQt5.QtWidgets import QMessageBox,QComboBox,QWidget,QPushButton,QVBoxLayout,QGridLayout,QTextEdit,QHBoxLayout,QGroupBox,QCheckBox,QAbstractItemView,QListView

from PyQt5.QtCore import QStringListModel,pyqtSignal, QThread

# from function.conf import res
from function.cores.stdmsg import reso
from function.cores.stdedit import stdinit
import threading
from function.piobuilder.piopltinstall import PioPlatformInstall
from urllib import request

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
            if stdinit.callch == 1:
                self.install_pio()

            elif stdinit.callch == 2:

                self.install_p()
        except:
            stdinit.std_signal_gobal.stdprintln()
        #a = (1, 2)
        #self.mysignal.emit(a)  # 发射自定义信号

    def install_pio(self):
        try:
            if stdinit.Piopalt_install.isinstalled_plat(stdinit.plat_choose_name):
                stdinit.std_signal_gobal.std_process(1, reso.package_uninstall)

                if stdinit.Piopalt_install.platform_uninstall(stdinit.plat_choose_name):
                    self.std_signal.emit(reso.install_lib)

                    stdinit.std_signal_gobal.std_process(0, reso.package_uninstall)

                else:
                    self.install.setEnabled(True)
                    self.std_signal.emit(reso.install_lib)
                    stdinit.std_signal_gobal.std_process(0, reso.package_uninstall)



            else:
                stdinit.std_signal_gobal.std_process(1, reso.downloading)
                if stdinit.Piopalt_install.platform_install(stdinit.plat_choose_name):
                    self.std_signal.emit(reso.package_uninstall)
                    stdinit.std_signal_gobal.std_process(0, reso.downloading)

                else:

                    self.std_signal.emit(reso.package_uninstall)
                    stdinit.std_signal_gobal.std_process(0, reso.downloading)

            pass
        except:
            stdinit.std_signal_gobal.stdprintln()

    def install_p(self):
        try:
            for i in range(0, 5):
                print(2)
                time.sleep(1)
        except:
            stdinit.std_signal_gobal.stdprintln()

class StdAddPlatforms(QWidget):  # 安装库文件



    def __init__(self):
        try:
            super(StdAddPlatforms, self).__init__()

            self.plat = PioPlatformInstall()
            self.add_lib_s_load_f = 0
            self.find_more_p = 1
            self.pio_libs = []
            self.pio_libs.append(0)
            self.lib_list = []

            self.initUi()
        except:
            stdinit.std_signal_gobal.stdprintln()

    def check_net(self):
        try:
            request.urlopen(url="https://www.baidu.com", timeout=3.0)
            # print(ret)
        except:
            stdinit.std_signal_gobal.std_echo_msg(1,reso.no_net)
            return False
        return True
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

            self.install = QPushButton(reso.install_lib, self)

            self.find_more = QPushButton(reso.lib_find_more, self)
            self.find_more.setEnabled(False)

            self.install_return = QPushButton(reso.library_installer, self)

            # self.find_more.setDisabled(True)


            self.install.setDisabled(True)

            self.find_more.clicked.connect(self.find_mores)

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
            if self.check_net()==False:
                return False
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
            self.vboxGroupBox2 = QGroupBox(reso.platform_list)
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
            if self.check_net()==False:
                return False
            # print(libraries)
            self.install_return.setText("Finding Platforms File...")
            # self.pio_lib=self.lib.lib_search(self.find_more_p)
            self.pio_plts=self.plat.platform_search()
            if self.pio_plts == None:

                target = stdinit.stdenv + "/.stduino/packages/pioenv/pioboards.json"  # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"
                if os.path.exists(target):
                    stdinit.std_signal_gobal.std_echo_msg(0, "请重启软件再次打开该界面若还存在该问题，请至插件安装界面卸载并重新安装Platformio！")
                else:
                    stdinit.std_signal_gobal.std_echo_msg(0, "当前插件安装存在文件缺失，请至插件安装界面卸载并重新安装Platformio！")
                return 0
            # print(self.pio_plts)
            #self.pio_libs.append(self.pio_lib)
            try:

                ii = len(self.pio_plts)
                i = 0

                while i < ii:
                    try:#libs['items'][0]['name']
                        lib_show=self.pio_plts[i]['title']+"\nby "+self.pio_plts[i]['ownername']+"    |    License:"+str(self.pio_plts[i]['license'])+"\nSupported frameworks:"
                        i_lib = len(self.pio_plts[i]['frameworks'])
                        i_li = 0
                        while i_li < i_lib:
                            if i_li>0:
                                lib_show = lib_show + ","+ self.pio_plts[i]['frameworks'][i_li]
                            else:
                                lib_show = lib_show + self.pio_plts[i]['frameworks'][i_li]

                            i_li=i_li+1
                        self.lib_list.append(lib_show+"\n")



                        #self.lib_list.append(self.pio_libs[self.find_more_p]['items'][i]['name']+"\nby "+self.pio_libs[self.find_more_p]['items'][i]['authornames'][0]+"    |   Downloads:"+str(self.pio_libs[self.find_more_p]['items'][i]['dllifetime'])+"\n")#

                    except:

                        stdinit.std_signal_gobal.stdprintln()
                        break
                    i = i + 1
                self.model_1.setStringList(self.lib_list)

                self.listview_1.setModel(self.model_1)
                self.install_return.setText(reso.library_installer)
            except:

                stdinit.std_signal_gobal.stdprintln()
                pass
        except:
            stdinit.std_signal_gobal.stdprintln()



    def install_ret(self):
        try:

            stdinit.std_signal_gobal.std_main_ui_change(2)
            # the_window.m_stackedLayout.setCurrentIndex(0)
            # the_window.liAct2.setEnabled(True)

        except:
            stdinit.std_signal_gobal.stdprintln()
    def clicked(self, qModelIndex):

        try:
            if self.check_net()==False:
                return False
            n_lin=qModelIndex.row()
            descrabe = self.pio_plts[n_lin]['description']
            # for i in
            self.combobox_1.clear()
            #self.pio_libs[self.find_more_p]['items'][i]['name']
            stdinit.plat_choose_name=self.pio_plts[n_lin]['name']
            self.combobox_1.addItem(self.pio_plts[n_lin]['versions'][0])
            if stdinit.Piopalt_install.isinstalled_plat(stdinit.plat_choose_name):
                self.install.setDisabled(False)
                self.install.setText(reso.package_uninstall)
                pass
            else:
                self.install.setDisabled(False)
                self.install.setText(reso.install_lib)
                pass
            # if self.find_more.isEnabled() == False:
            #     self.find_more.setDisabled(False)

            self.bigEditor.setText(descrabe)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def remove_readonly(self,func, path, _):
        "Clear the readonly bit and reattempt the removal"
        os.chmod(path, stat.S_IWRITE)
        func(path)
    def thread_return(self,strin):
        self.install.setText(strin)
        self.install.setEnabled(True)
        self.listview_1.setEnabled(True)
    def install_url(self):

        # from multiprocessing import Process
        # p = Process(target=self.install_url1, args=(1,))
        # print(1)
        try:

            self.install.setEnabled(False)
            self.listview_1.setEnabled(False)

            if stdinit.Piopalt_install.isinstalled_plat(stdinit.plat_choose_name):
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
            # blocknum:当前已经下载的块
            # blocksize:每次传输的块大小
            # totalsize:网页文件总大小
            # """
            per = 100 * blocknum * blocksize / totalsize

            if per > 100:
                per = 100
                self.install_return.setText("Installing Library...")


        except:
            stdinit.std_signal_gobal.stdprintln()

    def find_mores(self):
        try:
            if self.check_net()==False:
                return False
            self.install_return.setText("Finding More File...")
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


    # def find_lib(self):
    #     try:
    #
    #         lib_len = len(libraries["libraries"])
    #         self.lib_list = []
    #         self.lib_list_num = []
    #         first_n=""
    #         self.st_ar = 0
    #         try:
    #             ii = len(self.lib)
    #             i = 0
    #             while i < ii:
    #                 try:
    #                     if re.search(self.nameLineEdit.text(), self.lib[i]['lib_name'],flags=re.IGNORECASE) == None:  # search(self.nameLineEdit.text(), libraries["libraries"][i]["name"]) == None:
    #                         pass
    #                     else:
    #                         self.lib_list.append(str(self.lib[i]['lib_name']))
    #
    #                         self.lib_list_num.append(str(i))
    #
    #
    #                     # if self.lib[i]['id']:
    #                     # lib_list.append(str(self.lib[i]['lib_name']))
    #
    #
    #                     # print(c[i]['id'])
    #                 except:
    #                     break
    #                 i = i + 1
    #             self.st_ar = i
    #
    #         except:
    #             pass
    #
    #         for i in range(lib_len):
    #             try:
    #                 if re.search(self.nameLineEdit.text(),libraries["libraries"][i]["name"], flags=re.IGNORECASE)== None:#search(self.nameLineEdit.text(), libraries["libraries"][i]["name"]) == None:
    #                     pass
    #                 else:
    #                     if first_n!=libraries["libraries"][i]["name"]:
    #                         self.lib_list.append(str(libraries["libraries"][i]["name"]))
    #                         self.lib_list_num.append(str(i+self.st_ar))
    #                         first_n=libraries["libraries"][i]["name"]
    #                 # if self.lib[i]['id']:
    #                 # print(c[i]['id'])
    #             except:
    #                 print("Unexpected error:", sys.exc_info()[1])  # 错误内容
    #
    #                 break
    #         # ii = len(self.lib)
    #         # i = 0
    #         # lib_list = []
    #         # while i < ii:
    #         #     try:
    #         #         if re.search(self.nameLineEdit.text(), self.lib[i]['lib_name']) == None:
    #         #             pass
    #         #         else:
    #         #             lib_list.append(str(self.lib[i]['lib_name']))
    #         #     except:
    #         #         break
    #         #     i = i + 1
    #         self.model_1.setStringList(self.lib_list)
    #         self.listview_1.setModel(self.model_1)
    #     except:
    #         QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdlibs00035！\n You can search it in stduino.com",QMessageBox.Yes)
    #


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




