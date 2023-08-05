# -*- coding: utf-8 -*-

"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import subprocess
import os
import json
from shutil import copy2
from function.cores.stdedit import stdinit
from urllib import request
import time


#调用前先判断是否已经正常安装pio
class PioProjectManage():
    def __init__(self):
        if stdinit.platform_is == "Win":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio" + '"'

        elif stdinit.platform_is == "Linux":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio" + '"'

        elif stdinit.platform_is == "Darwin":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/bin/pio" + '"'





        #self.projects_dir = stdinit.stdenv+"/Documents/Stduino/Projects"
        #

        pass



    def check_net(self):
        try:
            return stdinit.std_signal_gobal.is_connected()

        except:
            return False
    def project_boards(self):#待完善
        try:
            target = stdinit.stdenv + "/.stduino/packages/pioenv/pioboards.json"
            if stdinit.pio_boards == None:

                if self.check_net():
                    if os.path.exists(target):

                        target_ini = stdinit.stdenv + "/.stduino/packages/pioenv/stdpio.ini"
                        stdinit.pro_conf.read(target_ini, encoding="utf-8")  # python3
                        now_time = int(time.time())
                        update_time = int(stdinit.pro_conf.get('update', 'boards_update'))

                        if (now_time - update_time) > 600:#456400:

                            try:
                                stdinit.pro_conf.set('update', 'boards_update', str(now_time))
                                stdinit.pro_conf.write(open(target_ini, 'w'))
                                cmd = self.pio_env+" boards --json-output"

                                rest = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道

                                try:
                                    data = str(rest.stdout.read(), encoding='gbk')
                                except:
                                    data = rest.stdout.read()
                                fo = open(target, "w", encoding="utf-8", newline="")  # gbk_utf_type
                                fo.write(data)
                                fo.close()
                                rest.stdout.close()
                                stdinit.pio_boards = json.loads(data)  # 字符串转json
                                return True
                            except:

                                stdinit.std_signal_gobal.stdprintln()
                                return False
                        else:
                            try:

                                fo = open(target, mode='r', encoding='UTF-8')
                                stdinit.pio_boards = fo.read()
                                fo.close()  # cmd_args["cmd_rtlib"]

                                stdinit.pio_boards = json.loads(stdinit.pio_boards)
                                return True
                            except:

                                stdinit.std_signal_gobal.stdprintln()
                                return False
                    else:

                        target_abs = stdinit.abs_path + "/tool/packages/pioboards.json"  # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"
                        try:
                            fo = open(target_abs, mode='r', encoding='UTF-8')
                            stdinit.pio_boards = fo.read()
                            fo.close()  # cmd_args["cmd_rtlib"]
                            stdinit.pio_boards = json.loads(stdinit.pio_boards)
                            copy2(target_abs, target)
                            return False
                        except:
                            stdinit.std_signal_gobal.stdprintln()
                            return False
                else:

                    if os.path.exists(target):
                        try:
                            fo = open(target, mode='r', encoding='UTF-8')
                            stdinit.pio_boards = fo.read()
                            fo.close()  # cmd_args["cmd_rtlib"]
                            stdinit.pio_boards = json.loads(stdinit.pio_boards)
                            return True
                        except:
                            stdinit.std_signal_gobal.stdprintln()
                            return False
                    else:
                        # return False

                        target_abs = stdinit.abs_path + "/tool/packages/pioboards.json"  # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"
                        try:
                            fo = open(target_abs, mode='r', encoding='UTF-8')
                            stdinit.pio_boards = fo.read()
                            fo.close()  # cmd_args["cmd_rtlib"]
                            stdinit.pio_boards = json.loads(stdinit.pio_boards)
                            copy2(target_abs,target)
                            return False
                        except:
                            stdinit.std_signal_gobal.stdprintln()
                            return False
            else:
                if os.path.exists(target):
                    return True
                else:
                    return False
        except:
            stdinit.std_signal_gobal.stdprintln()







            # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"




        # target = stdinit.stdenv + "/.stduino/packages/pioenv/stdpio.ini"  # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"
        # if os.path.exists(target):
        #     pass
        #
        #     return True
        # else:
        #     return False
        # cmd = stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio boards --json-output"
        # rest = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
        # data = str(rest.stdout.read(), encoding='gbk')
        # rest.stdout.close()
        # projectboards = json.loads(data)  # 字符串转json
        # return projectboards


    def project_config(self):#待完善
        try:
            cmd = self.pio_env+" project config --json-output"
            rest = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道

            try:
                data = str(rest.stdout.read(), encoding='gbk')
            except:
                data = rest.stdout.read()
            rest.stdout.close()
            projectconfig = json.loads(data)  # 字符串转json
            return projectconfig
        except:
            stdinit.std_signal_gobal.stdprintln()


    #Recently updated
    #Recently added
    #Recent keywords
    #Popular keywords
    # Featured: Today
    # Featured: Week
    # Featured: Month
    def project_data(self):
        try:
            cmd = self.pio_env+" project data --json-output"
            rest = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
            data = str(rest.stdout.read(), encoding='gbk')
            rest.stdout.close()
            libs = json.loads(data)  # 字符串转json
            return libs
        except:
            stdinit.std_signal_gobal.stdprintln()


        # print("data2['name']: ", libs[0]['ownername'])

    def generate_project_main(self,framework):
        try:
            time.sleep(0.5)
            stdinit.std_signal_gobal.std_work_space()
            main_content = None
            if framework == "arduino":
                main_content = "\n".join(
                    [
                        "#include <Arduino.h>",
                        "",
                        "void setup() {",
                        "  // put your setup code here, to run once:",
                        "}",
                        "",
                        "void loop() {",
                        "  // put your main code here, to run repeatedly:",
                        "}",
                        "",
                    ]
                )
            elif framework == "mbed":
                main_content = "\n".join(
                    [
                        "#include <mbed.h>",
                        "",
                        "int main() {",
                        "",
                        "  // put your setup code here, to run once:",
                        "",
                        "  while(1) {",
                        "    // put your main code here, to run repeatedly:",
                        "  }",
                        "}",
                        "",
                    ]
                )
            if not main_content:
                return True
            src_dir = stdinit.projects_dir + stdinit.project_name + "/src"
            main_path = stdinit.projects_dir + stdinit.project_name + "/src/main.cpp"
            if os.path.isfile(main_path):
                return True
            if not os.path.isdir(src_dir):
                os.makedirs(src_dir)
            with open(main_path, "w") as fp:
                fp.write(main_content.strip())
            return True
        except:
            stdinit.std_signal_gobal.stdprintln()


    def project_init(self,upload_m,framework):


        try:
            target_path = stdinit.projects_dir + stdinit.project_name
          #大小写区分待解决 win下
            if os.path.exists(target_path):
                pass
            else:
                os.makedirs(target_path)
            target_path='"' + target_path+ '"'

            if upload_m=="Disable":#upload_m 调试前根据这个进行判断是否可以支持调试
                cmd = self.pio_env+" project init -d " + target_path + " --board " + stdinit.board_id + " -O framework=" + framework
            else:
                cmd = self.pio_env+" project init -d " + target_path + " --board " + stdinit.board_id + " -O framework=" + framework + " -O debug_tool=" + upload_m


            # if upload_m=="Disable":#upload_m 调试前根据这个进行判断是否可以支持调试
            #     cmd = stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio project init -d " + target_path + " --board " + stdinit.board_id + " -O framework=" + framework
            # else:
            #     cmd = stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio project init -d " + target_path + " --board " + stdinit.board_id + " -O framework=" + framework + " -O debug_tool=" + upload_m
            #

            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            for line in iter(proc.stdout.readline, b''):
                try:
                    s1 = str(line, encoding='gbk')
                except:
                    s1=str(line)
                #print(s1)
                if not subprocess.Popen.poll(proc) is None:
                    if line == "":
                        break
            proc.stdout.close()


            return self.generate_project_main(framework)
        except:
            stdinit.std_signal_gobal.stdprintln()
            return False

    def project_conf_read(self):#待完善其他目录时情况
        try:
            if stdinit.pro_conf == None:
                pass
            else:
                stdinit.pro_conf.clear()
            stdinit.pro_conf.read(stdinit.ini_path, encoding="utf-8")  # python3
        except:
            stdinit.std_signal_gobal.stdprintln()
            return False

        #print(cfgpath)  # cfg.ini的路径
        # 创建管理对象
        # 读ini文件
        #stdinit.ini_path = stdinit.projects_dir + stdinit.project_name + "/platformio.ini"

    def project_conf_save(self):
        try:
            stdinit.pro_conf.write(open(stdinit.ini_path, 'w'))
        except:
            stdinit.std_signal_gobal.stdprintln()
            return False



        # 获取所有的section
        #
        #conf.write(open(cfgpath, "w", encoding="utf-8"))  # r+模式


    def project_conf_add(self,  section,item,value):
        try:
            self.project_conf_read()
            # # 添加一个section
            sections = stdinit.pro_conf.sections()
            value_s = 0
            for sec in sections:
                if sec == section:
                    value_s = 1
                pass
            if value_s == 1:
                stdinit.pro_conf.set(section, item, str(value))

            else:
                stdinit.pro_conf.add_section(section)
                stdinit.pro_conf.set(section, item, str(value))
                # 往select添加key和value
                pass

            stdinit.project_conf_save()
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()
            return False

    def project_conf_del(self, section,item,si_value):#0删item 1删section
        try:
            self.project_conf_read()
            if si_value == 0:
                # 删除一个 section中的一个 item（以键值KEY为标识）
                stdinit.pro_conf.remove_option(section, item)
            else:
                # 删除整个section这一项
                stdinit.pro_conf.remove_section(section)
                pass
            self.project_conf_save()
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()
            return False

    def project_conf_update(self, section,item,value):
        try:
            self.project_conf_read()
            # 往select添加key和value 如果已存在即为修改
            stdinit.pro_conf.set(section, item, value)
            self.project_conf_save()
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()
            return False

    def project_conf_find(self, board, framework):
        try:
            self.project_conf_read()
            sections = stdinit.pro_conf.sections()
            #print(sections)  # 返回list
            items = stdinit.pro_conf.items(sections[0])
            #print(items)  # list里面对象是元祖
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()
            return False



