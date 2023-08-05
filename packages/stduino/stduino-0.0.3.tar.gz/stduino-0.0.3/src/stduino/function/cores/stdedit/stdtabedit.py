# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
from function.cores.stdmsg import reso
from function.cores.stdedit.stdlexer import QsciLexerC
from function.cores import commenter
import os
from function.conf import res
import re
import threading
from PyQt5.QtWidgets import QAction,QMenu,QShortcut
import subprocess
from PyQt5.QtCore import QFileInfo,Qt,QSize
from PyQt5.QtGui import QColor,QImage,QPixmap,QFont,QFontMetrics,QCursor,QKeySequence
from PyQt5.Qsci import QsciScintilla,QsciAPIs
from function.cores.stdedit import stdinit
from subprocess import run
from shutil import copy2
class StdTabEdit(QsciScintilla):
    NextId = 1
    def __init__(self, filename, parent=None):
        super(StdTabEdit, self).__init__(parent)
        try:
            self.setAttribute(Qt.WA_DeleteOnClose)
            # self.setAttribute(Qt.WA_InputMethodEnabled, True) 启动后为中文输入，待完善为英文输入

            self.filename = filename
            self.mark_list=[]
            self.margin_double=None
            self.jump_word = None
            #self.textChange_s=StdSinal()
            self.textChanged.connect(self.textChange) #移植至ui中绑定测试
            self.linesChanged.connect(self.line_change)
            #self.textEdit.textChanged.connect(self.editchange)
            self.setContextMenuPolicy(Qt.CustomContextMenu)  # 右键菜单，如果不设为CustomContextMenu,无法使用customContextMenuRequested
            self.customContextMenuRequested.connect(self.showContextMenu)
            # self.setWrapMode(QsciScintilla.WrapWord)  # 编辑区宽度设置   不设置会出现水平进度条

            self.setWrapIndentMode(QsciScintilla.WrapIndentFixed)
            self.setIndentationsUseTabs(False)  # 设置TAB键及竖格效果
            self.setTabWidth(1)
            self.setIndentationGuides(True)
            self.setTabIndents(True)  # 设置TAB键及竖格效果
            self.setAutoIndent(True)  # 开启自动缩进
            # self.setCaretLineVisible(True)  #显示选中的行号 目前没效果就没开启
            # self.setColor(QColor("#008000"), QsciLexerCPP.CommentDoc)  # 文档注释 /**开头的颜色
            # self.setColor(QColor("#008000"), QsciLexerCPP.Comment)  # 块注释 的颜色
            # self.setColor(QColor("#008000"), QsciLexerCPP.CommentLine)  # 行注释的颜色
            # self.setColor(QColor("#007f7f"), QsciLexerCPP.Number)  # 数字 的颜色
            # print(QsciLexerCPP.Number)
            # self.setColor(QColor("#ff00ff"), QsciLexerCPP.DoubleQuotedString)  # 双引号字符串的颜色
            # self.setColor(QColor("#ff00ff"), QsciLexerCPP.SingleQuotedString)  # 单引号字符的颜色
            # self.setColor(QColor("#be07ff"), QsciLexerCPP.PreProcessor)  # 预编译语句的颜色
            # self.setColor(QColor("#191970"), QsciLexerCPP.Operator)
            self.setCaretForegroundColor(QColor("#00E5EE"))  # 设置光标颜色#ff0000ff
            self.setCaretLineVisible(True)  # 设置光标所在行背景凸显
            self.setCaretLineBackgroundColor(QColor("#2F4F4F"))  # 设置光标所在行背景颜色
            #
            #self.setMarkerBackgroundColor(QColor("#191970"))
            # self.markerLine(5)
            # self.markersAtLine(6)
            self.setCaretWidth(20)  # 设置光标宽度
            self.setMarginType(0, QsciScintilla.NumberMargin)
            self.setMarginWidth(0,30)  # 设置行号显示及显示的宽度#0, "0000000" 40  1位 15
            self.setMarginType(1, QsciScintilla.SymbolMargin)
            self.setMarginWidth(1,40)#设置断点的占位宽度
            #self.setEolMode(QsciScintilla.EolWindows)
            #self.setEolVisibility(True)
            #self.setMaximumWidth(50)
            self.setFolding(QsciScintilla.BoxedTreeFoldStyle)  # 折叠样式
            # self.setMarginsBackgroundColor(Qt.black)
            # self.setMarginBackgroundColor(QColor("#1fff"))
            self.setMarginsForegroundColor(QColor(121, 122, 123))  # 行号字体背景颜色
            # self.setFolding(QsciScintilla.BoxedFoldStyle)
            self.setFoldMarginColors(QColor(30, 30, 30), QColor(121, 122, 123))  # 折叠栏颜色  # 折叠背景颜色
            #self.setMarkerBackgroundColor(QColor(30, 30, 30))#


            self.setMarginsBackgroundColor(QColor(30, 30, 30))  # 行号背景颜色
            #editor.setMarginsBackgroundColor(PyQt5.QtGui.QColor(0x8a, 0x00, 0x34, 80))
            # Set the foreground color (the text on margins) of all margins.
            # If this is not set it defaults to Black.
            #self.setMarginsForegroundColor(QColor(0x00, 0x00, 0xff, 0xff))
            # Set the default font
            self.font = QFont()
            self.font.setFamily('Consolas')
            self.font.setFixedPitch(True)
            self.font.setPointSize(12)  # 行号字体大小
            self.setFont(self.font)
            # self.__editor.setMarginsFont(self.__editor.font)
            # Margin 0 is used for line numbers
            fontmetrics = QFontMetrics(self.font)
            self.setMarginsFont(self.font)
            # self.__editor.setMarginWidth(0, fontmetrics.width("000") + 6)
            self.setMarginLineNumbers(0, True)  # 是否显示行号
            self.setMarginSensitivity(1, True)



            # Indentation
            self.setIndentationWidth(4)
            self.setBackspaceUnindents(True)
            self.setEdgeMode(QsciScintilla.EdgeLine)
            self.setEdgeColumn(80)
            self.setEdgeColor(QColor(0, 0, 0))



            sym_0 = QImage("appearance/img/debug_stop_next.svg").scaled(QSize(26, 26))
            sym_1 = QImage("appearance/img/img_dot4.svg").scaled(QSize(20, 20))
            sym_2 = QImage("appearance/img/img_dot4.svg").scaled(QSize(20, 20))
            sym_3 = QImage("appearance/img/img_dot4.svg").scaled(QSize(20, 20))
            # sym_4 = QsciScintilla.Circle


            self.markerDefine(sym_0, 0)
            self.markerDefine(sym_1, 1)
            self.markerDefine(sym_2, 2)
            self.markerDefine(sym_3, 3)
            self.markerDefine(self.Background, 4)
            self.markerDefine(self.Underline, 5)
            self.setMarkerBackgroundColor(QColor("#191970"), 4)
            #self.setMarkerForegroundColor(QColor("#191970"), 4)
            self.setMarkerBackgroundColor(QColor("#696969"), 5)#000000  #2E8B57
            #self.setMarkerForegroundColor(QColor("#000000"), 5)

            self.setMarginMarkerMask(1, 0b1111)
            # self.setMarginMarkerMask(1, 0x02)

            # 6. Margin mouse clicks
            # -----------------------
            self.setMarginSensitivity(1, True)
            self.marginClicked.connect(self.__margin_left_clicked)

            # self.marginRightClicked.connect(self.__margin_right_clicked)





            # // 每输入1个字符就出现自动完成的提示
#####################################################################




            # Comment feature goes here

            # self.commenter.

            QShortcut(QKeySequence(Qt.ALT + Qt.Key_P), self, self.startsetcolor)
            QShortcut(QKeySequence(Qt.ALT + Qt.Key_F), self, self.Format)
            QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F), self, self.Find)
            self.commenter = commenter.Commenter(self, "//")
            #QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Slash), self, self.commenter.toggle_comments)
            # QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_E)

            lexer= QsciLexerC(self)


            self.api = QsciAPIs(lexer)

            self.setLexer(lexer)
            self.setAutoCompletionReplaceWord(False)#替换之后的文字

            self.setAutoCompletionSource(QsciScintilla.AcsAll)  # 自动补全。对于所有Ascii字符 AcsAPIs  AcsAll

            self.setAutoCompletionCaseSensitivity(True)  # 设置自动补全大小写敏感
            # self.setAutoCompletionFillupsEnabled(False)
            #

            #self.SCN_AUTOCCOMPLETED.connect(self._correct_autocompletion)  完成获取

            # SendScintilla(self, int, wParam: int = 0, lParam: int = 0) -> int
            # SendScintilla(self, int, int, sip.voidptr) -> int
            # SendScintilla(self, int, int, bytes) -> int
            # SendScintilla(self, int, bytes) -> int
            # SendScintilla(self, int, bytes, bytes) -> int
            # SendScintilla(self, int, int) -> int
            # SendScintilla(self, int, int, int, bytes) -> int
            # SendScintilla(self, int, int, Union[QColor, Qt.GlobalColor]) -> int
            # SendScintilla(self, int, Union[QColor, Qt.GlobalColor]) -> int
            # SendScintilla(self, int, int, QPainter, QRect, int, int) -> int
            # SendScintilla(self, int, int, QPixmap) -> int
            # SendScintilla(self, int, int, QImage) -> int


            self.setAutoCompletionThreshold(1)
            self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)  # AcusAlways AcusNever

            # // 设置缩进的显示方式
            #
            self.setIndentationGuides(QsciScintilla.SC_IV_LOOKBOTH)
            self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

            self.setUtf8(True)


            # Sets whether the characters to the right of the autocompletion
            # will be overwritten when an autocompletion is selected.


            self.SendScintilla(QsciScintilla.SCI_SETSCROLLWIDTHTRACKING, 1)
            #self.SendScintilla(QsciScintilla.SCI_AUTOCSETIGNORECASE, 0)
            #self.setAutoCompletionFillupsEnabled(False)


            self.setCallTipsVisible(0)  # 同时显示多条提示
            self.setCallTipsPosition(QsciScintilla.CallTipsAboveText)
            self.setCallTipsStyle(QsciScintilla.CallTipsContext)  # 出现的时间

            # Multiple cursor support
            self.SendScintilla(QsciScintilla.SCI_SETMULTIPLESELECTION, True)
            self.SendScintilla(QsciScintilla.SCI_SETMULTIPASTE, 1)
            self.SendScintilla(QsciScintilla.SCI_SETADDITIONALSELECTIONTYPING, True)

            self.SendScintilla(QsciScintilla.SCI_SETCODEPAGE, QsciScintilla.SC_CP_UTF8)


            # Register an image that will be displayed with an autocompletion
            autocompletion_image = QPixmap("appearance/img/st.PNG")
            self.registerImage(1, autocompletion_image)
            # Create a list of autocompletions


            # Add the functions to the api
            # self.auto_key_load()
            t1 = threading.Thread(target=self.auto_key_load, name='auto_key_load')
            t1.setDaemon(True)
            t1.start()
            # key_load = threading.Thread(target=self.auto_key_load, name='key_load')
            # #key_load.setDaemon(True)
            # key_load.start()

            # Example of removing an entry

            # self.__editor.setText(str)


            if not self.filename:
                self.filename = "Unnamed_{0}".format(StdTabEdit.NextId)
                StdTabEdit.NextId += 1
            # self.setModified(False) #新建文件时首次设置无改动
            self.setWindowTitle(QFileInfo(self.filename).fileName())

            # -------------------------------- #
            #  Connect function to indicators  #
            # -------------------------------- #

            #self.indicatorClicked.connect(self.indicator_clicked)
            # self.SCN_HOTSPOTDOUBLECLICK.connect(self.tes)


        except:
             stdinit.std_signal_gobal.stdprintln()



    # def indicator_clicked(self, line, index, keys):
    #     print(line)
    #     print(index)
    #     pos = self.positionFromLineIndex(line, index)
    #
    #     start = self.SendScintilla(QsciScintilla.SCI_INDICATORSTART, 0, pos)
    #     end = self.SendScintilla(QsciScintilla.SCI_INDICATOREND, 0, pos)
    #     text = self.text()[start:end]
    #     print("indicator '{}' clicked in line '{}', index '{}'".format(text, line, index))
    #
    #     relPath, line = self.__lexer.parser.where_to_jump(text)
    #     linefocus = int(line) - 1
    #     print(linefocus)
    #     print("jump to file: " + relPath)
    #
        # relPath = globals.projectFolderPath + '\\' + relPath
        #QTimer.singleShot(100, functools.partial(self.indicator_clicked_delayed, line, index, keys))

    ''''''


    def auto_key_load(self):
        try:
            if stdinit.auto_key_l == 0:

                stdinit.auto_key_l = 1

                # autocompletions = [
                #     "int",
                #     "#include",
                #     "#defind",
                #     "goto",
                #     "sizeof",
                #     "static",
                #     "const",
                #     "pow",
                #     "sqrt",
                #     "min",
                #     "max",
                #     "abs",
                #     "constrain",
                #     "long",
                #     "map",
                #     "if",
                #     "else",
                #     "while",
                #     "for",
                #     "switch",
                #     "case",
                #     "do",
                #     "break",
                #     "continue",
                #     "return",
                #     "void",
                #     "double",
                #     "float",
                #     "boolean",
                #     "String",
                #     "char",
                #     "unsigned",
                #     "HIGH",
                #     "LOW",
                #     "INPUT",
                #     "OUTPUT",  # This call tip has a description and an image
                #     "INPUT_PULLUP",
                #     "INPUT_PULSE",
                #     "INPUT_ANALOG",
                #     "OUTPUT_PULSE",
                #     "INPUT_PULLDW",
                #     "peek",
                #     "peekString",
                #     "delay",
                #     "delay(ms)",
                #     "delayMicroseconds",
                #     "delayMicroseconds(us)",
                #     "pinMode",
                #     "pinMode(pin, INPUT )//浮空输入",
                #     "pinMode(pin, OUTPUT)//推挽输出",
                #     "pinMode(pin, INPUT_PULLUP)//上拉输入",
                #     "digitalWrite",  # This call tip has a description and an image
                #     "digitalWrite(pin, value)",
                #     "digitalRead",
                #     "digitalRead(pin)",
                #     "analogRead",
                #     "analogRead(pin)",
                #     "analogWrite",
                #     "analogWrite(pin,value)",
                #     "millis",
                #     "micros",
                #     "random",
                #     "map",
                #     "tone",
                #     "noTone",
                #     "Serial.begin",
                #     "Serial1.begin",
                #     "Serial2.begin",
                #     "Serial.print",
                #     "Serial1.print",
                #     "Serial2.print",
                #     "Serial.println",
                #     "Serial1.println",
                #     "Serial2.println",
                #     "Serial.read",
                #     "Serial1.read",
                #     "Serial2.read",
                #     "Serial.available",
                #     "Serial1.available",
                #     "Serial2.available"
                # ]
                # for ac in autocompletions:
                #     self.api.add(ac)
                try:
                    pass
                    # for root, dirs, files in os.walk(res.library):
                    #     for name in files:
                    #
                    #         if name == 'keywords.txt':
                    #             try:
                    #                 stdinit.auto_key_list.append(os.path.join(root, name))
                    #                 #self.api.load(os.path.join(root, name))
                    #
                    #             except:
                    #                 pass
                    # # for root, dirs, files in os.walk(res.library, topdown=False):
                    # pass

                except:
                    stdinit.std_signal_gobal.stdprintln()

            try:

                ke_len = len(stdinit.auto_key_list)
                for i in range(ke_len):
                    self.api.load(stdinit.auto_key_list[i])
                target = stdinit.stdenv + "/.stduino/session/keywords.txt"  # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"
                if os.path.exists(target):
                    self.api.load(target)
                else:
                    target2 = stdinit.stdenv + "/.stduino/session"
                    if os.path.exists(target2):
                        copy2('./appearance/stduino_json/keywords.txt',target)
                        self.api.load(target)
                    else:
                        os.makedirs(target2)
                        copy2('./appearance/stduino_json/keywords.txt', target)
                        self.api.load(target)


                # self.api.remove("entry_that_will_be_removed_later")
                # Prepare the QsciAPIs instance information
                self.api.prepare()
            except:
                stdinit.std_signal_gobal.stdprintln()
        except:
            stdinit.std_signal_gobal.stdprintln()








    splitter = re.compile(r"(\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W)")


    def _correct_autocompletion(self, *args):

        #print(args)
        try:
            word, from_index, to_index, length = args
            word = word.decode("utf-8")
            #print(2)
            current_line = self.getCursorPosition()[0] + 1
            #print(4)
            #self.line_list[current_line]

            line = "dsd"
            #print(1)
            for token in self.splitter.findall(self.text()):


                if token.lower() == word.lower():
                    #print(32)
                    self.setCursorPosition(current_line - 1, len("sdsdsdsd"))

                    # self.line_list[current_line] = token.join(line.rsplit(word, 1))
                    # self.setCursorPosition(current_line - 1, len(self.line_list[current_line]))
                    break

        except:
            stdinit.std_signal_gobal.stdprintln()
            #print("Unexpected error:", sys.exc_info()[1])  # 错误内容


    def __margin_left_clicked(self, margin_nr, line_nr, state):
        #print(margin_nr
        try:
            if self.margin_double == None:
                self.margin_double = 1
            else:
                self.margin_double = None
            # print("Margin clicked (left mouse btn)!")
            # print(" -> margin_nr: " + str(margin_nr))
            # print(" -> line_nr:   " + str(line_nr))
            # (xyxy)
            # 2,0    2,2
            #print(self.lineLength(line_nr))

            self.setSelection(line_nr,0,line_nr, self.lineLength(line_nr)-2)#遇到有中文的行时会多选
            text=self.selectedText().replace(" ","")
            self.setCursorPosition(line_nr,0)
            if len(text)>0:
                if text[0].encode('UTF-8').isalpha():
                    if self in stdinit.mark_object:
                        pass
                    else:
                        stdinit.mark_object.append(self)
                    mark_line=self.filename + ":" + str(line_nr + 1)
                    if self.markersAtLine(line_nr) > 1:
                        if stdinit.debug_mark_start == 1:
                            stdinit.std_signal_gobal.std_gdb_cmd("d " + mark_line)
                            self.markerDelete(line_nr,1)
                            self.markerDelete(line_nr, 5)
                            #self.mark_list.remove(mark_line)
                            #stdinit.manual_mark.remove(mark_line)
                        else:
                            self.markerDelete(line_nr, 1)
                            self.markerDelete(line_nr, 5)

                            #stdinit.manual_mark.remove(mark_line)
                    else:
                        if stdinit.debug_mark_start == 1:
                            stdinit.std_signal_gobal.std_gdb_cmd("break " + mark_line)
                            # stdinit.manual_mark.append(mark_line)
                            a = self.markerAdd(line_nr, 1)
                            #self.markerAdd(line_nr, 4)
                            self.markerAdd(line_nr, 5)

                            self.mark_list.append(a)

                            # print(a)
                            # print(12)
                        else:
                            # stdinit.manual_mark.append(mark_line)
                            a = self.markerAdd(line_nr, 1)
                            self.markerAdd(line_nr,5)
                            #self.markerAdd(line_nr, 4)
                            #self.markerDelete(line_nr, 5)
                            #print(22222222222222)
                            self.mark_list.append(a)
                            # self.markerAdd(line_nr, 0)
                            # self.markerDelete(line_nr, margin_nr)
                            # a1 = self.markersAtLine(line_nr)

                            # print(a1)
                            #self.markerDeleteHandle(1)

                            #print(self.markerLine(a))

                            # a=self.markerDeleteHandle(1)

                            # print(a)
                            # print(12222222222)




        except:
            stdinit.std_signal_gobal.stdprintln()


    ''''''

    def __margin_right_clicked(self, margin_nr, line_nr, state):
        try:
            print("Margin clicked (right mouse btn)!")
            print(" -> margin_nr: " + str(margin_nr))
            print(" -> line_nr:   " + str(line_nr))
            print("")
        except:
            stdinit.std_signal_gobal.stdprintln()






    # def mouseDoubleClickEvent(self, args):
    #     try:
    #
    #         if self.margin_double==1:
    #             QsciScintilla.mouseDoubleClickEvent(self, args)
    #             pass
    #         else:
    #             text = self.wordAtPoint(args.pos())#temp_text=text.replace("_","")
    #             #print(text)
    #             if text == "":  # temp_text.encode( 'UTF-8' ).isalpha():
    #                 QsciScintilla.mouseDoubleClickEvent(self, args)
    #                 pass#temp_text.encode( 'UTF-8' ).isalpha()
    #             else:
    #                 relPath, line = stdinit.goto_init.where_to_jump(text)
    #                 if relPath == "0":
    #                     stdinit.std_signal_gobal.std_echo_msg(1, "未找到相关声明:" + text)
    #                     QsciScintilla.mouseDoubleClickEvent(self, args)
    #                 else:
    #                     linefocus = int(line) - 1
    #                     stdinit.std_signal_gobal.std_jump_to_look(relPath, linefocus, text)
    #     except:
    #         stdinit.std_signal_gobal.stdprintln()


    def keyPressEvent(self, e):
        try:
            # event->key() == Qt::Key_Return & & (event->modifiers() & Qt::ControlModifier)
            if (e.key() == Qt.Key_Slash) and (e.modifiers() == Qt.ControlModifier):

                self.commenter.toggle_comments()
            if res.std_auto==1:


                    # self.setText('111212↑')
                    # res.std_auto
                if e.key() == 40:

                    if self.hasSelectedText():
                        self.replaceSelectedText("(" + self.selectedText() + ")")  # self.selectedText()

                        cursor = self.getCursorPosition()
                        self.setCursorPosition(cursor[0], cursor[1] - 1)
                    else:
                        self.insert("()")
                        cursor = self.getCursorPosition()
                        self.setCursorPosition(cursor[0], cursor[1] + 1)
                elif e.key() == 34:
                    if self.hasSelectedText():
                        self.replaceSelectedText("\"" + self.selectedText() + "\"")
                        cursor = self.getCursorPosition()
                        self.setCursorPosition(cursor[0], cursor[1] - 1)
                    else:
                        self.insert("\"\"")
                        cursor = self.getCursorPosition()
                        self.setCursorPosition(cursor[0], cursor[1] + 1)
                elif e.key() == 39:

                    if self.hasSelectedText():
                        self.replaceSelectedText("\'" + self.selectedText() + "\'")
                        cursor = self.getCursorPosition()
                        self.setCursorPosition(cursor[0], cursor[1] - 1)
                    else:
                        self.insert("\'\'")
                        cursor = self.getCursorPosition()
                        self.setCursorPosition(cursor[0], cursor[1] + 1)
                elif e.key() == 123:
                    if self.hasSelectedText():
                        self.replaceSelectedText("{" + self.selectedText() + "}")
                        cursor = self.getCursorPosition()
                        self.setCursorPosition(cursor[0], cursor[1] - 1)
                    else:
                        self.insert("{}")
                        cursor = self.getCursorPosition()
                        self.setCursorPosition(cursor[0], cursor[1] + 1)
                elif e.key() == 91:
                    if self.hasSelectedText():
                        self.replaceSelectedText("[" + self.selectedText() + "]")
                        cursor = self.getCursorPosition()
                        self.setCursorPosition(cursor[0], cursor[1] - 1)
                    else:
                        self.insert("[]")
                        cursor = self.getCursorPosition()
                        self.setCursorPosition(cursor[0], cursor[1] + 1)
                else:

                    QsciScintilla.keyPressEvent(self, e)

            else:

                QsciScintilla.keyPressEvent(self, e)
        except:
            stdinit.std_signal_gobal.stdprintln()

    #
    # def mousePressEvent(self,  e):
    #
    #     print(21)
    #
    #     QsciScintilla.mousePressEvent(self, e)

        #print(a)
    def mousePressEvent(self, event):
        try:
            if event.buttons() == Qt.RightButton:  # 右键按下
                self.jump_word = self.wordAtPoint(event.pos())
                # line = self.lineAt(event.pos())
            QsciScintilla.mousePressEvent(self, event)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def jump(self):
        try:
            relPath, line = stdinit.goto_init.where_to_jump(self.jump_word)
            if relPath == "0":
                stdinit.std_signal_gobal.std_echo_msg(1,"未找到相关声明"+self.jump_word)
            else:
                linefocus = int(line) - 1
                stdinit.std_signal_gobal.std_jump_to_look(relPath, linefocus, self.jump_word)

        except:
            stdinit.std_signal_gobal.stdprintln()

    def open_curflod(self):
        try:

            filename=self.filename
            title=self.windowTitle()
            filepath=filename.replace(title,"")


            if os.path.exists(filepath):
                if stdinit.platform_is == "Win":
                    os.startfile(filepath)

                elif stdinit.platform_is == "Linux":
                    os.startfile(filepath)

                elif stdinit.platform_is == "Darwin":
                    subprocess.call(["open", filepath])

            else:
               # print("该文件路径有误！")
                stdinit.std_signal_gobal.std_echo_msg(0,"该文件路径有误！")

            pass

        except:
            stdinit.std_signal_gobal.stdprintln()


    def showContextMenu(self):  # 创建右键菜单
        try:

            #QsciScintilla.keyPressEvent(self, e)
            openflod_ac = QAction("打开当前文件所在文件夹", self)
            openflod_ac.setStatusTip("打开当前文件所在文件夹")
            openflod_ac.triggered.connect(self.open_curflod)
            jump_ac = QAction("转到声明" , self)
            jump_ac.setStatusTip("转到声明")
            jump_ac.triggered.connect(self.jump)
            paste_ac = QAction(reso.paste + ' Ctrl+V', self)
            paste_ac.setStatusTip(reso.paste)
            paste_ac.triggered.connect(self.paste)
            find_ac = QAction(reso.search + ' Ctrl+F', self)
            # find_ac.setShortcut('Ctrl+F')
            find_ac.setStatusTip(reso.search)
            find_ac.triggered.connect(self.Find)

            format_ac = QAction(reso.format1 + ' Alt+F', self)
            format_ac.setStatusTip(reso.format1)
            format_ac.triggered.connect(self.Format)

            comment_ac = QAction(reso.commenter + ' Ctrl+/', self)
            comment_ac.setStatusTip(reso.commenter)
            comment_ac.triggered.connect(self.commenter.toggle_comments)

            page_set = QAction(reso.editstyle + ' Alt+P', self)
            # page_set.setShortcut(QKeySequence(Qt.ALT+ Qt.Key_P))
            page_set.setStatusTip(reso.editstyle)
            page_set.triggered.connect(self.startsetcolor)

            # push_git = QAction('gitee_push', self)
            # push_git.setShortcut('')
            # push_git.setStatusTip('gitee_push')
            # push_git.triggered.connect(self.git_push)
            popMenu = QMenu()
            #temp_text = self.jump_word.replace("_", "")


            popMenu.addAction(openflod_ac)
            popMenu.addAction(find_ac)
            if stdinit.platform_is == "Win":
                if self.jump_word == "":  # temp_text.encode( 'UTF-8' ).isalpha():
                    pass
                else:
                    popMenu.addAction(jump_ac)
                popMenu.addAction(format_ac)

            elif stdinit.platform_is == "Linux":
                pass


            elif stdinit.platform_is == "Darwin":
                pass

            popMenu.addAction(comment_ac)
            popMenu.addAction(page_set)
            # popMenu.addAction(copy_ac)
            # popMenu.addAction(cut_ac)
            popMenu.addAction(paste_ac)
            # popMenu.addAction(select_ac)
            # popMenu.addAction(push_git)

            popMenu.exec_(QCursor.pos())
        except:
            stdinit.std_signal_gobal.stdprintln()




    # def git_push(self):
    #     pass
    #     # name = getpass.getuser()
    #
    #     if res.git_email == '' or res.git_project_url == '' or res.git_staus == '0':
    #         print('none git anme')
    #         if res.git_email == '':
    #             import getpass
    #             name = getpass.getuser()
    #             value, ok = QInputDialog.getText(self, "笔名", "请输入笔名:", QLineEdit.Normal, name)
    #             if ok == 1:
    #                 subprocess.call(['git', 'config', '--global', 'user.name', value])
    #             value, ok = QInputDialog.getText(self, "邮箱", "请输入联系邮箱:", QLineEdit.Normal, "123@qq.com")
    #             if ok == 1:
    #                 subprocess.call(['git', 'config', '--global', 'user.email', value])
    #                 setup.git_email(value)
    #             pass
    #         if res.git_project_url == '':
    #             value, ok = QInputDialog.getText(self, "Gitee仓库地址", "请输入正确的代码仓库地址:", QLineEdit.Normal,
    #                                              "https://gitee.com/stduino/stduino_projects.git")
    #             if ok == 1:
    #                 pos = os.path.abspath('.')
    #                 Path = r'C:\Users\sujinqiang\Documents\Stduino\git2'
    #                 os.chdir(Path)
    #                 setup.git_project_url(value)
    #                 subprocess.call(['git', 'remote', 'add', 'cs3', value])
    #                 os.chdir(pos)
    #             pass
    #         if res.git_staus == '0':
    #             value, ok = QInputDialog.getText(self, "Gitee仓库地址", "请输入正确的代码仓库地址:", QLineEdit.Normal,
    #                                              "https://gitee.com/stduino/stduino_projects.git")
    #             if ok == 1:
    #                 pos = os.path.abspath('.')
    #                 Path = r'C:\Users\sujinqiang\Documents\Stduino\git2'
    #                 os.chdir(Path)
    #                 setup.git_project_url(value)
    #                 if '.git' not in os.listdir():
    #                     subprocess.call(['git', 'clone', value])
    #                 # subprocess.call(['git', 'remote', 'add', 'cs3', value])
    #
    #                 os.chdir(pos)
    #             setup.git_staus("1")
    #     else:
    #         Path3 = r'C:\Users\sujinqiang\Documents\Stduino\git3'  # 本地git库路径
    #
    #         # change working directory
    #         pos = os.path.abspath('.')
    #         os.chdir(Path3)
    #         if '.git' not in os.listdir():
    #             git_remotes = subprocess.check_output(
    #                 ['git', 'clone', "https://gitee.com/stduino/stduino_projects.git", Path3])
    #             # new_repo = git.Repo.clone_from(url='https://gitee.com/stduino/stduino_projects.git', to_path=Path3)
    #             # git_remotes = subprocess.check_output(['git', 'config', 'user.name'])
    #             # c=subprocess.check_call(['git', 'init'])
    #             git_remotes_str = bytes.decode(git_remotes).strip()
    #             # print(git_remotes_str)
    #             # print(11)
    #
    #         subprocess.call(['git', 'add', "."])
    #         git_remotes = subprocess.check_output(['git', 'status'])
    #         git_remotes_str = bytes.decode(git_remotes).strip()
    #         a = re.search('Changes', git_remotes_str, re.I)
    #         print(git_remotes_str)
    #         if a == None:
    #             print("nothing to update")
    #             pass
    #         else:
    #             value, ok = QInputDialog.getText(self, "程序上传至仓库", "请输入本次更新的内容:", QLineEdit.Normal, "增加了驱动器")
    #             if ok == 1:
    #                 subprocess.call(['git', 'commit', '-m', value])
    #                 subprocess.check_call(['git', 'push', 'origin', 'master:master'])
    #             pass
    #         print('git')
    #         os.chdir(pos)
    #         pass

    def Find(self):
        try:
            pass
            stdinit.Std_Find.show()#待完善2021111
        except:
            stdinit.std_signal_gobal.stdprintln()


    def startsetcolor(self):  # startsetcolor

        # self.__lexer.setColor(QColor("#66CDAA"), QsciLexerCPP.CommentLine)  # 注释 #66CDAA  #1C1C1C  黑
        try:
            pass
            stdinit.Set_Back_Color1.show()#2021111注释
        except:
            stdinit.std_signal_gobal.stdprintln()

    def Format(self):
        try:

            file_path = self.SaveFile_format()
            options = "-xe"
            exe = '.\\appearance\AStyle\\bin\AStyle.exe'
            astyle = [exe, options, file_path]
            # retval = subprocess.call(astyle)#os.popen(
            retval = run(astyle, shell=True)
            # retval = os.popen(astyle)
            # print(retval)
            fo = open(file_path, mode='r', encoding='UTF-8')
            st = fo.read()
            fo.close()
            self.selectAll(True)
            # self.clear()
            self.replaceSelectedText(st)
            # self.insertAt('#include"stduino.h"\r\n',0,0)
            if retval:
                # print("Bad astyle return: " + str(retval))
                pass
                # error("Bad astyle return: " + str(retval))
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()


    def SaveFile_format(self):
        # global fileName
        try:

            pos = os.path.abspath('.')
            filename = pos + "\\appearance\AStyle\\bin\style.ino"
            fo = open(filename, "w", encoding="UTF-8", newline="")
            strr = self.text()
            # strr = self.__editor.text()
            # 在文件末尾写入一行self.combo.currentText()
            fo.write(strr)
            # 关闭文件
            fo.close()
            os.chdir(pos)
            return filename
        except:
            stdinit.std_signal_gobal.stdprintln()

    def save(self):
        try:

            if os.path.exists(self.filename):
                try:
                    fo = open(self.filename, "w", encoding="utf-8", newline="")  # gbk_utf_type
                    cs = self.text()
                    fo.write(cs)
                    fo.close()
                    self.setModified(False)
                    return 1
                except:
                    stdinit.std_signal_gobal.stdprintln()

            #the_window.setWindowTitle("Stduino IDE " + version_c + " [" + self.filename + ']')  # 文件名设置



        except:
            stdinit.std_signal_gobal.stdprintln()



    def load(self):
        try:

            fh = None
            try:
                # fh = QFile(self.filename)
                # if not fh.open(QIODevice.ReadOnly):
                #     fh.close()
                #     return 1
                #
                # stream = QTextStream(fh)
                fh = open(file=self.filename, mode='rb')  # 以二进制模式读取文件
                data = fh.read()  # 获取文件内容
                fh.close()  # 关闭文件unicode
                self.setText(data.decode("utf-8", 'ignore'))
                # self.insert(data.decode("utf-8", 'ignore'))
                self.setModified(False)

                if fh is not None:
                    fh.close()
                return 0
            except:
                stdinit.std_signal_gobal.stdprintln()
                fh.close()
                return 1
        except:
            stdinit.std_signal_gobal.stdprintln()



    # def keyPressEvent1(self,e):
    #
    #
    #     print(e.text())
    #     self.insert("\"")
    #     e.accept()
    # self.update()
    # QWidget.keyPressEvent(self, e)
    def line_change(self): #40
        try:
            m_lines = self.lines()
            margin_width = self.marginWidth(0)

            if m_lines < 10:
                m_lines = 30
                if m_lines == margin_width:
                    pass
                else:
                    self.setMarginWidth(0, m_lines)

            elif m_lines < 100:
                m_lines = 40
                if m_lines == margin_width:
                    pass
                else:

                    self.setMarginWidth(0, m_lines)
            elif m_lines < 1000:
                m_lines = 50
                if m_lines == margin_width:
                    pass
                else:
                    self.setMarginWidth(0, m_lines)

                pass
            elif m_lines < 10000:
                m_lines = 65
                if m_lines == margin_width:
                    pass
                else:
                    self.setMarginWidth(0, m_lines)

                pass
            elif m_lines < 10000:
                m_lines = 75
                if m_lines == margin_width:
                    pass
                else:
                    self.setMarginWidth(0, m_lines)
            else:
                m_lines = 80
                if m_lines == margin_width:
                    pass
                else:
                    self.setMarginWidth(0, m_lines)
        except:
            stdinit.std_signal_gobal.stdprintln()



        # print(m_lines)
        # m_lines=m_lines*15+35 # x=35+15*lines/10   0-9 10-99  100-999  1000-9999 10000-50000
        # margin_width=self.marginWidth(0)
        # print(margin_width)
        # if (margin_width<m_lines):
        #     self.setMarginWidth(0, m_lines)
        #     pass




        #self.setMarginWidth(0, 80)  # 设置行号显示及显示的宽度#0, "0000000"
    def textChange(self):

        try:
            # 待完善
            stdinit.savefileAction_staus =self.isModified()
            stdinit.saveallAction_staus = self.isModified()
            stdinit.forwardAction_staus = self.isRedoAvailable()
            stdinit.backAction_staus = self.isUndoAvailable()
            stdinit.std_signal_gobal.std_text_change()


            # self.savefileAction.setDisabled(not self.isModified())
            #
            # self.saveallAction.setDisabled(not self.isModified())
            # self.forwardAction.setDisabled(not self.isRedoAvailable())
            # self.backAction.setDisabled(not self.isUndoAvailable())stdtabedit

        except:
            stdinit.std_signal_gobal.stdprintln()




