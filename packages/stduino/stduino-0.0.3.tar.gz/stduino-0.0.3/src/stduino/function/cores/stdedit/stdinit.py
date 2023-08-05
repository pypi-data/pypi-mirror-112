# -*- coding: utf-8 -*-

"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

#global var
from function.cores.stdedit.stdsignals import StdSinal
import os
from shutil import copy2
from function.conf import configparser3
from platform import system
platform_is=None
stdenv = None
if system() == "Windows" or system() == "cli":
    platform_is="Win"
    stdenv = os.environ["USERPROFILE"].replace('\\', '/')

    username = os.environ['USERNAME']
elif system() == "Linux":
    platform_is="Linux"
    stdenv = os.environ["HOME"].replace('\\', '/')
    username = os.environ['USERNAME']
    # ctags_path = stdinit.abs_path + "/tool/packages/ctagslin32/"
elif system() == "Darwin":
    platform_is = "Darwin"
    stdenv = os.environ["HOME"].replace('\\', '/')
    username = os.environ['USER']

abs_path = os.path.abspath('.').replace('\\', '/')



projects_dir=stdenv+"/Documents/Stduino/Projects/"
#print(os.environ.keys())

# patherror = ''
# for char in stdenv:
#     if u'\u4e00' <= char <= u'\u9fa5':  # 判断是否是汉字，在isalpha()方法之前判断
#         patherror = patherror + char
# if patherror!="":
#     stdenv = "C:/Stduino"
#     if os.path.exists(stdenv):
#         pass
#     else:
#         os.makedirs(stdenv)

try:
    if os.path.exists(projects_dir):
        pass
    else:
        os.makedirs(projects_dir)

except:
    pass
session_dir=stdenv + "/.stduino/session"
try:
    if os.path.exists(session_dir):
        pass
    else:
        os.makedirs(session_dir)
        copy2(abs_path + "/appearance/config.cfg", stdenv + "/.stduino/session/config.cfg")
        copy2(abs_path + "/appearance/mainconfig.cfg", stdenv + "/.stduino/session/mainconfig.cfg")
        copy2(abs_path + "/tool/packages/other/comment", stdenv + "/.stduino/session/comment")
except:
    pass
#edit
auto_key_l=0
auto_key_list=[]
#IDE
version_c = "1.10.5"#'1.01'

#ui
savefileAction_staus=False
saveallAction_staus=False
forwardAction_staus=False
backAction_staus=False

#signal
std_signal_gobal=StdSinal()
thread_callch=0
#sub ui
File_tree_view=None
Std_Serial_Tool1= None
Std_Serial_Tool2= None
Set_Back_Color1=None
Std_makeboards=None
Std_Make=None
Std_Find=None
find_boards=None
device=None
std_make_board=None
#project
pio_boards=None
board_id=""
current_board=None
current_upload_m=None
upload_meds = []
profile_modify_ui=[]
profile_modify_all=[]
project_name=None#new_workspace=stdinit.pro_dir_name
pro_dir_name=None#old_workfpace=stdinit.pro_dir_name

#debug&goto
serialnumber=[]
last_com="None"
debug_mark_start = 0
manual_mark=[]
mark_object=[]
framework=None
platform=None
goto_platform_name=None
goto_init=None#.Instance
pro_conf=configparser3.ConfigParser()
init_path = None#platformio.ini
#plug
Pio_install=None
Piopalt_install=None
package_choose_name=""
plat_choose_name=""
#相关主目录
Std_help=None








