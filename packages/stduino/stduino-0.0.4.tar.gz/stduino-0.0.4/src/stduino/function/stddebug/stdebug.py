#from pygdbmi.gdbcontroller import GdbController
#gdbmi = GdbController("C:\stwork\\tool\\test32\packages\STM32\\tools\xpack-arm-none-eabi-gcc\9.2.1-1.1\\bin\arm-none-eabi-gdb.exe", [""]) #第一个参数指定gdb，第二个参数指定elf文件
# response = gdbmi.write('set mem inaccessible-by-default off')
# response = gdbmi.write('set arch riscv:rv32')
# response = gdbmi.write('target remote localhost:3333', 5) #5为timeout时间
# response = gdbmi.write('load', 6)

import subprocess
import os
#from pygdbmi.gdbcontroller import GdbController
import _thread
from function.cores.stdedit import stdinit
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

import sys
from PyQt5.QtCore import QStringListModel
import time
import re
global debug_staus2
debug_staus2=0
global debug_staus
debug_staus=0
global debug_staus_st
debug_staus_st=0


class StDebug(QWidget):
    debug_sig = pyqtSignal(int)  # 0 settext 1 appead 3process
    debug_return = pyqtSignal(str)  # 0 settext 1 appead 3process
    def __init__(self):
        super(StDebug, self).__init__()
        try:
            # self.setWindowOpacity(0.7)
            # self.setGeometry(50, 50, 50, 30)

            # self.setFixedSize(420, 220)
            self.setWindowTitle('StdDebug View')
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            stdinit.std_signal_gobal.gdb_cmd.connect(self.st_gdb_cmd)
            # self.setWindowIcon(QIcon("appearance/img/st.PNG"))

            # 全局布局（2中）：这里选择水平布局
            # wlayout = QHBoxLayout()
            wlayout = QVBoxLayout()

            # 局部布局：水平，垂直，网格，表单
            glayout = QGridLayout()

            self.de_start = QToolButton()  # 无背景
            self.de_start.clicked.connect(self.st_piodebug)
            self.de_start.setIcon(QIcon("./appearance/img/startup.png"))  # setIcon(QIcon("appearance/img/img_dot.png"))
            self.de_start.setToolTip("Start Debugging")

            self.de_continue = QToolButton()  # 无背景
            self.de_continue.clicked.connect(self.de_continue1)
            self.de_continue.setIcon(
                QIcon("./appearance/img/continue.png"))  # setIcon(QIcon("appearance/img/img_dot.png"))
            self.de_continue.setToolTip("Continue")
            self.de_continue.setDisabled(True)
            # de_pause = QToolButton()  # 无背景
            # de_pause.setIcon(QIcon("./appearance/img/pause.png"))  换图片
            self.debug_step_over = QToolButton()  # 无背景
            self.debug_step_over.clicked.connect(self.debug_step_over1)
            self.debug_step_over.setDisabled(True)

            self.debug_step_over.setIcon(QIcon("./appearance/img/debug_step_over.png"))
            self.debug_step_over.setToolTip("Step over")
            self.debug_step_into = QToolButton()  # 无背景
            self.debug_step_into.clicked.connect(self.debug_step_into1)
            self.debug_step_into.setDisabled(True)
            self.debug_step_into.setIcon(QIcon("./appearance/img/debug_step_into.png"))
            self.debug_step_into.setToolTip("Step into")
            self.debug_step_out = QToolButton()  # 无背景
            self.debug_step_out.setDisabled(True)
            self.debug_step_out.clicked.connect(self.debug_step_out1)
            self.debug_step_out.setIcon(QIcon("./appearance/img/debug_step_out.png"))
            self.debug_step_out.setToolTip("Step out")
            self.restart = QToolButton()  # 无背景
            self.restart.setDisabled(True)
            self.restart.clicked.connect(self.debug_restart1)
            self.restart.setIcon(QIcon("./appearance/img/restart.png"))
            self.restart.setToolTip("Restart")
            self.de_stop = QToolButton()  # 无背景
            self.de_stop.setDisabled(True)
            self.de_stop.clicked.connect(self.pio_de_stop2)
            self.de_stop.setIcon(QIcon("./appearance/img/stop.png"))
            self.de_stop.setToolTip("Stop")

            # 实例化列表视图
            listview = QListView()

            # 实例化列表模型，添加数据
            slm = QStringListModel()
            self.qList = ['gdb常用指令', 'b 函数名/行数', 'n/next', 'l/list', 'list 行号', 'list 函数名', 's/step', 'set var 变量名=值',
                          'bt(backtrace)', 'continue/c', 'whatis 变量名', 'info watchpoints', 'info breakpoints',
                          'info all-registers', 'd/delete', 'display var', 'wiki.stduino.com for detail']

            # 设置模型列表视图，加载数据列表
            slm.setStringList(self.qList)

            # 设置列表视图的模型
            listview.setModel(slm)

            glayout.addWidget(self.de_start, 0, 0)
            glayout.addWidget(self.de_continue, 1, 0)
            glayout.addWidget(self.debug_step_over, 1, 1)
            glayout.addWidget(self.debug_step_into, 1, 2)
            glayout.addWidget(self.debug_step_out, 1, 3)
            glayout.addWidget(self.restart, 1, 4)
            glayout.addWidget(self.de_stop, 1, 5)
            # 准备四个控件
            gwg = QWidget()
            # 使用四个控件设置局部布局
            gwg.setLayout(glayout)
            # 将四个控件添加到全局布局中
            wlayout.addWidget(gwg)
            wlayout.addWidget(listview)

            self.setLayout(wlayout)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def startgdbserver(self,threadName, delay):
        try:
            global debug_staus
            global debug_staus_st

            pos = os.path.abspath('.')
            path = pos + "\\tool\Servers\STM32CubeProgrammer\\binst"
            os.chdir(path)  # 通过更改当前运行目录F:\BaiduNetdiskDownload\stpython\stdemo\main
            cmd = "ST-LINK_CLI -c -P"
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            os.chdir(pos)
            i = 0
            for line in iter(proc.stdout.readline, b''):
                try:
                    s1 = str(line, encoding='utf-8')
                except:
                    pass
                a = re.search('Unable', s1)
                if a == None:
                    pass
                else:
                    QMessageBox.warning(self, "Can't DEBUG", "Please check that your stlink is connected properly?",
                                        QMessageBox.Yes)
                    # self.debug_return.emit("Please check that your stlink is connected properly?")
                    debug_staus = 1
                    return 1
            os.chdir(pos + "/tool/Servers/ST-LINK_gdbserver")
            cmd = "ST-LINK_gdbserver -e -p 61237 -r 15 -d"
            self.proc_server = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            os.chdir(pos)
            debug_staus = 0
            for line in iter(self.proc_server.stdout.readline, b''):
                pass
                s1 = str(line, encoding='gbk')
                # print(s1)
                if "Waiting for connection" in s1:
                    debug_staus_st = 1
                else:
                    debug_staus_st = 0

                # else:
                #     QMessageBox.warning(self, "Can't DEBUG", "ST-LINK: Could not verify ST device! Abort connection",
                #                         QMessageBox.Yes)
                # print(s1)
            #         pass
            # self.startgdb("st",1)
            return 0
        except:
            stdinit.std_signal_gobal.stdprintln()



    def st_gdb_cmd(self,cmd):

        try:

            if not cmd.endswith("\n"):
                cmd = cmd + "\n"
            self.proc.stdin.write(cmd.encode())
            self.proc.stdin.flush()
            if cmd == "quit\n" or cmd == "q\n":
            #if cmd == "y\n":
                self.debug_sig.emit(1)  #指令发送进行关闭时触发
                self.proc.terminate()
                self.pio_de_stop1()
                time.sleep(1)
            if cmd == "machinequit\n":
                self.proc.terminate()
                self.pio_de_stop1()

                #os.popen('taskkill /IM ST-LINK_gdbserver.exe /F')

        except:
            stdinit.std_signal_gobal.stdprintln()

    def startgdb(self,threadName, delay):
        try:
            # self.thread.trigger.connect(self.ListShow)
            pos = os.path.abspath('.')  # C:/stwork/stdemo2019827/tool/gcc/bin/arm-none-eabi-gdb.exe C:/stwork/stdemo2019827/tool/test/bin/test.elf
            cmd = pos + "/tool/gcc/bin/arm-none-eabi-gdb.exe " + pos + "/tool/test/bin/test.elf --quiet"

            # cmd = "C:/stwork/stdemo2019827/tool/gcc/bin/arm-none-eabi-gdb.exe C:/stwork/stdemo2019827/tool/test/bin/test.elf --quiet"

            self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True,
                                         stdin=subprocess.PIPE)
            for line in iter(self.proc.stdout.readline, b''):
                s1 = str(line, encoding='gbk')
                if s1 == "":
                    pass
                elif "answered Y" in s1:
                    self.debug_return.emit("Successful execution!")
                else:
                    self.debug_return.emit(s1)
                    # print(s1)

            # self.gdbmi = GdbController("C:/stwork/stdemo2019827/tool/gcc/bin/arm-none-eabi-gdb.exe",["C:/stwork/stdemo2019827/tool/test/bin/test.elf"])  # 第一个参数指定gdb，第二个参数指定elf文件
            # #
            # print(self.gdbmi.get_subprocess_cmd())  # print actual command run as subprocess
            # response = self.gdbmi.write('target remote localhost:65539')  # 5为timeout时间
            # print(response)
            # response = self.gdbmi.write('load')
            # print(response)
            # response = self.gdbmi.write('b setup')
            # print(response)
            # response = self.gdbmi.write('b loop')
            # print(response)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def de_continue1(self):
        try:
            self.st_gdb_cmd('c\n')
            # response = self.gdbmi.write('c', 6)
            # print(response)
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()

    def debug_step_over1(self):
        try:
            self.st_gdb_cmd('n\n')
            # response = self.gdbmi.write('n', 6)
            # print(response)

        except:
            stdinit.std_signal_gobal.stdprintln()

    def debug_step_into1(self):
        try:
            self.st_gdb_cmd('s\n')
            # response = self.gdbmi.write('s', 6)
            # print(response)
            pass

        except:
            stdinit.std_signal_gobal.stdprintln()

    def debug_step_out1(self):
        try:
            self.st_gdb_cmd('finish\n')
            # response = self.gdbmi.write('finish', 6)
            # print(response)
            pass

        except:
            stdinit.std_signal_gobal.stdprintln()

    def debug_restart1(self):
        try:
            # self.st_gdb_cmd('finish')
            # response = self.gdbmi.write('fin', 6)
            # self.st_debug()
            # print(response)
            self.st_gdb_cmd('monitor reset\n')

        except:
            stdinit.std_signal_gobal.stdprintln()

    def pio_de_stop1(self):
        try:
            # response = self.gdbmi.write('quit', 6)
            # print(response)
            self.debug_step_out.setDisabled(True)
            self.debug_step_into.setDisabled(True)
            self.debug_step_over.setDisabled(True)
            self.de_continue.setDisabled(True)
            self.restart.setDisabled(True)
            self.de_stop.setDisabled(True)
            self.de_start.setDisabled(False)

        except:
            stdinit.std_signal_gobal.stdprintln()


    def pio_de_stop2(self):
        try:
            self.st_gdb_cmd('quit')
            self.de_start.setDisabled(False)
            self.debug_step_out.setDisabled(True)
            self.debug_step_into.setDisabled(True)
            self.debug_step_over.setDisabled(True)
            self.de_continue.setDisabled(True)
            self.restart.setDisabled(True)
            self.de_stop.setDisabled(True)


        except:
            stdinit.std_signal_gobal.stdprintln()

    def return_de_staus2(self,i):
        pass
    def gdb_init(self):
        try:
            cmd = "target remote localhost:61237\n"
            self.st_gdb_cmd(cmd)
            cmd = "load\n"
            self.st_gdb_cmd(cmd)
            cmd = "b setup\n"
            self.st_gdb_cmd(cmd)
            cmd = "b loop\n"
            self.st_gdb_cmd(cmd)
        except:
            stdinit.std_signal_gobal.stdprintln()


    #You can't do that
    def pio_cmd_init(self,cmd):
        try:
            cmd = "b setup\n"
            self.st_gdb_cmd(cmd)
            cmd = "b loop\n"
            self.st_gdb_cmd(cmd)
            cmd = "c\n"
            self.st_gdb_cmd(cmd)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def pio_de_start(self):
        try:
            self.de_start.setDisabled(True)
            self.debug_step_out.setDisabled(False)
            self.debug_step_into.setDisabled(False)
            self.debug_step_over.setDisabled(False)
            self.de_continue.setDisabled(False)
            self.restart.setDisabled(False)
            self.de_stop.setDisabled(False)
        except:
            stdinit.std_signal_gobal.stdprintln()



    def piodebug(self,t,tt):#stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio
        try:
            self.debug_sig.emit(0)  # 指令发送进行关闭时触发
            pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio" + '"'
            piogdb_path = pio_env+" debug -d " +'"' +  stdinit.projects_dir+ stdinit.project_name+ '"' + " --interface=gdb --interpreter mi -x .pioinit"#--interpreter mi
            self.proc = subprocess.Popen(piogdb_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True,
                                         stdin=subprocess.PIPE)
            for line in iter(self.proc.stdout.readline, b''):
                try:
                    s1 = str(line, encoding='utf-8')
                    self.debug_return.emit(s1)
                except:
                    print("debug:error")
            pass
        except:
            stdinit.std_signal_gobal.std_process(0, "DEBUG初始化失败")
            self.debug_return.emit("DEBUG初始化失败!")
            stdinit.std_signal_gobal.stdprintln()


    def st_piodebug(self):
        try:
            if stdinit.init_path == None:
                stdinit.std_signal_gobal.std_echo_msg(0, "请先构建或双击激活一个已存在的工作空间(Projects下的项目文件)！")
                return 0

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

                            stdinit.std_signal_gobal.std_echo_msg(0, "当前工作空间platformio.ini文件中存在多款芯片，请注释掉其他芯片后再进行Debug操作！")
                            return 0
                        else:

                            _thread.start_new_thread(self.piodebug, ("Thread-1", 1,))
                            self.pio_de_start()
                            stdinit.std_signal_gobal.std_process(1, "DEBUG初始化")
                    else:

                        _thread.start_new_thread(self.piodebug, ("Thread-1", 1,))
                        self.pio_de_start()
                        stdinit.std_signal_gobal.std_process(1, "DEBUG初始化")
                except:
                    stdinit.std_signal_gobal.stdprintln()
                    return 0
            else:
                stdinit.std_signal_gobal.std_echo_msg(0,"请先构建或双击激活一个已存在的工作空间(Projects下的项目文件)！")


        except:
            stdinit.std_signal_gobal.stdprintln()



    def st_debug1(self):
        try:
            global debug_staus2
            global debug_staus
            global debug_staus_st

            if debug_staus2 == 1:

                try:
                    _thread.start_new_thread(self.startgdbserver, ("Thread-1", 1,))
                    # s=self.startgdbserver("Thread-1", 1)
                    time.sleep(1)
                    # _thread.start_new_thread(self.startgdb, ("Thread-2", 2,))
                    # time.sleep(1)
                    # self.gdb_init()
                    # s=1
                    # self.debug_sig.emit(0)
                    if debug_staus == 1:
                        pass
                    else:
                        if debug_staus_st == 1:
                            self.debug_sig.emit(0)
                            _thread.start_new_thread(self.startgdb, ("Thread-2", 2,))
                            time.sleep(1)
                            self.gdb_init()
                            # self.startgdb("Thread-2", 4)
                            self.debug_step_out.setDisabled(False)
                            self.debug_step_into.setDisabled(False)
                            self.debug_step_over.setDisabled(False)
                            self.de_continue.setDisabled(False)
                            self.restart.setDisabled(False)
                            self.de_stop.setDisabled(False)
                            self.de_start.setDisabled(True)
                            pass
                        else:
                            self.de_stop2()
                            QMessageBox.warning(self, "Can't DEBUG",
                                                "ST-LINK: Could not verify ST device! Abort connection",
                                                QMessageBox.Yes)
                            pass

                    # time.sleep(1)

                except:
                    # print("Error: 无法启动线程")
                    stdinit.std_signal_gobal.stdprintln()
            else:
                QMessageBox.warning(self, "Can't DEBUG", "Please recompile with the optimition of DEBUG mode First!",
                                    QMessageBox.Yes)
        except:
            stdinit.std_signal_gobal.stdprintln()





# if __name__ == "__main__":
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     widget =StDebug()
#
#     widget.show()
#     sys.exit(app.exec_())