# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
__author__ = 'Su Jin Qiang'


#import zipfile  # 解压文件


from function.cores.stdedit import stdinit
from PyQt5.QtCore import pyqtSignal,QObject
from function.cores.stdmsg import reso
from function.piobuilder.piorun import PioRunManage

class Stdmake(QObject):

    def __init__(self):
        super(Stdmake, self).__init__()
        self.Pio_run = PioRunManage()
    def std_run(self):
        try:

            stdinit.std_signal_gobal.std_process(1, reso.complexing)  # complexing
            self.Pio_run.pio_run()
            stdinit.std_signal_gobal.std_process(0, reso.complex_complete)
            #self.make_signal.emit(0)
            stdinit.std_signal_gobal.std_make_signal(0)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def std_upload(self):
        try:
            stdinit.std_signal_gobal.std_process(1, reso.downloading)  # complexing
            self.Pio_run.pio_upload()
            stdinit.std_signal_gobal.std_process(0, reso.downloaded)
            stdinit.std_signal_gobal.std_make_signal(0)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def std_upload_fast(self):
        try:
            stdinit.std_signal_gobal.std_process(1, reso.downloading)  # complexing
            self.Pio_run.pio_upload()
            stdinit.std_signal_gobal.std_process(0, reso.downloaded)
            stdinit.std_signal_gobal.std_make_signal(0)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def std_clean(self):
        try:
            stdinit.std_signal_gobal.std_process(1, reso.clean)  # complexing
            self.Pio_run.pio_clean()
            stdinit.std_signal_gobal.std_process(0, reso.clean)
            stdinit.std_signal_gobal.std_make_signal(0)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def std_device_list(self):
        try:
            self.Pio_run.pio_device_list()
            stdinit.std_signal_gobal.std_make_signal(1)
        except:
            stdinit.std_signal_gobal.stdprintln()

