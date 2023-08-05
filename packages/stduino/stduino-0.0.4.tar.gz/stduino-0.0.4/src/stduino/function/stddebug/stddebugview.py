#!/usr/bin/python3
from PyQt5.QtCore import  Qt, QEvent,QSettings
from PyQt5.QtWidgets import QWidget, QApplication,  QPlainTextEdit, QVBoxLayout, QMainWindow, QAction
from PyQt5.QtGui import QIcon, QTextCursor
import sys
from function.cores.stdedit import stdinit
from pygdbmi import gdbmiparser

class Std_termainal(QMainWindow):
    #termin = pyqtSignal(str)  # 0 settext 1 appead 3process


    def __init__(self):
        super(Std_termainal, self).__init__()
        try:
            self.commandslist = []
            self.tracker = 0
            self.watch_id = []
            # os.chdir(os.path.expanduser("~"))
            #        print(os.getcwd())
            # self.name = (str(getpass.getuser()) + "@" + str(socket.gethostname())+ ":" + str(os.getcwd()) + "$ ")
            self.name = ">"
            self.setWindowTitle('sterminal')
            self.setWindowIcon(QIcon.fromTheme("terminal-emulator"))
            self.createStatusBar()
            self.commandfield = QPlainTextEdit()
            self.commandfield.setAttribute(Qt.WA_InputMethodEnabled, False)

            self.commandfield.setStyleSheet(
                "font-family: Noto Sans Mono; font-size: 18pt; background-color: #212821; color:#B0E2FF; padding: 2; border: none;")

            self.commandfield.setLineWrapMode(QPlainTextEdit.NoWrap)
            self.commandfield.setFixedHeight(44)
            self.commandfield.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.commandfield.setAcceptDrops(False)
            self.cursor = self.commandfield.textCursor()

            self.textWindow = QPlainTextEdit(self)  #
            self.textWindow.setStyleSheet(
                "font-family: Noto Sans Mono; font-size: 12pt; background-color: #212121; color: #00FF00; padding: 2; border: none;")
            self.setStyleSheet(mystylesheet(self))
            self.textWindow.setReadOnly(True)
            layout = QVBoxLayout()
            layout.addWidget(self.textWindow)
            layout.addWidget(self.commandfield)
            self.wid = QWidget()
            self.wid.setLayout(layout)
            self.setCentralWidget(self.wid)
            self.setGeometry(0, 0, 600, 500)
            self.commandfield.setPlainText(self.name)

            self.commandfield.setFocus()
            self.copySelectedTextAction = QAction(QIcon.fromTheme("edit-copy"), "Copy", shortcut="Shift+Ctrl+c",
                                                  triggered=self.copyText)
            self.textWindow.addAction(self.copySelectedTextAction)
            self.pasteTextAction = QAction(QIcon.fromTheme("edit-paste"), "Copy", shortcut="Shift+Ctrl+v",
                                           triggered=self.pasteText)
            self.commandfield.addAction(self.pasteTextAction)
            #
            # self.cancelAction = QAction("Cancel", shortcut="Ctrl+c", triggered=self.killProcess)
            # self.textWindow.addAction(self.cancelAction)

            self.commandfield.installEventFilter(self)
            self.commandfield.setCursorWidth(4)
            #        self.textWindow.installEventFilter(self)
            QApplication.setCursorFlashTime(1000)
            self.cursorEnd()
            # self.settings = QSettings("QTerminal", "QTerminal")
            # self.readSettings()
        except:
            stdinit.std_signal_gobal.stdprintln()





    def closeEvent(self, e):
        pass
        #self.writeSettings()

    def cursorEnd(self):
        try:
            # self.name = (str(getpass.getuser()) + "@" + str(socket.gethostname())+ ":" + str(os.getcwd()) + "$ ")
            self.name = ">"
            self.commandfield.setPlainText(self.name)
            cursor = self.commandfield.textCursor()
            cursor.movePosition(11, 0)

            self.commandfield.setTextCursor(cursor)
            self.commandfield.setFocus()
        except:
            stdinit.std_signal_gobal.stdprintln()




    def eventFilter(self, source, event):
        try:
            if source == self.commandfield:
                if (event.type() == QEvent.DragEnter):
                    event.accept()
                    return True
                # elif (event.type() == QEvent.Drop):
                #     print('Drop')
                #     self.setDropEvent(event)
                #     return True
                elif (event.type() == QEvent.KeyPress):
                    cursor = self.commandfield.textCursor()
                    #                print('key press:', (event.key(), event.text()))
                    if event.key() == Qt.Key_Backspace:
                        if cursor.positionInBlock() <= len(self.name):
                            return True
                        else:
                            return False

                    elif event.key() == Qt.Key_Return:
                        self.run()
                        return True

                    elif event.key() == Qt.Key_Left:
                        if cursor.positionInBlock() <= len(self.name):
                            return True
                        else:
                            return False

                    elif event.key() == Qt.Key_Delete:
                        if cursor.positionInBlock() <= len(self.name) - 1:
                            return True
                        else:
                            return False

                    # elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
                    #     self.killProcess()
                    #     return True

                    elif event.key() == Qt.Key_Up:
                        try:
                            if self.tracker != 0:
                                cursor.select(QTextCursor.BlockUnderCursor)
                                cursor.removeSelectedText()
                                self.commandfield.appendPlainText(self.name)

                            self.commandfield.insertPlainText(self.commandslist[self.tracker])
                            self.tracker -= 1

                        except IndexError:
                            self.tracker = 0
                        return True

                    elif event.key() == Qt.Key_Down:
                        try:
                            if self.tracker != 0:
                                cursor.select(QTextCursor.BlockUnderCursor)
                                cursor.removeSelectedText()
                                self.commandfield.appendPlainText(self.name)

                            self.commandfield.insertPlainText(self.commandslist[self.tracker])
                            self.tracker += 1

                        except IndexError:
                            self.tracker = 0
                        return True

                    else:
                        return False
                else:
                    return False
            else:
                return False
        except:
            stdinit.std_signal_gobal.stdprintln()


    def copyText(self):
        try:
            self.textWindow.copy()
        except:
            stdinit.std_signal_gobal.stdprintln()


    def pasteText(self):
        try:
            self.commandfield.paste()
        except:
            stdinit.std_signal_gobal.stdprintln()


    def createStatusBar(self):
        try:
            # sysinfo = QSysInfo()
            # myMachine = "current CPU Architecture: " + sysinfo.currentCpuArchitecture() + " *** " + sysinfo.prettyProductName() + " *** " + sysinfo.kernelType() + " " + sysinfo.kernelVersion()
            myMachine = "GDB"
            self.statusBar().showMessage(myMachine, 0)
        except:
            stdinit.std_signal_gobal.stdprintln()



    def back_text(self,text):
        try:
            response = gdbmiparser.parse_response(text)
            if response["type"] == "notify":
                if response["message"] == "stopped":
                    try:
                        if stdinit.debug_mark_start == 0:
                            stdinit.std_signal_gobal.std_process(0, "DEBUG初始化完成")
                            stdinit.debug_mark_start = 1
                            currant_pro = stdinit.projects_dir + stdinit.project_name
                            if len(stdinit.manual_mark) > 0:
                                for i in stdinit.manual_mark:
                                    if currant_pro in i:
                                        # self.termin.emit("break "+i)
                                        stdinit.std_signal_gobal.std_gdb_cmd(i)

                        else:
                            if response["payload"]["reason"] == "signal-received":
                                stdinit.std_signal_gobal.std_debug_goto(response["payload"]["frame"]["fullname"],
                                                                        response["payload"]["frame"]["func"],
                                                                        "1",
                                                                        response["payload"]["frame"]["line"],
                                                                        response["message"])

                            else:
                                stdinit.std_signal_gobal.std_debug_goto(response["payload"]["frame"]["fullname"],
                                                                        response["payload"]["frame"]["func"],
                                                                        "1",
                                                                        response["payload"]["frame"]["line"],
                                                                        response["message"])


                    except:
                        stdinit.std_signal_gobal.stdprintln()

            else:
                try:
                    self.textWindow.setFocus()
                    out = response["payload"]
                    if type(out) == str:


                        self.textWindow.appendPlainText(out.replace("\\n", "").replace("\\t", " "))
                        if "Error" in out:
                            stdinit.std_signal_gobal.std_gdb_cmd("machinequit")
                            stdinit.std_signal_gobal.std_process(0, "DEBUG初始化失败")
                            self.textWindow.appendPlainText("请检查当前项目platformio.ini文件中相关设置是否正确")
                except:
                    stdinit.std_signal_gobal.stdprintln()

                # self.textWindow.appendPlainText(response["payload"].replace("\\n",""))
            self.cursorEnd()
        except:
            stdinit.std_signal_gobal.stdprintln()


    def run(self):
        #print("started")

        try:

            cmd = self.commandfield.toPlainText()

            self.textWindow.setFocus()
            self.textWindow.appendPlainText(cmd)
            cmd = cmd.replace(self.name, '')
            # self.termin.emit(cmd)
            stdinit.std_signal_gobal.std_gdb_cmd(cmd)
            self.cursorEnd()
            if stdinit.stdenv not in cmd:
                self.commandslist.append(cmd)
        except:
            stdinit.std_signal_gobal.stdprintln()
    def readSettings(self):
        pass
        # if self.settings.contains("commands"):
        #     self.commandslist = self.settings.value("commands")
    def writeSettings(self):
        pass
        #self.settings.setValue("commands", self.commandslist)




def mystylesheet(self):
    return """
QMainWindow{
background-color: #212121; }

QMainWindow:title
{

color: #3465a4;
}

QPlainTextEdit:focus { 
border: none; }

QScrollBar {            
border: 1px solid #2e3436;
background: #292929;
width:8px;
height: 8px;
margin: 0px 0px 0px 0px;
}
QScrollBar::handle {
background: #2e3436;
min-height: 0px;
min-width: 0px;
}
QScrollBar::add-line {
background: #2e3436;
height: 0px;
width: 0px;
subcontrol-position: bottom;
subcontrol-origin: margin;
}
QScrollBar::sub-line {
background: #2e3436;
height: 0px;
width: 0px;
subcontrol-position: top;
subcontrol-origin: margin;
}

QStatusBar {
font-family: Noto Sans Mono; 
font-size: 7pt; 
color: #729fcf;}

"""


def main():
    app = QApplication(sys.argv)
    ex = Std_termainal()
    ex.show()
    #ex.raise_()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()