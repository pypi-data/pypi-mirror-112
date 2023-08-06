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
config_p=stdenv+"/.stduino/session/config.cfg"
if os.path.exists(config_p):
    pass
else:
    config_p="./appearance/config.cfg"
cf.read(config_p)  # 读取配置文件内容

#此处读出的均为字符串

version_id=cf.get('default_c', 'version_id')
keywordversion_id=cf.get('default_c', 'keywordversion_id')
boardversion_id=cf.get('default_c', 'boardversion_id')
updateversion_id=cf.get('default_c', 'updateversion_id')
updatetime=cf.get('default_c', 'updatetime')

creatshortcut= cf.get('language', 'st1')  # 返回_a章节里面key为a_key2的值，返回为int类型

#test
#xyz=zh_hans.xyz

#img
#pathstaus2


