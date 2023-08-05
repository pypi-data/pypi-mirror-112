# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
import subprocess
import os,stat
from function.cores.stdedit import stdinit
from function.conf import res, setup
from shutil import copytree,rmtree,copy2
import threading
import requests
import json
import zipfile
import time
#调用前先判断是否已经正常安装pio
class PioInstall():
    def __init__(self):
        stdinit.std_signal_gobal.stdenvir_init.connect(self.all_init)
        if stdinit.platform_is == "Win":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio" + '"'

        elif stdinit.platform_is == "Linux":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pio" + '"'

        elif stdinit.platform_is == "Darwin":
            self.pio_env = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/bin/pio" + '"'


        #print(self.abs_path)
        #self.pip_fast()

    def pip_fast(self):#all the time
        try:
            if res.msg == "1":  # 中
                target = stdinit.stdenv + "/pip"
                # target="C:/stwork/stdemo2019827/tool/packages/pip2/pip.ini"
                if os.path.exists(target):
                    pass
                else:
                    try:
                        source = stdinit.abs_path + "/tool/packages/pip"
                        # print(source)
                        # target=os.environ["USERPROFILE"] + "/pip/pip.ini"
                        copytree(source, target)
                    except:
                        stdinit.std_signal_gobal.stdprintln()
                    pass
                pass
        except:
            stdinit.std_signal_gobal.stdprintln()

    def is_installed_pio(self):#mac 和linux 好像不同
        try:



            target = stdinit.stdenv + "/.stduino/packages/pioenv"  # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"
            #print(target)
            if os.path.exists(target):
                return True
            else:
                return False
        except:

            stdinit.std_signal_gobal.stdprintln()


    def is_init_pioenv(self):
        try:
            target = stdinit.stdenv + "/.stduino/packages/pioenv"
            if os.path.exists(target):
                return True
            else:
                return False
        except:
            stdinit.std_signal_gobal.stdprintln()


    def pioenv_init(self):

        try:
            if stdinit.platform_is == "Win":
                cmd = stdinit.abs_path + "/tool/packages/python3/python -m venv " + '"' +stdinit.stdenv + "/.stduino/packages/pioenv"+ '"'

            elif stdinit.platform_is == "Linux":
                cmd = stdinit.abs_path + "/tool/packages/python3/bin/python -m venv " + '"' +stdinit.stdenv + "/.stduino/packages/pioenv"+ '"'

            elif stdinit.platform_is == "Darwin":
                cmd = stdinit.abs_path + "/tool/packages/python3/bin/python -m venv " + '"' + stdinit.stdenv + "/.stduino/packages/pioenv" + '"'

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
    def check_net(self):
        try:
            return stdinit.std_signal_gobal.is_connected()

        except:
            return False


            # if stdinit.platform_is == "Win":
            #     request.urlopen(url="https://www.baidu.com", timeout=3.0)
            #
            #
            # elif stdinit.platform_is == "Linux":
            #     pass
            #
            # elif stdinit.platform_is == "Darwin":
            #     pass

            # print(ret)


    def install_pio(self):
        try:
            if stdinit.platform_is == "Win":
                env_path = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pip" + '"'
                cmd = env_path + " install -i https://pypi.tuna.tsinghua.edu.cn/simple -U platformio"
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                for line in iter(proc.stdout.readline, b''):
                    try:
                        s1 = str(line, encoding='gbk')
                    except:
                        s1 =  str(line)
                    # print(s1)
                    if not subprocess.Popen.poll(proc) is None:
                        if line == "":
                            break
                proc.stdout.close()  # pioenv\Lib\site-packages\platformio\package\manager
                regi = stdinit.stdenv + "/.stduino/packages/pioenv/Lib/site-packages/platformio/package/manager/_registry.py"
                self.delete_file(regi)
                copy2(stdinit.abs_path + "/tool/packages/python3/Scripts/stdload.py", regi)

                copy2(stdinit.abs_path + "/tool/packages/python3/Scripts/stdini.py",
                      stdinit.stdenv + "/.stduino/packages/pioenv/Lib/site-packages/platformio/ide/ideini.py")

            elif stdinit.platform_is == "Linux":
                env_path= '"' +stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pip"+ '"'
                cmd = env_path + " install -i https://pypi.tuna.tsinghua.edu.cn/simple -U platformio"
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                for line in iter(proc.stdout.readline, b''):
                    try:
                        s1 = str(line, encoding='gbk')
                    except:
                        s1 =  str(line)
                    # print(s1)
                    if not subprocess.Popen.poll(proc) is None:
                        if line == "":
                            break
                proc.stdout.close()  # pioenv\Lib\site-packages\platformio\package\manager
                regi = stdinit.stdenv + "/.stduino/packages/pioenv/Lib/site-packages/platformio/package/manager/_registry.py"
                self.delete_file(regi)
                copy2(stdinit.abs_path + "/tool/packages/python3/Scripts/stdload.py", regi)

                copy2(stdinit.abs_path + "/tool/packages/python3/Scripts/stdini.py",
                      stdinit.stdenv + "/.stduino/packages/pioenv/Lib/site-packages/platformio/ide/ideini.py")

            elif stdinit.platform_is == "Darwin":
                env_path= '"' +stdinit.stdenv + "/.stduino/packages/pioenv/bin/pip"+ '"'
                cmd = env_path + " install -i https://pypi.tuna.tsinghua.edu.cn/simple -U platformio"
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                for line in iter(proc.stdout.readline, b''):
                    try:
                        s1 = str(line, encoding='gbk')
                    except:
                        s1 = str(line)
                    # print(s1)
                    if not subprocess.Popen.poll(proc) is None:
                        if line == "":
                            break
                proc.stdout.close()  # pioenv\Lib\site-packages\platformio\package\manager
                regi = stdinit.stdenv + "/.stduino/packages/pioenv/lib/python3.8/site-packages/platformio/package/manager/_registry.py"

                self.delete_file(regi)

                copy2(stdinit.abs_path + "/tool/packages/python3/Scripts/stdload.py", regi)

                copy2(stdinit.abs_path + "/tool/packages/python3/Scripts/stdini.py",
                      stdinit.stdenv + "/.stduino/packages/pioenv/lib/python3.8/site-packages/platformio/ide/ideini.py")


            # if res.msg == "1":  # 中
            #     cmd = stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U platformio"
            # else:
            #     cmd = stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pip install -U platformio"

            copy2(stdinit.abs_path + "/tool/packages/pioboards.json",
                  stdinit.stdenv + "/.stduino/packages/pioenv/pioboards.json")
            copy2(stdinit.abs_path + "/tool/packages/stdpio.ini",
                  stdinit.stdenv + "/.stduino/packages/pioenv/stdpio.ini")


            return True
        except:
            stdinit.std_signal_gobal.stdprintln()
    def get_board_v(self):
        try:
            if ((int(time.time()) - int(res.updatetime)) > 586400):
                setup.updatetime(str(int(time.time())))
                r = requests.get("http://api.stduino.com/getvboards")
                if (r.status_code == 200):
                    version_data = json.loads(r.text)
                    if (int(version_data['version_id']) != int(res.version_id)):
                        cmd = "curl -fL https://stduino-generic.pkg.coding.net/stduino_packages/boards/boards.zip?version=latest -o boards.zip"
                        # res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
                        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                        for line in iter(proc.stdout.readline, b''):
                            try:
                                s1 = str(line, encoding='utf8')
                            except:
                                pass
                            if not subprocess.Popen.poll(proc) is None:
                                if line == "":
                                    break
                        proc.stdout.close()
                        cmd = "curl -fL https://stduino-generic.pkg.coding.net/stduino_packages/boards/Custom.zip?version=latest -o Custom.zip"
                        # res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
                        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                        for line in iter(proc.stdout.readline, b''):
                            try:
                                s1 = str(line, encoding='utf8')
                            except:
                                pass
                            if not subprocess.Popen.poll(proc) is None:
                                if line == "":
                                    break
                        proc.stdout.close()
                        try:
                            board_p = stdinit.stdenv + "/.platformio/boards"
                            core_p = stdinit.stdenv + "/.platformio/"
                            board_pin_p = stdinit.stdenv + "/.platformio/packages/framework-arduinoststm32/variants/Custom"
                            core_pin_p = stdinit.stdenv + "/.platformio/packages/framework-arduinoststm32/variants/"
                            if os.path.exists(board_p):
                                self.delete_file(board_p)

                            with zipfile.ZipFile("boards.zip", mode="r") as f:
                                f.extractall(core_p)  # .platformio ##将文件解压到指定目录，解压密码为root
                            if os.path.exists(board_pin_p):
                                self.delete_file(board_pin_p)

                            with zipfile.ZipFile("Custom.zip", mode="r") as f:
                                f.extractall(core_pin_p)  # .platformio ##将文件解压到指定目录，解压密码为root
                        except:
                            stdinit.std_signal_gobal.stdprintln()
                        f.close()
                        if os.path.exists("boards.zip"):
                            self.delete_file("boards.zip")
                        if os.path.exists("Custom.zip"):
                            self.delete_file("Custom.zip")
                        setup.version_id(str(version_data['version_id']))
                pass

        except:
            stdinit.std_signal_gobal.stdprintln()


    def generate_project_main(self):
        try:
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

            src_dir = stdinit.projects_dir +  "stdtest" + "/src"
            main_path = stdinit.projects_dir + "stdtest"+ "/src/main.cpp"
            if os.path.isfile(main_path):
                return True
            if os.path.exists(src_dir):
                pass
            else:
                os.makedirs(src_dir)
            with open(main_path, "w") as fp:
                fp.write(main_content.strip())
            return True
        except:
            stdinit.std_signal_gobal.stdprintln()
    def std_board_init(self):
        try:
            cmd = "curl -fL https://stduino-generic.pkg.coding.net/stduino_packages/boards/boards.zip?version=latest -o boards.zip"
            # res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            for line in iter(proc.stdout.readline, b''):
                try:
                    s1 = str(line, encoding='utf8')
                except:
                    pass
                if not subprocess.Popen.poll(proc) is None:
                    if line == "":
                        break
            proc.stdout.close()
            cmd = "curl -fL https://stduino-generic.pkg.coding.net/stduino_packages/boards/Custom.zip?version=latest -o Custom.zip"
            # res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)  # 使用管道
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            for line in iter(proc.stdout.readline, b''):
                try:
                    s1 = str(line, encoding='utf8')
                except:
                    pass
                if not subprocess.Popen.poll(proc) is None:
                    if line == "":
                        break
            proc.stdout.close()
            try:
                board_p = stdinit.stdenv + "/.platformio/boards"
                core_p = stdinit.stdenv + "/.platformio/"
                board_pin_p = stdinit.stdenv + "/.platformio/packages/framework-arduinoststm32/variants/Custom"
                core_pin_p = stdinit.stdenv + "/.platformio/packages/framework-arduinoststm32/variants/"
                if os.path.exists(board_p):
                    self.delete_file(board_p)

                with zipfile.ZipFile("boards.zip", mode="r") as f:
                    f.extractall(core_p)  # .platformio ##将文件解压到指定目录，解压密码为root
                if os.path.exists(board_pin_p):
                    self.delete_file(board_pin_p)

                with zipfile.ZipFile("Custom.zip", mode="r") as f:
                    f.extractall(core_pin_p)  # .platformio ##将文件解压到指定目录，解压密码为root
            except:
                stdinit.std_signal_gobal.stdprintln()
            f.close()
            if os.path.exists("boards.zip"):
                self.delete_file("boards.zip")
            if os.path.exists("Custom.zip"):
                self.delete_file("Custom.zip")
            r = requests.get("http://api.stduino.com/getvboards")
            if (r.status_code == 200):
                version_data = json.loads(r.text)
                setup.version_id(str(version_data['version_id']))
                setup.updatetime(str(int(time.time())))

        except: 
            stdinit.std_signal_gobal.stdprintln()


    def std_init(self):
        try:
            init_ok = 0
            target_path = stdinit.projects_dir + "stdtest"
            if os.path.exists(target_path):
                self.delete_file(target_path)
                os.makedirs(target_path)
            else:
                os.makedirs(target_path)
            cmd = self.pio_env + " project init -d " + target_path + " --board bluepill_f103c8 -O framework=arduino -O debug_tool=blackmagic"
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            for line in iter(proc.stdout.readline, b''):
                try:
                    s1 = str(line, encoding='gbk')
                except:
                    s1 = str(line)
                # print(s1)
                if not subprocess.Popen.poll(proc) is None:
                    if line == "":
                        break
            proc.stdout.close()  # pioenv\Lib\site-packages\platformio\package\manager
            self.generate_project_main()
            # ststm32 project init
            # cmd="C:/Users/debug/.stduino/packages/pioenv/Scripts/pio" project init -d "C:/Users/debug/Documents/Stduino/Projects/stdtest" --board bluepill_f103c8 -O framework=arduino -O debug_tool=blackmagic
            pass
            cmd = self.pio_env + " run -d " + target_path
            stdinit.std_signal_gobal.std_process(1, "环境初始化")  # complexing
            stdinit.std_signal_gobal.std_echo_msg(0, "第一次启动，软件正在初始化,请稍等片刻~")
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            for line in iter(proc.stdout.readline, b''):
                try:
                    s1 = str(line, encoding='gbk')
                    # if "SUCCESS" in s1:
                    #     init_ok=1
                except:
                    s1 = str(line)
                if not subprocess.Popen.poll(proc) is None:
                    if line == "":
                        break
            proc.stdout.close()  # pioenv\Lib\site-packages\platformio\package\manager
            if init_ok == 1:
                pass
            self.std_board_init()
            stdinit.std_signal_gobal.std_process(0, "初始化完成")  # complexing
            stdinit.std_signal_gobal.std_echo_msg(0, "初始化完成，若在使用过程中遇到问题，欢迎随时至www.stduino.com进行发帖交流！")

            # copy2(stdinit.abs_path + "/tool/packages/stdinit/pioboards.json",
            #       stdinit.stdenv + "/.stduino/packages/pioenv/pioboards.json")
            # copy2(stdinit.abs_path + "/tool/packages/stdpio.ini",
            #       stdinit.stdenv + "/.stduino/packages/pioenv/stdpio.ini")

            # "C:/Users/debug/.stduino/packages/pioenv/Scripts/pio" run -d "C:/Users/debug/Documents/Stduino/Projects/stdtest"
            # project run
            # Building.pio\build\bluepill_f103c8\firmware.bin
            # SUCCESS
            pass
            # copy stdfile——》plaforms&packages
            pass
        except:
            stdinit.std_signal_gobal.std_process(0, "初始化失败")  # complexing
            stdinit.std_signal_gobal.std_echo_msg(0, "初始化失败，请重启后再次进行初始化，欢迎随时至www.stduino.com进行发帖交流！")


    def all_inits(self):
        try:
            if self.check_net() == False:
                return False
            stm32_platpath = stdinit.stdenv + "/.platformio/platforms/ststm32"
            stm32_frampath = stdinit.stdenv + "/.platformio/packages/framework-arduinoststm32"
            if self.pio_install():
                if os.path.exists(stm32_platpath):
                    if os.path.exists(stm32_frampath):
                        board_p = stdinit.stdenv + "/.platformio/boards"
                        if os.path.exists(board_p):
                            self.get_board_v()
                        else:
                            self.std_board_init()
                    else:
                        self.std_init()
                    pass
                else:
                    self.std_init()
            self.get_board_v()
        except:
            pass

    def all_init(self):
        t1 = threading.Thread(target=self.all_inits, name='all_inits')
        t1.setDaemon(True)
        t1.start()  # File_tree_init



    #     if os.path.exists(stdenv):
    #         pass
    #     else:
    #         os.makedirs(stdenv)
    def pio_install(self):
        try:

            if self.is_installed_pio() == False:

                if self.check_net()==False:
                    return False

                if self.is_init_pioenv() == False:

                    self.pioenv_init()
                    self.install_pio()
                    return True
                else:
                    self.install_pio()
                    return True

            return True
        except:
            stdinit.std_signal_gobal.stdprintln()
            return False

        #self.pip_fast()
        # if os.environ["USERPROFILE"]+"/pip":

        #     pass

    def remove_readonly(self,func, path, _):
        try:
            # "Clear the readonly bit and reattempt the removal"
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def delete_file(self,path):
        try:
            if os.path.isdir(path):
                try:
                    rmtree(path, onerror=self.remove_readonly)
                except:
                    stdinit.std_signal_gobal.stdprintln()
                    # self.listwidget.append("Delete error:" + "\n 请手动至该文件夹处删除\nPlease manually delete to this folder")
                    # self.add_lib_si(python3, 0, "Unexpected error:" + "\n 请手动至该文件夹处删除\nPlease manually delete to this folder")
                    # QMessageBox.warning(self, "Delete error",
                    #                     "Unexpected error:" + "\n 请手动至该文件夹处删除\nPlease manually delete to this folder",
                    #                     QMessageBox.Yes)
                    pass
            else:
                try:
                    os.remove(path)
                except:
                    try:
                        # shutil.rmtree(path, onerror=self.remove_readonly)
                        os.chmod(path, stat.S_IWRITE)
                        os.remove(path)
                    except:
                        stdinit.std_signal_gobal.stdprintln()
                pass
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()

    def pio_uninstall(self):
        try:
            if self.is_init_pioenv() == False:
                pass
            else:
                try:
                    self.delete_file(stdinit.stdenv + "/.stduino/packages/pioenv")
                    return True
                except:
                    stdinit.std_signal_gobal.stdprintln()
                    return False

        except:
            stdinit.std_signal_gobal.stdprintln()

    def pio_test(self):
        try:
            print(stdinit.board)
            stdinit.board = "ddds"
        except:
            stdinit.std_signal_gobal.stdprintln()


if __name__ == '__main__':  # main函数
    pass
    #PioInstall() langeage 工作目录需在test里进行测试
    # get_board_v()





