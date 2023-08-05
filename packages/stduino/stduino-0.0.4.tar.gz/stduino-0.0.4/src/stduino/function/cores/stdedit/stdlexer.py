# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
import PyQt5.QtPrintSupport
from PyQt5.QtGui import QColor,QFont
from PyQt5.Qsci import QsciScintilla,QsciLexerCPP
from function.conf import res
from function.cores.stdedit import stdinit

global key_load_high
key_load_high=0
global key_load
key_load=""
global auto_key_l
auto_key_l=0
global auto_key_list
auto_key_list=[]
class QsciLexerC(QsciLexerCPP):
    def __init__(self, parent):
        super(QsciLexerC, self).__init__(parent)
        try:

            #
            # Initialize colors per style
            # ----------------------------
            # self.setColor(QColor("#ff" + "000000"), 0)  # black
            # self.setColor(QColor("#ff" + "000000"), 1)  # black <b>
            # self.setColor(QColor("#ff" + "d60404"), 2)  # red
            # self.setColor(QColor("#ff" + "d60404"), python3)  # red <b>
            # self.setColor(QColor("#ff" + "ff7f00"), 4)  # orange
            # self.setColor(QColor("#ff" + "ff7f00"), 5)  # orange <b>
            # self.setColor(QColor("#ff" + "ba9b00"), 6)  # yellow
            # self.setColor(QColor("#ff" + "ba9b00"), 7)  # yellow <b>
            # self.setColor(QColor("#ff" + "20ad20"), 8)  # lightgreen
            # self.setColor(QColor("#ff" + "20ad20"), 9)  # lightgreen <b>
            # self.setColor(QColor("#ff" + "005900"), 10)  # green
            # self.setColor(QColor("#ff" + "005900"), 11)  # green <b>
            # self.setColor(QColor("#ff" + "0202ce"), 12)  # blue
            # self.setColor(QColor("#ff" + "0202ce"), 13)  # blue <b>
            # self.setColor(QColor("#ff" + "9400d3"), 14)  # lightpurple
            # self.setColor(QColor("#ff" + "9400d3"), 15)  # lightpurple <b>
            # self.setColor(QColor("#ff" + "4b0082"), 16)  # purple
            # self.setColor(QColor("#ff" + "4b0082"), 17)  # purple <b>
            # self.setColor(QColor("#ff" + "0668d1"), 18)  # cyan
            # self.setColor(QColor("#ff" + "0668d1"), 19)  # cyan <b>
            # #
            # # # Initialize paper colors per style
            # # ----------------------------------

            #
            # # Initialize fonts per style
            # # ---------------------------
            # self.setFont(QFont("Consolas", 13, ), 0)
            # self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 1)
            # self.setFont(QFont("Consolas", 13, ), 2)
            # self.setFont(QFont("Consolas", 13, weight=QFont.Bold), python3)
            # self.setFont(QFont("Consolas", 13, ), 4)
            # self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 5)
            # self.setFont(QFont("Consolas", 13, ), 6)
            # self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 7)
            # self.setFont(QFont("Consolas", 12, ), 8)
            # self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 9)
            # self.setFont(QFont("Consolas", 13, ), 10)
            # self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 11)
            # self.setFont(QFont("Consolas", 13, ), 12)
            # self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 13)
            # self.setFont(QFont("Consolas", 13, ), 14)
            # self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 15)
            # self.setFont(QFont("Consolas", 13, ), 16)
            # self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 17)
            # self.setFont(QFont("Consolas", 13, ), 18)
            # self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 19)

            self.setDefaultFont(QFont("Consolas", 14))  # 字体大小及样式
            self.setDefaultColor(QColor(res.default_text))  # 普通文字背景
            self.setDefaultPaper(QColor(res.default_main))  # 背景  #363636  95%背景颜色#363636
            self.setPaper(QColor(res.default_main), 0)  # Style 0: #363636  python3% 空格背景颜色
            self.setPaper(QColor(res.default_main), 1)  # Style 0: #363636  python3% 空格背景颜色
            self.setPaper(QColor(res.default_main), 2)  # Style 2: #363636  python3% 空格背景颜色
            self.setPaper(QColor(res.default_main), 3)  # Style 0: #363636  python3% 空格背景颜色
            self.setPaper(QColor(res.default_main), 4)  # Style 0: #363636  python3% 空格背景颜色
            self.setPaper(QColor(res.default_main), 5)  # Style 2: #363636  python3% 空格背景颜色
            self.setPaper(QColor(res.default_main), 6)  # Style 2: #363636  python3% 空格背景颜色

            # Initialize fonts per style
            # ---------------------------
            # self.setFont(QFont('华文楷体', 10))
            c_conmmert = QFont("Consolas", 14, weight=QFont.Bold)
            c_conmmert.setItalic(True)  # 斜体

            self.setFont(QFont("Consolas", 14, weight=QFont.Bold), 0)  # Style 0: Consolas 14pt
            self.setFont(QFont("Consolas", 14, weight=QFont.Bold), 1)  # Style 1: Consolas 14pt
            self.setFont(c_conmmert, 2)  # Style 2: Consolas 14pt
            self.setFont(c_conmmert, 3)  # Style python3: Consolas 14pt
            self.setFont(QFont("Consolas", 14, weight=QFont.Bold), 6)  # Style 1: Consolas 14pt
            self.setColor(QColor(res.default_mainkey1), 5)  # 主关键字
            self.setColor(QColor(res.default_mainkey2), 16)  # 008B45 主关键字2
            self.setColor(QColor(res.default_kh), 10)  # 点颜色 分号及括号颜色 运算符
            self.setColor(QColor(res.default_comment), 2)  # 行注释
            self.setColor(QColor(res.default_comment), 3)  # 块注释
            self.setColor(QColor(res.default_num), 4)  # 数字
            self.setColor(QColor(res.default_zh_hans), 6)  # 汉语
            self.setColor(QColor(res.default_include), 9)  # 预编译
            self.setColor(QColor(res.default_include), 19)  # 预编译
            self.setColor(QColor(res.default_include), 23)  # 预编译
            self.setColor(QColor(res.default_include), 24)  # 预编译

            #
            self.setFoldAtElse(True)
            self.setFoldComments(True)
            self.setFoldCompact(False)
            self.setFoldPreprocessor(True)
            self.setStylePreprocessor(True)


        except:
            stdinit.std_signal_gobal.stdprintln()
            ''''''







    def key_load_h(self):

        try:
            # 关键词1
            key_load1 = ""
            try:
                pass
                # for root, dirs, files in os.walk(res.library):
                #     for name in files:
                #         if name == 'keywords.txt':
                #
                #             try:
                #                 f = open(os.path.join(root, name))  # 返回一个文件对象
                #                 # line = f.readline()  # 调用文件的 readline()方法
                #                 lines = f.readlines()  # 调用文件的 readline()方法
                #                 for line in lines:
                #
                #
                #                     if "#" in line or line == "\n":
                #
                #                         pass
                #                     else:
                #
                #                         key_load1 += line.replace("\n", " ")
                #
                #                 f.close()
                #                 # key2 += "\n"
                #             except:
                #                 print("Unexpected error:", sys.exc_info()[1])  # 错误内容
                                # QMessageBox.warning(self, "BUG Warning",
                                #                     "Waring|Error:00013！\n You can search it in stduino.com",
                                #                     QMessageBox.Yes)
                pass
            except:
                stdinit.std_signal_gobal.stdprintln()

               # QMessageBox.warning(self, "BUG Warning", "Waring|Error:00014！\n You can search it in stduino.com",
               #                      QMessageBox.Yes)
            key_load1 = key_load1 + " setup loop HIGH LOW INPUT available read begin print println OUTPUT INPUT_PULSE INPUT_PULLUP INPUT_ANALOG OUTPUT_PULSE " \
                          "delay delayMicroseconds pinMode digitalWrite digitalRead analogRead analogWrite millis micros random " \
                          "map tone noTone if else while for switch case do break continue return goto min max abs constrain " \
                          "sizeof static const pow sqrt peek peekString"
            #print(key_load1)
            return key_load1
        except:
            #QMessageBox.warning(self, "BUG Warning", "Waring|Error:00015！\n You can search it in stduino.com",QMessageBox.Yes)
            stdinit.std_signal_gobal.stdprintln()
            pass
        # try:
        #     # 关键词1
        #     if p_int == 1:
        #         # print(13)
        #         return "int void double float boolean String char unsigned long Serial  Serial1 Serial2 Serial3 Serial4"
        #
        #     # 关键词2
        #     if p_int == 2:
        #         # print(python3)
        #         key2 = ""
        #         try:
        #             for root, dirs, files in os.walk(res.library):
        #                 for name in files:
        #                     if name == 'keywords.txt':
        #
        #
        #                         try:
        #                             f = open(os.path.join(root, name))  # 返回一个文件对象
        #                             # line = f.readline()  # 调用文件的 readline()方法
        #                             lines = f.readlines()  # 调用文件的 readline()方法
        #                             for line in lines:
        #
        #                                if "#" in line or line=="\n":
        #
        #                                    pass
        #                                else:
        #
        #                                    key2 += line.replace("\n", " ")
        #
        #
        #                             f.close()
        #                             # key2 += "\n"
        #                         except:
        #                             #print("Unexpected error:", sys.exc_info()[1])  # 错误内容
        #                             QMessageBox.warning(self, "BUG Warning", "Waring|Error:00013！\n You can search it in stduino.com",QMessageBox.Yes)
        #             pass
        #         except:
        #             QMessageBox.warning(self, "BUG Warning", "Waring|Error:00014！\n You can search it in stduino.com",QMessageBox.Yes)
        #         key2 = key2 + " setup loop HIGH LOW INPUT available read begin print println OUTPUT INPUT_PULSE INPUT_PULLUP INPUT_ANALOG OUTPUT_PULSE " \
        #                       "delay delayMicroseconds pinMode digitalWrite digitalRead analogRead analogWrite millis micros random " \
        #                       "map tone noTone if else while for switch case do break continue return goto min max abs constrain " \
        #                       "sizeof static const pow sqrt peek peekString"
        #         return key2
        # except:
        #     QMessageBox.warning(self, "BUG Warning", "Waring|Error:00015！\n You can search it in stduino.com",QMessageBox.Yes)
        #     # print("Unexpected error:", sys.exc_info()[1])  # 错误内容
        #     pass


    def keywords(self, p_int):
        try:
            global key_load_high
            global key_load
            if key_load_high == 0:

                key_load_high = 1
                key_load=self.key_load_h()

            # key_load = threading.Thread(target=self.key_load_h, name='key_load_hi')
            # # key_load.setDaemon(True)
            # key_load.start()
            if p_int == 1:
                # print(13)
                return "int void double float boolean String char unsigned long Serial  Serial1 Serial2 Serial3 Serial4"
            if p_int == 2:
                # print(python3)
                key2 = key_load
                return key2
        except:
            stdinit.std_signal_gobal.stdprintln()
