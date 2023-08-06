# !/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2015-present Stduino <service001@stduino.com>
#
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file.  Please review the
# following information to ensure the GNU General Public License version 3.0
# requirements will be met: http://www.gnu.org/copyleft/gpl.html.
#
# If you do not wish to use this file under the terms of the GPL version 3.0
# then you may purchase a commercial license.  For more information contact
# service001@stduino.com.
#
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
# 开发本软件消耗了太多时间精力，一路走来，太不容易，写下此行留为纪念，尤其感谢几位学弟（林鉴波、梁莅、房杰、刘席鸣等一直以来的各方面支持）。——2019.10.22晚


__author__ = 'Su Jin Qiang'

import os
import sys
import re
from function.cores.stdedit import stdinit

pos = sys.prefix.replace("\\", "/")
if re.search("main", pos) == None:
    pos = os.path.abspath('.')
    pass
os.chdir(pos)
pos = os.path.abspath('.').replace("\\","/")
from PyQt5.QtWidgets import QApplication,QFileDialog,QMessageBox,QMainWindow,QLabel,QSizePolicy,QVBoxLayout,QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from function.cores.stdmsg import reso
import qdarkstyle

from function.cores.stdserial import StdSerial
from function.cores.stdpersonal import StdBackColor
from function.cores.stdedit.stdmainui import StdMainWindow
from function.cores.stdedit.stdfind import StdFind
from function.cores.stdboards import StdFindBoards
from function.cores.stdedit.stdfile import StdPathHandler
from function.cores.stdmakeboards import StdMakeBoard
from function.cores.stdmake import Stdmake
from function.piobuilder.pioinstall import PioInstall
from function.piobuilder.piopltinstall import PioPlatformInstall
from function.cores.stdauto.ctags_parser import Ctags_parser
import threading
from shutil import copy2
#import time
# import webview
#
# def worker(que1):
#     while True:
#         ress=que1.get()
#
#         if ress=="help":
#             webview.create_window('Stduino使用教程','http://www.stduino.com/forum.php?mod=viewthread&tid=105',text_select=True,on_top=True)
#             webview.start()
#
#
#         elif ress=="quan":
#             webview.create_window('额外省','http://taobao.stduino.com', text_select=True,on_top=True)
#             webview.start()
#         time.sleep(0.1)


version_c = "1.10.4内测版"#'1.01'



################################################
#######创建主窗口
################################################
class FirstMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(reso.startup_failed)

        ###### 创建界面 ######
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.Layout = QVBoxLayout(self.centralwidget)

        # 设置顶部三个按钮
        # self.topwidget = QWidget()
        # self.Layout.addWidget(self.topwidget)
        # self.buttonLayout = QHBoxLayout(self.topwidget)
        #
        # self.pushButton1 = QPushButton()
        # self.pushButton1.setText("创建新项目文件")
        # self.buttonLayout.addWidget(self.pushButton1)
        #
        # self.pushButton2 = QPushButton()
        # self.pushButton2.setText("打开已有项目文件")
        # self.buttonLayout.addWidget(self.pushButton2)
        #
        # self.pushButton3 = QPushButton()
        # self.pushButton3.setText("配置软件")
        # self.buttonLayout.addWidget(self.pushButton3)

        # 设置中间文本
        self.label = QLabel()
        self.label.setText(reso.search_tip)
        self.label.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Roman times", 10, QFont.Bold))
        self.Layout.addWidget(self.label)

        # 设置状态栏
        self.statusBar().showMessage(reso.web_site + 'www.stduino.com')
        self.setGeometry(500, 300, 600, 300)

    def on_pushButton1_clicked(self):

        # myGUI = CustomMainWindow()
        try:
            pos = os.path.abspath('.')
            path = pos + '.\\appearance\projects'
            fileName, ok2 = QFileDialog.getSaveFileName(self,
                                                        reso.file_save,
                                                        path,
                                                        "Target File(*.ino)")

            # print(fileName)
            fo = open(fileName, "wb")
            fo.close()
            st = ''
            the_window = StdMainWindow()
            the_window.fileName = fileName

            # the_window =SecondWindow()
            self.windowList.append(the_window)  ##注：没有这句，是不打开另一个主界面的！
            # the_window.EditorShow(st)
            the_window.setWindowTitle("Stduino IDE " + version_c + " [" + fileName + ']')  # 文件名设置
            self.close()
            the_window.show()
        # except OSError as err:
        #    print("OS error: {0}".format(err))
        # except ValueError:
        #   print("Could not convert data to an integer.")
        except:
            stdinit.std_signal_gobal.stdprintln()
            # print("Unexpected error:", sys.exc_info()[1]) #错误内容

    # 按钮二：打开现有项目文件
    def on_pushButton2_clicked(self):

        try:
            pos = os.path.abspath('.')
            path = pos + '.\\appearance\projects'
            fileName, filetype = QFileDialog.getOpenFileName(self,
                                                             reso.select_file,
                                                             path,
                                                             "Target File(*.ino)")  # 设置文件扩展名过滤,注意用双分号间隔
            fo = open(fileName, mode='r', encoding='UTF-8')
            st = fo.read()
            fo.close()

            # print(fileName)
            # self.label.setText(st
            the_window = StdMainWindow()
            the_window.fileName = fileName
            the_window.setWindowTitle("Stduino IDE " + version_c + " [" + fileName + ']')  # 文件名设置

            # the_window =SecondWindow()
            self.windowList.append(the_window)  ##注：没有这句，是不打开另一个主界面的！
            the_window.EditorShow(st)
            self.close()
            the_window.show()
            # except OSError as err:
            #    print("OS error: {0}".format(err))
            # except ValueError:
            #   print("Could not convert data to an integer.")
        except:
            stdinit.std_signal_gobal.stdprintln()
            #print("Unexpected error:", sys.exc_info()[1])  # 错误内容

        # the_dialog = TestdemoDialog()
        # if the_dialog.exec_() == QDialog.Accepted:
        # pass

    # 按钮三：打开提示框
    def on_pushButton3_clicked(self):
        QMessageBox.information(self, reso.tip, reso.function_development)
        # QMessageBox.question(self, "提示", "这是question框！")
        # QMessageBox.warning(self, "提示", "这是warning框！")
        # QMessageBox.about(self, "提示", "这是about框！")

def is_fast_file_in():
    try:
        if stdinit.platform_is=="Win":
            ideini = stdinit.stdenv + "/.stduino/packages/pioenv/Lib/site-packages/platformio"
            if os.path.exists(ideini):
                pass
            else:
                return 0
            ideini = stdinit.stdenv + "/.stduino/packages/pioenv/Lib/site-packages/platformio/ide/ideini.py"
            if os.path.exists(ideini):
                pass
            else:
                regi_p = stdinit.stdenv + "/.stduino/packages/pioenv/Lib/site-packages/platformio"
                regi = stdinit.stdenv + "/.stduino/packages/pioenv/Lib/site-packages/platformio/package/manager/_registry.py"
                if os.path.exists(regi_p):
                    os.remove(regi)
                    copy2(stdinit.abs_path + "/tool/packages/python3/Scripts/stdini.py",
                          stdinit.stdenv + "/.stduino/packages/pioenv/Lib/site-packages/platformio/ide/ideini.py")
                    copy2(stdinit.abs_path + "/tool/packages/python3/Scripts/stdload.py", regi)
        elif stdinit.platform_is == "Linux":
            pass
            #ctags_path = stdinit.abs_path + "/tool/packages/ctagslin32/"
        elif stdinit.platform_is == "Darwin":
            pass
        else:
            print("Cannot indentify platform: " + stdinit.platform_is)

    except:
        stdinit.std_signal_gobal.stdprintln()


            #创建快捷方式
    # pos = os.path.abspath('.')
    #
    # if res.creatshortcut == "1":
    #
    #     try:
    #         desk_path = stdinit.stdenv + "\Desktop"
    #         isExists = os.path.exists(desk_path)
    #         pos_path = pos[:-5]
    #         pos_name = pos_path + "\Stduino.exe"
    #
    #         if isExists:
    #             os.chdir(desk_path)  # 通过更改当前运行目录
    #             shell = client.Dispatch("WScript.Shell")
    #             shortcut = shell.CreateShortCut("Stduino.lnk")
    #             shortcut.WorkingDirectory = os.path.abspath(pos_path)  # 设置快捷方式的起始位置, 不然会出现找不到辅助文件的情况
    #             shortcut.TargetPath = os.path.abspath(pos_name)
    #             # shortcut.WorkingDirectory = "C:\stwork\stdemo2019827\dist\Stduino1.0"  # 设置快捷方式的起始位置, 不然会出现找不到辅助文件的情况
    #             # shortcut.TargetPath = "C:\stwork\stdemo2019827\dist\Stduino1.0\Stduino.exe"
    #             shortcut.save()
    #             os.chdir(pos)  # 通过更改当前运行目录
    #             # QMessageBox.warning(self, "快捷方式创建", "在桌面创建快捷方式\n Create shortcut on Desktop", QMessageBox.Yes)
    #         else:
    #             shell = client.Dispatch("WScript.Shell")
    #             shortcut = shell.CreateShortCut("Stduino.lnk")
    #             shortcut.WorkingDirectory = os.path.abspath(pos_path)  # 设置快捷方式的起始位置, 不然会出现找不到辅助文件的情况
    #             shortcut.TargetPath = os.path.abspath(pos_name)
    #             # shortcut.WorkingDirectory = "C:\stwork\stdemo2019827\dist\Stduino1.0"  # 设置快捷方式的起始位置, 不然会出现找不到辅助文件的情况
    #             # shortcut.TargetPath = "C:\stwork\stdemo2019827\dist\Stduino1.0\Stduino.exe"
    #             shortcut.save()
    #             QMessageBox.warning(self, "快捷方式创建",
    #                                 "已在" + pos_path + "创建快捷方式,请自行拷贝至桌面\n has Created shortcut on " + pos_path,
    #                                 QMessageBox.Yes)
    #
    #     except:
    #         QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdmainui0049！\n You can search it in stduino.com",
    #                             QMessageBox.Yes)




def view_init():
    pass

# from PyQt5.QtCore import QUrl
# import time
# from PyQt5.QtWidgets import *
# from PyQt5.QtWebEngineWidgets import QWebEngineView
#
# class Stduser():
#   def __init__(self):
#     super(Stduser, self).__init__()
#     self.browser=QWebEngineView()
#     #加载外部的web界面
#     self.browser.load(QUrl('http://api.stduino.com/users'))
#     time.sleep(10)
#
#     del self.browser
#     del self

if __name__ == '__main__':  # main函数
    app = QApplication(sys.argv)
    try:

        t1 = threading.Thread(target=is_fast_file_in, name='is_fast_file_in')
        t1.setDaemon(True)
        t1.start()#
        #p = Process(target=worker, args=(stdinit.Std_help,))
        #p.daemon = True
        #p.start()
        #stdinit.Std_help.put("help")

        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())#qdarkgraystyle
        #app.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())

        # t1 = threading.Thread(target=view_init, name='is_fast_file_in')
        # t1.setDaemon(True)
        # t1.start()  # view_init

        stdinit.goto_init = Ctags_parser()
        stdinit.Pio_install = PioInstall()
        stdinit.Piopalt_install = PioPlatformInstall()
        stdinit.File_tree_view = StdPathHandler()
        stdinit.find_boards = StdFindBoards()
        stdinit.Std_Serial_Tool1 = StdSerial(0)
        stdinit.Std_Serial_Tool2 = StdSerial(1)
        stdinit.Set_Back_Color1 = StdBackColor()
        stdinit.Std_Find = StdFind()
        stdinit.Std_makeboards = StdMakeBoard()
        stdinit.Std_Make = Stdmake()
        std_main = StdMainWindow()
        std_main.show()
        std_main.readSession()
        stdinit.std_signal_gobal.all_stdenvir_init()

    except:
        stdinit.std_signal_gobal.stdprintln()
        std_main = FirstMainWindow()
        std_main.show()
        sys.exit(app.exec_())

    sys.exit(app.exec_())


    #setCompleter 自动补全实现方案 两个 一个textedit 加上setCompleter  二通过listview +查找工能

''''''