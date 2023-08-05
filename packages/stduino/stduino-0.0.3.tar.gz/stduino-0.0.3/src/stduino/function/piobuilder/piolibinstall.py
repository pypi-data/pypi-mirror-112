# -*- coding: utf-8 -*-

"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
import subprocess
import json
from function.cores.stdedit import stdinit
from function.cores.stdmsg import reso


#调用前先判断是否已经正常安装pio
class PioLibInstall():
    def __init__(self):
        if stdinit.platform_is == "Win":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio" + '"'

        elif stdinit.platform_is == "Linux":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio" + '"'

        elif stdinit.platform_is == "Darwin":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/bin/pio" + '"'


    def lib_builtin(self):#待完善
        try:
            cmd = self.pio_env+" lib builtin --json-output"
            rest = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
            try:
                data = str(rest.stdout.read(), encoding='gbk')
            except:
                data = str(rest.stdout.read())
            rest.stdout.close()
            libs = json.loads(data)  # 字符串转json
            return libs
        except:
            stdinit.std_signal_gobal.stdprintln()
    def check_net(self):
        try:
            return stdinit.std_signal_gobal.is_connected()

        except:
            return False


    #Recently updated
    #Recently added
    #Recent keywords
    #Popular keywords
    # Featured: Today
    # Featured: Week
    # Featured: Month
    def lib_stats(self):
        try:

            cmd = self.pio_env+" lib stats --json-output"
            rest = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
            try:
                data = str(rest.stdout.read(), encoding='gbk')
            except:
                data = str(rest.stdout.read())
            rest.stdout.close()
            libs = json.loads(data)  # 字符串转json
            return libs
        except:
            stdinit.std_signal_gobal.stdprintln()


        # print("data2['name']: ", libs[0]['ownername'])
    def lib_search_k(self,k,p):#page
        try:

            cmd = self.pio_env+" lib search " + k + " --json-output --page " + str(p)
            rest = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
            try:
                data = str(rest.stdout.read(), encoding='gbk')
            except:
                data = str(rest.stdout.read())

            rest.stdout.close()
            libs = json.loads(data)  # 字符串转json
            # print(libs['items'][0]['name'])
            return libs
        except:
            stdinit.std_signal_gobal.stdprintln()


    def lib_search(self,p):#page
        try:

            cmd = self.pio_env+" lib search --page " + str(p) + " --json-output"
            rest = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
            try:
                data = str(rest.stdout.read(), encoding='gbk')
            except:
                data = str(rest.stdout.read())

            rest.stdout.close()
            libs = json.loads(data)  # 字符串转json
            # print(libs['items'][0]['name'])
            return libs
        except:
            stdinit.std_signal_gobal.stdprintln()

        # print("data2['name']: ", libs[0]['ownername'])
    def is_installed_lib(self):

        pass



    def lib_list(self):  # installed
        try:

            cmd = self.pio_env+" lib list --json-output"
            rest = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
            try:
                data = str(rest.stdout.read(), encoding='gbk')
            except:
                data= str(rest.stdout.read())
            rest.stdout.close()
            pioplatforms = json.loads(data)  # 字符串转json
            return pioplatforms
            # print("data2['name']: ", self.pioplatforms[0]['ownername'])

            pass
        except:
            stdinit.std_signal_gobal.stdprintln()


    def lib_show(self, name):  # installed
        try:

            cmd = self.pio_env+" lib show " + name
            rest = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
            data = str(rest.stdout.read(), encoding='gbk')
            rest.stdout.close()
            pioplatform = json.loads(data)  # 字符串转json
            return pioplatform
            # print("data2['name']: ", self.pioplatforms[0]['ownername'])
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()


    def lib_install(self, id):#pro_path
        try:

            cmd = self.pio_env+" lib -d " + '"' +stdinit.projects_dir + stdinit.project_name+ '"'  + " install " + id
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
        except:
            stdinit.std_signal_gobal.stdprintln()



    def lib_uninstall(self, id):
        try:
            cmd = self.pio_env+" lib -d " + '"' +stdinit.projects_dir + stdinit.project_name+ '"'  + " uninstall " + id
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
        except:
            stdinit.std_signal_gobal.stdprintln()


    def lib_update(self,pro_path):  # 待完善
        try:
            if self.check_net()==False:
                return False
            cmd = self.pio_env+" lib --storage-dir " + '"' +pro_path + '"' + " update"
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            for line in iter(proc.stdout.readline, b''):
                try:
                    s1 = str(line, encoding='gbk')
                except:
                    s1 = str(line)

                if not subprocess.Popen.poll(proc) is None:
                    if line == "":
                        break
        except:
            stdinit.std_signal_gobal.stdprintln()

    def lib_all_update(self):  # 待完善Update all installed libraries in global storage
        try:
            if self.check_net()==False:
                return False
            cmd = self.pio_env+" lib -g update"
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            for line in iter(proc.stdout.readline, b''):
                try:
                    s1 = str(line, encoding='gbk')
                except:
                    s1 = str(line)
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
