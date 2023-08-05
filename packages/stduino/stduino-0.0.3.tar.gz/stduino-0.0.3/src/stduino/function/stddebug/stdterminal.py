#!/usr/bin/python3
from PyQt5.QtCore import QProcess, QSysInfo, Qt, QEvent, QSettings, QPoint, QSize
from PyQt5.QtWidgets import QWidget, QApplication,  QPlainTextEdit, QVBoxLayout, QMainWindow, QAction
from PyQt5.QtGui import QIcon, QTextCursor
import sys
import getpass
import socket
import os
from PyQt5.QtCore import pyqtSignal
from function.cores.stdedit import stdinit

class Std_Termainal(QMainWindow):
    termin = pyqtSignal(str)  # 0 settext 1 appead 3process

    def __init__(self):
        super(Std_Termainal, self).__init__()
        try:
            # self.setStyleSheet(mystylesheet(self))

            self.commandslist = []
            self.tracker = 0
            # os.chdir(os.path.expanduser("~"))
            #        print(os.getcwd())
            # self.name = (str(getpass.getuser()) + "@" + str(socket.gethostname())+ ":" + str(os.getcwd()) + "$ ")
            self.name = "GDB>"
            self.setWindowTitle('Stdterminal')
            self.setWindowIcon(QIcon.fromTheme("terminal-emulator"))
            self.process = QProcess(self)
            self.process.setProcessChannelMode(QProcess.MergedChannels)
            self.process.readyRead.connect(self.dataReady)
            self.process.readyReadStandardError.connect(self.onReadyReadStandardError)
            self.process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)
            self.process.finished.connect(self.isFinished)
            self.process.setWorkingDirectory(os.getcwd())
            self.createStatusBar()

            self.commandfield = QPlainTextEdit()
            self.commandfield.setLineWrapMode(QPlainTextEdit.NoWrap)
            self.commandfield.setAttribute(Qt.WA_InputMethodEnabled,
                                           False)  # setAttribute(Qt::WA_InputMethodEnabled, false)
            self.commandfield.setFixedHeight(44)
            self.commandfield.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.commandfield.setAcceptDrops(True)
            self.cursor = self.commandfield.textCursor()

            self.textWindow = QPlainTextEdit(self)

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
            #        self.textWindow.installEventFilter(self)
            QApplication.setCursorFlashTime(1000)
            self.cursorEnd()
            # print(self.process.workingDirectory())
            self.settings = QSettings("QTerminal", "QTerminal")
            self.readSettings()
            self.commandfield.setCursorWidth(5)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def closeEvent(self, e):
        try:
            self.writeSettings()
        except:
            stdinit.std_signal_gobal.stdprintln()


    def cursorEnd(self):
        try:
            # self.name = (str(getpass.getuser()) + "@" + str(socket.gethostname())+ ":" + str(os.getcwd()) + "$ ")
            self.name = "GDB>"
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
                elif (event.type() == QEvent.Drop):
                    print('Drop')
                    self.setDropEvent(event)
                    return True
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


    # def killProcess(self):
    #     #print("cancelled")
    #     self.process.kill()
    #     #self.textWindow.appendPlainText("cancelled")
    #     self.cursorEnd()

    def createStatusBar(self):
        try:
            sysinfo = QSysInfo()
            # myMachine = "current CPU Architecture: " + sysinfo.currentCpuArchitecture() + " *** " + sysinfo.prettyProductName() + " *** " + sysinfo.kernelType() + " " + sysinfo.kernelVersion()
            myMachine = "GDB"
            self.statusBar().showMessage(myMachine, 0)
        except:
            stdinit.std_signal_gobal.stdprintln()



    def setDropEvent(self, event):
        try:
            self.commandfield.setFocus()
            if event.mimeData().hasUrls():
                f = str(event.mimeData().urls()[0].toLocalFile())
                print("is file:", f)
                if " " in f:
                    self.commandfield.insertPlainText("'{}'".format(f))
                else:
                    self.commandfield.insertPlainText(f)
                event.accept()
            elif event.mimeData().hasText():
                ft = event.mimeData().text()
                print("is text:", ft)
                if " " in ft:
                    self.commandfield.insertPlainText("'{}'".format(ft))
                else:
                    self.commandfield.insertPlainText(ft)
            else:
                event.ignore()
        except:
            stdinit.std_signal_gobal.stdprintln()

    def back_text(self,text):
        try:
            if "Couldn't determine a path for the index cache directory" in text:
                pass
                self.textWindow.setFocus()
                self.textWindow.setPlainText("Start debugging~")
                self.cursorEnd()

            else:
                self.textWindow.setFocus()
                self.textWindow.appendPlainText(str(text))
                self.cursorEnd()
        except:
            stdinit.std_signal_gobal.stdprintln()




    # Target is not responding, retrying...
    #
    # Debugger connection lost.
    #
    # Shutting down...
    def run(self):
        #print("started")

        try:
            cmd = self.commandfield.toPlainText()
            # t = ""
            self.textWindow.setFocus()
            self.textWindow.appendPlainText(cmd)
            # print(self.commandfield.toPlainText())
            cmd = cmd.replace(self.name, '')
            self.termin.emit(cmd)
            # print("command not found ...")
            # self.textWindow.appendPlainText("command not found ...")
            self.cursorEnd()
        except:
            stdinit.std_signal_gobal.stdprintln()

        #cli = []



        #cli = shlex.split(self.commandfield.toPlainText().replace(self.name, '').replace("'", '"'), posix=False)
        #cmd = str(cli)  ### is the executable
        #print(cmd)


        # if cmd == "exit":
        #     quit()
        #
        # elif cmd == "cd":
        #     del cli[0]
        #     path = " ".join(cli)
        #     os.chdir(os.path.abspath(path))
        #     self.process.setWorkingDirectory(os.getcwd())
        #     print("workingDirectory:", self.process.workingDirectory())
        #     self.cursorEnd()
        # else:
        #     self.process.setWorkingDirectory(os.getcwd())
        #     print("workingDirectory", self.process.workingDirectory())
        #     del cli[0]
        #     if (QStandardPaths.findExecutable(cmd)):
        #         self.commandslist.append(self.commandfield.toPlainText().replace(self.name, ""))
        #         print("command", cmd, "found")
        #         t = " ".join(cli)
        #         if self.process.state() != 2:
        #             self.process.waitForStarted()
        #             self.process.waitForFinished()
        #             if "|" in t or ">" in t or "<" in t:
        #                 print("special characters")
        #                 self.process.start('sh -c "' + cmd + ' ' + t + '"')
        #                 print("running", ('sh -c "' + cmd + ' ' + t + '"'))
        #             else:
        #                 self.process.start(cmd + " " + t)
        #                 print("running", (cmd + " " + t))
        #     else:
        #         print("command not found ...")
        #         self.textWindow.appendPlainText("command not found ...")
        #         self.cursorEnd()


    def dataReady(self):
        out = ""
        try:
            out = str(self.process.readAll(), encoding='utf8').rstrip()
        except TypeError:
            stdinit.std_signal_gobal.stdprintln()
            out = str(self.process.readAll()).rstrip()
            self.textWindow.moveCursor(self.cursor.Start)  ### changed
        self.textWindow.appendPlainText(out)

    def onReadyReadStandardError(self):
        try:
            self.error = self.process.readAllStandardError().data().decode()
            self.textWindow.appendPlainText(self.error.strip('\n'))
            self.cursorEnd()
        except TypeError:
            stdinit.std_signal_gobal.stdprintln()


    def onReadyReadStandardOutput(self):
        try:
            self.result = self.process.readAllStandardOutput().data().decode()
            self.textWindow.appendPlainText(self.result.strip('\n'))
            self.cursorEnd()
            self.state = self.process.state()
        except TypeError:
            stdinit.std_signal_gobal.stdprintln()


    def isFinished(self):
        try:

            self.name = (str(getpass.getuser()) + "@" + str(socket.gethostname())
                         + ":" + str(os.getcwd()) + "$ ")
            self.commandfield.setPlainText(self.name)
            self.cursorEnd()
        except:
            stdinit.std_signal_gobal.stdprintln()


    def readSettings(self):
        try:
            if self.settings.contains("commands"):
                self.commandslist = self.settings.value("commands")
            if self.settings.contains("pos"):
                pos = self.settings.value("pos", QPoint(200, 200))
                self.move(pos)
            if self.settings.contains("size"):
                size = self.settings.value("size", QSize(400, 400))
                self.resize(size)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def writeSettings(self):
        try:
            self.settings.setValue("commands", self.commandslist)
            self.settings.setValue("pos", self.pos())
            self.settings.setValue("size", self.size())
        except:
            stdinit.std_signal_gobal.stdprintln()



def mystylesheet(self):
    return """
QMainWindow{
background-color: #212121; }

QMainWindow:title
{
background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);
color: #3465a4;
}

QPlainTextEdit
 {font-family: Noto Sans Mono; 
font-size: 8pt; 
background-color: #212121; 
color: #FFD700; padding: 2; 
border: none;}

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
    ex = Std_Termainal()
    ex.show()
    #ex.raise_()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()