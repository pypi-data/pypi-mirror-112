# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo_1.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore,  QtWidgets
from function.cores.stdedit import stdinit

class Std_Serial_Ui(object):
    def setupUi(self, Form):
        try:
            Form.setObjectName("Std_Serial_Ui")
            Form.resize(707, 658)  # 458
            self.formGroupBox = QtWidgets.QGroupBox(Form)  # x y Lenth with
            self.formGroupBox.setGeometry(QtCore.QRect(20, 280, 175, 240))
            self.formGroupBox.setObjectName("formGroupBox")
            self.formLayout = QtWidgets.QFormLayout(self.formGroupBox)
            self.formLayout.setContentsMargins(10, 10, 10, 10)  # 串口检测区
            self.formLayout.setSpacing(10)
            self.formLayout.setObjectName("formLayout")
            self.s1__lb_1 = QtWidgets.QLabel(self.formGroupBox)
            self.s1__lb_1.setObjectName("s1__lb_1")
            self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.s1__lb_1)
            self.s1__box_1 = QtWidgets.QPushButton(self.formGroupBox)
            self.s1__box_1.setAutoRepeatInterval(100)
            self.s1__box_1.setDefault(True)
            self.s1__box_1.setObjectName("s1__box_1")
            self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.s1__box_1)
            self.s1__lb_2 = QtWidgets.QLabel(self.formGroupBox)
            self.s1__lb_2.setObjectName("s1__lb_2")
            self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.s1__lb_2)
            self.s1__box_2 = QtWidgets.QComboBox(self.formGroupBox)
            self.s1__box_2.setObjectName("s1__box_2")
            self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.s1__box_2)
            self.s1__lb_3 = QtWidgets.QLabel(self.formGroupBox)
            self.s1__lb_3.setObjectName("s1__lb_3")
            self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.s1__lb_3)
            self.s1__box_3 = QtWidgets.QComboBox(self.formGroupBox)
            self.s1__box_3.setObjectName("s1__box_3")
            self.s1__box_3.addItem("")
            self.s1__box_3.addItem("")
            self.s1__box_3.addItem("")
            self.s1__box_3.addItem("")
            self.s1__box_3.addItem("")
            self.s1__box_3.addItem("")
            self.s1__box_3.addItem("")
            self.s1__box_3.addItem("")
            self.s1__box_3.addItem("")
            self.s1__box_3.addItem("")
            self.s1__box_3.addItem("")
            self.s1__box_3.addItem("")
            self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.s1__box_3)
            # self.s1__lb_4 = QtWidgets.QLabel(self.formGroupBox)
            # self.s1__lb_4.setObjectName("s1__lb_4")
            # self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.s1__lb_4)
            # self.s1__box_4 = QtWidgets.QComboBox(self.formGroupBox)
            # self.s1__box_4.setObjectName("s1__box_4")
            # self.s1__box_4.addItem("")
            # self.s1__box_4.addItem("")
            # self.s1__box_4.addItem("")
            # self.s1__box_4.addItem("")
            # self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.s1__box_4)
            # self.s1__lb_5 = QtWidgets.QLabel(self.formGroupBox)
            # self.s1__lb_5.setObjectName("s1__lb_5")
            # self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.s1__lb_5)
            # self.s1__box_5 = QtWidgets.QComboBox(self.formGroupBox)
            # self.s1__box_5.setObjectName("s1__box_5")
            # self.s1__box_5.addItem("")
            # self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.s1__box_5)
            self.open_button = QtWidgets.QPushButton(self.formGroupBox)
            self.open_button.setObjectName("open_button")
            self.formLayout.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.open_button)
            self.close_button = QtWidgets.QPushButton(self.formGroupBox)
            self.close_button.setObjectName("close_button")
            self.formLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.close_button)
            # self.s1__lb_6 = QtWidgets.QLabel(self.formGroupBox)
            # self.s1__lb_6.setObjectName("s1__lb_6")
            # self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.s1__lb_6)
            # self.s1__box_6 = QtWidgets.QComboBox(self.formGroupBox)
            # self.s1__box_6.setObjectName("s1__box_6")
            # self.s1__box_6.addItem("")
            # self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.s1__box_6)
            self.state_label = QtWidgets.QLabel(self.formGroupBox)
            self.state_label.setText("")
            self.state_label.setTextFormat(QtCore.Qt.AutoText)
            self.state_label.setScaledContents(True)
            self.state_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
            self.state_label.setObjectName("state_label")
            self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.state_label)
            self.verticalGroupBox = QtWidgets.QGroupBox(Form)
            self.verticalGroupBox.setGeometry(QtCore.QRect(10, 20, 701, 241))  # 接收区
            self.verticalGroupBox.setObjectName("verticalGroupBox")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalGroupBox)
            self.verticalLayout.setContentsMargins(10, 10, 10, 10)
            self.verticalLayout.setObjectName("verticalLayout")
            self.s2__receive_text = QtWidgets.QTextBrowser(
                self.verticalGroupBox)  # QtWidgets.QTextEdit(self.verticalGroupBox)#
            # self.s2__receive_text.setReadOnly(True)
            self.s2__receive_text.setObjectName("s2__receive_text")
            self.verticalLayout.addWidget(self.s2__receive_text)
            self.verticalGroupBox_2 = QtWidgets.QGroupBox(Form)
            self.verticalGroupBox_2.setGeometry(QtCore.QRect(210, 280, 500, 101))
            self.verticalGroupBox_2.setObjectName("verticalGroupBox_2")
            self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalGroupBox_2)
            self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)  # 发送区
            self.verticalLayout_2.setObjectName("verticalLayout_2")
            self.s3__send_text = QtWidgets.QTextEdit(self.verticalGroupBox_2)
            self.s3__send_text.setObjectName("s3__send_text")
            self.verticalLayout_2.addWidget(self.s3__send_text)
            self.s3__send_button = QtWidgets.QPushButton(Form)
            self.s3__send_button.setGeometry(QtCore.QRect(635, 400, 70, 30))  # 发送按钮
            self.s3__send_button.setObjectName("s3__send_button")
            # self.s3__clear_button = QtWidgets.QPushButton(Form)
            # self.s3__clear_button.setGeometry(QtCore.QRect(620, 350, 61, 31))#清除按钮
            # self.s3__clear_button.setObjectName("s3__clear_button")
            self.formGroupBox1 = QtWidgets.QGroupBox(Form)
            self.formGroupBox1.setGeometry(QtCore.QRect(210, 415, 155, 105))  # 串口状态
            self.formGroupBox1.setObjectName("formGroupBox1")
            self.formLayout_2 = QtWidgets.QFormLayout(self.formGroupBox1)
            self.formLayout_2.setContentsMargins(10, 10, 10, 10)
            self.formLayout_2.setSpacing(10)
            self.formLayout_2.setObjectName("formLayout_2")
            self.label = QtWidgets.QLabel(self.formGroupBox1)
            self.label.setObjectName("label")
            self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
            self.label_2 = QtWidgets.QLabel(self.formGroupBox1)
            self.label_2.setObjectName("label_2")
            self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
            self.lineEdit = QtWidgets.QLineEdit(self.formGroupBox1)

            self.lineEdit.setObjectName("lineEdit")
            self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
            self.lineEdit_2 = QtWidgets.QLineEdit(self.formGroupBox1)
            self.lineEdit_2.setObjectName("lineEdit_2")
            # self.lineEdit_2.setReadOnly(True)
            self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
            self.hex_send = QtWidgets.QCheckBox(Form)
            self.hex_send.setGeometry(QtCore.QRect(415, 276, 85, 22))  # 串口发送
            self.hex_send.setObjectName("hex_send")
            self.hex_receive = QtWidgets.QCheckBox(Form)
            self.hex_receive.setGeometry(QtCore.QRect(310, 276, 85, 22))  # 串口接收
            self.hex_receive.setObjectName("hex_receive")
            self.time_dot = QtWidgets.QCheckBox(Form)
            self.time_dot.setGeometry(QtCore.QRect(530, 276, 85, 22))  # 串口接收
            self.time_dot.setObjectName("time_dot")
            self.s2__clear_button = QtWidgets.QPushButton(Form)
            self.s2__clear_button.setGeometry(QtCore.QRect(635, 263, 70, 30))  # 串口清除
            self.s2__clear_button.setObjectName("s2__clear_button")
            self.timer_send_cb = QtWidgets.QCheckBox(Form)
            self.timer_send_cb.setGeometry(QtCore.QRect(385, 400, 85, 22))  # 定时发送
            self.timer_send_cb.setObjectName("timer_send_cb")

            self.DTR = QtWidgets.QCheckBox(Form)
            self.DTR.setGeometry(QtCore.QRect(415, 450, 71, 22))  # DTR
            self.DTR.setObjectName("DTR")
            self.RTS = QtWidgets.QCheckBox(Form)
            self.RTS.setGeometry(QtCore.QRect(415, 480, 71, 22))  # RTS
            self.RTS.setObjectName("RTS")

            self.s4__calc = QtWidgets.QPushButton(Form)
            self.s4__calc.setGeometry(QtCore.QRect(635, 485, 80, 30))  # 计算器
            self.s4__calc.setObjectName("s4__calc")

            self.lineEdit_3 = QtWidgets.QLineEdit(Form)
            self.lineEdit_3.setGeometry(QtCore.QRect(475, 400, 61, 20))  # 发送框定时发送
            self.lineEdit_3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
            self.lineEdit_3.setObjectName("lineEdit_3")
            self.dw = QtWidgets.QLabel(Form)
            self.dw.setGeometry(QtCore.QRect(541, 400, 54, 20))
            self.dw.setObjectName("dw")
            self.verticalGroupBox.raise_()
            self.verticalGroupBox_2.raise_()
            self.formGroupBox.raise_()
            self.s3__send_button.raise_()
            # self.s3__clear_button.raise_()
            self.formGroupBox.raise_()
            self.hex_send.raise_()
            self.hex_receive.raise_()
            self.time_dot.raise_()
            self.s2__clear_button.raise_()
            self.timer_send_cb.raise_()
            self.DTR.raise_()
            self.RTS.raise_()
            self.s4__calc.raise_()

            self.lineEdit_3.raise_()
            self.dw.raise_()

            self.retranslateUi(Form)
            QtCore.QMetaObject.connectSlotsByName(Form)
        except:
            stdinit.std_signal_gobal.stdprintln()



    def retranslateUi(self, Form):
        try:
            _translate = QtCore.QCoreApplication.translate
            Form.setWindowTitle(_translate("Form", "Form"))
            self.formGroupBox.setTitle(_translate("Form", "串口设置"))
            self.s1__lb_1.setText(_translate("Form", "串口检测："))
            self.s1__box_1.setText(_translate("Form", "检测串口"))
            self.s1__lb_2.setText(_translate("Form", "串口选择："))
            self.s1__lb_3.setText(_translate("Form", "波特率："))
            self.s1__box_3.setItemText(0, _translate("Form", "9600"))
            self.s1__box_3.setItemText(1, _translate("Form", "2400"))
            self.s1__box_3.setItemText(2, _translate("Form", "4800"))
            self.s1__box_3.setItemText(3, _translate("Form", "14400"))
            self.s1__box_3.setItemText(4, _translate("Form", "19200"))
            self.s1__box_3.setItemText(5, _translate("Form", "38400"))
            self.s1__box_3.setItemText(6, _translate("Form", "57600"))
            self.s1__box_3.setItemText(7, _translate("Form", "115200"))
            self.s1__box_3.setItemText(8, _translate("Form", "76800"))
            self.s1__box_3.setItemText(9, _translate("Form", "12800"))
            self.s1__box_3.setItemText(10, _translate("Form", "230400"))
            self.s1__box_3.setItemText(11, _translate("Form", "460800"))
            # self.s1__lb_4.setText(_translate("Form", "数据位："))
            # self.s1__box_4.setItemText(0, _translate("Form", "8"))
            # self.s1__box_4.setItemText(1, _translate("Form", "7"))
            # self.s1__box_4.setItemText(2, _translate("Form", "6"))
            # self.s1__box_4.setItemText(python3, _translate("Form", "5"))
            # self.s1__lb_5.setText(_translate("Form", "校验位："))
            # self.s1__box_5.setItemText(0, _translate("Form", "N"))
            # self.s1__lb_6.setText(_translate("Form", "停止位："))
            # self.s1__box_6.setItemText(0, _translate("Form", "1"))

            self.open_button.setText(_translate("Form", "打开串口"))
            self.close_button.setText(_translate("Form", "关闭串口"))
            self.verticalGroupBox.setTitle(_translate("Form", "接收区"))
            self.verticalGroupBox_2.setTitle(_translate("Form", "发送区"))
            self.s3__send_text.setHtml(_translate("Form",
                                                  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                  "p, li { white-space: pre-wrap; }\n"
                                                  "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">123456</p></body></html>"))
            self.s3__send_button.setText(_translate("Form", "串口发送"))
            # self.s3__clear_button.setText(_translate("Form", "1清除"))
            self.formGroupBox1.setTitle(_translate("Form", "串口状态"))
            self.label.setText(_translate("Form", "已接收："))
            self.label_2.setText(_translate("Form", "已发送："))
            self.hex_send.setText(_translate("Form", "Hex发送"))
            self.hex_receive.setText(_translate("Form", "Hex接收"))
            self.time_dot.setText(_translate("Form", "时间戳"))
            self.s2__clear_button.setText(_translate("Form", "清除窗口"))
            self.timer_send_cb.setText(_translate("Form", "定时发送"))
            self.DTR.setText(_translate("Form", "DTR"))
            self.RTS.setText(_translate("Form", "RTS"))
            if stdinit.platform_is == "Win":
                self.s4__calc.setText(_translate("Form", "打开计算器"))
            self.lineEdit_3.setText(_translate("Form", "1000"))
            self.dw.setText(_translate("Form", "ms/次"))
        except:
            stdinit.std_signal_gobal.stdprintln()


