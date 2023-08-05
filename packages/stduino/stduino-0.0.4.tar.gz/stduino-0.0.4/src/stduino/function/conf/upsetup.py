# -*- coding: utf-8 -*-

import configparser
import os
from shutil import copy2

abs_path = os.path.abspath('.').replace('\\', '/')
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
    session_dir = stdenv + "/.stduino/session"
    if os.path.exists(session_dir):
        copy2(abs_path + "/appearance/config.cfg", stdenv + "/.stduino/session/config.cfg")
        copy2(abs_path + "/appearance/mainconfig.cfg", stdenv + "/.stduino/session/config.cfg")
    else:
        os.makedirs(session_dir)
    copy2(abs_path + "/appearance/config.cfg", stdenv + "/.stduino/session/config.cfg")
    copy2(abs_path + "/appearance/mainconfig.cfg", stdenv + "/.stduino/session/config.cfg")


cf.read(config_p)  # 读取配置文件内容

def changemsg(msg):
    cf.set("language", "msg",msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中
def version_id(msg):
    cf.set("default_c", "version_id", msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中
def updatetime(msg):
    cf.set("default_c", "updatetime", msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中
def updateversion_id(msg):
    cf.set("default_c", "updateversion_id", msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中
def std_type(msg):
    cf.set("std_type", "stdtype",msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中
def download_type(msg):
    cf.set("std_type", "download_type",msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中

def save_mstyle(msg):
    cf.set("personal_style", "main", msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中

def save_tstyle(msg):
    cf.set("personal_style", "text", msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中

def save_cstyle(msg):
    cf.set("personal_style", "comment", msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中

def save_confirm(msg):
    cf.set("default_c", "c", msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中

def save_tfont(msg):
    cf.set("personal_style", "font",msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中
def save_4style(msg):
    cf.set("personal_style", "mainkey1", msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中
def save_5style(msg):
    cf.set("personal_style", "mainkey2", msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中
def save_6style(msg):
    cf.set("personal_style", "kh", msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中
def save_7style(msg):
    cf.set("personal_style", "zh_hans", msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中
def save_8style(msg):
    cf.set("personal_style", "num", msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中
def save_9style(msg):
    cf.set("personal_style", "include", msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中
def paths(msg):
    cf.set("path", "staus",msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中
def gbk_type(msg):
    cf.set("gbk_utf", "type",msg)  # 章节a里面添加一个key为b_key3，值为new-$r，如果key存在就更新key的值
    cf.write(open(config_p, "w"))  # 把修改写入到文件test.conf中


