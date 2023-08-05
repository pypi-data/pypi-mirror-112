# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal,QObject
from function.cores.stdedit import stdinit
class StdEcho(QObject):
    std_echo_msg = pyqtSignal(int,str)  # 0 settext 1 appead 3process
    # def __init__(self):
    #     pass
        #print(self.abs_path)
        #self.pip_fast()

    def std_message(self,method):#all the time
        stdinit.std_signal_gobal.stdprintln()
    def std_echo(self,staus,msg):#all the time #staus 0 清空
        try:
            self.std_echo_msg.emit(staus, msg)  # 具体实现模仿sterminal的实现方式 绑定
        except:
            stdinit.std_signal_gobal.stdprintln()
