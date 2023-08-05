# -*- coding: utf-8 -*-

"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
# from pygdbmi import gdbmiparser
import subprocess
import json
import os
from function.cores.stdedit import stdinit

#调用前先判断是否已经正常安装pio
class PioRunManage():
    def __init__(self):
        if stdinit.platform_is == "Win":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio" + '"'

        elif stdinit.platform_is == "Linux":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio" + '"'

        elif stdinit.platform_is == "Darwin":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/bin/pio" + '"'




    def pio_run(self):#待完善make#分离目录获取第 7个值  C:\Users\debug\Documents\Stduino\Projects
        try:
            stdinit.std_signal_gobal.std_echo_msg(0, "")
            if stdinit.project_name==None:
                stdinit.std_signal_gobal.std_echo_msg(1,"软件正在初始化,请稍等片刻~")
                return 0
            else:

                pro_curt = '"' + stdinit.projects_dir + stdinit.project_name + '"'
                if stdinit.std_make_board == None:
                    cmd = self.pio_env+" run -d " + pro_curt
                else:
                    cmd = self.pio_env+" run -e " + stdinit.std_make_board + " -d " +pro_curt

                # pio run -e uno -t upload.


                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                for line in iter(proc.stdout.readline, b''):
                    #s1 = str(line)#
                    try:
                        s1 = str(line, encoding='gbk')
                    except:
                        s1 = str(line)
                    # print(s1)
                    # response = gdbmiparser.parse_response(s1)
                    # print(response)
                    stdinit.std_signal_gobal.std_echo_msg(1, s1)
                    #print(s1)
                    if not subprocess.Popen.poll(proc) is None:
                        if line == "":
                            break
                proc.stdout.close()
        except:
            stdinit.std_signal_gobal.stdprintln()
    def pio_clean(self):#待完善
        try:
            stdinit.std_signal_gobal.std_echo_msg(0, "")
            if stdinit.project_name==None:
                stdinit.std_signal_gobal.std_echo_msg(1,"软件正在初始化,请稍等片刻~")
                return 0
            else:
                pro_curt='"'+stdinit.projects_dir + stdinit.project_name+'"'
                if stdinit.std_make_board == None:
                    cmd = self.pio_env+" run -d " + pro_curt + " -t clean"
                else:
                    cmd = self.pio_env+" run -e " + stdinit.std_make_board + " -d " + pro_curt + " -t clean"
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                for line in iter(proc.stdout.readline, b''):
                    try:
                        s1 = str(line, encoding='gbk')
                    except:
                        s1 = str(line)
                    stdinit.std_signal_gobal.std_echo_msg(1, s1)
                    if not subprocess.Popen.poll(proc) is None:
                        if line == "":
                            break
                proc.stdout.close()



        except:
            stdinit.std_signal_gobal.stdprintln()

    def pio_upload(self):#待完善
        try:
            stdinit.std_signal_gobal.std_echo_msg(0, "")
            if stdinit.project_name==None:
                stdinit.std_signal_gobal.std_echo_msg(1,"软件正在初始化,请稍等片刻~")
                return 0
            else:

                if stdinit.current_upload_m=="serial" and stdinit.platform=="ststm32":
                    stdinit.std_signal_gobal.std_upload_rts_dtr()


                pro_curt = '"' + stdinit.projects_dir + stdinit.project_name + '"'
                if stdinit.std_make_board == None:
                    cmd = self.pio_env+" run -d " + pro_curt + " -t upload"

                else:
                    cmd = self.pio_env+" run -e " + stdinit.std_make_board + " -d " + pro_curt + " -t upload"
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                for line in iter(proc.stdout.readline, b''):
                    try:
                        s1 = str(line, encoding='gbk')
                    except:
                        s1 = str(line)
                    stdinit.std_signal_gobal.std_echo_msg(1, s1)
                    if not subprocess.Popen.poll(proc) is None:
                        if line == "":
                            break
                proc.stdout.close()
        except:
            stdinit.std_signal_gobal.stdprintln()


    def pio_device_list(self):#待完善
        try:

            cmd = self.pio_env+" device list --json-output"
            rest = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
            try:
                data = str(rest.stdout.read(), encoding='gbk')
            except:
                data = str(rest.stdout.read())

            rest.stdout.close()
            stdinit.device = json.loads(data)
            return True
        except:
            stdinit.std_signal_gobal.stdprintln()
