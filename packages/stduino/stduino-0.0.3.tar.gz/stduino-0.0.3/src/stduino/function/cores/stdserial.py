# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
__author__ = 'Su Jin Qiang'


import os
import time
from PyQt5.QtGui import QTextCursor,QIcon
from function.cores.stdmsg import reso
import serial  # pyserial
from function.cores.stdedit import stdinit
import serial.tools.list_ports
from PyQt5.QtCore import QTimer
from function.cores.uiserial import Std_Serial_Ui
from PyQt5 import QtCore, QtWidgets
# from function import process
# dsd = process.ProgressBar_start() #启动第一时间无法保证显示


#import tempfile
# 开发本软件消耗了太多时间精力，一路走来，太不容易，写下此行留为纪念，尤其感谢几位学弟（林鉴波、梁莅、房杰、刘席鸣等一直以来的各方面支持）。——2019.10.22晚


#pos = os.path.abspath('.')
#path = pos + "\\tool\msy"

#os.chdir("C:\stwork\stdemo2019827\dist\Stduinodebug\main")  # 通过更改当前运行目录F:\BaiduNetdiskDownload\stpython\stdemo\main


class StdSerial(QtWidgets.QWidget,Std_Serial_Ui):

    def __init__(self,id):
        super(StdSerial, self).__init__()
        try:
            stdinit.std_signal_gobal.upload_Close_check.connect(self.port_close)
            self.setupUi(self)  ############
            self.num_id=id
            self.init()
            self.setWindowTitle('Stduino ' + reso.serial_port_helper)
            self.setWindowIcon(QIcon("appearance/img/st.PNG"))
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.setStyleSheet("color:#2F4F4F; background-color:483D8B;")  ##########
            self.close_button.setStyleSheet("color:#000000; background-color:#458B00;")

            self.setFixedSize(730, 550)  # 480
            # self.setMinimumSize(730, 480)
            # self.setMaximumSize(830, 680)

            self.ser = serial.Serial()
            self.port_check()

            # 接收数据和发送数据数目置零
            self.data_num_received = 0

            self.lineEdit.setText(str(self.data_num_received))
            self.data_num_sended = 0
            self.lineEdit_2.setText(str(self.data_num_sended))
        except:
            stdinit.std_signal_gobal.stdprintln()


    def init(self):
        try:
            # 串口检测按钮
            self.s1__box_1.clicked.connect(self.port_check)

            # 串口信息显示
            self.s1__box_2.currentTextChanged.connect(self.port_imf)

            # 打开串口按钮
            self.open_button.clicked.connect(self.port_open)

            # 关闭串口按钮
            self.close_button.clicked.connect(self.port_close)

            # 发送数据按钮
            self.s3__send_button.clicked.connect(self.data_send)

            # 定时发送数据


            self.timer_send = QTimer()
            self.timer_send.timeout.connect(self.data_send)
            self.timer_send_cb.stateChanged.connect(self.data_send_timer)

            # 定时器接收数据
            self.timer = QTimer()
            self.timer.timeout.connect(self.data_receive)

            # 清除发送窗口
            # self.s3__clear_button.clicked.connect(self.send_data_clear)

            # 清除接收窗口
            self.s2__clear_button.clicked.connect(self.receive_data_clear)

            # dtr rts
            self.DTR.clicked.connect(self.dtr)
            self.RTS.clicked.connect(self.rts)
            self.time_dot.clicked.connect(self.time_dt)

            self.hex_send.clicked.connect(self.hex_d)
            self.s4__calc.clicked.connect(self.calc)
        except:
            stdinit.std_signal_gobal.stdprintln()
    def time_dt(self):
        pass

    def timer_del(self):
        try:
            if self.timer is not None:
                self.timer.stop()
            if self.timer_send is not None:
                self.timer_send.stop()
        except:
            stdinit.std_signal_gobal.stdprintln()



    # 串口检测
    def port_check(self):
        try:
            self.Com_Dict = {}
            port_list = list(serial.tools.list_ports.comports())
            self.s1__box_2.clear()
            for port in port_list:
                self.Com_Dict["%s" % port[0]] = "%s" % port[1]
                self.s1__box_2.addItem(port[0])
            if len(self.Com_Dict) == 0:
                self.state_label.setText(" 无串口")
        except:
            stdinit.std_signal_gobal.stdprintln()
        # 检测所有存在的串口，将信息存储在字典中


    # 串口信息
    def port_imf(self):
        try:
            # 显示选定的串口的详细信息
            imf_s = self.s1__box_2.currentText()
            if imf_s != "":
                self.state_label.setText(self.Com_Dict[self.s1__box_2.currentText()])

        except:
            stdinit.std_signal_gobal.stdprintln()


    # 打开串口
    def port_open(self):
        try:
            self.ser.port = self.s1__box_2.currentText()
            if "COM" in self.ser.port:
                pass
            else:
                stdinit.std_signal_gobal.std_echo_msg(1,"None Serial port to Open")
                return 0
            self.ser.baudrate = int(self.s1__box_3.currentText())
            self.s1__box_3.setEnabled(False)
            self.ser.bytesize = 8  # int(self.s1__box_4.currentText())
            self.ser.stopbits = 1  # int(self.s1__box_6.currentText())
            self.ser.parity = "N"  # self.s1__box_5.currentText()
            self.ser.open()
            # 串口复位
            time.sleep(0.01)
            self.ser.rts = True
            self.ser.dtr = True
            self.ser.dtr = False
            time.sleep(0.01)
            self.ser.rts = False
            time.sleep(0.01)
            self.ser.dtr = True
            time.sleep(0.01)
            self.ser.rts = True
            self.ser.rts = False
            self.timer.start(2)

            if self.ser.isOpen():
                self.open_button.setEnabled(False)
                # self.open_button.setStyle("background-color:483D8B;")
                self.close_button.setStyleSheet("color:#2F4F4F; background-color:#f0f0f0;")  ##########
                self.open_button.setStyleSheet("color:#000000; background-color:#458B00;")  ##########
                self.close_button.setEnabled(True)
                self.formGroupBox1.setTitle(reso.serial_port_staus_o)
        except:
            stdinit.std_signal_gobal.stdprintln()
            stdinit.std_signal_gobal.std_echo_msg(1, "None Serial port to Open")
            return None
        #print(123322)


        # self.ser.xonxoff=False

        # xonxoff = 0,  # enable software flow control
        # rtscts = 0,  # enable RTS/CTS flow control




        # 打开串口接收定时器，周期为2ms


    # 关闭串口
    def port_close(self):
        try:
            self.timer.stop()
            self.timer_send.stop()

            if self.ser.isOpen():
                try:
                    self.s1__box_3.setEnabled(True)
                    self.ser.close()
                except:
                    stdinit.std_signal_gobal.stdprintln()

            self.open_button.setEnabled(True)
            self.close_button.setStyleSheet(
                "color:#000000; background-color:#458B00;")  ##########setStyleSheet("color:#2F4F4F; background-color:483D8B;")  ##########
            self.open_button.setStyleSheet("color:#2F4F4F; background-color:#f0f0f0;")  ##########
            self.close_button.setEnabled(False)
            self.lineEdit_3.setEnabled(True)
            # 接收数据和发送数据数目置零
            # self.data_num_received = 0
            # self.lineEdit.setText(str(self.data_num_received))
            # self.data_num_sended = 0
            # self.lineEdit_2.setText(str(self.data_num_sended))
            self.formGroupBox1.setTitle(reso.serial_port_staus_c)

        except:
            stdinit.std_signal_gobal.stdprintln()


    # 发送数据
    def data_send(self):
        try:

            if self.ser.isOpen():
                input_s = self.s3__send_text.toPlainText()
                if input_s != "":
                    # 非空字符串
                    if self.hex_send.isChecked():

                        # hex发送
                        input_s = input_s.strip()
                        send_list = []
                        while input_s != '':
                            try:
                                num = int(input_s[0:2], 16)
                            except:
                                stdinit.std_signal_gobal.stdprintln()
                                return None
                            input_s = input_s[2:].strip()
                            send_list.append(num)
                        input_s = bytes(send_list)

                        # hex显示
                        data = input_s
                        out_s = ''
                        for i in range(0, len(data)):
                            out_s = out_s + '{:02X}'.format(data[i]) + ' '
                        if self.time_dot.isChecked():
                            self.s2__receive_text.append(
                                time.strftime("%H:%M:%S", time.localtime()) + reso.send_hex + out_s + ']')
                            # self.s2__receive_text.insertPlainText(time.strftime("%H:%M:%S", time.localtime()) + reso.receive_hex + out_s + ']' + '\r\n')
                            pass
                        else:
                            self.s2__receive_text.append(out_s)
                            pass

                    else:
                        # ascii发送
                        input_s = (input_s).encode("utf-8")

                        # hex显示
                        data = input_s
                        # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
                        if self.time_dot.isChecked():
                            self.s2__receive_text.append(
                                time.strftime("%H:%M:%S", time.localtime()) + reso.send_dec + data.decode(
                                    "utf-8") + ']')
                            # self.s2__receive_text.insertPlainText(time.strftime("%H:%M:%S", time.localtime()) + reso.receive_hex + out_s + ']' + '\r\n')
                            pass
                        else:
                            self.s2__receive_text.append(data.decode("utf-8"))
                            pass

                    num = self.ser.write(input_s)
                    self.data_num_sended += num
                    self.lineEdit_2.setText(str(self.data_num_sended))

                    # 获取到text光标
                    textCursor = self.s2__receive_text.textCursor()
                    # 滚动到底部
                    textCursor.movePosition(textCursor.End)
                    # 设置光标到text中去
                    self.s2__receive_text.setTextCursor(textCursor)
            else:
                pass
        except:
            stdinit.std_signal_gobal.stdprintln()



    # 接收数据
    def data_receive(self):


        try:
            num = self.ser.inWaiting()
        except:
            stdinit.std_signal_gobal.stdprintln()
            self.port_close()
            return None
        try:
            if num > 0:
                time.sleep(0.2)
                #刷新速度过快，易产生接收分离的情况，这样就会出现解码错误

                data = self.ser.read(num)
                num = len(data)
                # hex显示
                if self.hex_receive.checkState():
                    out_s = ''
                    for i in range(0, len(data)):
                        out_s = out_s + '{:02X}'.format(data[i]) + ' '
                    if self.time_dot.isChecked():
                        self.s2__receive_text.append(
                            time.strftime("%H:%M:%S", time.localtime()) + reso.receive_hex + out_s + ']')
                        # self.s2__receive_text.insertPlainText(time.strftime("%H:%M:%S", time.localtime()) + reso.receive_hex + out_s + ']' + '\r\n')
                        pass
                    else:
                        self.s2__receive_text.append(out_s)
                        pass
                else:
                    if self.time_dot.isChecked():
                        self.s2__receive_text.append(
                            time.strftime("%H:%M:%S", time.localtime()) + reso.receive_dec + data.decode(
                                "utf-8") + ']')
                        pass
                    else:

                        self.s2__receive_text.moveCursor(QTextCursor.End)
                        self.s2__receive_text.insertPlainText(data.decode("utf-8", 'ignore'))

                        pass

                self.data_num_received += num
                self.lineEdit.setText(str(self.data_num_received))

                # 获取到text光标
                textCursor = self.s2__receive_text.textCursor()
                # 滚动到底部
                textCursor.movePosition(textCursor.End)
                # 设置光标到text中去
                self.s2__receive_text.setTextCursor(textCursor)
            else:
                pass
        except:
            stdinit.std_signal_gobal.stdprintln()
            #print("Unexpected error:", sys.exc_info()[1])  # 错误内容

    # 定时发送数据
    def data_send_timer(self):
        try:
            if self.timer_send_cb.isChecked():
                self.timer_send.start(int(self.lineEdit_3.text()))
                self.lineEdit_3.setEnabled(False)
            else:
                self.timer_send.stop()
                self.lineEdit_3.setEnabled(True)
        except:
            stdinit.std_signal_gobal.stdprintln()


        # dtr

    def dtr(self):
        try:
            if self.DTR.isChecked():
                if self.ser.isOpen():
                    self.ser.dtr = False

            else:
                if self.ser.isOpen():
                    self.ser.dtr = True

        except:
            stdinit.std_signal_gobal.stdprintln()


    def rts(self):
        try:
            if self.RTS.isChecked():
                if self.ser.isOpen():
                    self.ser.rts = False

            else:
                if self.ser.isOpen():
                    self.ser.rts = True
        except:
            stdinit.std_signal_gobal.stdprintln()


    def hex_d(self):
        try:
            if self.hex_send.isChecked():
                self.s3__send_text.setText("FF 00 30")

            else:
                self.s3__send_text.setText("123456")
        except:
            stdinit.std_signal_gobal.stdprintln()


    def calc(self):
        try:
            os.popen("calc.exe")
        except:
            stdinit.std_signal_gobal.stdprintln()



    # 清除显示
    # def send_data_clear(self):
    #     self.s3__send_text.setText("")

    def receive_data_clear(self):
        try:
            self.data_num_sended = 0
            self.lineEdit_2.setText(str(self.data_num_sended))
            self.data_num_received = 0
            self.lineEdit.setText(str(self.data_num_received))
            self.s2__receive_text.setText("")
        except:
            stdinit.std_signal_gobal.stdprintln()


    def closeEvent(self, event):
        try:
            if self.ser.isOpen():
                self.port_close()
            stdinit.serialnumber.remove(self.num_id)
            event.accept()
        except:
            stdinit.std_signal_gobal.stdprintln()





        #the_window.status2.setText(text + reso.on + the_window.wcombo.currentText() + reso.download_type_1 + 'USB_ISP')
        #the_window.status2.setText()

