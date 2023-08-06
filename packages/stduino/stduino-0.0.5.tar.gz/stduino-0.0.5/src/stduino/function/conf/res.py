# -*- coding: utf-8 -*-
#import appearance.language.zh_hans

#import appearance.language.en

import os
import configparser
from platform import system
stdenv = None
if system() == "Windows" or system() == "cli":

    stdenv = os.environ["USERPROFILE"].replace('\\', '/')

elif system() == "Linux":

    stdenv = os.environ["HOME"].replace('\\', '/')

elif system() == "Darwin":

    stdenv = os.environ["HOME"].replace('\\', '/')
cf =configparser.ConfigParser()
config_p=stdenv+"/.stduino/session/mainconfig.cfg"
if os.path.exists(config_p):
    pass
else:
    config_p="./appearance/mainconfig.cfg"
cf.read(config_p)  # 读取配置文件内容



msg= cf.get('language', 'msg')  # 返回_a章节里面key为a_key2的值，返回为int类型
lastfile=cf.get('filepath', 'lastfile')  # 返回_a章节里面key为a_key2的值，返回为int类型
stdtype=cf.get('std_type', 'stdtype')
download_type=cf.get('std_type', 'download_type')

try:
    std_auto = int(cf.get('std_type', 'std_auto'))
except:

    cf.set("std_type", "std_auto", "1")  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中
    std_auto = 1
gbk_type=cf.get('gbk_utf', 'type')


#此处读出的均为字符串
default_c=int(cf.get('default_c', 'c'))
#pathstaus=int(cf.get('path', 'staus'))
# pathstaus2=cf.get('path', 'staus2')
version_id=cf.get('default_c', 'version_id')
keywordversion_id=cf.get('default_c', 'keywordversion_id')
boardversion_id=cf.get('default_c', 'boardversion_id')
updateversion_id=cf.get('default_c', 'updateversion_id')
updatetime=cf.get('default_c', 'updatetime')
creatshortcut= cf.get('language', 'st1')  # 返回_a章节里面key为a_key2的值，返回为int类型

if default_c==0:
    default_main = cf.get('defaultd_style', 'main')
    default_text = cf.get('defaultd_style', 'text')
    default_comment = cf.get('defaultd_style', 'comment')
    default_font = cf.get('defaultd_style', 'font')
    default_mainkey1 = cf.get('defaultd_style', 'mainkey1')
    default_mainkey2 = cf.get('defaultd_style', 'mainkey2')
    default_kh = cf.get('defaultd_style', 'kh')
    default_zh_hans = cf.get('defaultd_style', 'zh_hans')
    default_num = cf.get('defaultd_style', 'num')
    default_include = cf.get('defaultd_style', 'include')
elif default_c==1:
    default_main = cf.get('defaultl_style', 'main')
    default_text = cf.get('defaultl_style', 'text')
    default_comment = cf.get('defaultl_style', 'comment')
    default_font = cf.get('defaultl_style', 'font')
    default_mainkey1 = cf.get('defaultl_style', 'mainkey1')
    default_mainkey2 = cf.get('defaultl_style', 'mainkey2')
    default_kh = cf.get('defaultl_style', 'kh')
    default_zh_hans = cf.get('defaultl_style', 'zh_hans')
    default_num = cf.get('defaultl_style', 'num')
    default_include = cf.get('defaultl_style', 'include')
else :
    default_main = cf.get('personal_style', 'main')
    default_text = cf.get('personal_style', 'text')
    default_comment = cf.get('personal_style', 'comment')
    default_font = cf.get('personal_style', 'font')
    default_mainkey1 = cf.get('personal_style', 'mainkey1')
    default_mainkey2 = cf.get('personal_style', 'mainkey2')
    default_kh = cf.get('personal_style', 'kh')
    default_zh_hans = cf.get('personal_style', 'zh_hans')
    default_num = cf.get('personal_style', 'num')
    default_include = cf.get('personal_style', 'include')

#test
#xyz=zh_hans.xyz

#img
#pathstaus2

# import getpass
# from function.conf import setup

# path = getpass.getuser()

# if path != pathstaus2:
#     creatshortcut = cf.get('language', 'st0')  # 返回_a章节里面key为a_key2的值，返回为int类型
#
#
#     pos = os.path.abspath('.').replace("\\","/")
#     library = pos + "/tool/Documents/libraries"
#     projects = pos + "/tool/Documents/projects"
#     setup.library(library)
#     setup.projects(projects)
#     setup.paths2(path)
#     pass
# else:
#     library = cf.get('path', 'library')
#     projects = cf.get('path', 'projects')
#     pass

img_fileclose = 'appearance/img/fileclose.png'
img_complex = 'appearance/img/img_complex3.png'
img_uploadfast = 'appearance/img/img_uploadfast.png'
img_upload = 'appearance/img/img_upload.png'
img_back = 'appearance/img/img_back.png'
img_forward = 'appearance/img/img_forward.png'
img_search = 'appearance/img/img_search.png'
img_save = 'appearance/img/img_save.png'
img_saveall = 'appearance/img/img_saveall.png'
img_open = 'appearance/img/img_open.png'
img_addfile = 'appearance/img/img_addfile.png'
img_serial = 'appearance/img/img_serial.png'
img_serialp = 'appearance/img/img_serialp.jpg'
img_clean = 'appearance/img/img_clean.png'
img_msg = 'appearance/img/img_msg.png'
img_help = 'appearance/img/img_help.png'
img_web = 'appearance/img/img_web.png'
img_about = 'appearance/img/img_about.png'
img_setup = 'appearance/img/img_setup.png'
img_fold = 'appearance/img/img_fold.png'
img_exit = 'appearance/img/img_exit.png'
img_lib = 'appearance/img/img_lib.png'
img_lib_file = 'appearance/img/img_lib_file.png'
img_feedback = 'appearance/img/feedback.png'
img_library='appearance/img/library2.png'
img_library_add='appearance/img/library_add.png'
img_library_fold='appearance/img/library_fold.png'
img_example='appearance/img/example.png'
img_projects='appearance/img/img_projects.png'
img_projects2='appearance/img/img_projects2.png'
img_platform='appearance/img/platform.png'
img_package='appearance/img/package.png'
img_pio='appearance/img/piofavicon.ico'
img_heart='appearance/img/good.svg'
img = 'appearance/img/st.PNG'