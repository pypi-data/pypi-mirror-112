import os
import subprocess
import time
import json
import sqlite3
from PyQt5.QtCore import QObject
from function.cores.stdedit import stdinit
# from function.cores.stdauto.Singleton import Singleton
import threading

'''================================================================================'''
'''|                               CTAGS PARSER                                   |'''
'''================================================================================'''


# @Singleton
class Ctags_parser(QObject):

    def __init__(self, parent=None):
        super(Ctags_parser, self).__init__(parent)

        try:
            self.json_string = None
            self.json_data = None
            self.conn = None
            self.cursor = None
            stdinit.std_signal_gobal.jump_init.connect(self.go_jump_iit)
        except:
            stdinit.std_signal_gobal.stdprintln()
        #self.build_ctags()


    ''''''
    def init_tags(self):
        try:
            platform_tags = stdinit.stdenv + "/.stduino/session/tags/" + stdinit.platform + stdinit.framework + ".tag"
            p_tags = stdinit.stdenv + "/.stduino/session/tags"
            if os.path.exists(p_tags):
                pass
            else:
                os.makedirs(p_tags)
            if os.path.exists(platform_tags):
                self.deledatabase()
                self.bulid_ctags_database2(platform_tags)
            else:

                platform_json_path = stdinit.stdenv + "/.platformio/platforms/" + stdinit.platform + "/platform.json"
                # print(platform_json_path)
                if os.path.exists(platform_json_path):
                    fo = open(platform_json_path, mode='r', encoding='UTF-8')
                    st = fo.read()
                    fo.close()
                    psd = json.loads(st)

                    frame_name = psd["frameworks"]["arduino"]["package"]

                    frame_path = stdinit.stdenv + "/.platformio/packages/" + frame_name + "/cores"
                    if os.path.exists(frame_path):
                        self.deledatabase()
                        self.build_ctags1(platform_tags, frame_path)

        except:
            stdinit.std_signal_gobal.stdprintln()

    def go_jump_iit(self):
        try:
            t1 = threading.Thread(target=self.init_tags, name='init_tags' + stdinit.platform)
            t1.setDaemon(True)
            t1.start()  #
        except:
            stdinit.std_signal_gobal.stdprintln()
        #print(t1)



    def build_ctags1(self,platform_tags,path):#ctags -x --c-types=f   tree-1.6.0/tree.c
        try:
            #print("ctags_path")
            #print(ctags_path)
            # os.chdir("C:/Users/debug/.platformio/packages/framework-arduinoststm32/cores")
            # r0=time.time()
            #ctags_path = None
            # print("Launching ctags on: " + path)
            # r0 = time.time()#C:\Users\debug\.platformio\packages\framework-arduino-gd32v\cores
            if stdinit.platform_is == "Win":
                ctags_path = stdinit.abs_path + "/tool/packages/ctagswin32/"

            elif stdinit.platform_is == "Linux":
                pass


            elif stdinit.platform_is == "Darwin":
                pass

            else:
                print("Cannot indentify platform: " + stdinit.platform_is)
                ctags_path = None

            if os.path.exists(ctags_path) == False:

                return 0
            #print(ctags_path)

            #cmd = "ctags -R --output-format=json --fields=+n --c-types=+l " + '"' + path + '"'  # C:/Users/debug/.platformio/packages/framework-arduino-gd32v/cores"#C:/Users/debug/.platformio/packages/framework-arduinoststm32/cores"

            cmd = ctags_path + "ctags -R --output-format=json --fields=+n --c-types=+l " + '"' + path + '"'   # C:/Users/debug/.platformio/packages/framework-arduino-gd32v/cores"#C:/Users/debug/.platformio/packages/framework-arduinoststm32/cores"
            # cmd="C:/Users/debug/Documents/Stduino/ctags32/ctags --output-format=json ctags -I __THROW –file-scope=yes –langmap=c:+.h –languages=c,c++ –links=yes –c-kinds=+p --fields=+S -R C:/Users/debug/.platformio/packages/framework-arduinoststm32/cores*"
            proc = subprocess.Popen(cmd,
                                    stdout=subprocess.PIPE, shell=True)
            # proc = subprocess.Popen(["C:/Users/debug/Documents/Stduino/ctags32/ctags", "-R", "--output-format=json",
            #                          "--fields=+n", "--c-types=+l","C:/Users/debug/.platformio/packages/framework-arduinoststm32/cores"],
            #                         stdout=subprocess.PIPE, shell=True)

            time.sleep(0.1)
            #print("Waiting for ctags to finish")
            time.sleep(0.1)
            # r1 = time.time()
            # print(r1-r0)
            # print(proc.communicate()[0])
            # print(proc.communicate())
            # fo = open("./appearance/stduino_json/personal.json", mode='r', encoding='UTF-8')
            # st = fo.read()
            # fo.close()  # cmd_args["cmd_rtlib"]
            self.json_string = (proc.communicate()[0]).decode('utf-8')
            # print(self.json_string)
            # print("")
            # print("")

            self.build_ctags_database(platform_tags)
        except:
            stdinit.std_signal_gobal.stdprintln()



    ''''''
    def bulid_ctags_database2(self,platform_tags):
        try:

            try:

                fo = open(platform_tags, mode='r', encoding='UTF-8')
                st = fo.read()
                fo.close()
                self.json_data = json.loads(st)


            except:
                stdinit.std_signal_gobal.stdprintln()

            self.conn = sqlite3.connect(":memory:",check_same_thread=False)

            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                       CREATE TABLE IF NOT EXISTS main
                       (_type TEXT, name TEXT, path TEXT, pattern TEXT, line TEXT,
                       typeref TEXT, kind TEXT, scope TEXT, scopeKind TEXT)
                   """)

            for entry in self.json_data:
                # print(entry)

                self.cursor.execute("""
                       INSERT INTO main
                       (_type, name, path, pattern, line, typeref, kind, scope, scopeKind)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                    (entry["_type"] if "_type" in entry else None,
                                     entry["name"] if "name" in entry else None,
                                     entry["path"] if "path" in entry else None,
                                     entry["pattern"] if "pattern" in entry else None,
                                     entry["line"] if "line" in entry else None,
                                     entry["typeref"] if "typeref" in entry else None,
                                     entry["kind"] if "kind" in entry else None,
                                     entry["scope"] if "scope" in entry else None,
                                     entry["scopeKind"] if "scopeKind" in entry else None
                                     )
                                    )
        except:
            stdinit.std_signal_gobal.stdprintln()

    def build_ctags_database(self,platform_tags):
        try:
            self.json_string = self.json_string.replace("}\r\n", "},\r\n")
            self.json_string = "[" + self.json_string + "]"
            self.json_string = self.json_string.replace("},\r\n]", "}\r\n]")

            try:
                #print(self.json_string)
                fo = open(platform_tags, "w+", encoding='UTF-8')
                fo.write(self.json_string)
                fo.close()
                self.json_data = json.loads(self.json_string)

            except:
                stdinit.std_signal_gobal.stdprintln()

            self.conn = sqlite3.connect(":memory:",check_same_thread=False)

            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                       CREATE TABLE IF NOT EXISTS main
                       (_type TEXT, name TEXT, path TEXT, pattern TEXT, line TEXT,
                       typeref TEXT, kind TEXT, scope TEXT, scopeKind TEXT)
                   """)

            for entry in self.json_data:
                # print(entry)

                self.cursor.execute("""
                       INSERT INTO main
                       (_type, name, path, pattern, line, typeref, kind, scope, scopeKind)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                    (entry["_type"] if "_type" in entry else None,
                                     entry["name"] if "name" in entry else None,
                                     entry["path"] if "path" in entry else None,
                                     entry["pattern"] if "pattern" in entry else None,
                                     entry["line"] if "line" in entry else None,
                                     entry["typeref"] if "typeref" in entry else None,
                                     entry["kind"] if "kind" in entry else None,
                                     entry["scope"] if "scope" in entry else None,
                                     entry["scopeKind"] if "scopeKind" in entry else None
                                     )
                                    )
        except:
            stdinit.std_signal_gobal.stdprintln()




        ###

    ''''''

    def get_symbol_kind(self, name):
        try:
            data = None
            try:
                self.cursor.execute("SELECT name,kind FROM main WHERE name = \"{n}\"".format(n=name))
                data = self.cursor.fetchone()
            except:
                pass

            if data is None:
                return ("", "")
            else:
                return (data[0], data[1])  # 自动补全功能，返回的数据是否可重复利用
        except:
            pass

        ###

    ''''''


    def where_to_jump(self, name):
        try:




            self.cursor.execute("SELECT path,line FROM main WHERE name = \"{n}\"".format(n=name))
            data =self.cursor.fetchone()


        except:
            stdinit.std_signal_gobal.stdprintln()
        try:
            if data == None:
                return ("0", "0")
            else:
                return data
        except:
            stdinit.std_signal_gobal.stdprintln()


        ###

    ''''''
    def deledatabase(self):
        try:
            if self.conn is not None:
                self.conn.commit()
                self.conn.close()
        except:
            stdinit.std_signal_gobal.stdprintln()
    def __del__(self):
        try:
            if self.conn is not None:
                self.conn.commit()
                self.conn.close()
        except:
            stdinit.std_signal_gobal.stdprintln()
        #print("Database closed")

    ''''''


'''=== end Class ==='''