# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
__author__ = 'Su Jin Qiang'
from function.stddebug.stddebugview import Std_termainal
from function.stddebug.stdebug import StDebug
from function.cores.stdedit.stdtabedit import StdTabEdit
import shutil
import requests
from function.cores.stdlibs import StdAddLibs
from function.cores.stdplatforms import StdAddPlatforms
from function.cores.stdexamples import StdOpenExamples
from function.cores.stdpackages import StdAddPackages
#import zipfile  # 解压文件
# import subprocess
import sys,os
import re
import webview

#import base64
#import getpass
# 进度条
import time

from PyQt5.QtCore import QFileInfo,Qt,QSize,QUrl
from PyQt5.QtGui import QColor,QTextCursor,QIcon,QFont,QTextOption
from PyQt5.Qsci import QsciLexerCPP
import webbrowser

from function.conf import res, setup
from function.cores.stdmsg import reso
from PyQt5.QtWidgets import QApplication,QInputDialog,QToolBar,QComboBox,QToolButton,QFileDialog,QMessageBox,QMainWindow,QTextEdit,QTabWidget,QLabel,QProgressBar,QSizePolicy,QFrame,QVBoxLayout,QSplitter,QStackedLayout,QWidget,QAction,QMenu
import serial  # pyserial
import serial.tools.list_ports
# from uics1 import Ui_Form

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from xml.etree import ElementTree as ET
from xml.dom import minidom
import xml.dom.minidom
#from PyQt5.QtWebEngineWidgets import QWebEngineView  # QtWebEng
# 文件监控
from function.cores.stdedit import stdinit
import threading

# from function import process
# dsd = process.ProgressBar_start() #启动第一时间无法保证显示


#import tempfile
# 开发本软件消耗了太多时间精力，一路走来，太不容易，写下此行留为纪念，尤其感谢几位学弟（林鉴波、梁莅、房杰、刘席鸣等一直以来的各方面支持）。——2019.10.22晚

my_sender = 'sam9661@qq.com'  # 发件人邮箱账号sam9661@qq.com  stduino@foxmail.com
my_pass = 'jrtuhtpsukpocjii'  # 发件人邮箱密码   squxhquxrlalbaae
my_user = 'service001@stduino.com'  # 收件人邮箱账号，我这边发送给自己
myCodeSample = ""

#pos = os.path.abspath('.')
#path = pos + "\\tool\msy"

#os.chdir("C:\stwork\stdemo2019827\dist\Stduinodebug\main")  # 通过更改当前运行目录F:\BaiduNetdiskDownload\stpython\stdemo\main




# class Std_Console(QObject):
#     textWritten = pyqtSignal(str)  # 定义一个发送str的信号
#
#     def write(self, text):
#         self.textWritten.emit(str(text))
class StdMainWindow(QMainWindow):
    # staus_change = pyqtSignal(str, str)

    # my_signal = pyqtSignal(int, str, str) #self.my_signal.connect(parent.my_signal.emit)

    fileName = ''
    NextId = 1

    def __init__(self):
        super(StdMainWindow, self).__init__()


        try:  # 统计用户
            self.debug_dict = {"last_ob": None, "last_ob_line": None}
            self.project_staus = 0  # 控制文件树开合
            # pos = os.path.abspath('.')
            # sys.stdout = Std_Console(textWritten=self.list_echo2)
            # sys.stderr = Std_Console(textWritten=self.list_echo2)


            stdinit.std_signal_gobal.make_signal.connect(self.std_make_enable)
            stdinit.std_signal_gobal.find_change.connect(self.Tofind)
            stdinit.std_signal_gobal.text_change.connect(self.text_Change)
            stdinit.std_signal_gobal.back_color.connect(self.setcolor_all)
            stdinit.std_signal_gobal.process_p.connect(self.std_process)#std_process
            stdinit.std_signal_gobal.main_ui_change.connect(self.libui_c)
            stdinit.std_signal_gobal.echo_msg.connect(self.list_echo)
            stdinit.std_signal_gobal.find_staus_change.connect(self.find_button_enable)
            stdinit.std_signal_gobal.jump_to_look.connect(self.Jump_To_Look_W)
            stdinit.std_signal_gobal.debug_goto.connect(self.Debug_goto_S)
            stdinit.std_signal_gobal.upload_list_change.connect(self.upload_method_ch)
            stdinit.std_signal_gobal.file_modify.connect(self.file_modify_check)
            stdinit.std_signal_gobal.upload_rts_dtr.connect(self.dtrrst)

            self.tabWidget_change_from=None#use for save
            self.tabWidget_no=1

            t1 = threading.Thread(target=self.load_user_url, name='li_user_url')
            t1.setDaemon(True)
            t1.start() #File_tree_init
            # print(time.time()-t)
            self.setAcceptDrops(True)

        except:
            stdinit.std_signal_gobal.stdprintln()



        try:  # 统计用户
            self.listwidget = QTextEdit()

            self.listwidget.setWordWrapMode(QTextOption.NoWrap)

            self.listwidget.setReadOnly(True)
            self.tabWidget = QTabWidget()

            # self.tabWidget.tabBar().setStyleSheet("QTabBar::tab{color:rgb(255,0,255);background-color:rbg(0,255,255,0);}")#

            # self.tabWidget.tabBar().setStyleSheet("QTabBar::tab:selected{color:rgb(255,255,0);background:rgb(30,30,30)}")
            # 倒角效果 min-width:175px; border: 2px solid;border-top-left-radius: 10px;border-top-right-radius: 10px;padding:5px;
            self.tabWidget.setStyleSheet("* {background:rgb(37,37,38);}")  # border: 0px solid;
            tab_str_css = "QTabBar::close-button {image: url(appearance/img/img_close2.png)}" + \
                          "QTabBar::close-button:selected {image: url(appearance/img/img_close3.png)}" + \
                          "QTabBar::tab {background-color:rgb(45,45,45);padding:3px;border: 2px;}" \
                          "QTabBar::tab:!selected {margin-top: 5px;color:rgb(150,150,150);}" \
                          "QTabBar::tab:selected {color:rgb(255,255,255);background-color:rgb(30,30,30);}" + \
                          "QTabBar::tab:hover{background:rgb(10, 10, 10);}"
            #"QTabBar::tab:hover{background:rgb(10, 10, 10, 50);}"  win

            # self.setStyleSheet("* {color:rgb(181,181,162);background-color:rgb(255,37,38)}")  #主题框架背景

            font = QFont('Consolas', 10)
            font.setBold(True)  # 设置字体加粗
            self.tabWidget.setFont(font)  # 设置字体加粗
            # table.horizontalHeader().setFont(font)  # 设置表头字体

            self.tabWidget.setStyleSheet(tab_str_css)  # TAB背景
            #self.listwidget.setStyleSheet("background:rgb(56,56,56)")  ####调试框颜色
            # self.listwidget.setTextBackgroundColor(QColor(0, 0,0))
            #self.listwidget.setTextColor(QColor(0,255,0))  # QColor(105, 105, 105)
            self.listwidget.setStyleSheet(
                "font-family: Noto Sans Mono; font-size: 12pt; background-color: #383838; color: #00FF00; padding: 2; border: none;")
            self.listwidget.setText("若在使用过程中遇到问题，欢迎随时至www.stduino.com进行发帖交流！")

            # auto
            # cur_text_color = m_textline->textColor();
            # // 设置当前行要使用的颜色，假设为红色
            # m_textline->setTextColor(Qt::red);
            # // 写入一行内容
            # QString
            # str = u8
            # "This a test line";
            # m_textline.append(str);
            # // 最后恢复原来的颜色
            # m_textline->setTextColor(cur_text_color);

            # palette = QPalette()
            #         # palette.setColor(QPalette.Background, Qt.black)
            #         # self.tabWidget.setPalette(palette)
            # str = "QTabBar::tab{background-color:rbg(255,255,255,0);}"
            # self.tabWidget.setStyleSheet(str)

            # str = "QTabBar::tab{background-color:rbg(255,255,255);}" + \
            #       "QTabBar::tab:selected{color:red;background-color:rbg(255,0,255);} "
            # self.tabWidget.setStyleSheet(str)

            # self.tabWidget.setStyleSheet("* { color: #000;background:rgb(37,37,38) ;border: 1px solid black}")

            # self.tabWidget.setTabShape(QTabWidget.Triangular)  # rectangle Triangular
            self.tabWidget.setDocumentMode(False)  # 为True 时有白色横线
            self.tabWidget.setMovable(True)
            self.tabWidget.setTabsClosable(True)
            self.tabWidget.tabCloseRequested.connect(self.close_Tab)
            self.tabWidget.currentChanged.connect(self.tabChange)
            # self.tabWidget.currentWidget().setStyle("* { color: #FFF0F5;background:black ;border: 1px solid black}")

            # self.tabWidget.
            self.setCentralWidget(self.tabWidget)

            # staus bar
            self.statusbar = self.statusBar()
            self.statusbar.showMessage('Ready')
            # setStatusTip
            self.status1 = QLabel("")

            self.status2 = QLabel("")
            # self.gbk_status3=QPushButton("Feedback")  #可在状态栏上加按钮
            # feedback=QToolButton()#无设置文字
            # feedback.setToolTip("Feedback")
            # #sd=QCommandLinkButton("feedback") #无背景
            #
            # #sd =QDialogButtonBox("ds")  # 无背景
            # feedback.setIcon(QIcon(QPixmap(res.img_feedback)))
            # feedback.clicked.connect(self.st_feedback)
            # self.gbk_status3.clicked.connect(self.st_feedback)

            # self.gbk_status3.setIcon(QIcon(QPixmap(res.img_feedback)))
            # self.gbk_status3.setFixedWidth(80)
            self.gbk_status = QLabel("UTF-8")
            # self.pb11 = QProgressBar()
            # self.pb11.setOrientation(Qt.Horizontal)
            # self.pb11.setStyle()
            # self.pb11.setMinimum(0)
            # self.pb11.setMaximum(0)
            # self.pb11.setFixedSize(108,18)
            # self.pb1_1 = QLabel('正在编译：')
            # self.pb1_1.setText('cdcdcd')
            # self.pb11.setVisible(False)
            # self.pb1_1.setVisible(False)
            self.pb12 = QProgressBar()
            # self.pb12.setOrientation(Qt.Horizontal)
            # self.pb12.setFixedSize(108, 18)
            self.pb12.setMaximumWidth(200)
            self.pb12.setMaximumHeight(6)
            # self.pb12.setInvertedAppearance(False)
            #
            self.pb12.setMinimum(0)
            self.pb12.setMaximum(0)
            self.pb1_2 = QLabel(reso.lib_download)
            # self.pb12.setFormat("%v")
            self.pb12.setVisible(False)
            self.pb1_2.setVisible(False)

            # self.pb12.setValue(self.step)
            # self.status1.setText('ccdd')
            # self.status2 = QLabel("")
            # self.status2.setText(self.combo.currentText() + ' 在 ' + self.wcombo.currentText())
            self.gbk_status.setAlignment(Qt.AlignRight)
            self.status1.setAlignment(Qt.AlignCenter)
            self.status2.setAlignment(Qt.AlignRight)

            self.status1.setMinimumWidth(100)
            self.status2.setMinimumWidth(200)

            self.gbk_status.setMinimumWidth(50)
            # self.wcombo2 = QComboBox(self)
            # self.wcombo2.addItem(reso.serial_port)

            self.statusbar.addPermanentWidget(self.pb1_2)
            self.statusbar.addPermanentWidget(self.pb12)
            self.statusbar.addPermanentWidget(self.gbk_status)

            self.statusbar.addPermanentWidget(self.status1)

            self.statusbar.addPermanentWidget(self.status2)
            # self.statusbar.addPermanentWidget(feedback)
            # Window setup
            # --------------

            # 1. Define the geometry of the main window
            self.setGeometry(300, 100, 1100, 750)
            self.showMaximized()
            # self.setMinimumSize(1050,300)
            self.setWindowTitle("Stduino IDE " + stdinit.version_c)
            self.setWindowIcon(QIcon(res.img))
            #####创建tabwidget   标签
            # 2. Create frame and layout
            # self.__frm.setStyleSheet("QWidget { background-color: #FFFFFF }")
            # 创建一个TextEdit部件
            # self.la=QLabel()

            # stduino_msg = (
            # '学的不仅是技术,更是梦想!', 'Stduino 一直在等你！', '要么做第一个，要么做最好的一个。', '什么是鸡肋课？就是每个人都在自己课表的这门课旁边标注一个“可旷”或者“选修”。',
            # '所谓好的病毒就是要：“持续时间特别长，波及范围特别广，破坏力特别大。”', '当你不是黑客的时候，总说：“我是个黑客”。当你真正成为黑客的时候，你往往会说：“我不是黑客”',
            # '程序员是值得尊敬的，程序员的双手是魔术师的双手，他们把枯燥无味的代码变成了丰富多彩的软件……', '指针，是C语言最复杂的东西，也是C语言的灵魂',
            # '正如美女都不在大街上逛一样，高手根本不在群里混。美女去哪里了？多半在私家车里，高手去哪里了？多半在写程序。',
            # '所以说做程序员，要做就得做高手，做什么都不重要关键的是做成牛人。成了牛人就不一样了，掌握公司的核心技术，老板感随便让你走人吗？你一周随便去一个公司或者创业，对他都是极大的压力。',
            # '一个人静静的坐在电脑前写代码的感觉，那是什么感觉？那就是武林高手闭关修炼的感觉。',
            # '天空一声巨响，老子闪亮登场。',
            # '资本家啊，精于成本计算。难道就没想到雇佣十个劳动生产率为0的人，就算雇佣车成本是10。也顶不上一个劳动生产率为1，雇佣成本为10的人，因为前面的那10的成本可是完全打了水漂啊。',
            # '所以从某种意义上说，电影好不好看，并不是电影本身好不好看，而是跟谁看。',
            # '一本好书，就像高级武功秘籍一样，哪怕只从里面领悟个一招半式，功力提升起来都是惊人的，眉超风学的那半生不熟的九阴真经就是证明。',
            # '你要是交了很多钱，你就是上帝，就是VIP。叫你VIP实际上是叫你VERY IMPORTANT PIG ！为啥？因为你老给人家送钱，所以你就是VIP。',
            # '为了追求“幸福”，不得不放弃自己的梦想，回到现实中来，回到自己一直鄙视的庸俗中来。', '力的作用是相互的，你打别人有多疼，自己的手就有多疼。与其大家都疼，还不如最开始就不要下手打。',
            # '写程序并不是一辈子都只是写代码。IT这一行是相当广博的，不管你是男的还是女的，不管你技术是初级、中级还是高级，你都能在这行中找到你自己合适的位置。如果你真的用心了，它带给你的会是一生的回报。',
            # '“现在，最重要的是，我们要好好研究一下如何才能把技术变成钱，否则，我们就永远只是IT界挖沙的民工。”',
            # '“疯狂的程序员”绝对不是靠狂妄和拼命的程序员，而是能够脚踏实地、持续努力的程序员。一个程序员真正做到了这两点，技术上去之后，唯一能够限制他的只有想像力，到那个时候，才算“疯狂的程序员”，这种程序员啊，才能令竞争对手无比恐 惧。',
            # '技术其实还是我们最需要的东西，以前我们没有过硬的技术，所以疯狂地追求它。现在呢？有了一点技术，便觉得技术不那么重要。如果这样放任下去，等到我们失去技术的那一天，一定会后悔莫及的！',
            # '永不放弃！永不放弃又有两个原则，第一个原则是：永不放弃！第二个原则是当你想放弃时回头看第一个原则：永不放弃！')
            # # msg_id=random.randint(0, 22) #以上文字来源于疯狂的程序员
            # self.listwidget.setPlainText(stduino_msg[msg_id])
            # self.listwidget.append('')
            # self.listwidget.append('                                                                                         ——摘自疯狂的程序员')
            # 去掉鸡汤#
            # Serial初始化

            #self.Com_Dict = {}  # wcombo
            # self.__frm = QFrame(self)  # 框架
            # # self.__frm.setStyleSheet("QWidget { background-color: #FFFFFF }")
            # self.__lyt = QVBoxLayout()
            # self.__frm.setLayout(self.__lyt)

            # layout = QHBoxLayout()

            # layout.addWidget(button2)

            # self.__lyt.addWidget(self.__btn)

            # 创建一个Tree部件
            # self.treewidget = QTreeWidget()
            # self.treewidget.setHeaderLabels(['This', 'is', 'a', 'TreeWidgets!'])
            self.listwidget.moveCursor(QTextCursor.End)
            try:
                stdinit.File_tree_view.my_signal.connect(self.new_me)

            except:
                stdinit.std_signal_gobal.stdprintln()
                QMessageBox.warning(self, "BUG Warning",
                                    "Waring|Error:stdmainui0050！\n You can search it in stduino.com",
                                    QMessageBox.Yes)
                pass

            ############

                # print("Unexpected error:", sys.exc_info()[1])  # 错误内容

            # 设置第一个Splitter的布局方向


            self.splitter1 = QSplitter(Qt.Horizontal)
            # self.my_signal.connect(self.new_me)

            # self.staus_change.connect(self.status2_show)

            # 为第一个Splitter添加控件，并设置两个控件所占空间大小
            # from function import findboards

            # self.find_boards=Findboards_all()
            # self.find_boards = Findboards()


            # time_start = time.time()
            # # t1 = threading.Thread(target=self.readcs, name='readS1')
            # #
            # # t1.start()
            # time_end = time.time()
            # print('totally cost', time_end - time_start)


            self.debug_a = StDebug()
            self.debug_a.debug_sig.connect(self.debug_sign)
            self.debug_a.debug_return.connect(self.debug_return)
            self.terminald = Std_termainal()
            #self.terminald.termin.connect(self.ter_cmd)

            # 主窗口
            self.addlib_json = StdAddLibs()
            self.addPackage = StdAddPackages()
            self.addPlatform = StdAddPlatforms()
            self.openExample =StdOpenExamples()


            self.m_stackedLayout = QStackedLayout()
            m_gwg = QWidget()
            # 使用四个控件设置局部布局
            m_gwg.setLayout(self.m_stackedLayout)
            # self.m_stackedLayout.addWidget(self.find_boards)
            self.m_stackedLayout.addWidget(self.tabWidget)
            self.m_stackedLayout.addWidget(self.addlib_json)
            self.m_stackedLayout.addWidget(self.addPackage)
            self.m_stackedLayout.addWidget(self.addPlatform)
            self.m_stackedLayout.addWidget(self.openExample)

            self.m_stackedLayout.setCurrentIndex(0)
            # 主窗口

            # 左侧工具窗口
            self.stackedLayout = QStackedLayout()

            gwg = QWidget()
            # 使用四个控件设置局部布局
            gwg.setLayout(self.stackedLayout)
            #self.stackedLayout.addWidget(self.find_boards)
            self.stackedLayout.addWidget(stdinit.File_tree_view)
            self.stackedLayout.addWidget(self.debug_a)
            self.stackedLayout.setCurrentIndex(0)
            # 左侧工具窗口

            # 调试窗口
            self.stackedLayout2 = QStackedLayout()
            gwg_2 = QWidget()
            # 使用四个控件设置局部布局
            gwg_2.setLayout(self.stackedLayout2)
            self.stackedLayout2.addWidget(self.terminald)
            self.stackedLayout2.addWidget(self.listwidget)
            self.stackedLayout2.setCurrentIndex(1)
            # self.splitter1.addWidget(self.file_tree_view)

            self.splitter1.addWidget(gwg)# 调试
            # ds=Setbackcolor()
            self.splitter1.addWidget(m_gwg)  ##主窗口
            # self.splitter1.setSizes([2, 500])
            # self.splitter1.addWidget(self.tabWidget)
            self.splitter1.setSizes([1, 1400])  # 板子发现

            #####################
            # 创建一个QSplitter，用来分割窗口
            splitter = QSplitter(self)
            # mainSplitter->setHandleWidth(20);
            splitter.setHandleWidth(20)
            # splitter.setHandleWidth(20)
            # splitter.windowHandle.

            # splitter.addWidget(self.splitter1)

            splitter.addWidget(self.splitter1)
            splitter.addWidget(gwg_2)
            # self.listw = QTextEdit()
            # self.create_tab(self.__frm2)
            splitter.setOrientation(Qt.Vertical)
            splitter.setStretchFactor(0, 8)
            # splitter.setStretchFactor(1, 2)
            self.setCentralWidget(splitter)

            # self.setCentralWidget(self.__frm)
            self.__myFont = QFont()
            self.__myFont.setPointSize(14)  # 14

            # 菜单栏按钮
            projectfileAction = QAction(QIcon(), reso.projectfile, self)
            projectfileAction.setShortcut('')
            projectfileAction.setStatusTip('Projectfile')
            projectfileAction.triggered.connect(self.close)

            ExitAction = QAction(QIcon(res.img_exit), reso.exit, self)
            ExitAction.setShortcut('Ctrl+Q')
            ExitAction.setStatusTip(reso.exit)
            ExitAction.triggered.connect(self.close)

            # openrecent = QAction(QIcon(), res.openrecent, self)
            # openrecent.setShortcut('Ctrl+O')
            # openrecent.setStatusTip('OpenRecent File')
            # # openrecent.addAction(self.close)
            # openrecent.triggered.connect(self.close)

            self.savefileAction = QAction(QIcon(res.img_save), reso.save, self)
            self.savefileAction.setShortcut('Ctrl+S')
            self.savefileAction.setStatusTip('Save File')
            self.savefileAction.triggered.connect(lambda: self.fileSave())
            self.savefileas = QAction(QIcon(res.img_save), "Save As", self)
            self.savefileas.setStatusTip('Save File As')
            self.savefileas.triggered.connect(self.fileSaveAs)



            openfileAction = QAction(QIcon(res.img_open), reso.open, self)
            openfileAction.setShortcut('Ctrl+O')
            openfileAction.setStatusTip('OpenFile')
            openfileAction.triggered.connect(self.fileOpen)

            openautofile = QAction(QIcon(res.img_open), "自定义自动完成词库", self)
            openautofile.setStatusTip('自定义自动完成词库')
            openautofile.triggered.connect(self.autofileOpen)

            newfileAction = QAction(QIcon(res.img_addfile), reso.new, self)
            newfileAction.setShortcut('Ctrl+N')
            newfileAction.setStatusTip('New file')
            newfileAction.triggered.connect(stdinit.File_tree_view.NewFileMenuShow)  # 当传送值为1时，可进行选择block 进行编程
            prAct1 = QAction(QIcon(res.img_fold), reso.open_folder, self)
            prAct1.triggered.connect(self.openProject)
            edit_styleAction = QAction(QIcon(res.img_setup), reso.editstyle, self)
            # edit_styleAction.setShortcut('Alt+P')
            edit_styleAction.setStatusTip(reso.editstyle)
            edit_styleAction.triggered.connect(self.startsetcolor)
            self.uploadAction = QAction(QIcon(res.img_upload), reso.upload, self)
            self.upload_fast_Action = QAction(QIcon(res.img_uploadfast), reso.uploadfast, self)
            # self.uploadAction.setShortcut('Ctrl+U')
            self.uploadAction.setStatusTip('Compile and Download')
            self.upload_fast_Action.setStatusTip('Download')
            self.upload_fast_Action.triggered.connect(self.uploadfast)
            self.upload_fast_Action.setShortcut('Ctrl+Alt+F')

            self.uploadAction.triggered.connect(self.upload)
            self.uploadAction.setShortcut('Ctrl+Alt+D')

            self.complexAction = QAction(QIcon(res.img_complex), reso.complex, self)
            # self.complexAction.setShortcut('Ctrl+M')
            self.complexAction.setStatusTip('Compile')
            # complexAction.addAction(self.__btn_action)
            self.complexAction.triggered.connect(self.make)
            self.complexAction.setShortcut('Ctrl+R')

            self.cleanAction = QAction(QIcon(res.img_clean), reso.clean, self)
            self.cleanAction.setShortcut('Alt+C')
            self.cleanAction.setStatusTip('Clean Complex File')
            self.cleanAction.triggered.connect(self.make_clean)

            searchAction = QAction(QIcon(res.img_search), reso.search, self)
            #searchAction.setShortcut('Alt+F')
            # openfileAction.setShortcut('Ctrl+O')
            searchAction.setStatusTip('Complex File')
            # complexAction.addAction(self.__btn_action)
            searchAction.triggered.connect(self.Find)

            self.backAction = QAction(QIcon(res.img_back), reso.back, self)
            self.backAction.setShortcut('Ctrl+B')
            self.backAction.setStatusTip('Complex File')
            # complexAction.addAction(self.__btn_action)
            self.backAction.triggered.connect(self.undo1)

            self.forwardAction = QAction(QIcon(res.img_forward), reso.forward, self)
            self.forwardAction.setShortcut('')
            self.forwardAction.setStatusTip('Complex File')
            # complexAction.addAction(self.__btn_action)
            self.forwardAction.triggered.connect(self.redo1)

            self.serialAction = QAction(QIcon(res.img_serial), reso.serial, self)
            # self.serialAction.setShortcut('Ctrl+E')
            self.serialAction.setStatusTip(reso.serial)
            self.serialAction.triggered.connect(self.startSerial)

            # projects
            self.project_Action = QAction(QIcon(res.img_projects2), reso.project_list, self)  # ,
            #self.project_Action.setStatusTip("Projects")
            self.project_Action.triggered.connect(self.start_project)
            self.project_example = QAction(QIcon("./appearance/img/img_examples.svg"), reso.example_list, self)  # ,
            #self.project_example.setStatusTip("Projects")
            self.project_example.triggered.connect(self.start_examples)
            self.find_b_Action = QAction(QIcon("./appearance/img/boards.png"), reso.board_list, self)  # ,
            #self.find_b_Action.setStatusTip("Boards")
            self.find_b_Action.triggered.connect(self.start_find_b)
            self.debug_Action = QAction(QIcon("./appearance/img/debug.png"), reso.debug_button, self)  # ,
            #self.debug_Action.setStatusTip("Debug")
            self.debug_Action.triggered.connect(self.start_debug)
            # feedback = QAction(QIcon(res.img_feedback),
            # feedback.triggered.connect(self.st_feedback)
            # feedback=QCommandLinkButton("feedback") #无背景
            #
            # #sd =QDialogButtonBox("ds")  # 无背景
            # feedback.setIcon(QIcon(QPixmap(res.img_feedback)))
            # feedback.clicked.connect(self.st_feedback)

            # serialpAction = QAction(QIcon(res.img_serialp), reso.serialp, self)  #绘图相关
            # # serialpAction.setShortcut('Ctrl+W')
            # serialpAction.setStatusTip(reso.serialp)
            # serialpAction.triggered.connect(self.startSerial)

            # libraryAction = QAction(QIcon(res.img_serialp), reso.serialp, self)
            # # libraryAction.setShortcut('Ctrl+L')
            # libraryAction.setStatusTip(reso.serialp)
            # libraryAction.triggered.connect(self.libraryNew)
            langh_menu = QMenu(reso.language, self)

            self.language1 = QAction('中文', self, checkable=True)
            self.language1.triggered.connect(lambda: self.changemsg('1'))
            self.language2 = QAction('English', self, checkable=True)
            self.language2.triggered.connect(lambda: self.changemsg('2'))
            self.language3 = QAction('русский язык', self, checkable=True)
            self.language3.triggered.connect(lambda: self.changemsg('python3'))
            self.language4 = QAction('Deutsch', self, checkable=True)
            self.language4.triggered.connect(lambda: self.changemsg('4'))
            self.language5 = QAction('わご', self, checkable=True)
            self.language5.triggered.connect(lambda: self.changemsg('5'))
            self.language6 = QAction('한어', self, checkable=True)
            self.language6.triggered.connect(lambda: self.changemsg('6'))
            self.language7 = QAction('español', self, checkable=True)
            self.language7.triggered.connect(lambda: self.changemsg('7'))
            self.language8 = QAction('français', self, checkable=True)
            self.language8.triggered.connect(lambda: self.changemsg('8'))
            self.language9 = QAction('العربية', self, checkable=True)
            self.language9.triggered.connect(lambda: self.changemsg('9'))

            langh_menu.addAction(self.language1)
            langh_menu.addAction(self.language2)
            langh_menu.addAction(self.language3)
            langh_menu.addAction(self.language4)
            langh_menu.addAction(self.language5)
            langh_menu.addAction(self.language6)
            langh_menu.addAction(self.language7)
            langh_menu.addAction(self.language8)
            langh_menu.addAction(self.language9)
            self.changemsg2(res.msg)



            # ADD a menubar菜单栏
            menubar = self.menuBar()
            menubar.setNativeMenuBar(False)
            # ADD a filemenu
            fileMenu = menubar.addMenu(reso.file)
            fileMenu.addAction(newfileAction)
            fileMenu.addAction(openfileAction)  # lib_file_menu
            fileMenu.addAction(openautofile)  # lib_file_menu


            fileMenu.addAction(self.savefileAction)
            fileMenu.addAction(self.savefileas)
            fileMenu.addAction(prAct1)
            fileMenu.addAction(edit_styleAction)
            # fileMenu.addAction(openfileAction)
            fileMenu.addAction(ExitAction)
            # Import Library


            # 编辑
            fileMenu = menubar.addMenu(reso.editor)
            fileMenu.addMenu(langh_menu)
            # fileMenu.addAction(comment)
            fileMenu.addAction(searchAction)
            # fileMenu.addAction(complexAction)
            # 项目
            fileMenu = menubar.addMenu(reso.project)
            fileMenu.addAction(self.complexAction)
            fileMenu.addAction(self.uploadAction)
            fileMenu.addAction(self.upload_fast_Action)
            fileMenu.addAction(self.cleanAction)
            # 工具
            driver = QAction(QIcon(res.img_complex), reso.install_driver, self)
            # comment.setShortcut('Ctrl+G')
            driver.setStatusTip('Languege change')
            # complexAction.addAction(self.__btn_action)
            driver.triggered.connect(self.open_driver)
            # Complex type
            # set_gbk_utf_8 = QMenu("编码格式", self)
            # self.set_gbk = QAction("GBK", self, checkable=True)
            # self.set_utf_8 = QAction("UTF-8", self, checkable=True)
            # set_gbk_utf_8.addAction(self.set_gbk)
            # set_gbk_utf_8.addAction(self.set_utf_8)
            # self.set_gbk.triggered.connect(lambda: self.set_gbk_utf("GBK"))
            # self.set_utf_8.triggered.connect(lambda: self.set_gbk_utf("UTF-8"))
            # self.gbk_status.setText(res.gbk_type)
            # global gbk_utf_type
            #
            # gbk_utf_type = res.gbk_type
            # try:
            #     if res.gbk_type == "GBK":
            #         self.set_gbk.setChecked(True)
            #         self.set_utf_8.setChecked(False)
            #     else:
            #         self.set_gbk.setChecked(False)
            #         self.set_utf_8.setChecked(True)
            # except:
            #     QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdmainui0052！\n You can search it in stduino.com",
            #                         QMessageBox.Yes)
            #     pass

            # downtype = QMenu(reso.choose_down_type, self)
            # download_type = int(res.download_type)
            # self.usblink = QAction(reso.usb_link, self, checkable=True)
            # self.usblink.setStatusTip(reso.usb_link)
            # self.usblink.triggered.connect(lambda: self.toggleMenu3(0))
            # self.stlink = QAction(reso.st_link, self, checkable=True)
            # self.stlink.setStatusTip(reso.st_link)
            # self.stlink.triggered.connect(lambda: self.toggleMenu3(1))
            # if download_type == 0:
            #     self.usblink.setChecked(True)
            #     self.stlink.setChecked(False)
            #
            #
            # else:
            #     self.usblink.setChecked(False)
            #     self.stlink.setChecked(True)

            # downtype.addAction(self.usblink)
            # downtype.addAction(self.stlink)
            fileMenu = menubar.addMenu(reso.tool)
            fileMenu.addAction(self.serialAction)
            fileMenu.addAction(driver)
            # fileMenu.addMenu(downtype)
            #fileMenu.addMenu(set_gbk_utf_8)
            # fileMenu.addAction(serialpAction)                 #待开发
            # 帮助
            # setIcon(QIcon(QPixmap("./按钮/sound.png").scaled(ui->pushButton_music->rect().size())));
            std_help = QAction(QIcon(res.img_help), reso.help, self)

            # comment.setShortcut('Ctrl+G')
            std_help.setStatusTip('How to use?')
            # complexAction.addAction(self.__btn_action)
            std_help.triggered.connect(self.st_help)
            # 反馈
            std_feedback = QAction(QIcon(res.img_feedback), reso.feedback, self)
            # comment.setShortcut('Ctrl+G')
            std_feedback.setStatusTip('FeedBack!')
            # complexAction.addAction(self.__btn_action)
            std_feedback.triggered.connect(self.st_feedback)
            std_taobao = QAction(QIcon(res.img_heart), "优惠券", self)
            # comment.setShortcut('Ctrl+G')
            std_taobao.setStatusTip('领张优惠券支持下作者')
            # complexAction.addAction(self.__btn_action)
            std_taobao.triggered.connect(self.goto_taobao)
            fileMenu = menubar.addMenu(reso.help)
            fileMenu.addAction(std_help)
            # self.statusbar.addPermanentWidget(std_feedback)
            fileMenu.addAction(std_feedback)

            # 社区
            # viewStatAct = QAction('View statusbar', self, checkable=True)
            # viewStatAct.setStatusTip('技术社区')
            # viewStatAct.setChecked(True)
            # viewStatAct.triggered.connect(self.toggleMenu)

            viewMenu = menubar.addMenu(reso.tcommunity)
            viewStatAct = QAction(QIcon(res.img_web), reso.community_web, self)
            viewStatAct.setStatusTip(reso.tcommunity)
            viewStatAct.triggered.connect(self.openstduino)
            viewStatAc = QAction(QIcon(res.img_about), reso.about, self)
            viewStatAc.setStatusTip(reso.about)
            viewStatAc.triggered.connect(self.guanyu)

            viewMenu.addAction(viewStatAct)
            viewMenu.addAction(viewStatAc)
            # viewMenu.addAction(viewStatA)
            # viewMenu.addAction(viewStat)
            # viewMenu.addAction(viewSta)
            # 扩展

            fileMenu = menubar.addMenu(reso.li_development)
            # impMenu = QMenu('Import', self)
            # impAct = QAction('Import mail', self)
            # impMenu.addAction(impAct)
            # impMenu.addAction(viewStatAc)
            # impMenu.addAction(viewStatAc)
            # impMenu.addAction(viewStatA)
            # impMenu.addAction(viewStat)
            # impMenu.addAction(viewSta)

            Lib_new_add = QAction(QIcon(res.img_library_add), reso.create_lib, self)
            Lib_new_add.triggered.connect(self.libraryNew)
            self.Load_lib = QAction(QIcon(res.img_library), reso.search_lib, self)
            self.Load_lib.triggered.connect(self.AddLibs)
            self.platform = QAction(QIcon(res.img_platform), reso.platform_list, self)
            self.platform.triggered.connect(self.Platforms)
            self.package = QAction(QIcon(res.img_package), reso.package_list, self)
            self.package.triggered.connect(self.Packages)



            # self.package=QToolButton(self)
            # #btn_first = QToolButton(self)
            # self.package.setIcon(QApplication.style().standardIcon(QStyle.SP_MediaSkipBackward))
            # self.package.setText("到头")


            # sharel = QMenu('分享自建库', self)
            # sharel1 = QAction('新增分享库', self)
            # sharel1.triggered.connect(self.searchLibrary)
            # sharel2 = QAction('更新已分享', self)
            # sharel2.triggered.connect(self.searchLibrary)
            # sharel.addAction(sharel1)
            # sharel.addAction(sharel2)

            Open_lib = QAction(QIcon(res.img_library_fold), reso.open_lib, self)

            Open_lib.triggered.connect(self.openLibrary)

            fileMenu.addAction(Lib_new_add)
            fileMenu.addAction(self.Load_lib)
            fileMenu.addAction(self.platform)
            fileMenu.addAction(self.package)
            # fileMenu.addMenu(sharel)
            fileMenu.addAction(Open_lib)
            # fileMenu.addMenu(impMenu)

            # ADD a toolbar
            self.toolbar = self.addToolBar('daiding')
            self.toolbar.setIconSize(QSize(20, 20))
            self.toolbar.addAction(self.complexAction)
            self.toolbar.addAction(self.uploadAction)
            self.toolbar.addAction(self.upload_fast_Action)
            self.toolbar.addAction(self.cleanAction)
            self.toolbar.addAction(newfileAction)
            self.toolbar.addAction(openfileAction)
            self.toolbar.addAction(self.savefileAction)

            self.toolbar.addAction(searchAction)
            self.toolbar.addAction(self.backAction)
            self.toolbar.addAction(self.forwardAction)  #


            self.right_to_left = QWidget()
            self.right_to_left.setStyleSheet("* { background:rgb(52,65,75) ;border-bottom : 0px solid #19232D;}")  # color: #32414B;
            self.right_to_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) #dark 52,65,75  darkgray 50,50,50
            self.toolbar.addWidget(self.right_to_left)
            self.up_to_down = QWidget()
            self.up_to_down.setStyleSheet("* { background:rgb(52,65,75);}")  # color: #32414B; 52,65,75   69 83 100
            self.up_to_down.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            try:
                # toolbar.addSeparator() #竖直分割线
                # AS=QToolButton()
                # liAct56.addItem(self.combo11, 'cs')
                # toolbar.addAction(liAct56)
                # toolbar.addAction(self.stlink)
                # toolbar.addAction(self.stlink)

                # status3 = QLabel("Line: 1  Col: 1")
                # status3.setAlignment(Qt.AlignRight)
                # toolbar.addWidget(status3)
                self.toolBar = QToolBar()  ########
                self.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                #m_pToolBar->setToolButtonStyle(Qt::ToolButtonTextUnderIcon);
                # MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
                self.toolBar.addAction(self.project_Action)  # startproject_Action#########
                self.toolBar.addAction(self.project_Action)  # startproject_Action#########
                self.toolBar.addAction(self.project_example)  # startproject_Action#########

                self.toolBar.addAction(self.find_b_Action)  # startproject_Action#########
                self.toolBar.addAction(self.debug_Action)  # startproject_Action#########
                self.toolBar.addAction(self.Load_lib)  # startproject_Action#########
                self.toolBar.addAction(self.platform)  # startproject_Action#########
                #teddd=QLabel("平台")
                #self.toolBar.addAction(teddd)
                #self.toolBar.addWidget(teddd)
                self.toolBar.addAction(self.package)  # startproject_Action#########
                self.toolBar.addWidget(self.up_to_down)
                self.toolBar.addAction(std_taobao)
                self.toolBar.addAction(std_help)
                self.toolBar.addAction(std_feedback)  # startproject_Action#########
                # self.addToolBar(Qt.RightToolBarArea, self.toolBar)
                # self.toolBar.addAction(serialpAction)
                # self.toolBar.addAction(libraryAction)
                self.addToolBar(Qt.LeftToolBarArea, self.toolBar)  ############
                # self.combo = QComboBox(self)
                # self.lbl = QLabel(reso.choose_board, self)
                # self.lbl.setStyleSheet("background-color:#32414b;border-bottom : 1px solid #19232D;")  # 需设置跟随主题背景

                # self.toolbar.addWidget(self.lbl)  ################
                # self.toolbar.addWidget(self.combo)  ############

                # 板型加载
                # fo = open("./appearance/stduino_json/boards.json", mode='r', encoding='UTF-8')
                # st = fo.read()
                # fo.close()
                # self.boards = json.loads(st)
                # ii = len(self.boards['boards'])
                # # print(ii)
                # i = 0
                # while i < ii:
                #     try:
                #         # if self.lib[i]['id']:
                #         # print(lib['boards'][i]['name'])
                #         self.combo.addItem(self.boards['boards'][i]['name'])  # l m l l m h m h h
                #         # lib_list.append(str(self.lib[i]['lib_name']))
                #         # print(c[i]['id'])
                #     except:
                #         QMessageBox.warning(self, "BUG Warning",
                #                             "Waring|Error:0053！\n You can search it in stduino.com", QMessageBox.Yes)
                #         break
                #     i = i + 1
                # self.combo.addItem("Stduino Nano_Small ")  # l m l l m h m h h
                # self.combo.addItem("Stduino Nano_Medium")
                # self.combo.addItem("Stduino Uno        ")
                # self.combo.addItem("Stduino Pro_Small  ")
                # self.combo.addItem("Stduino Pro_Medium ")
                # self.combo.addItem("Stduino Pro_High   ")
                # self.combo.addItem("Stduino Plus_Medium")
                # self.combo.addItem("Stduino Plus_High  ")
                # self.combo.addItem("Stduino Max        ")

                # 板型加载

                # stdtype = int(res.stdtype)
                # self.combo.setCurrentIndex(stdtype)
                # self.combo.setVisible(False)
                # toolbar.addAction(self.lbl)
                # toolbar.addAction(self.combo)

                # self.combo.currentIndexChanged.connect(self.toggleMenu)

                # self.lb2 = QLabel("选择下载方式", self)
                # self.combo1 = QComboBox(self)
                # self.combo1.addItem("USB_ISP")
                # self.combo1.addItem("St_link v2")
                # self.combo1.setCurrentIndex(download_type)
                # self.combo1.currentIndexChanged.connect(self.toggleMenu3)
                # self.combo1.move(585, 25)
                # self.lb2.move(510, 25)
                self.upload_list_la = QLabel(reso.choose_down_type, self)#gray#323232
                self.upload_list_la.setStyleSheet("background-color:#32414b;border-bottom : 0px solid #19232D;")  #dark #32414b需设置跟随主题背景
                self.upload_list_show = QComboBox(self)
                self.upload_list_show.setFixedWidth(135)
                self.upload_list_show.addItem("None")  #
                self.upload_list_show.activated.connect(self.upload_method_change)
                self.lbw = QLabel(reso.choose_port, self)
                self.lbw.setStyleSheet("background-color:#32414b;border-bottom : 0px solid #19232D;")  # 需设置跟随主题背景
                self.wcombo = QComboBox(self)
                self.wcombo.setFixedWidth(100)

                self.wcombo.addItem("None")#
                self.wcombo.activated.connect(self.upload_port_change)

                self.serialFind = QToolButton(self)
                self.serialFind.setStyleSheet("background-color:#708090;")  ########## 串口查找按钮
                self.toolbar.addWidget(self.upload_list_la)
                self.toolbar.addWidget(self.upload_list_show)
                self.toolbar.addWidget(self.lbw)
                self.toolbar.addWidget(self.wcombo)
                self.toolbar.addWidget(self.serialFind)
                self.toolbar.addSeparator()  # 竖直分割线
                self.toolbar.addAction(self.serialAction)  # 串口监视器
                self.seri = serial.Serial()


                # self.toggleMenu2()

                self.serialFind.setText(reso.check_port)
                self.serialFind.clicked.connect(self.load_device)
                # self.toggleMenu3(download_type)
                #self.toggleMenu4()

                # self.browser.deleteLater() #影响统计数据


                # bss 运行内存占用，不占用 存储  text +data =总编译文件大小
                #self.readSession()
                #self.file_init_open()





                pass
            except:
                stdinit.std_signal_gobal.stdprintln()
                pass
                # print("Unexpected error:", sys.exc_info()[1])  # 错误内容
        except:
            stdinit.std_signal_gobal.stdprintln()
            QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdmainui0054！\n You can search it in stduino.com",
                                QMessageBox.Yes)

        ####self.show()           #不用这句可以？
    def text_Change(self):

        try:
            # 待完善
            self.savefileAction.setEnabled(stdinit.savefileAction_staus)
            self.forwardAction.setEnabled(stdinit.forwardAction_staus)
            self.backAction.setEnabled(stdinit.backAction_staus)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def load_user_url(self):
        try:
            #url = 'http://api.stduino.com/users'
            # browser = QWebEngineView()
            # browser.load(QUrl(url))


            requests.get("http://api.stduino.com/users")
            # if (r.status_code == 200):
            #     print(r.text)
            #time.sleep(20)
            #del browser

        except:
            pass

            #stdinit.std_signal_gobal.stdprintln()


        #time.sleep(5)
        # print(25)
        #os.popen('taskkill /IM Qtwebengineprocess.exe /F')


    # i_type 操作类型 int
    # i_name 文件名/文件类型 str
    # path  文件/文件夹路径 str
    def debug_return(self, text):
        try:

            self.terminald.back_text(text)
            # print(path_m)
        except:
            stdinit.std_signal_gobal.stdprintln()

        pass
    def manu_gdb_list(self):
        try:
            self.fileSave()
            stdinit.manual_mark.clear()
            for obj in stdinit.mark_object:
                mark_list = obj.mark_list
                if len(mark_list) > 0:
                    for i in mark_list:
                        pass
                        line = obj.markerLine(i)
                        if line > 0:
                            stdinit.manual_mark.append("break " + obj.filename + ":" + str(
                                line + 1))  # self.filename + ":" + str(line_nr + 1)
                        else:
                            obj.mark_list.remove(i)

            # print(stdinit.manual_mark)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def debug_sign(self, i):
        try:

            if i == 0:
                #self.textEdit.setReadOnly(True)
                #self.tabWidget.currentWidget()

                self.complexAction.setDisabled(True)
                self.uploadAction.setDisabled(True)
                self.upload_fast_Action.setDisabled(True)
                self.cleanAction.setDisabled(True)
                self.stackedLayout2.setCurrentIndex(0)
                t1 = threading.Thread(target=self.manu_gdb_list, name='manu_gdb_list' + str(i))
                t1.setDaemon(True)
                t1.start()  # File_tree_init




            else:
                #self.textEdit.setReadOnly(False)
                self.complexAction.setDisabled(False)
                self.uploadAction.setDisabled(False)
                self.upload_fast_Action.setDisabled(False)
                self.cleanAction.setDisabled(False)
                self.stackedLayout2.setCurrentIndex(1)
                stdinit.debug_mark_start = 0
                if self.debug_dict["last_ob"]==None:
                    pass
                else:
                    self.debug_dict["last_ob"].markerDelete(self.debug_dict["last_ob_line"], 0)
                    self.debug_dict["last_ob"].markerDelete(self.debug_dict["last_ob_line"], 4)
                    self.debug_dict["last_ob"] = None



        except:
            stdinit.std_signal_gobal.stdprintln()




    def list_echo(self, staus, msg):
        try:


            if staus == 1:
                if "error" in msg or "Error" in msg:
                    try:
                        self.listwidget.setTextColor(QColor(205,133,0))#
                        self.listwidget.append(msg)
                        self.listwidget.setTextColor(QColor(0, 255, 0))
                    except:
                        self.listwidget.setTextColor(QColor(0, 255, 0))

                else:
                    self.listwidget.append(msg)

            else:  # 0 清空

                self.listwidget.setText(msg)
        except:
            stdinit.std_signal_gobal.stdprintln()



    # def ter_cmd(self, cmd):
    #     try:
    #         print(11111111111111111111)
    #         self.debug_a.st_gdb_cmd(cmd)
    #         # self.terminald.back_text(text)
    #     except:
    #         print("Unexpected error:", sys.exc_info()[1])  # 错误内容

    # \packages\STM32\tools\STM32Tools\1.4.0/tools/win/stm32CubeProg.bat 0 C:\Users\debug\AppData\Local\Temp\arduino_build_764923/sketch_jul26a.ino.bin -g(SWD)
    # \packages\STM32\tools\STM32Tools\1.4.0/tools/win/stm32CubeProg.bat 1 C:\Users\debug\AppData\Local\Temp\arduino_build_764923/sketch_jul26a.ino.bin -s(Serial)
    # \packages\STM32\tools\STM32Tools\1.4.0/tools/win/stm32CubeProg.bat 2 C:\Users\debug\AppData\Local\Temp\arduino_build_764923/sketch_jul26a.ino.bin -g(DFU)
    # \packages\STM32\tools\STM32Tools\1.4.0/tools/win/hid-flash.exe C:\Users\debug\AppData\Local\Temp\arduino_build_764923/sketch_jul26a.ino.bin COM5
    # \packages\STM32\tools\STM32Tools\1.4.0/tools/win/maple_upload.bat COM5 2 1EAF:0003 C:\Users\debug\AppData\Local\Temp\arduino_build_764923/sketch_jul26a.ino.bin
    # \packages\STM32\tools\STM32Tools\1.4.0/tools/win/maple_upload.bat COM5 1 1EAF:0003 C:\Users\debug\AppData\Local\Temp\arduino_build_764923/sketch_jul26a.ino.bin
    # \packages\STM32\tools\STM32Tools\1.4.0/tools/win/massStorageCopy.bat -I C:\Users\debug\AppData\Local\Temp\arduino_build_764923/sketch_jul26a.ino.bin -O NODE_F031K6
    # \packages\STM32\tools\STM32Tools\1.4.0/tools/win/massStorageCopy.bat -I C:\Users\debug\AppData\Local\Temp\arduino_build_764923/sketch_jul26a.ino.bin -O NODE_L031K6

    def find_button_enable(self):
        try:
            self.find_b_Action.setEnabled(True)
        except:
            stdinit.std_signal_gobal.stdprintln()


        # self.status2.setText(text + reso.on + self.wcombo.currentText() + reso.download_type_1 + upload_me)

    def new_me(self, i_type, i_name, path):

        try:
            if i_type == 1:
                if path:
                    ist = 0
                    for i in range(self.tabWidget.count()):
                        self.textEdit = self.tabWidget.widget(i)
                        if self.textEdit.filename == path:
                            self.tabWidget.setCurrentWidget(self.textEdit)
                            ist = 1
                            break

                    if ist == 0:
                        self.loadFile(path)

            elif i_type == 5:#移动后新的路径更新

                for i in range(self.tabWidget.count()):
                    self.textEdit = self.tabWidget.widget(i)
                    if self.textEdit.filename == i_name:
                        self.textEdit.setWindowTitle(path)
                        self.textEdit.filename = path
                        try:
                            pass
                            self.tabWidget.setTabText(i, QFileInfo(self.textEdit.filename).fileName())
                        except:
                            pass
                            # print("Unexpected error:", sys.exc_info()[1])  # 错误内容

                        break
            elif i_type == 6:

                for i in range(self.tabWidget.count()):
                    self.textEdit = self.tabWidget.widget(i)
                    if self.textEdit.filename == i_name:
                        self.tabWidget.removeTab(i)
                        break

            else:
                self.textEdit = StdTabEdit(i_name)
                self.textEdit.setText(myCodeSample)  # 新建文件插入默认注释
                self.textEdit.setModified(True)
                self.tabWidget.addTab(self.textEdit, QFileInfo(self.textEdit.filename).fileName())
                self.tabWidget.setCurrentWidget(self.textEdit)

        except:
            stdinit.std_signal_gobal.stdprintln()

    def Debug_goto_S(self,fullname,func,number,line,message):
        try:
            fullname = fullname.replace("\\", "/")
            line = int(line) - 1
            ist = 0
            for i in range(self.tabWidget.count()):
                if self.tabWidget.widget(i).filename == fullname:
                    # self.tabWidget.setCurrentIndex(i)
                    self.textEdit = self.tabWidget.widget(i)
                    self.textEdit.setCursorPosition(line, 0)

                    # print(line)
                    # self.tabWidget.widget(i).findFirst(findtext, False, True, True, True)
                    ist = 1
                    # stdinit.std_signal_gobal.std_echo_msg(1,"已成功跳转至："+findtext)
                    break
            if ist == 0:
                # print(111111)
                self.textEdit = StdTabEdit(fullname)

                try:
                    fh = open(file=fullname, mode='rb')  # 以二进制模式读取文件
                    data = fh.read()  # 获取文件内容
                    fh.close()  # 关闭文件unicode
                    self.textEdit.setText(data.decode("utf-8", 'ignore'))
                    self.textEdit.setModified(False)
                    self.tabWidget.addTab(self.textEdit, self.textEdit.windowTitle())
                    self.textEdit.setCursorPosition(line, 0)
                except EnvironmentError as e:
                    stdinit.std_signal_gobal.stdprintln()
                    QMessageBox.warning(self,
                                        "Stduino IDE  -- Load Error",
                                        "Failed to load {0}: {1}".format(fullname, e))
                    self.textEdit.close()
                    del self.textEdit
            # if message == "breakpoint-created":
            #     pass
            if message == "stopped":
                try:
                    # print(22222222222222111111111111)
                    # self.debug_dict["fullname" + number] = fullname
                    # self.debug_dict["line" + number] = line
                    if self.debug_dict["last_ob"] == None:
                        self.textEdit.markerAdd(line, 0)
                        self.textEdit.markerAdd(line, 4)

                        self.tabWidget.setCurrentWidget(self.textEdit)
                        self.debug_dict["last_ob"] = self.textEdit
                        self.debug_dict["last_ob_line"] = line  # line #handle
                    else:
                        if self.debug_dict["last_ob"].markersAtLine(self.debug_dict["last_ob_line"]) > 1:  # markerLine(self.debug_dict["last_ob_line"])> 0:
                            self.debug_dict["last_ob"].markerDelete(self.debug_dict["last_ob_line"], 0)
                            self.debug_dict["last_ob"].markerDelete(self.debug_dict["last_ob_line"], 4)

                            # self.debug_dict["last_ob"].markerDeleteHandle(self.debug_dict["last_ob_line"])
                            # self.debug_dict["last_ob"].markerAdd(self.debug_dict["last_ob_line"], 1)
                            # self.debug_dict["last_ob"].markerAdd(self.debug_dict["last_ob_line"], 1)
                            # 如果用户自行点击的则通过判断del的方式搞定

                            self.textEdit.markerAdd(line, 0)
                            self.textEdit.markerAdd(line, 4)

                            self.tabWidget.setCurrentWidget(self.textEdit)
                            self.debug_dict["last_ob"] = self.textEdit
                            self.debug_dict["last_ob_line"] = line
                        else:

                            # self.debug_dict["last_ob"].markerDelete(self.debug_dict["last_ob_line"])
                            # self.debug_dict["last_ob"].markerAdd(self.debug_dict["last_ob_line"], 1)
                            # 如果用户自行点击的则通过判断del的方式搞定

                            self.tabWidget.setCurrentWidget(self.textEdit)
                            self.textEdit.markerAdd(line, 0)
                            self.textEdit.markerAdd(line, 4)
                            self.tabWidget.setCurrentWidget(self.textEdit)
                            self.debug_dict["last_ob"] = self.textEdit
                            self.debug_dict["last_ob_line"] = line

                except EnvironmentError as e:
                    stdinit.std_signal_gobal.stdprintln()

            # if message == "breakpoint-deleted":
            #     try:
            #         fullname = self.debug_dict["fullname" + number]
            #         line = self.debug_dict["line" + number]
            #         for i in range(self.tabWidget.count()):
            #             if self.tabWidget.widget(i).filename == fullname:
            #                 self.textEdit = self.tabWidget.widget(i)
            #                 print(888888888888888888)
            #                 print(self.textEdit.markersAtLine(line))
            #                 if self.textEdit.markersAtLine(line) == python3:
            #                     self.textEdit.markerDelete(line)
            #                     self.textEdit.markerAdd(line, 0)
            #                 elif self.textEdit.markersAtLine(line) == 8:
            #                     self.textEdit.markerDelete(line)
            #
            #                     # self.textEdit.markerAdd(line, 0)
            #
            #                     # self.textEdit.markerAdd(line, 0)
            #                 break
            #     except EnvironmentError as e:
            #         print("Unexpected error:", sys.exc_info()[1])  # 错误内容
            #         QMessageBox.warning(self,
            #                             "Stduino IDE  -- Load Error",
            #                             "Failed to load {0}: {1}".format(fullname, e))










        except:

            stdinit.std_signal_gobal.stdprintln()



    def Jump_To_Look_W(self,path,line,findtext):
        try:
            ist = 0
            for i in range(self.tabWidget.count()):
                if self.tabWidget.widget(i).filename == path:

                    #self.tabWidget.setCurrentWidget(self.textEdit)
                    self.tabWidget.setCurrentIndex(i)
                    #time.sleep(0.1)
                    #self.tabWidget.widget(i).unsetCursor()
                    self.tabWidget.widget(i).setCursorPosition(line,0)
                    #print(line)
                    self.tabWidget.widget(i).findFirst(findtext, False, True, True, True)
                    ist = 1
                    stdinit.std_signal_gobal.std_echo_msg(1,"已成功跳转至："+findtext)
                    break
            if ist == 0:
                #print(111111)
                #print(111111)
                self.textEdit = StdTabEdit(path)
                try:
                    fh = open(file=path, mode='rb')  # 以二进制模式读取文件
                    data = fh.read()  # 获取文件内容
                    fh.close()  # 关闭文件unicode
                    self.textEdit.setText(data.decode("utf-8", 'ignore'))
                    self.textEdit.lineIndexFromPosition(line)
                    self.textEdit.setCursorPosition(line, 0)
                    self.textEdit.findFirst(findtext, False, True, True, True)
                    self.textEdit.setModified(False)

                    self.tabWidget.addTab(self.textEdit, self.textEdit.windowTitle())
                    self.tabWidget.setCurrentWidget(self.textEdit)
                    stdinit.std_signal_gobal.std_echo_msg(1, "已成功跳转至：" + findtext)
                    return 0

                except EnvironmentError as e:
                    stdinit.std_signal_gobal.stdprintln()

                    self.textEdit.close()
                    del self.textEdit



        except:
            stdinit.std_signal_gobal.stdprintln()


    ''''''



    def fileOpen_lib_example(self, q):
        try:
            QMessageBox.information(self, "感谢您的使用", "功能正在完善中欢迎至stduino.com 提供建议",QMessageBox.Yes)
            return 0
            filename = q.text()
            # print()
            for file in self.lib_example_path:
                # print(file)
                if re.search(filename, file) == None:
                    pass
                else:
                    try:
                        if file:
                            ist = 0
                            for i in range(self.tabWidget.count()):
                                self.textEdit = self.tabWidget.widget(i)
                                if self.textEdit.filename == file:
                                    self.tabWidget.setCurrentWidget(self.textEdit)
                                    ist = 1
                                    break
                            if ist == 0:
                                self.loadFile(file)
                        pass

                    except:
                        pass
                    pass
        except:
            stdinit.std_signal_gobal.stdprintln()
            # try:
            #     if file:
            #         for i in range(self.tabWidget.count()):
            #             textEdit = self.tabWidget.widget(i)
            #             if textEdit.filename == file:
            #                 self.tabWidget.setCurrentWidget(textEdit)
            #                 break
            #         else:
            #             self.loadFile(file)
            #     pass
            #
            # except:
            #     pass

    def import_lib(self, q):
        try:
            QMessageBox.information(self, "感谢您的使用", "功能正在完善中欢迎至stduino.com 提供建议",QMessageBox.Yes)
            return 0
            lib = q.text()
            # print(lib)
            self.tabWidget.currentWidget().setCursorPosition(0, 0)
            self.tabWidget.currentWidget().insert('#include "' + lib + '.h"\n')
            # textEdit = StdTabEdit()
            # textEdit.setText()
            # textEdit.setCursorPosition()
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()
    def goto_taobao(self):
        try:
            pass
            webview.create_window('Stduino', 'http://taobao.stduino.com')
            webview.start()
            # pos = os.path.abspath('.').replace("\\", "/") + "/cs quan"
            # subprocess.Popen(pos, shell=True, stdout=subprocess.PIPE)  # 使用管道
            #QMessageBox.Yes="立即支持"
            # webbrowser.open("wiki.stduino.com")
            #stdinit.Std_help.put("quan")
            # if stdinit.std_he_qu==0:
            #     stdinit.Std_help.put("quan")
            # else:
            #
            #     QMessageBox.about(self, "优惠券", "界面已经打开了，若看不到，点击状态栏中Stduino IDE图标即可看到", QMessageBox.Yes | QMessageBox.No)



            # reply =QMessageBox.information(self,
            #                         "领个优惠券支持下开发者",
            #                         "stduino IDE自2015年开始开发，熬了不知多少个夜晚，如果确实帮到了你，欢迎在需要的时候至 taobao.stduino.com 领个优惠券购买些生活用品支持下呗\n",
            #                         QMessageBox.Ok | QMessageBox.No)
            #
            # if reply==1024:
            #     webbrowser.open("taobao.stduino.com")
            #QMessageBox.about(self, "taobao.stduino.com", "", QMessageBox.Yes | QMessageBox.No)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def st_help(self):
        try:
            pass
            webview.create_window("Stduino", "http://www.stduino.com/forum.php?mod=viewthread&tid=105")
            webview.start()

            # pos = os.path.abspath('.').replace("\\", "/")+"/cs help"
            #
            # subprocess.Popen(pos, shell=True, stdout=subprocess.PIPE)  # 使用管道

            #stdinit.Std_help.put("help")

            # tdh = threading.Thread(target=self.st_helps, name='st_helps' )
            # tdh.setDaemon(True)
            # tdh.start()  # File_tree_init
            #webbrowser.open("wiki.stduino.com")
        except:
            stdinit.std_signal_gobal.stdprintln()

    def st_feedback(self):
        try:
            value, ok = QInputDialog.getMultiLineText(self, "FeedBack",
                                                      reso.server + "\n\nThank you for your feedback!",
                                                      reso.server_detail)
            # self.echo(value)
            if ok == 1:
                ret = True
                try:
                    msg = MIMEText(value, 'plain', 'utf-8')
                    msg['From'] = formataddr(["FromStduinoIDE", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
                    msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
                    msg['Subject'] = "StduinoIDE " + reso.feed_back  # 邮件的主题，也可以说是标题
                    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
                    server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
                    server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
                    server.quit()  # 关闭连接
                except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
                    stdinit.std_signal_gobal.stdprintln()

                    ret = False

                if ret:
                    self.listwidget.setText(reso.feed_back_thank)
                else:
                    self.listwidget.setText(reso.feed_back_failed)
                pass
        except:
            stdinit.std_signal_gobal.stdprintln()

    def openstduino(self):
        try:
            webbrowser.open("www.stduino.com")
        except:
            stdinit.std_signal_gobal.stdprintln()

    def open_driver(self):
        try:
            os.startfile('.\\tool\driver')
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()

    def guanyu(self):
        try:
            QMessageBox.information(self,
                                    reso.about_ide,
                                    "Stduino IDE是一款面向32位处理器快速入门学习的集成开发平台，将陆续集成更多框架平台，敬请期待！\nStduino IDE is a 32-bit processor for quick start to learn the integrated development platform, will gradually integrate more framework platform, stay tuned!\nDesigned By stduino.com",
                                    QMessageBox.Yes)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def openProject(self):
        try:
            os.startfile(stdinit.projects_dir)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def openLibrary(self):
        try:
            QMessageBox.information(self, "感谢您的使用", "功能正在完善中欢迎至stduino.com 提供建议",QMessageBox.Yes)
            # os.startfile(stdinit.projects_dir)
        except:
            stdinit.std_signal_gobal.stdprintln()

        # print(cs)
        # open(res.library)

    def searchLibrary(self):
        try:
            reply = QMessageBox.information(self,
                                            reso.tip,
                                            reso.function_development,
                                            QMessageBox.Yes)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def shareLibrary(self):
        try:
            QMessageBox.information(self, "感谢您的使用", "功能正在完善中欢迎至stduino.com 提供建议",QMessageBox.Yes)
            # dir = QFileDialog.getExistingDirectory(self,
            #                                        reso.lib_share,
            #                                        stdinit.projects_dir)  # 起始路径
            #
            # dirname = QFileInfo(dir).fileName()
            # pos = os.path.abspath('.')
            # os.chdir(dir)



        #  * @ attention
        # 努力让祖国更强大
        # ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
        except:
            stdinit.std_signal_gobal.stdprintln()

    def libraryNew(self):
        try:
            QMessageBox.information(self, "感谢您的使用", "功能正在完善中欢迎至stduino.com 提供建议",QMessageBox.Yes)

            return 0
            # myCodeSample
            li_c = r"""/***********************************************************************
  * @代码说明：
  * @作者：
  * @日期：
  * @开发指导：wiki.stduino.com
  ***********************************************************************/

/* Includes ------------------------------------------------------------------*/

//例如：#include "stm32f10x_abc.h"

/*上面不用动，开始你的表演 ------------------------------------------------------*/""".replace("\n", "\r\n")
            li_c_h = r"""/***********************************************************************
  * @代码说明：
  * @作者：
  * @日期：
  * @开发指导：wiki.stduino.com
  ***********************************************************************/
/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef  __XXX_H //例如：#ifndef __ABC_H
#define  __XXX_H  //例如：#define __ABC_H
#include "Stduino.h"
#ifdef __cplusplus
extern "C" {
#endif
/*上面不用动，开始你的表演 ------------------------------------------------------------------*/











/*下面不用动，表演结束------------------------------------------------------------------*/

#ifdef __cplusplus
}
#endif

#endif""".replace("\n", "\r\n")
            li_cpp = r"""/***********************************************************************
  * @代码说明：
  * @作者：
  * @日期：
  * @开发指导：wiki.stduino.com
  ***********************************************************************/
/* Includes ------------------------------------------------------------------*/
//例如：#include "stm32f10x_abc.h"
/*上面不用动，开始你的表演 ------------------------------------------------------------------*/""".replace("\n", "\r\n")
            li_cpp_h = r"""/***********************************************************************
  * @代码说明：
  * @作者：
  * @日期：
  * @开发指导：wiki.stduino.com
  ***********************************************************************/
/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __XXX_H //例如：#ifndef __ABC_H
#define __XXX_H //例如：#define __ABC_H
#include "Stduino.h"
/*上面不用动，开始你的表演 ------------------------------------------------------------------*/













/*下面不用动，表演结束------------------------------------------------------------------*/
#endif /*__XXX_XXX_H */""".replace("\n", "\r\n")
            library_properties = r"""
version = 1.0
author = """.replace("\n", "\r\n")

            message = QMessageBox()
            message.setWindowIcon(QIcon(res.img))
            message.setWindowTitle(reso.language_choose)
            message.setIcon(QMessageBox.Question)
            message.setText(reso.language_select)
            message.addButton("C", QMessageBox.AcceptRole)
            message.addButton(reso.cancel, QMessageBox.NoRole)
            message.addButton("C++", QMessageBox.ApplyRole)
            # message.setDefaultButton(msg_no)
            reply = message.exec_()
            if reply == 0:
                path = stdinit.projects_dir + "/test_{0}".format(self.NextId)
                isExists = os.path.exists(path)
                # print(path)
                while isExists:
                    self.NextId += 1
                    path = stdinit.projects_dir + "/test_{0}".format(self.NextId)
                    isExists = os.path.exists(path)
                value, ok = QInputDialog.getText(self, reso.lib_name, reso.file_name, QLineEdit.Normal,
                                                 "test_{0}".format(self.NextId))
                if ok == True:
                    path = stdinit.projects_dir + '/' + value
                    os.makedirs(path)
                    time.sleep(0.4)
                    # os.makedirs(path + "/src")
                    os.makedirs(path + "/src")
                    os.makedirs(path + "/example")
                    self.NextId += 1
                    self.textEdit = StdTabEdit(path + '/src/' + value + '.c')

                    li_c = "#include \"" + value + ".h\"\n" + li_c
                    fo = open(path + '/src/' + value + '.c', "w", encoding='UTF-8')
                    fo.write(li_c)
                    fo.close()
                    self.textEdit.setText(li_c)  # 新建文件插入默认注释
                    self.textEdit.setModified(True)
                    self.tabWidget.addTab(self.textEdit, QFileInfo(self.textEdit.filename).fileName())
                    self.tabWidget.setCurrentWidget(self.textEdit)

                    self.textEdit = StdTabEdit(path + '/src/' + value + '.h')

                    fo = open(path + '/src/' + value + '.h', "w", encoding='UTF-8')
                    fo.write(li_c_h)
                    fo.close()
                    self.textEdit.setText(li_c_h)  # 新建文件插入默认注释
                    self.textEdit.setModified(True)
                    self.tabWidget.addTab(self.textEdit, QFileInfo(self.textEdit.filename).fileName())
                    self.tabWidget.setCurrentWidget(self.textEdit)

                    self.textEdit = StdTabEdit(path + '/library.properties')

                    library_properties = "name =" + value + library_properties
                    fo = open(path + '/library.properties', "w", encoding='UTF-8')
                    fo.write(library_properties)
                    fo.close()
                    self.textEdit.setText(library_properties)  # 新建文件插入默认注释
                    self.textEdit.setModified(True)
                    self.tabWidget.addTab(self.textEdit, QFileInfo(self.textEdit.filename).fileName())
                    self.tabWidget.setCurrentWidget(self.textEdit)

                    self.textEdit = StdTabEdit(path + '/' + 'keywords.txt')

                    fo = open(path + '/' + 'keywords.txt', "w", encoding='UTF-8')
                    fo.write("//One keyword per line, delete the line after completion")
                    fo.close()

                    self.textEdit.setText("//One keyword per line, delete the line after completion")  # 新建文件插入默认注释
                    self.textEdit.setModified(True)
                    self.tabWidget.addTab(self.textEdit, QFileInfo(self.textEdit.filename).fileName())
                    self.tabWidget.setCurrentWidget(self.textEdit)

                    self.textEdit = StdTabEdit(path + '/example/' + value + '_example.ino')

                    myCode = "#include <" + value + ".h>\n" + myCodeSample
                    fo = open(path + '/example/' + value + '_example.ino', "w", encoding='UTF-8')
                    fo.write(myCode)
                    fo.close()
                    self.textEdit.setText(myCode)  # 新建文件插入默认注释
                    self.textEdit.setModified(True)
                    self.tabWidget.addTab(self.textEdit, QFileInfo(self.textEdit.filename).fileName())
                    self.tabWidget.setCurrentWidget(self.textEdit)

            if reply == 2:
                path = stdinit.projects_dir + "/test_{0}".format(self.NextId)
                isExists = os.path.exists(path)

                while isExists:
                    self.NextId += 1
                    path = stdinit.projects_dir + "/test_{0}".format(self.NextId)
                    isExists = os.path.exists(path)
                value, ok = QInputDialog.getText(self, reso.lib_name, reso.file_name, QLineEdit.Normal,
                                                 "test_{0}".format(self.NextId))
                if ok == True:
                    path = stdinit.projects_dir + '/' + value
                    os.makedirs(path)
                    time.sleep(0.4)
                    # os.makedirs(path + "/inc")
                    os.makedirs(path + "/src")
                    os.makedirs(path + "/example")
                    self.NextId += 1
                    self.textEdit = StdTabEdit(path + '/src/' + value + '.cpp')

                    li_cpp = "#include \"" + value + ".h\"\n" + li_cpp
                    fo = open(path + '/src/' + value + '.cpp', "w", encoding='UTF-8')
                    fo.write(li_cpp)
                    fo.close()
                    self.textEdit.setText(li_cpp)  # 新建文件插入默认注释
                    self.textEdit.setModified(True)
                    self.tabWidget.addTab(self.textEdit, QFileInfo(self.textEdit.filename).fileName())
                    self.tabWidget.setCurrentWidget(self.textEdit)

                    self.textEdit = StdTabEdit(path + '/src/' + value + '.h')

                    fo = open(path + '/src/' + value + '.h', "w", encoding='UTF-8')
                    fo.write(li_cpp_h)
                    fo.close()
                    self.textEdit.setText(li_cpp_h)  # 新建文件插入默认注释
                    self.textEdit.setModified(True)
                    self.tabWidget.addTab(self.textEdit, QFileInfo(self.textEdit.filename).fileName())
                    self.tabWidget.setCurrentWidget(self.textEdit)

                    self.textEdit = StdTabEdit(path + '/library.properties')

                    library_properties = "name =" + value + library_properties
                    fo = open(path + '/library.properties', "w", encoding='UTF-8')
                    fo.write(library_properties)
                    fo.close()
                    self.textEdit.setText(library_properties)  # 新建文件插入默认注释
                    self.textEdit.setModified(True)
                    self.tabWidget.addTab(self.textEdit, QFileInfo(self.textEdit.filename).fileName())
                    self.tabWidget.setCurrentWidget(self.textEdit)

                    self.textEdit = StdTabEdit(path + '/' + 'keywords.txt')

                    fo = open(path + '/' + 'keywords.txt', "w", encoding='UTF-8')
                    fo.write("//One keyword per line, delete the line after completion")
                    fo.close()
                    self.textEdit.setText("//One keyword per line, delete the line after completion")  # 新建文件插入默认注释
                    self.textEdit.setModified(True)
                    self.tabWidget.addTab(self.textEdit, QFileInfo(self.textEdit.filename).fileName())
                    self.tabWidget.setCurrentWidget(self.textEdit)

                    self.textEdit = StdTabEdit(path + '/example/' + value + '_example.ino')

                    myCode = "#include <" + value + ".h>\n" + myCodeSample
                    fo = open(path + '/example/' + value + '_example.ino', "w", encoding='UTF-8')
                    fo.write(myCode)
                    fo.close()
                    self.textEdit.setText(myCode)  # 新建文件插入默认注释
                    self.textEdit.setModified(True)
                    self.tabWidget.addTab(self.textEdit, QFileInfo(self.textEdit.filename).fileName())
                    self.tabWidget.setCurrentWidget(self.textEdit)

        # def fileNew(self):
        #
        #     textEdit = StdTabEdit('')
        #     textEdit.setText(myCodeSample)          #新建文件插入默认注释
        #     textEdit.setModified(True)
        #     self.tabWidget.addTab(textEdit, textEdit.filename)
        #     #self.setText(stream.readAll())
        #
        #     self.tabWidget.setCurrentWidget(textEdit)
        except:
            stdinit.std_signal_gobal.stdprintln()

        # self.textBrowser.setText('文件路径:\n' + os.path.dirname((event.mimeData().urls())[0].toLocalFile()))

    def fileOpen_trop(self, filename):
        try:

            if filename:
                ist = 0
                for i in range(self.tabWidget.count()):
                    self.textEdit = self.tabWidget.widget(i)
                    if self.textEdit.filename == filename:
                        self.tabWidget.setCurrentWidget(self.textEdit)
                        ist = 1
                        break
                if ist == 0:
                    self.loadFile(filename)

        except:
            stdinit.std_signal_gobal.stdprintln()

        # print(1)

    def dragEnterEvent(self, event):
        try:
            self.fileOpen_trop(event.mimeData().text().replace('file:///', ''))
        except:
            stdinit.std_signal_gobal.stdprintln()
        # print('文件路径:\n' + os.path.dirname((event.mimeData().urls())[0].toLocalFile()))


    def fileOpen(self):
        try:
            filename, filetype = QFileDialog.getOpenFileName(self,
                                                             "Stduino IDE -- Open File",
                                                             stdinit.projects_dir,
                                                             "All Files (*)")  # 设置文件扩展名过滤,注意用双分号间隔

            if filename:
                ist = 0
                for i in range(self.tabWidget.count()):
                    self.textEdit = self.tabWidget.widget(i)
                    if self.textEdit.filename == filename:
                        self.tabWidget.setCurrentWidget(self.textEdit)
                        ist = 1
                        break
                if ist == 0:
                    self.loadFile(filename)

        except:
            stdinit.std_signal_gobal.stdprintln()

    def autofileOpen(self):
        try:
            target = stdinit.stdenv + "/.stduino/session/keywords.txt"  # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"
            if os.path.exists(target):
                ist = 0
                for i in range(self.tabWidget.count()):
                    self.textEdit = self.tabWidget.widget(i)
                    if self.textEdit.filename == target:
                        self.tabWidget.setCurrentWidget(self.textEdit)
                        ist = 1
                        break
                if ist == 0:
                    self.loadFile(target)
            else:
                target2 = stdinit.stdenv + "/.stduino/session"
                if os.path.exists(target2):
                    shutil.copy2('./appearance/stduino_json/keywords.txt', target)
                    self.loadFile(target)
                else:
                    os.makedirs(target2)
                    shutil.copy2('./appearance/stduino_json/keywords.txt', target)
                    self.loadFile(target)

        except:
            stdinit.std_signal_gobal.stdprintln()

    def loadFile(self, filename):
        try:
            self.textEdit = StdTabEdit(filename)

            self.textEdit.setModified(False)
            try:
                x = self.textEdit.load()
                if x == 1:
                    return 1
                else:
                    self.tabWidget.addTab(self.textEdit, self.textEdit.windowTitle())
                    self.tabWidget.setCurrentWidget(self.textEdit)
                    return 0
            except EnvironmentError as e:
                stdinit.std_signal_gobal.stdprintln()
                self.textEdit.close()
                del self.textEdit

        except:
            stdinit.std_signal_gobal.stdprintln()

    def fileSave(self):


        try:
            self.textEdit = self.tabWidget.currentWidget()
            try:
                name = self.textEdit.filename
                if name in stdinit.profile_modify_ui:
                    pass
                else:
                    stdinit.profile_modify_ui.append(name)
                self.textEdit.save()
                #self.tabWidget.setTabText(self.tabWidget.currentIndex(), QFileInfo(self.textEdit.filename).fileName())
                # print(QFileInfo(textEdit.filename).fileName())
                self.savefileAction.setDisabled(True)

                #self.setWindowTitle("Stduino IDE " + stdinit.version_c + " [" + self.textEdit.filename + ']')  # 文件名设置        待完善

                # self.savefileAction.setDisabled(True)
                # for i in range(self.tabWidget.count()):
                #     self.textEdit = self.tabWidget.widget(i)
                #     if self.textEdit.isModified():
                #         try:
                #             # textEdit.save()
                #             self.savefileAction.setDisabled(False)
                #
                #         except EnvironmentError as e:
                #             print(e)
                #             pass
                            # errors.append("{0}: {1}".format(textEdit.filename, e))
                return True
            except EnvironmentError as e:
                stdinit.std_signal_gobal.stdprintln()
                return False


        except:
            stdinit.std_signal_gobal.stdprintln()

    def fileSaveAs(self):
        try:

            self.textEdit = self.tabWidget.currentWidget()
            if self.textEdit is None:
                return True
            filename, filetype = QFileDialog.getSaveFileName(self,
                                                             "Stduino IDE  -- Save File As", self.textEdit.filename,
                                                             "All Files (*.)")

            if filename:
                #fh = QFile(self.filename)
                fo = open(filename, "w+", encoding="utf-8", newline="")  # gbk_utf_type
                fo.write(self.textEdit.text())
                fo.close()


        except:
            stdinit.std_signal_gobal.stdprintln()

    def fileSaveAll(self):
        try:
            errors = []

            self.savefileAction.setDisabled(True)
            for i in range(self.tabWidget.count()):
                self.textEdit = self.tabWidget.widget(i)
                if self.textEdit.isModified():
                    try:
                        name=self.textEdit.filename
                        if name in stdinit.profile_modify_ui:
                            pass
                        else:
                            stdinit.profile_modify_ui.append(name)

                        self.textEdit.save()

                    except EnvironmentError as e:
                        errors.append("{0}: {1}".format(self.textEdit.filename, e))
            if errors:
                QMessageBox.warning(self, "Stduino IDE  -- "
                                          "Save All Error",
                                    "Failed to save\n{0}".format("\n".join(errors)))

        except:
            stdinit.std_signal_gobal.stdprintln()

    def funcXML(self, elem):
        try:
            '''
                    将节点转化成字符串，并添加缩进
                    :param elem:
                    :return:
                    '''
            rough_string = ET.tostring(elem, 'utf-8')
            reparsed = minidom.parseString(rough_string)
            # 返回缩进
            return reparsed.toprettyxml(indent="\t")

        except:
            stdinit.std_signal_gobal.stdprintln()

    def readSession(self):
        try:

            newuser = 0
            unnew = 0
            # 使用minidom解析器打开 XML 文档
            session = stdinit.session_dir + "/session.xml"

            isExists = os.path.exists(session)
            if isExists:
                try:
                    DOMTree = xml.dom.minidom.parse(session)
                except:
                    try:
                        comment_p = stdinit.session_dir + "/comment"
                        if os.path.exists(comment_p):
                            self.loadFile(comment_p)
                        else:
                            if os.path.exists(stdinit.session_dir):
                                shutil.copy2(stdinit.abs_path + "/tool/packages/other/comment", comment_p)
                                self.loadFile(comment_p)
                            else:
                                os.makedirs(stdinit.session_dir)
                                shutil.copy2(stdinit.abs_path + "/tool/packages/other/comment", comment_p)
                                self.loadFile(comment_p)


                        return  3
                    except:
                        stdinit.std_signal_gobal.stdprintln()

                collection = DOMTree.documentElement

                # 在集合中获取所有文件
                activeIndex = collection.getAttribute("activeIndex")
                stdinit.project_name = collection.getAttribute("ProjectActive")
                stdinit.std_signal_gobal.std_work_space()
                indexNum = int(collection.getAttribute("indexNum"))
                files = collection.getElementsByTagName("File")


                if indexNum == 0:

                    try:
                        comment_p = stdinit.session_dir + "/comment"
                        if os.path.exists(comment_p):
                            self.loadFile(comment_p)
                        else:
                            if os.path.exists(stdinit.session_dir):
                                shutil.copy2(stdinit.abs_path + "/tool/packages/other/comment", comment_p)
                                self.loadFile(comment_p)
                            else:
                                os.makedirs(stdinit.session_dir)
                                shutil.copy2(stdinit.abs_path + "/tool/packages/other/comment", comment_p)
                                self.loadFile(comment_p)
                    except:
                        stdinit.std_signal_gobal.stdprintln()




                    #self.fileNew(0)
                else:
                    # 打开每个文件

                    for file in files:
                        try:
                            path = file.getAttribute("filePath")
                            isExists = os.path.exists(path)
                            if isExists:
                                unnew = 1
                                xi = self.loadFile(path)
                                if xi == 0:
                                    Cursor = file.getAttribute("CursorPosition")
                                    b = eval(Cursor)
                                    #print(b[0])
                                    Digitx = b[0]
                                    Digity = b[1]

                                    # for i in Cursor:
                                    #     if i == ",":
                                    #         xi = 1
                                    #     if i.isdigit():
                                    #         if xi == 0:
                                    #             Digitx += i
                                    #         else:
                                    #             Digity += i
                                    self.tabWidget.currentWidget().setCursorPosition(Digitx, Digity)

                            else:
                                newuser = 1

                        except:
                            stdinit.std_signal_gobal.stdprintln()
                            # print("Unexpected error:", sys.exc_info()[1])  # 错误内容
                            newuser = 1
                            pass

                    # print("Unexpected error:", sys.exc_info()[1])  # 错误内容
                    self.tabWidget.setCurrentIndex(int(activeIndex))
                    if unnew:
                        newuser = 0
                    if newuser == 1:
                        try:
                            comment_p = stdinit.session_dir + "/comment"
                            if os.path.exists(comment_p):
                                self.loadFile(comment_p)
                            else:
                                if os.path.exists(stdinit.session_dir):
                                    shutil.copy2(stdinit.abs_path + "/tool/packages/other/comment", comment_p)
                                    self.loadFile(comment_p)
                                else:
                                    os.makedirs(stdinit.session_dir)
                                    shutil.copy2(stdinit.abs_path + "/tool/packages/other/comment", comment_p)
                                    self.loadFile(comment_p)
                        except:
                            stdinit.std_signal_gobal.stdprintln()

                        #self.fileNew(0)
            else:
                try:
                    if os.path.exists(stdinit.session_dir):
                        shutil.copy2(stdinit.abs_path + "/tool/packages/session.xml",stdinit.stdenv + "/.stduino/session/session.xml")
                    else:
                        os.makedirs(stdinit.session_dir)
                        shutil.copy2(stdinit.abs_path + "/tool/packages/session.xml",stdinit.stdenv + "/.stduino/session/session.xml")
                    comment_p = stdinit.session_dir + "/comment"
                    if os.path.exists(comment_p):
                        self.loadFile(comment_p)
                    else:
                        if os.path.exists(stdinit.session_dir):
                            shutil.copy2(stdinit.abs_path + "/tool/packages/other/comment", comment_p)
                            self.loadFile(comment_p)
                        else:
                            os.makedirs(stdinit.session_dir)
                            shutil.copy2(stdinit.abs_path + "/tool/packages/other/comment", comment_p)
                            self.loadFile(comment_p)
                except:
                    stdinit.std_signal_gobal.stdprintln()



                #self.fileNew(0)
                pass



            try:
                if len(sys.argv) >= 2:
                    filename = sys.argv[1].replace("\\", "/")

                    # print(filename)
                    self.loadFile(filename)

                # self.tabWidget.setCurrentIndex(int(activeIndex))

                pass
            except:
                stdinit.std_signal_gobal.stdprintln()

            self.savefileAction.setEnabled(False)
            self.forwardAction.setDisabled(True)
            self.backAction.setDisabled(True)


        except:
            stdinit.std_signal_gobal.stdprintln()

    def saveSession(self):
        try:
            num = self.tabWidget.count()
            # 创建子节点
            son1 = ET.Element('MainView', {'activeIndex': str(self.tabWidget.currentIndex())})
            for x in range(self.tabWidget.count()):
                self.textEdit = self.tabWidget.widget(x)
                if self.textEdit.filename.startswith("Unnamed"):
                    num = num - 1
                    pass
                else:
                    son2 = ET.Element('File',
                                      {'CursorPosition': str(self.textEdit.getCursorPosition()),
                                       'filePath': self.textEdit.filename})
                    son1.append(son2)
            root = ET.Element("StduinoView",{'activeIndex': str(self.tabWidget.currentIndex()), 'indexNum': str(num),'ProjectActive': stdinit.project_name})  # 创建根节点
            # 将子节点追加到根节点中
            root.append(son1)
            if root==None:

                return 0

            # 保存
            r = self.funcXML(root)

            if os.path.exists(stdinit.session_dir):
                pass
            else:
                os.mkdir(stdinit.session_dir)
            session=stdinit.session_dir+"/session.xml"
            f = open(session, 'w+', encoding='utf-8')
            f.write(r)
            f.close()

        except:
            stdinit.std_signal_gobal.stdprintln()

    def closeEvent(self, event):

        try:

            #child3.close()         #test20211.11注释
            self.saveSession()
            for i in range(self.tabWidget.count()):
                self.textEdit = self.tabWidget.widget(i)
                if self.textEdit.isModified():
                    self.textEdit.save()
            # stdinit.Std_Serial_Tool1.timer_del()
            # stdinit.Std_Serial_Tool2.timer_del()
            #print(threading.active_count(), len(threading.enumerate()), threading.enumerate())
            if stdinit.File_tree_view is not None:
                del stdinit.File_tree_view
            if stdinit.find_boards is not None:
                del stdinit.find_boards
            if stdinit.Std_Serial_Tool2 is not None:
                del stdinit.Std_Serial_Tool2
            if stdinit.Std_Serial_Tool1 is not None:
                del stdinit.Std_Serial_Tool1
            if stdinit.Set_Back_Color1 is not None:
                del stdinit.Set_Back_Color1
            if stdinit.Std_Find is not None:
                del stdinit.Std_Find
            del self







            #event.accept()



            # reply = QMessageBox.warning(self, reso.exit,
            #                              "确定退出Stduino IDE？",
            #                              QMessageBox.Yes | QMessageBox.Cancel)
            # if reply == QMessageBox.Yes:
            #     event.accept()  # 关闭窗口即软件
            #     pass
            # elif reply == QMessageBox.Cancel:
            #     event.ignore()  # 不关闭窗口即软件
            #     pass
                # setup.savefilepath(self.fileName)

        except:
            stdinit.std_signal_gobal.stdprintln()


    # 关闭tab
    def close_Tab(self, index):
        # print(index)
        try:
            self.textEdit = self.tabWidget.widget(index)
            if self.textEdit in stdinit.mark_object:
                stdinit.mark_object.remove(self.textEdit)
            if self.textEdit.isModified():
                try:
                    name = self.textEdit.filename
                    if name in stdinit.profile_modify_ui:
                        pass
                    else:
                        stdinit.profile_modify_ui.append(name)

                    self.textEdit.save()
                except:
                    stdinit.std_signal_gobal.stdprintln()
            if self.tabWidget.count() > 1:
                try:

                    self.tabWidget.removeTab(index)
                except:
                    # print("Unexpected error:", sys.exc_info())  # 错误内容
                    pass
            else:
                self.tabWidget_no = 0
                self.tabWidget.removeTab(index)
                try:
                    comment_p = stdinit.session_dir + "/comment"
                    if os.path.exists(comment_p):
                        self.loadFile(comment_p)
                    else:
                        if os.path.exists(stdinit.session_dir):
                            shutil.copy2(stdinit.abs_path + "/tool/packages/other/comment", comment_p)
                            self.loadFile(comment_p)
                        else:
                            os.makedirs(stdinit.session_dir)
                            shutil.copy2(stdinit.abs_path + "/tool/packages/other/comment", comment_p)
                            self.loadFile(comment_p)
                except:
                    stdinit.std_signal_gobal.stdprintln()
                #self.loadFile(stdinit.abs_path + "/tool/packages/other/comment")
                # reply = QMessageBox.question(self, reso.tip, reso.last_close,
                #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                # if reply == QMessageBox.Yes:
                #     self.tabWidget_no = 0
                #     self.tabWidget.removeTab(index)
                #     self.loadFile(stdinit.abs_path + "/tool/packages/other/comment")
                #
                #
                #     #self.close()  # 当只有1个tab时，关闭主窗口_退出
                #     pass
                # else:
                #     pass
        except:
            stdinit.std_signal_gobal.stdprintln()

    def fileNew(self, num):#图形化开发
        try:
            num = 0
            if num == 0:
                reply = 0
            else:
                message = QMessageBox()
                message.setWindowIcon(QIcon(res.img))
                message.setWindowTitle('Stduino 开发模式选择')
                message.setIcon(QMessageBox.Question)
                message.setText("请选择开发模式")
                message.addButton("Code", QMessageBox.AcceptRole)
                message.addButton("取消", QMessageBox.NoRole)
                message.addButton("Block", QMessageBox.ApplyRole)
                # message.setDefaultButton(msg_no)
                reply = message.exec_()
            # reply=0
            if reply == 0:
                self.textEdit = StdTabEdit('')


                self.textEdit.setText(myCodeSample)  # 新建文件插入默认注释
                self.textEdit.setModified(True)
                self.tabWidget.addTab(self.textEdit, self.textEdit.filename)
                self.tabWidget.setCurrentWidget(self.textEdit)

                pass
            if reply == 2:
                try:
                    # view1 = QWebEngineView()
                    # view1.load(QUrl("file:///./appearance/editor/index.html"))  #
                    # self.tabWidget.addTab(view1, 'c')
                    # self.tabWidget.setCurrentWidget(view1)
                    pass
                except:
                    stdinit.std_signal_gobal.stdprintln()
                # print(2)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def upload_port_change(self):
        try:
            text = self.wcombo.currentText()
            if text == None:
                pass
            else:
                if stdinit.last_com == text:
                    pass
                else:
                    stdinit.last_com = text
                    self.status2.setText(stdinit.current_upload_m + ":" + text)
                    #init_path = stdinit.init_path
                    # stdinit.pro_conf.clear()
                    # stdinit.pro_conf.read(init_path, encoding="utf-8")  # python3
                    # stdinit.pro_conf.set(stdinit.pro_conf.sections()[0], "upload_port", text)
                    # stdinit.pro_conf.write(open(init_path, 'w'))
        except:
            stdinit.std_signal_gobal.stdprintln()



    def upload_method_change(self):
        try:
            if stdinit.current_upload_m == self.upload_list_show.currentText():
                pass
            else:
                if self.upload_list_show.currentText()=="Default" or self.upload_list_show.currentText()=="None":
                    return 0


                stdinit.current_upload_m = self.upload_list_show.currentText()
                self.status2.setText(stdinit.current_upload_m+":"+stdinit.last_com)
                init_path = stdinit.init_path
                stdinit.pro_conf.clear()
                stdinit.pro_conf.read(init_path, encoding="utf-8")  # python3
                stdinit.pro_conf.set(stdinit.pro_conf.sections()[0], "upload_protocol", stdinit.current_upload_m)
                stdinit.pro_conf.write(open(init_path, 'w'))

        except:
            stdinit.std_signal_gobal.stdprintln()



    def upload_method_ch(self):
        try:
            self.upload_list_show.clear()
            for i in stdinit.upload_meds:
                self.upload_list_show.addItem(i)
            self.upload_list_show.setCurrentText(stdinit.current_upload_m)
            self.status2.setText(stdinit.current_upload_m)
        except:
            stdinit.std_signal_gobal.stdprintln()


        # print(stdinit.upload_meds)
        # print(stdinit.upload_medd)#default
    def file_modify_check(self):
        try:
            for i in range(self.tabWidget.count()):
                self.textEdit = self.tabWidget.widget(i)
                name = self.textEdit.filename
                if name in stdinit.profile_modify_all:
                    fo = open(name, mode='r', encoding='UTF-8')
                    st = fo.read()
                    fo.close()
                    self.textEdit.setText(st)
            stdinit.profile_modify_all.clear()
        except:
            stdinit.std_signal_gobal.stdprintln()

    def tab_change_save(self,index):
        try:
            if index == None:
                pass
            else:

                self.textEdit = self.tabWidget.widget(index)
                if self.textEdit == None:  # 被关闭的已经被保存不存在对象了已经
                    pass
                else:

                    name = self.textEdit.filename
                    if self.textEdit.isModified():
                        if name in stdinit.profile_modify_ui:
                            pass
                        else:
                            stdinit.profile_modify_ui.append(name)
                        self.textEdit.save()
                        self.savefileAction.setEnabled(False)
                    else:
                        pass
        except:
            stdinit.std_signal_gobal.stdprintln()








    def tabChange(self, index):

        try:
            if self.tabWidget_no==0:

                pass
            else:
                t1 = threading.Thread(target=self.tab_change_save, name='li_change_save'+str(index),args=(self.tabWidget_change_from,))
                t1.setDaemon(True)
                t1.start()  # File_tree_init
                self.tabWidget_change_from = index
                class_name = self.tabWidget.widget(index).__class__.__name__
                s1 = self.tabWidget.currentWidget().windowTitle()

                if (class_name == 'StdTabEdit'):
                    work_path = self.tabWidget.currentWidget().filename
                    # print(work_path)

                    # print(c_file[6])
                    a = os.path.exists(work_path)
                    if a:
                        c_file = work_path.split("/")
                        if len(c_file) > 6:
                            # print(c_file)
                            if c_file[5] == "Projects":
                                stdinit.project_name = c_file[6]
                                stdinit.std_signal_gobal.std_work_space()
                        self.setWindowTitle("Stduino IDE " + stdinit.version_c + " [" + work_path + ']')  # 文件名设置
                        #self.savefileAction.setDisabled(not self.tabWidget.currentWidget().isModified())
                        self.forwardAction.setDisabled(not self.tabWidget.currentWidget().isRedoAvailable())
                        self.backAction.setDisabled(not self.tabWidget.currentWidget().isUndoAvailable())
                        # s1 = self.tabWidget.currentWidget().windowTitle()
                        self.textEdit = self.tabWidget.currentWidget()
                        # a = re.search('.ino', s1, re.I)
                    else:

                        if s1.startswith("Unnamed"):
                            pass
                        else:

                            ok = QMessageBox.warning(self, "File loss",
                                                     "文件丢失，是否保留该文件窗口?\n File is missing. Do you want to keep the file window?",
                                                     QMessageBox.Yes, QMessageBox.No)
                            if ok == QMessageBox.No:
                                self.close_Tab(self.tabWidget.currentIndex())

                        pass

                    # self.saveallAction.setDisabled(not self.tabWidget.currentWidget().isModified())
                else:

                    work_path = self.tabWidget.currentWidget().filename
                    if os.path.exists(work_path):
                        self.setWindowTitle("Stduino IDE " + stdinit.version_c + " [" + work_path + ']')  # 文件名设置
                        self.savefileAction.setDisabled(not self.tabWidget.currentWidget().isModified())
                        self.forwardAction.setDisabled(not self.tabWidget.currentWidget().isRedoAvailable())
                        self.backAction.setDisabled(not self.tabWidget.currentWidget().isUndoAvailable())
                    else:
                        if s1.startswith("Unnamed"):
                            pass
                        else:
                            ok = QMessageBox.warning(self, "File loss",
                                                     "文件丢失，是否保留该文件窗口?\n File is missing. Do you want to keep the file window?",
                                                     QMessageBox.Yes, QMessageBox.No)
                            if ok == QMessageBox.No:
                                self.close_Tab(self.tabWidget.currentIndex())

        except:
            stdinit.std_signal_gobal.stdprintln()



    def Find(self):
        try:


            stdinit.Std_Find.show()#2021111注释

        except:
            stdinit.std_signal_gobal.stdprintln()
    def libui_c(self,id):
        try:
            if id == 1:
                self.Load_lib.setEnabled(True)
            elif id == 2:
                self.platform.setEnabled(True)
            elif id == 3:
                self.package.setEnabled(True)
            elif id == 4:
                self.project_example.setEnabled(True)

            else:
                pass
            self.m_stackedLayout.setCurrentIndex(0)
        except:
            stdinit.std_signal_gobal.stdprintln()




    def add_lib_thread(self):
        self.addlib_json.libr_load()

    def AddLibs(self):
        try:
            t1 = threading.Thread(target=self.add_lib_thread, name='add_lib_thread')
            t1.setDaemon(True)
            t1.start()  # File_tree_init

            self.m_stackedLayout.setCurrentIndex(1)
            self.Load_lib.setEnabled(False)
            self.project_example.setEnabled(True)
            self.platform.setEnabled(True)
            self.package.setEnabled(True)
        except:
            stdinit.std_signal_gobal.stdprintln()
        # Addlibrary=childWindow3()
    def lplatforms_thread(self):
        self.addPlatform.libr_load()
    def Platforms(self):
        try:
            t1 = threading.Thread(target=self.lplatforms_thread, name='lplatforms_thread')
            t1.setDaemon(True)
            t1.start()  # File_tree_init

            self.m_stackedLayout.setCurrentIndex(3)
            self.platform.setEnabled(False)
            self.project_example.setEnabled(True)
            self.package.setEnabled(True)
            self.Load_lib.setEnabled(True)
        except:
            stdinit.std_signal_gobal.stdprintln()
    def lpackages_thread(self):
        self.addPackage.libr_load()
    def Packages(self):
        try:
            t1 = threading.Thread(target=self.lpackages_thread, name='lpackages_thread')
            t1.setDaemon(True)
            t1.start()  # File_tree_init

            self.m_stackedLayout.setCurrentIndex(2)
            self.package.setEnabled(False)
            self.project_example.setEnabled(True)
            self.platform.setEnabled(True)
            self.Load_lib.setEnabled(True)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def Tofind_all(self, id, changetext, findtext, qfind):#待完善 多线程处理 当前涉及ui 所以会崩溃
        try:
            num = 0
            find = 0
            id = int(id)
            if qfind == "True":
                qfind = False
            else:
                qfind = True


            # if qfind:  # 完全匹配
            #     qfind = False
            # else:
            #     qfind = True

            if id == 0:
                find = self.textEdit.findFirst(findtext, qfind, True, True, True)
                if find:
                    # print(find)
                    pass
                else:
                    self.listwidget.setText(reso.find_text_none)

            elif id == 1:

                if (self.textEdit.selectedText()):

                    self.textEdit.replaceSelectedText(changetext)
                else:
                    find = self.textEdit.findFirst(findtext, qfind, True, True, True)
                    if find:
                        self.textEdit.replaceSelectedText(changetext)
                        # self.tabWidget.currentWidget().findFirst(changetext, qfind, True, True, True)
                    else:

                        self.listwidget.setText(reso.change_text_none)


            elif id == 2:
                # find = self.__editor.findFirst(findtext, qfind, True, True, True)
                while self.tabWidget.currentWidget().findFirst(findtext, qfind, True, True, True):
                    self.tabWidget.currentWidget().replaceSelectedText(changetext)

                    num = num + 1
                self.listwidget.setText(reso.change_text_num + str(num))
        except:
            stdinit.std_signal_gobal.stdprintln()

    def Tofind(self, id, changetext, findtext, qfind):
        try:
            num = 0
            find = 0
            # id = int(id)
            # if qfind == "True":
            #     qfind = False
            # else:
            #     qfind = True


            if qfind:  # 完全匹配
                qfind = False
            else:
                qfind = True

            if id == 0:
                find = self.textEdit.findFirst(findtext, qfind, True, True, True)
                if find:
                    # print(find)
                    pass
                else:
                    self.listwidget.setText(reso.find_text_none)

            elif id == 1:

                if (self.textEdit.selectedText()):

                    self.textEdit.replaceSelectedText(changetext)
                else:
                    find = self.textEdit.findFirst(findtext, qfind, True, True, True)
                    if find:
                        self.textEdit.replaceSelectedText(changetext)
                        # self.tabWidget.currentWidget().findFirst(changetext, qfind, True, True, True)
                    else:

                        self.listwidget.setText(reso.change_text_none)


            elif id == 2:
                # find = self.__editor.findFirst(findtext, qfind, True, True, True)
                while self.tabWidget.currentWidget().findFirst(findtext, qfind, True, True, True):
                    self.tabWidget.currentWidget().replaceSelectedText(changetext)

                    num = num + 1
                self.listwidget.setText(reso.change_text_num + str(num))
        except:
            stdinit.std_signal_gobal.stdprintln()

        # try:
        #     pass
        #     # print(id)
        #     # print(type(id))
        #     #
        #     # print(changetext)
        #     # print(type(changetext))
        #     # print(findtext)
        #     # print(type(findtext))
        #     # print(qfind)
        #     # print(type(qfind))
        #
        # except:
        #     stdinit.std_signal_gobal.stdprintln()
        # return 0
        # try:
        #     t1 = threading.Thread(target=self.Tofind_all, name='Tofind_thread',args=(str(id), changetext, findtext, str(qfind), ))
        #     t1.setDaemon(True)
        #     t1.start()  # File_tree_init
        #     print(1212)
        # except:
        #     stdinit.std_signal_gobal.stdprintln()


    def undo1(self):
        try:
            self.tabWidget.currentWidget().undo()
        except:
            stdinit.std_signal_gobal.stdprintln()


    def redo1(self):
        try:
            self.tabWidget.currentWidget().redo()
            self.tabWidget.currentWidget()
        except:
            stdinit.std_signal_gobal.stdprintln()

        # TabEdit.delete

    def mail(self):
        try:

            try:
                my_sender = 'sam9661@qq.com'  # 发件人邮箱账号sam9661@qq.com  stduino@foxmail.com
                my_pass = 'jrtuhtpsukpocjii'  # 发件人邮箱密码   squxhquxrlalbaae
                my_user = 'service001@stduino.com'  # 收件人邮箱账号，我这边发送给自己
                ret = True
                msg = MIMEText('欢迎您的使用！', 'plain', 'utf-8')
                msg['From'] = formataddr(["FromStduino", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
                msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
                msg['Subject'] = "Stduino 团队测试"  # 邮件的主题，也可以说是标题
                server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
                server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
                server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
                server.quit()  # 关闭连接
            except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
                stdinit.std_signal_gobal.stdprintln()
                ret = False

            if ret:
                self.listwidget.setText(reso.mail_sended)
            else:
                self.listwidget.setText(reso.mail_send_failed)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def changemsg2(self, event):
        try:
            self.language1.setChecked(False)
            self.language2.setChecked(False)
            self.language3.setChecked(False)
            self.language4.setChecked(False)
            self.language5.setChecked(False)
            self.language6.setChecked(False)
            self.language7.setChecked(False)
            self.language8.setChecked(False)
            self.language9.setChecked(False)

            if event == '1':
                self.status1.setText("中文")
                self.language1.setChecked(True)
            elif event == '2':
                self.status1.setText('English')
                self.language2.setChecked(True)
            elif event == 'python3':
                self.status1.setText('русский язык')
                self.language3.setChecked(True)
            elif event == '4':
                self.status1.setText('Deutsch')
                self.language4.setChecked(True)
            elif event == '5':
                self.status1.setText('わご')
                self.language5.setChecked(True)
            elif event == '6':
                self.status1.setText('한어')
                self.language6.setChecked(True)
            elif event == '7':
                self.status1.setText('español')
                self.language7.setChecked(True)
            elif event == '8':
                self.status1.setText('français')
                self.language8.setChecked(True)
            elif event == '9':
                self.status1.setText('العربية')
                self.language9.setChecked(True)
        except:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            stdinit.std_signal_gobal.stdprintln()


    def changemsg(self, event):
        try:
            reply = QMessageBox.question(self, 'Tip', reso.restart_effect,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.changemsg2(event)
                setup.changemsg(event)
                pass

                # event.accept()
            else:
                if event == '1':
                    self.language1.setChecked(False)
                elif event == '2':
                    self.language2.setChecked(False)
                elif event == 'python3':
                    self.language3.setChecked(False)
                elif event == '4':
                    self.language4.setChecked(False)
                elif event == '5':
                    self.language5.setChecked(False)
                elif event == '6':
                    self.language6.setChecked(False)
                elif event == '7':
                    self.language7.setChecked(False)
                elif event == '8':
                    self.language8.setChecked(False)
                elif event == '9':
                    self.language9.setChecked(False)
                # event.ignore()
        except:
            stdinit.std_signal_gobal.stdprintln()




    def std_make_enable(self,id):
        try:
            if id == 0:
                self.complexAction.setDisabled(False)
                self.uploadAction.setDisabled(False)
                self.upload_fast_Action.setDisabled(False)
                self.cleanAction.setDisabled(False)
            else:
                self.wcombo.clear()
                if len(stdinit.device) > 0:
                    for i in stdinit.device:
                        self.wcombo.addItem(i["port"])
                    self.status2.setText(stdinit.current_upload_m + ":"+stdinit.device[0]["port"])
                else:
                    self.wcombo.addItem("None")

                pass
        except:
            stdinit.std_signal_gobal.stdprintln()



    def make_load(self,id):
        try:

            if id == "1":
                self.fileSave()
                stdinit.Std_Make.std_run()
            elif id == "2":
                self.fileSave()
                if stdinit.current_upload_m=="serial" and self.wcombo.currentText()=="None":
                    stdinit.Std_Make.std_device_list()
                stdinit.std_signal_gobal.std_upload_Close_check()
                stdinit.Std_Make.std_upload()

                #self.Std_Make.std_device_list()
            elif id == "python3":
                self.fileSave()
                if stdinit.current_upload_m=="serial" and self.wcombo.currentText()=="None":
                    stdinit.Std_Make.std_device_list()
                stdinit.std_signal_gobal.std_upload_Close_check()
                stdinit.Std_Make.std_upload_fast()


            elif id == "4":
                stdinit.Std_Make.std_clean()
            elif id == "5":

                stdinit.Std_Make.std_device_list()
        except:
            stdinit.std_signal_gobal.stdprintln()



    def make(self):
        try:

            if stdinit.init_path==None:
                stdinit.std_signal_gobal.std_echo_msg(0,"请先构建或双击激活一个已存在的工作空间(Projects下的项目文件)！")
                return 0
            self.complexAction.setDisabled(True)
            self.uploadAction.setDisabled(True)
            self.upload_fast_Action.setDisabled(True)
            self.cleanAction.setDisabled(True)
            if os.path.exists(stdinit.init_path):
                stdinit.pro_conf.clear()
                stdinit.pro_conf.read(stdinit.init_path, encoding="utf-8")  # python3
                it = []
                try:
                    ii = len(stdinit.pro_conf.sections())

                    if ii > 0:
                        for i in range(ii):
                            if "env:" in stdinit.pro_conf.sections()[i]:
                                it.append(stdinit.pro_conf.sections()[i].replace("env:", ""))

                        if len(it) > 1:
                            stdinit.Std_makeboards.cb.clear()
                            stdinit.Std_makeboards.cb.addItems(it)
                            stdinit.Std_makeboards.make_sec=1
                            self.fileSave()
                            stdinit.Std_makeboards.show()

                        else:
                            stdinit.std_make_board=None
                            t1 = threading.Thread(target=self.make_load, name='li_load1', args=("1",))
                            t1.setDaemon(True)
                            t1.start()
                    else:
                        stdinit.std_make_board = None
                        t1 = threading.Thread(target=self.make_load, name='li_load1', args=("1",))
                        t1.setDaemon(True)
                        t1.start()
                except:
                    stdinit.std_signal_gobal.stdprintln()
                    return 0
            else:
                stdinit.std_signal_gobal.std_echo_msg(0,"请先构建或双击激活一个已存在的工作空间(Projects下的项目文件)！")



        except:
            stdinit.std_signal_gobal.stdprintln()




    def make_clean(self):
        try:



            if stdinit.init_path==None:
                stdinit.std_signal_gobal.std_echo_msg(0,"请先构建或双击激活一个已存在的工作空间(Projects下的项目文件)！")
                return 0
            self.complexAction.setDisabled(True)
            self.uploadAction.setDisabled(True)
            self.upload_fast_Action.setDisabled(True)
            self.cleanAction.setDisabled(True)
            if os.path.exists(stdinit.init_path):
                stdinit.pro_conf.clear()
                stdinit.pro_conf.read(stdinit.init_path, encoding="utf-8")  # python3
                it = []
                try:
                    ii = len(stdinit.pro_conf.sections())

                    if ii > 0:
                        for i in range(ii):
                            if "env:" in stdinit.pro_conf.sections()[i]:
                                it.append(stdinit.pro_conf.sections()[i].replace("env:", ""))

                        if len(it) > 1:
                            stdinit.Std_makeboards.cb.clear()
                            stdinit.Std_makeboards.cb.addItems(it)
                            stdinit.Std_makeboards.make_sec = 4
                            stdinit.Std_makeboards.show()

                        else:
                            stdinit.std_make_board = None
                            t1 = threading.Thread(target=self.make_load, name='li_load1', args=("1",))
                            t1.setDaemon(True)
                            t1.start()
                    else:
                        stdinit.std_make_board = None
                        t1 = threading.Thread(target=self.make_load, name='li_load1', args=("1",))
                        t1.setDaemon(True)
                        t1.start()
                except:
                    stdinit.std_signal_gobal.stdprintln()
                    return 0
            else:
                stdinit.std_signal_gobal.std_echo_msg(0,"请先构建或双击激活一个已存在的工作空间(Projects下的项目文件)！")
            # self.complexAction.setDisabled(True)
            # self.uploadAction.setDisabled(True)
            # self.upload_fast_Action.setDisabled(True)
            # self.cleanAction.setDisabled(True)
            # t1 = threading.Thread(target=self.make_load, name='li_load1',args=("4",))
            # t1.setDaemon(True)
            # t1.start()
        except:
            stdinit.std_signal_gobal.stdprintln()

    def upload(self):
        try:


            if stdinit.init_path == None:
                stdinit.std_signal_gobal.std_echo_msg(0,"请先构建或双击激活一个已存在的工作空间(Projects下的项目文件)！")
                return 0
            self.complexAction.setDisabled(True)
            self.uploadAction.setDisabled(True)
            self.upload_fast_Action.setDisabled(True)
            self.cleanAction.setDisabled(True)
            if os.path.exists(stdinit.init_path):
                stdinit.pro_conf.clear()
                stdinit.pro_conf.read(stdinit.init_path, encoding="utf-8")  # python3
                it = []
                try:
                    ii = len(stdinit.pro_conf.sections())

                    if ii > 0:
                        for i in range(ii):
                            if "env:" in stdinit.pro_conf.sections()[i]:
                                it.append(stdinit.pro_conf.sections()[i].replace("env:", ""))

                        if len(it) > 1:
                            stdinit.Std_makeboards.cb.clear()
                            stdinit.Std_makeboards.cb.addItems(it)
                            stdinit.Std_makeboards.make_sec = 2
                            self.fileSave()
                            stdinit.Std_makeboards.show()

                        else:
                            stdinit.std_make_board = None
                            t1 = threading.Thread(target=self.make_load, name='li_load1', args=("2",))
                            t1.setDaemon(True)
                            t1.start()
                    else:
                        stdinit.std_make_board = None
                        t1 = threading.Thread(target=self.make_load, name='li_load1', args=("2",))
                        t1.setDaemon(True)
                        t1.start()
                except:
                    stdinit.std_signal_gobal.stdprintln()
                    return 0
            else:
                stdinit.std_signal_gobal.std_echo_msg(1,"请先构建或双击激活一个已存在的工作空间(Projects下的项目文件)！")
        except:
            stdinit.std_signal_gobal.stdprintln()


    def uploadfast(self):
        try:
            if stdinit.init_path == None:
                stdinit.std_signal_gobal.std_echo_msg(0,"请先构建或双击激活一个已存在的工作空间(Projects下的项目文件)！")
                return 0
            self.complexAction.setDisabled(True)
            self.uploadAction.setDisabled(True)
            self.upload_fast_Action.setDisabled(True)
            self.cleanAction.setDisabled(True)
            if os.path.exists(stdinit.init_path):
                stdinit.pro_conf.clear()
                stdinit.pro_conf.read(stdinit.init_path, encoding="utf-8")  # python3
                it = []
                try:
                    ii = len(stdinit.pro_conf.sections())

                    if ii > 0:
                        for i in range(ii):
                            if "env:" in stdinit.pro_conf.sections()[i]:
                                it.append(stdinit.pro_conf.sections()[i].replace("env:", ""))

                        if len(it) > 1:
                            stdinit.Std_makeboards.cb.clear()
                            stdinit.Std_makeboards.cb.addItems(it)
                            stdinit.Std_makeboards.make_sec = 3
                            self.fileSave()
                            stdinit.Std_makeboards.show()

                        else:
                            stdinit.std_make_board = None
                            t1 = threading.Thread(target=self.make_load, name='li_load1', args=("python3",))
                            t1.setDaemon(True)
                            t1.start()
                    else:
                        stdinit.std_make_board = None
                        t1 = threading.Thread(target=self.make_load, name='li_load1', args=("python3",))
                        t1.setDaemon(True)
                        t1.start()

                except:
                    stdinit.std_signal_gobal.stdprintln()
                    return 0
            else:
                stdinit.std_signal_gobal.std_echo_msg(0,"请先构建或双击激活一个已存在的工作空间(Projects下的项目文件)！")
        except:
            stdinit.std_signal_gobal.stdprintln()
    def load_device(self):
        try:
            t1 = threading.Thread(target=self.make_load, name='li_load1',args=("5",))
            t1.setDaemon(True)
            t1.start()
        except:
            stdinit.std_signal_gobal.stdprintln()


    def EditorShow(self, st):
        try:
            self.tabWidget.currentWidget().setText(st)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def std_process(self, staus,text):
        try:
            self.pb1_2.setText(text)
            if staus == 1:
                if self.pb12.isVisible():
                    pass
                else:
                    self.pb1_2.setVisible(True)
                    self.pb12.setVisible(True)
            else:
                if self.pb12.isVisible():
                    self.pb12.setVisible(False)
                    self.pb1_2.setVisible(False)


        except:
            stdinit.std_signal_gobal.stdprintln()

    def toggleMenu(self):
        try:
            text = stdinit.find_boards.get_board_num()
            self.status2.setText(text + reso.on + self.wcombo.currentText() + reso.download_type_1 + 'USB_ISP')
        except:
            stdinit.std_signal_gobal.stdprintln()



    def toggleMenu2(self):
        try:

            text = self.find_boards.get_board_num()

            self.port_check1()
            self.status2.setText(text + reso.on + self.wcombo.currentText() + reso.download_type_1 + 'USB_ISP')
        except:
            stdinit.std_signal_gobal.stdprintln()

        # print(212)###改这里

        # self.wcombo.clear()
        # if(state!=False):
        #    self.wcombo.setCurrentText(state)
        #    self.status2.setText(
        #    self.combo.currentText() + reso.on + self.wcombo.currentText() + reso.download_type_1 + 'USB_ISP')


    def toggleMenu4(self):
        pass



        # self.status2.setText(self.combo.currentText() + reso.on + self.wcombo.currentText() + reso.download_type_1 + 'USB_ISP')

        #self.status2.setText(text + reso.on + self.wcombo.currentText() + reso.download_type_1 + upload_me)

        # self.port_check1()

    # def set_gbk_utf(self, state):
    #     global gbk_utf_type
    #     gbk_utf_type = state
    #     setup.gbk_type(state)
    #     self.gbk_status.setText(state)
    #     try:
    #         if state == "GBK":
    #             self.set_gbk.setChecked(True)
    #             self.set_utf_8.setChecked(False)
    #         else:
    #             self.set_gbk.setChecked(False)
    #             self.set_utf_8.setChecked(True)
    #         strr = "DCODE=" + state
    #         pos = os.path.abspath('.')
    #         # makefile change
    #         filename = pos + "\\tool\msy\gbk.conf"
    #         fo = open(filename, "w", encoding='UTF-8')
    #         # strr = self.__editor.text()
    #         # 在文件末尾写入一行self.combo.currentText()
    #         fo.write(strr)
    #         # 关闭文件
    #         fo.close()
    #     except:
    #         QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdmainui0092！\n You can search it in stduino.com",
    #                             QMessageBox.Yes)
    #         pass
    #
    #     pass

    def toggleMenu3(self, state):
        try:
            text = self.find_boards.get_board_num()
            if state == 0:

                self.usblink.setChecked(True)
                self.stlink.setChecked(False)
                self.wcombo.setEnabled(True)
                self.serialFind.setEnabled(True)
                self.port_check1()
                # self.lbw.setText('选择下载端口')

                # self.wcombo.clear()

                # self.toolbar2.setVisible(True)############
                # self.lbw.setVisible(True)
                # self.wcombo.setVisible(True)
                # self.serialFind.setVisible(True)
                # print(self.serialFind.isVisible())
                # self.wcombo.setHidden(False)
                # self.serialFind.setHidden(False)

                self.status2.setText(
                    text + reso.on + self.wcombo.currentText() + reso.download_type_1 + 'USB_ISP')
                pass
            else:

                self.usblink.setChecked(False)

                self.stlink.setChecked(True)
                self.wcombo.setEnabled(False)
                self.serialFind.setEnabled(False)
                # self.wcombo.clear()
                # self.lbw.clear()
                # self.toolbar2.setVisible(False)###############
                # self.lbw.setVisible(False)
                # self.serialFind.setHidden(True)
                # self.wcombo.setVisible(False)
                # self.serialFind.setVisible(False)
                # self.wcombo.setHidden(True)
                # self.serialFind.setHidden(True)
                # print(self.serialFind.isVisible())

                self.status2.setText(text + reso.download_type_1 + 'St_link')
                pass
        except:
            stdinit.std_signal_gobal.stdprintln()


    def port_check1(self):
        try:
            port_list = list(serial.tools.list_ports.comports())
            QApplication.processEvents()
            if len(port_list) == 0:
                self.wcombo.clear()
                self.wcombo.addItem(reso.serial_port)

                pass
            else:
                sd = self.wcombo.currentText()
                self.wcombo.clear()

                for port in port_list:
                    # print(port)
                    self.wcombo.addItem(port[0])
                self.wcombo.setCurrentText(sd)
        except:
            stdinit.std_signal_gobal.stdprintln()



        # print(12)
        # 检测所有存在的串口，将信息存储在字典中



            # print(port[0])
            # print(len(self.Com_Dict))
        # self.Com_Dict = port_list

    # if len(port_list) != len(self.Com_Dict):
    #     print(13)
    #
    #
    #
    #
    #
    # elif len(port_list) == 0:
    #     print(12)
    #     self.wcombo.clear()
    #     self.wcombo.addItem(res.check_port)
    #     Serialport = 0
    #     pass
    # 串口检测

    # 串口信息
    # def port_imf1(self):
    #     try:
    #         imf_s = self.s1__box_2.currentText()
    #         if imf_s != "":
    #             self.state_label.setText(self.Com_Dict[self.s1__box_2.currentText()])
    #     except:
    #         stdinit.std_signal_gobal.stdprintln()
        # 显示选定的串口的详细信息


    # 打开串口
    def port_open1(self):

        if self.seri.isOpen():
            pass
        else:

            self.seri.port = self.wcombo.currentText()
            self.seri.baudrate = 9600
            self.seri.bytesize = 8
            self.seri.stopbits = 1
            self.seri.parity = "N"
            # self.ser.xonxoff=False
            # xonxoff = 0,  # enable software flow control
            # rtscts = 0,  # enable RTS/CTS flow control
            try:
                pass
                self.seri.open()
                # self.ser.rtscts()
            except:
                stdinit.std_signal_gobal.stdprintln()
                return False
            # 打开串口接收定时器，周期为2ms
            # self.timer.start(2)

            # self.open_button.setEnabled(False)
            # self.close_button.setEnabled(True)
            # print("串口状态（已开启）")
            # self.formGroupBox1.setTitle("串口状态（已开启）")

    # 关闭串口
    def port_close1(self):
        try:
            if self.seri.isOpen():
                try:
                    self.seri.close()
                except:
                    stdinit.std_signal_gobal.stdprintln()
                    return False
                    pass

        except:
            stdinit.std_signal_gobal.stdprintln()

    # rts脚
    def dtrrst(self):
        try:
            Error = self.port_open1()
            if Error == False:
                return False
            self.seri.rts = True
            self.seri.dtr = True
            self.seri.dtr = False
            time.sleep(0.01)
            self.seri.dtr = True
            time.sleep(0.01)
            self.seri.rts = False
            time.sleep(0.01)
            Error = self.port_close1()
            if Error == False:
                return False
        except:
            stdinit.std_signal_gobal.stdprintln()
            return False
            pass

    # dtr脚
    def rst(self):
        try:
            Error = self.port_open1()
            if Error == False:
                return False
            self.seri.rts = True
            self.seri.dtr = True
            self.seri.dtr = False
            time.sleep(0.01)
            self.seri.rts = False
            time.sleep(0.01)
            self.seri.dtr = True
            time.sleep(0.01)
            self.seri.rts = True
            self.seri.rts = False
            time.sleep(0.01)
            Error = self.port_close1()
            if Error == False:
                return False
        except:
            stdinit.std_signal_gobal.stdprintln()
            return False

    def startsetcolor(self):  # startsetcolor
        # self.__lexer.setColor(QColor("#66CDAA"), QsciLexerCPP.CommentLine)  # 注释 #66CDAA  #1C1C1C  黑
        try:
            stdinit.Set_Back_Color1.show()#2021111注释
        except:
            stdinit.std_signal_gobal.stdprintln()

    def setcolor_all(self, str, id):  # startsetcolor


        # self.__lexer.setColor(QColor("#66CDAA"), QsciLexerCPP.CommentLine)  # 注释 #66CDAA  #1C1C1C  黑
        try:
            self.textEdit.setStyleSheet(*{"background:rgb(56,56,56)"})  ####调试框颜色
            # self.__lexer.setDefaultFont(QFont( "Times", 12 ))  # 字体大小及样式
            # self.__lexer.setFont(str)  # 字体大小及样式
            if id == 1:  # 编辑框背景颜色
                setup.save_mstyle(str)
                # self.__frm.setStyleSheet('QWidget{background-color:%s}' % str) #setStyleSheet('QWidget{background-color:%s}' % color.name() #边框
                self.textEdit.lexer().setDefaultPaper(QColor(str))  # 背景  #363636  95%背景颜色

                # self.textEdit.setStyleSheet("background:"+str+";")
                self.textEdit.lexer().setPaper(QColor(str), 0)  # Style 0: #363636  python3% 空格背景颜色
                self.textEdit.lexer().setPaper(QColor(str), 1)  # Style 0: #363636  python3% 空格背景颜色
                self.textEdit.lexer().setPaper(QColor(str), 3)  # Style 0: #363636  python3% 空格背景颜色
                self.textEdit.lexer().setPaper(QColor(str), 2)  # Style 2: #363636  python3% 空格背景颜色
                self.textEdit.lexer().setPaper(QColor(str), 4)  # Style 2: #363636  python3% 空格背景颜色
                self.textEdit.lexer().setPaper(QColor(str), 5)  # Style 2: #363636  python3% 空格背景颜色
                self.textEdit.lexer().setPaper(QColor(str), 6)  # Style 2: #363636  python3% 空格背景颜色
                # self.textEdit.lexer().setColor(QColor(str), 0)  # Style python3: green
                # self.textEdit.lexer().setColor(QColor(str), 1)  # Style python3: green

            # 1.编辑栏背景 2.正常文字背景 python3.注释背景颜色 4.主关键字背景 5.函数关键字背景 6.括号背景

            elif id == 2:  # 正常文字背景颜色
                setup.save_tstyle(str)
                self.textEdit.setDefaultColor(QColor(str))  # 正文字背景  #363636
            elif id == 3:  # 注释背景颜色
                setup.save_cstyle(str)
                try:
                    # self.textEdit.lexer().setColor(QColor(str), QsciLexerCPP.CommentLine)  # 注释 #66CDAA  #1C1C1C  黑 # font-style:itelic;
                    self.textEdit.lexer().setColor(QColor(str), 2)  # Style python3: green#单条注释背景
                    self.textEdit.lexer().setColor(QColor(str), 3)  # Style python3: green多条注释背景


                except:
                    stdinit.std_signal_gobal.stdprintln()
                # print("Unexpected error:", sys.exc_info()[1])
            elif id == 4:  # 4.主关键字背景
                setup.save_4style(str)
                self.textEdit.lexer().setColor(QColor(str), QsciLexerCPP.Keyword)  # 7B68EE
                pass
            elif id == 5:  # 5.函数关键字背景
                setup.save_5style(str)
                self.textEdit.lexer().setColor(QColor(str), QsciLexerCPP.KeywordSet2)  # 008B45
                pass

            elif id == 6:  # 6.括号背景
                setup.save_6style(str)
                self.textEdit.lexer().setColor(QColor(str), QsciLexerCPP.Operator)  # 分号及括号颜色
                pass
            elif id == 7:  # 7.汉字背景  4  9 19
                setup.save_7style(str)
                self.textEdit.lexer().setColor(QColor(str), 6)  # 分号及括号颜色
                pass
            elif id == 8:  # .数字背景  4  9 19
                setup.save_8style(str)
                self.textEdit.lexer().setColor(QColor(str), 4)  # 分号及括号颜色
                pass
            else:  # 9.预编译背景   9 19
                setup.save_9style(str)
                self.textEdit.lexer().setColor(QColor(str), 19)  # 分号及括号颜色
                self.textEdit.lexer().setColor(QColor(str), 9)  # 分号及括号颜色
                pass
            # self.__lexer.setColor(QColor(str), QsciLexerCPP.CommentLine)  # 注释 #66CDAA  #1C1C1C  黑
        except:
            stdinit.std_signal_gobal.stdprintln()

            # self.lbl.setStyleSheet("background-color:#32414b;border-bottom : 1px solid #19232D;")  # 需设置跟随主题背景
            #
            # self.serialFind.setStyleSheet("background-color:#708090;")  ########## 串口查找按钮
            # self.lbw.setStyleSheet("background-color:#32414b;border-bottom : 1px solid #19232D;")  # 需设置跟随主题背景
            # self.setStyleSheet("* {color:rgb(181,181,162);background-color:rgb(37,37,38)}")  # 主题框架背景
            # tab_str_css = "QTabBar::close-button {image: url(appearance/img/img_close2.png)}" + \
            #               "QTabBar::close-button:selected {image: url(appearance/img/img_close.png)}" + \
            #               "QTabBar::tab {background-color:rgb(45,45,45);padding:3px;border: 2px;}" \
            #               "QTabBar::tab:!selected {margin-top: 5px;color:rgb(150,150,150);}" \
            #               "QTabBar::tab:selected {color:rgb(255,255,255);background-color:rgb(30,30,30);}" + \
            #               "QTabBar::tab:hover{background:rgb(10, 10, 10,50);}"
            #
            # self.tabWidget.setStyleSheet(tab_str_css)  # TAB背景
            # #self.listwidget.setStyleSheet("background:#383838")  ####调试框颜色
            # self.right_to_left.setStyleSheet(
            #     "* { background:rgb(52,65,75) ;border-bottom : 1px solid #19232D;}")  # color: #32414B;
            # pass

    def start_debug(self):  # debug_sign
        try:
            self.project_staus = 2

            self.debug_Action.setDisabled(True)
            self.stackedLayout.setCurrentIndex(1)
            # self.project_Action.setIcon(QIcon(res.img_projects2))

            # self.splitter1.setSizes([2, 500])
            self.splitter1.setSizes([1, 1400])  # 板子发
        except:
            stdinit.std_signal_gobal.stdprintln()



    def start_find_b(self):
        try:
            self.find_b_Action.setDisabled(True)
            # self.debug_Action.setDisabled(False)
            stdinit.find_boards.load_boards()
            stdinit.find_boards.show()
        except:
            stdinit.std_signal_gobal.stdprintln()

    def lexample_thread(self):
        self.openExample.libr_load()
    def start_examples(self):
        try:

            t1 = threading.Thread(target=self.lexample_thread, name='lexample_thread')
            t1.setDaemon(True)
            t1.start()  # File_tree_init
            self.m_stackedLayout.setCurrentIndex(4)
            self.project_example.setEnabled(False)
            self.package.setEnabled(True)
            self.platform.setEnabled(True)
            self.Load_lib.setEnabled(True)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def start_project(self):
        try:
            self.debug_Action.setDisabled(False)

            # items = ["Spring", "Summer", "Fall", "Winter"]
            # value, ok = QInputDialog.getItem(self, "输入框标题", "这是提示信息\n\n请选择季节:", items, 1, True)
            # self.echo(value)
            if self.project_staus == 1:
                self.stackedLayout.setCurrentIndex(0)
                self.splitter1.setSizes([1, 1400])  # 板子发现
                self.project_Action.setIcon(QIcon(res.img_projects2))
                self.project_staus = 0
                # self.splitter1.setSizes([2, 500])
            # elif self.stackedLayout.currentIndex()!= 0 and project_staus == 0:
            #     self.stackedLayout.setCurrentIndex(0)
            elif self.project_staus == 2:
                self.stackedLayout.setCurrentIndex(0)
                self.project_staus = 0

            else:
                self.project_staus = 1

                self.stackedLayout.setCurrentIndex(0)
                self.project_Action.setIcon(QIcon(res.img_projects))
                # self.splitter1.setSizes([0, 500])
                self.splitter1.setSizes([0, 1400])  # 板子发现
        except:
            stdinit.std_signal_gobal.stdprintln()



    def startSerial(self):
        try:
            # app = QtWidgets.QApplication(sys.argv)
            # app = QApplication(sys.argv)
            if 0 not in stdinit.serialnumber:
                stdinit.Std_Serial_Tool1.show()  # 2021111注释
                stdinit.serialnumber.append(0)
            elif 1 not in stdinit.serialnumber:
                stdinit.Std_Serial_Tool2.show()  # 2021111注释
                stdinit.serialnumber.append(1)
        except:
            stdinit.std_signal_gobal.stdprintln()

        # self.append(myshow)
        # self.show()
        # myshow.show()
        # sys.exit(app.exec_())

    ''''''


''' End Class '''
