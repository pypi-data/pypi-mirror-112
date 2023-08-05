# -*- coding: utf-8 -*-

"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
import subprocess
import os,sys
import json
from function.cores.stdedit import stdinit
from function.cores.stdmsg import reso


#调用前先判断是否已经正常安装pio
class PioPlatformInstall():
    def __init__(self):
        if stdinit.platform_is == "Win":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio" + '"'

        elif stdinit.platform_is == "Linux":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio" + '"'

        elif stdinit.platform_is == "Darwin":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/bin/pio" + '"'


    def check_net(self):
        try:
            return stdinit.std_signal_gobal.is_connected()

        except:
            return False
    def platform_search(self):
        try:
            if self.check_net()==False:
                return False

            cmd = self.pio_env+" platform search --json-output"
            rest = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道

            try:
                data = str(rest.stdout.read(), encoding='gbk')
            except:
                data=str(rest.stdout.read())
            #print(data)

            rest.stdout.close()
            pioplatforms = json.loads(data)  # 字符串转json
            return pioplatforms
            # print("data2['name']: ", self.pioplatforms[0]['ownername'])

            pass
        except:
            stdinit.std_signal_gobal.stdprintln()

    def platform_list(self):#installed
        try:
            if self.check_net()==False:
                return False

            cmd = self.pio_env+" platform list --json-output"
            rest = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
            data = str(rest.stdout.read(), encoding='gbk')

            rest.stdout.close()
            pioplatforms = json.loads(data)  # 字符串转json
            return pioplatforms
            # print("data2['name']: ", self.pioplatforms[0]['ownername'])

            pass
        except:
            stdinit.std_signal_gobal.stdprintln()


    def platform_show(self,name):#installed
        try:
            if self.check_net()==False:
                return False

            cmd = self.pio_env+" platform show " + name
            rest = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
            data = str(rest.stdout.read(), encoding='gbk')
            rest.stdout.close()
            pioplatform = json.loads(data)  # 字符串转json
            return pioplatform
            # print("data2['name']: ", self.pioplatforms[0]['ownername'])
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()

    def isinstalled_plat(self,name):
        try:

            target = stdinit.stdenv + "/.platformio/platforms/" + name  # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"
            if os.path.exists(target):
                return True
            else:
                return False

            pass
        except:
            stdinit.std_signal_gobal.stdprintln()

    def platform_install(self,name):# 直接从国内源进行安装，先进行判断是否有国内源，没有就从国外安装
        try:
            if self.check_net()==False:
                return False

            cmd = self.pio_env+" platform install " + name
            print(cmd)
            return 0

            # res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
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
            return True
        except:
            stdinit.std_signal_gobal.stdprintln()


    def platform_uninstall(self,name):
        try:

            cmd =self.pio_env+" platform uninstall " + name
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
            return True
        except:
            stdinit.std_signal_gobal.stdprintln()

    def platform_update(self):#待完善
        try:
            if self.check_net()==False:
                return False
            cmd = self.pio_env+" platform update"
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            for line in iter(proc.stdout.readline, b''):
                try:
                    s1 = str(line, encoding='gbk')
                except:
                    s1 = str(line)
                #print(s1)
                if not subprocess.Popen.poll(proc) is None:
                    if line == "":
                        break
        except:
            stdinit.std_signal_gobal.stdprintln()


# pio platform install [OPTIONS] [PLATFORM...]
#
# # [PLATFORM...] forms
# pio platform install <name>
# pio platform install <name>@<version>
# pio platform install <name>@<version range>
# pio platform install <ownername>@<version>
# pio platform install <ownername>@<version range>
# pio platform install <zip or tarball url>
# pio platform install file://<zip or tarball file>
# pio platform install file://<folder>
# pio platform install <repository>
# pio platform install <name=repository> (name it should have locally)
# pio platform install <repository#tag> ("tag" can be commit, branch or tag)
    def install_plat(self):
        pass
        #self.platforminstall(self.pioplatforms[0]['name'])
        #stdinit.std_signal_gobal.stdprintln()
