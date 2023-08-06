from PyQt5.QtCore import pyqtSignal,QObject
import sys,traceback
import requests
from function.cores.stdmsg import reso
class StdSinal(QObject):
    try:
        find_change = pyqtSignal(int, str, str, bool)
        text_change = pyqtSignal()
        back_color = pyqtSignal(str, int)
        main_ui_change = pyqtSignal(int)
        process_p = pyqtSignal(int, str)  # 0 settext 1 appead 3process
        echo_msg = pyqtSignal(int, str)  # 0 settext 1 appead 3process
        work_space = pyqtSignal()  #
        find_staus_change = pyqtSignal()  #
        jump_to_look = pyqtSignal(str, int, str)
        debug_goto = pyqtSignal(str, str, str, str, str)  # fullname func number line
        gdb_cmd = pyqtSignal(str)  # fullname func number line
        jump_init = pyqtSignal()
        upload_list_change = pyqtSignal()
        file_modify = pyqtSignal()
        make_signal = pyqtSignal(int)  # 0 settext 1 appead 3process
        upload_Close_check = pyqtSignal()  # 0 settext 1 appead 3process
        upload_rts_dtr= pyqtSignal()  # 0 settext 1 appead 3process
        stdenvir_init=pyqtSignal()
    except:
        print(traceback.format_exc())
    def all_stdenvir_init(self):
        self.stdenvir_init.emit()


    def is_connected(self):
        try:
            html = requests.get("http://www.baidu.com", timeout=2)
        except:
            self.std_echo_msg(1, reso.no_net)
            return False
        return True


    def stdprintln(self):
        try:
            #print(traceback.format_exc())
            #print("Unexpected error:", sys.exc_info()[1])  # 错误内容
            self.echo_msg.emit(1, "Unexpected error:" + str(sys.exc_info()[1]))

            self.echo_msg.emit(1, traceback.format_exc())
            self.echo_msg.emit(1,"当你看到这段报错时，请根据使用情况进行判断是否影响正常使用，若严重影响使用请及时反馈，我将于2021年6月份后根据具体情况逐一修复；可通过软件左下角反馈功能反馈亦可至www.stduino.com进行反馈！\n 感谢您的使用，让我们一起在磨砺中成长。")
        except:
            print(traceback.format_exc())


        #还可以将信息写入到文件 发布后用这个方式进行收集错误
        #traceback.print_exc(file=open(‘error.txt','a+'))
        #print("Unexpected error:", sys.exc_info()[1])  # 错误内容
        # QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile00040！\n You can search it in stduino.com",QMessageBox.Yes)
    def std_upload_rts_dtr(self):  # all the time
        try:
            self.upload_rts_dtr.emit()  # 具体实现模仿sterminal的实现方式 绑定
        except:
            self.stdprintln()
    def std_process(self, staus, text):  # all the time
        try:
            self.process_p.emit(staus, text)  # 具体实现模仿sterminal的实现方式 绑定
        except:
            self.stdprintln()

    def std_find(self,idd, changetext, findtext, afind):
        try:
            self.find_change.emit(idd, changetext, findtext, afind)
        except:
            self.stdprintln()

    def std_text_change(self):
        try:
            self.text_change.emit()
        except:
            self.stdprintln()

    def std_back_color(self,str, id):  # startsetcolor
        try:
            self.back_color.emit(str, id)
        except:
            self.stdprintln()

    def std_main_ui_change(self,id):
        try:
            self.main_ui_change.emit(id)
        except:
            self.stdprintln()

    def std_echo_msg(self,staus,msg):#all the time #staus 0 清空
        try:
            self.echo_msg.emit(staus,msg) #具体实现模仿sterminal的实现方式 绑定
        except:
            self.stdprintln()


    def std_work_space(self):
        try:
            self.work_space.emit()
        except:
            self.stdprintln()

    def std_find_staus_change(self):
        try:
            self.find_staus_change.emit()
        except:
            self.stdprintln()

    def std_jump_to_look(self,path,line,text):
        try:
            self.jump_to_look.emit(path,line,text)
        except:
            self.stdprintln()

    def std_debug_goto(self,fullname,func,number,line,message):
        try:
            self.debug_goto.emit(fullname,func,number,line,message)
        except:
            self.stdprintln()

    def std_gdb_cmd(self,cmd):
        try:
            self.gdb_cmd.emit(cmd)
        except:
            self.stdprintln()

    def std_jump_init(self):
        try:
            self.jump_init.emit()
        except:
            self.stdprintln()

    def std_upload_list_change(self):
        try:
            self.upload_list_change.emit()
        except:
            self.stdprintln()

    def std_file_modify(self):
        try:
            self.file_modify.emit()
        except:
            self.stdprintln()
    def std_make_signal(self,id):
        try:
            self.make_signal.emit(id)
        except:
            self.stdprintln()

    def std_upload_Close_check(self):
        try:
            self.upload_Close_check.emit()
        except:
            self.stdprintln()



