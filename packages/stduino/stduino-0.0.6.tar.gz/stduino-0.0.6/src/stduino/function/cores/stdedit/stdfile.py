# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


#import zipfile  # 解压文件
import shutil  # 用于压缩
import stat,os
# from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication,QInputDialog,QTreeWidget,QFileIconProvider,QTreeWidgetItem,QLineEdit,QMessageBox,QVBoxLayout,QWidget,QAction,QMenu,QAbstractItemView,QFileDialog

from PyQt5.QtCore import QFileInfo,Qt,QSize,pyqtSignal
from PyQt5.QtGui import QIcon,QCursor, QBrush
from function.conf import res
from function.cores.stdmsg import reso
# 文件监控
import json
from function.cores.stdedit import stdinit
from watchdog.events import FileSystemEventHandler
import threading
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff
# from function import process
# dsd = process.ProgressBar_start() #启动第一时间无法保证显示
from watchdog.observers import Observer
import subprocess
# 文件夹监控
class StdPathHandler(FileSystemEventHandler,QWidget):
    # trigger = pyqtSignal(int, str)  # 0 settext 1 appead 3process
    my_signal = pyqtSignal(int, str, str)


    def __init__(self):
        super(StdPathHandler, self).__init__()

        try:
            aim_path = stdinit.projects_dir.replace("/Projects/", "")
            stdinit.std_signal_gobal.work_space.connect(self.workspace_change)
            self.brush_red = QBrush(Qt.red)
            self.brush_white = QBrush(Qt.white)
            # self.trigger.emit(1, reso.row_line + str(Digit) + '/' + s2[it:])
            #self.my_signal.connect(parent.my_signal.emit)

            self.aim_path = aim_path
            self.dic_name = ""
            self.timer = None
            self.observer = Observer()
            self.observer.schedule(self, aim_path, True)
            self.observer.start()

            t1 = threading.Thread(target=self.init_p, name='init_p')
            t1.setDaemon(True)
            t1.start()  # File_tree_init


            self.setWindowTitle('Stduino Project')
            self.tree = QTreeWidget(self)

            self.tree.setHeaderHidden(True)
            # self.tree.clicked.connect(self.onTreeClicked)
            self.tree.doubleClicked.connect(self.ondoubleClicked)

            # 给树状文件列表添加右键菜单
            self.tree.setContextMenuPolicy(Qt.CustomContextMenu)  # 开放右键策略
            self.tree.customContextMenuRequested.connect(self.OnTreeRightMenuShow)  # 关联右键槽函数
            self.mainLayout = QVBoxLayout(self)
            #self.init_open()







            # self.Open_Folder()
            # from function.filetree import TreeExplorer
            # file_explorer =TreeExplorer(None)
            # print(os.getcwd())
            # file_explorer.display_directory("C:/stwork/stdemo2019827/dist/Stduino/main/tool","C:/stwork/stdemo2019827/dist/Stduino/main/tool")#os.getcwd())
            # file_explorer.open_file_signal.connect(self.open_file)
            # file_explorer.icon_manipulator.set_icon(
            #     file_explorer,
            #     'tango_icons/system-show-cwd-tree-blue.png'
            #     # functions.create_icon(
            #     #     'tango_icons/system-show-cwd-tree-blue.png'
            #     # )
            # )
            # self.mainLayout.addWidget(file_explorer)#test
            self.setLayout(self.mainLayout)
        except:
            stdinit.std_signal_gobal.stdprintln()

            #QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile00036！\n You can search it in stduino.com",QMessageBox.Yes)



    def init_p(self):
        try:
            self.snapshot = DirectorySnapshot(self.aim_path)
            self.init_open()
        except:
            stdinit.std_signal_gobal.stdprintln()



    # def work_sp(self):
    #     self.workspace_change()



    def on_any_event(self, event):
        try:

            if self.timer:
                self.timer.cancel()
            self.timer = threading.Timer(0.5, self.checkSnapshot)
            self.timer.start()

        except:
            stdinit.std_signal_gobal.stdprintln()


    def dir_created(self, r_path):

        try:
            for path in r_path:

                path = path.replace('\\', '/')
                #print(path)
                fileInfo = QFileInfo(path)
                fileIcon = QFileIconProvider()
                icon = QIcon(fileIcon.icon(fileInfo))
                c_file = path.split("/")
                c_name = c_file[-1]
                c_file[-1] = ""
                new_len = c_file[-2]
                # old_p=c_file.index(self.dic_name)
                postion = c_file.count(new_len) - 1
                ####### f_word = "^" + new_len + "[\w|\W]*"
                # root_item = self.tree.findItems(new_len, Qt.MatchExactly | Qt.MatchRecursive, 0)[postion]  # 第一个0是第几列的意思，本树仅一列，但递归有多个
                #
                # child = QTreeWidgetItem(root_item)
                #
                # # c_name=c_file[-1]
                # child.setText(0, c_name)
                # child.setData(0, Qt.UserRole + 1, path)
                # child.setIcon(0, QIcon(icon))
                # if ".ino" in c_name:
                #
                #     child.setIcon(0, QIcon("appearance/img/img_ino.png"))
                # elif ".cpp" in c_name:
                #
                #     child.setIcon(0, QIcon("appearance/img/img_cpp.png"))
                # elif ".h" in c_name:
                #
                #     child.setIcon(0, QIcon("appearance/img/img_h.png"))
                # elif ".c" in c_name:
                #     child.setIcon(0, QIcon("appearance/img/img_c.png"))
                # elif os.path.isdir(path):
                #     child.setIcon(0, QIcon("appearance/img/img_folder.png"))
                # else:
                #     icon = QIcon(fileIcon.icon(fileInfo))
                #     child.setIcon(0, QIcon(icon))
        except:
            stdinit.std_signal_gobal.stdprintln()
            #QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile00037！\n You can search it in stduino.com",QMessageBox.Yes)
    def tags_uploads(self):
        try:
            init_path = stdinit.init_path
            stdinit.pro_conf.clear()
            stdinit.pro_conf.read(init_path, encoding="utf-8")  # python3
            i = 0
            try:
                ii = len(stdinit.pro_conf.sections())

                if ii>0:
                    for i in range(ii):

                        if "env:" in stdinit.pro_conf.sections()[i]:
                            break
                else:
                    return 0
            except:
                stdinit.std_signal_gobal.stdprintln()
                return 0

            try:
                stdinit.framework = stdinit.pro_conf.get(stdinit.pro_conf.sections()[i], "framework")
            except:
                return 0
            try:
                current_boardn = stdinit.pro_conf.get(stdinit.pro_conf.sections()[i], "board")
            except:
                return 0
            try:
                platformnew = stdinit.pro_conf.get(stdinit.pro_conf.sections()[i], "platform")
            except:
                return 0

            # try:
            #     stdinit.last_com = stdinit.pro_conf.get(stdinit.pro_conf.sections()[i], "upload_port")
            # except:
            #     stdinit.last_com = "None"
            #     pass
            try:
                stdinit.current_upload_m = stdinit.pro_conf.get(stdinit.pro_conf.sections()[i], "upload_protocol")
            except:
                stdinit.current_upload_m = None
                pass

            if stdinit.platform == None:
                # print(253)

                if stdinit.framework == "arduino":
                    stdinit.platform = platformnew
                    if stdinit.platform_is == "Win":
                        stdinit.std_signal_gobal.std_jump_init()
                    elif stdinit.platform_is == "Linux":
                        pass
                    elif stdinit.platform_is == "Darwin":
                        pass

            else:
                if stdinit.platform == platformnew:
                    pass
                else:
                    if stdinit.framework == "arduino":
                        stdinit.platform = platformnew
                        if stdinit.platform_is == "Win":
                            stdinit.std_signal_gobal.std_jump_init()
                        elif stdinit.platform_is == "Linux":
                            pass
                        elif stdinit.platform_is == "Darwin":
                            pass

                        # stdinit.std_signal_gobal.std_jump_to_look_iit()
                        # stdinit.goto_init.go_jump_iit()
                        # print(254)
            if stdinit.current_board == current_boardn:
                pass
            else:
                upload_p = stdinit.stdenv + "/.platformio/boards/"  + current_boardn + ".json"
                if os.path.exists(upload_p):
                    stdinit.upload_meds.clear()
                    stdinit.current_board = current_boardn
                    fo = open(upload_p, mode='r', encoding='UTF-8')
                    st = fo.read()
                    fo.close()
                    psd = json.loads(st)
                    try:
                        upload_medd = psd["upload"]["protocol"]
                    except:
                        upload_medd = "Default"
                    try:
                        stdinit.upload_meds = psd["upload"]["protocols"]
                    except:
                        stdinit.upload_meds.append("Default")

                    if stdinit.current_upload_m == None:
                        if upload_medd == "Default":
                            stdinit.current_upload_m = upload_medd
                        else:
                            stdinit.pro_conf.set(stdinit.pro_conf.sections()[i], "upload_protocol", upload_medd)
                            stdinit.current_upload_m = upload_medd
                            stdinit.pro_conf.write(open(init_path, 'w'))
                    stdinit.std_signal_gobal.std_upload_list_change()
                else:
                    upload_p = stdinit.stdenv + "/.platformio/platforms/" + platformnew + "/boards/" + current_boardn + ".json"
                    if os.path.exists(upload_p):
                        stdinit.upload_meds.clear()
                        stdinit.current_board = current_boardn
                        fo = open(upload_p, mode='r', encoding='UTF-8')
                        st = fo.read()
                        fo.close()
                        psd = json.loads(st)
                        try:
                            upload_medd = psd["upload"]["protocol"]
                        except:
                            upload_medd = "Default"
                        try:
                            stdinit.upload_meds = psd["upload"]["protocols"]
                        except:
                            stdinit.upload_meds.append("Default")

                        if stdinit.current_upload_m == None:
                            if upload_medd == "Default":
                                stdinit.current_upload_m = upload_medd
                            else:
                                stdinit.pro_conf.set(stdinit.pro_conf.sections()[i], "upload_protocol", upload_medd)
                                stdinit.current_upload_m = upload_medd
                                stdinit.pro_conf.write(open(init_path, 'w'))

                        stdinit.std_signal_gobal.std_upload_list_change()
                    pass


        except:
            stdinit.std_signal_gobal.stdprintln()

    def workspace_change(self):

        try:
            work_path = stdinit.projects_dir
            old_workfpace = stdinit.pro_dir_name
            new_workspace = stdinit.project_name

            # 开启新工作空间
            # print("new_workspace"+new_workspace)
            # print("old_workfpace " + old_workfpace )
            if old_workfpace == new_workspace:
                return 0

            root_item = self.tree.findItems(new_workspace, Qt.MatchExactly | Qt.MatchRecursive, 0)
            f_len = len(root_item)
            # print(c_path)
            root_item_id = None
            #print(new_workspace)

            if f_len > 1:
                #print("new2"+new_workspace)
                for i in range(f_len):
                    if work_path + new_workspace == root_item[i].data(0, Qt.UserRole + 1):
                        root_item_id = root_item[i]
                        # print(root_item[i].data(0, Qt.UserRole + 1))
                pass
            elif f_len == 1:
                #print("new1" + new_workspace)
                if work_path + new_workspace == root_item[0].data(0, Qt.UserRole + 1):
                    root_item_id = root_item[0]
                    pass
            else:
                #print("new3" + new_workspace)
                return 0

            if root_item_id != None:
                dir_is=stdinit.projects_dir + stdinit.project_name
                if os.path.isdir(dir_is):
                    # root_item_id.setBackground(0,brush_red)
                    root_item_id.setForeground(0, self.brush_red)
                    root_item_id.setToolTip(0, "Working~")
                    root_item_id.setIcon(0, QIcon("appearance/img/run.png"))

                    try:

                        stdinit.init_path = stdinit.projects_dir + stdinit.project_name + "/platformio.ini"
                        if os.path.exists(stdinit.init_path):
                            t1 = threading.Thread(target=self.tags_uploads, name=stdinit.project_name)
                            t1.setDaemon(True)
                            t1.start()  # File_tree_init
                            # platformnew = stdinit.pro_conf.get(stdinit.pro_conf.sections()[0], "platform")
                                    #
                        else:
                            stdinit.init_path = None
                    except:
                        stdinit.std_signal_gobal.stdprintln()

                else:
                    return 0

                # 关闭之前工作空间
            if old_workfpace != None:
                root_item = self.tree.findItems(old_workfpace, Qt.MatchExactly | Qt.MatchRecursive, 0)
                stdinit.pro_dir_name = stdinit.project_name
                f_len = len(root_item)
                # print(c_path)
                root_item_id = None

                if f_len > 1:
                    for i in range(f_len):
                        if work_path + old_workfpace == root_item[i].data(0, Qt.UserRole + 1):
                            root_item_id = root_item[i]
                            # print(root_item[i].data(0, Qt.UserRole + 1))
                    pass
                elif f_len == 1:
                    if work_path + old_workfpace == root_item[0].data(0, Qt.UserRole + 1):
                        root_item_id = root_item[0]
                        pass

                else:

                    return 0
                if root_item_id != None:
                    # root_item_id.setBackground(0,brush_red)
                    root_item_id.setForeground(0, self.brush_white)
                    root_item_id.setToolTip(0, "")
                    # root_item_id.setIcon(0, QIcon("appearance/img/img_folder.png"))
                    if ".ino" in old_workfpace:
                        root_item_id.setIcon(0, QIcon("appearance/img/img_ino.png"))
                    elif ".cpp" in old_workfpace:

                        root_item_id.setIcon(0, QIcon("appearance/img/img_cpp.png"))
                    elif ".h" in old_workfpace:

                        root_item_id.setIcon(0, QIcon("appearance/img/img_h.png"))
                    elif ".c" in old_workfpace:
                        root_item_id.setIcon(0, QIcon("appearance/img/img_c.png"))
                    elif ".ini" in old_workfpace:
                        root_item_id.setIcon(0, QIcon("appearance/img/piofavicon.svg"))
                    else:
                        root_item_id.setIcon(0, QIcon("appearance/img/img_folder.png"))
                    # root_item_id.setCheckState(0, Qt.Unchecked)
            stdinit.pro_dir_name = stdinit.project_name

        except:
            stdinit.std_signal_gobal.stdprintln()
            #print("Unexpected error:", sys.exc_info()[1])  # 错误内容

    def file_created(self, r_path):
        try:
            r_path = sorted(r_path, key=lambda i: len(i), reverse=False)

            for path in r_path:
                path = path.replace('\\', '/')
                #print(path)
                fileInfo = QFileInfo(path)
                fileIcon = QFileIconProvider()
                #icon = QIcon(fileIcon.icon(fileInfo))
                c_file = path.split("/")
                c_name = c_file[-1]
                c_file[-1] = ""
                #print(len(c_file))
                #fnew_len = c_file[-python3]  # 父
                new_len = c_file[-2]#父
                #print(new_len)
                c_path = path.replace("/"+c_name,"")
                # old_p=c_file.index(self.dic_name)
               # postion = c_file.count(new_len) - 1

                ####### f_word = "^" + new_len + "[\w|\W]*"
                root_item = self.tree.findItems(new_len, Qt.MatchExactly | Qt.MatchRecursive, 0)


                f_len=len(root_item)
                #print(c_path)
                root_item_id=None


                if f_len>1:
                    for i in range(f_len):
                        if c_path==root_item[i].data(0, Qt.UserRole + 1):
                            root_item_id=root_item[i]
                            #print(root_item[i].data(0, Qt.UserRole + 1))
                    pass
                elif f_len==1:
                    if c_path == root_item[0].data(0, Qt.UserRole + 1):
                        root_item_id = root_item[0]
                        pass

                else:
                    return 0
                if root_item_id!=None:
                    child = QTreeWidgetItem(root_item_id)
                    # child.setCheckState(0,Qt.Checked)

                    # c_name=c_file[-1]
                    child.setText(0, c_name)
                    child.setData(0, Qt.UserRole + 1, path)

                    # child.setIcon(0, QIcon(icon))
                    if ".ino" in c_name:
                        child.setIcon(0, QIcon("appearance/img/img_ino.png"))
                    elif ".cpp" in c_name:

                        child.setIcon(0, QIcon("appearance/img/img_cpp.png"))
                    elif ".h" in c_name:

                        child.setIcon(0, QIcon("appearance/img/img_h.png"))
                    elif ".c" in c_name:
                        child.setIcon(0, QIcon("appearance/img/img_c.png"))
                    elif ".ini" in c_name:
                        child.setIcon(0, QIcon("appearance/img/piofavicon.svg"))
                    elif os.path.isdir(path):
                        child.setIcon(0, QIcon("appearance/img/img_folder.png"))
                    else:
                        icon = QIcon(fileIcon.icon(fileInfo))
                        child.setIcon(0, QIcon(icon))


                #print(root_item[0].parent().data(0, Qt.UserRole + 1))
                #return 0

                #root_item = self.tree.findItems(new_len, Qt.MatchExactly | Qt.MatchRecursive, 0)[postion]  # 第一个0是第几列的意思，本树仅一列，但递归有多个


        except:
            stdinit.std_signal_gobal.stdprintln()
            #print("Unexpected error:", sys.exc_info()[1])  # 错误内容
            #QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile00038！\n You can search it in stduino.com",QMessageBox.Yes)
        # print()

    def file_deleted(self, r_path):
        try:
            r_path = sorted(r_path, key=lambda i: len(i), reverse=True)
            for path in r_path:
                #print(path)
                path = path.replace('\\', '/')
                #print("del"+path)

                c_file = path.split("/")
                new_len = c_file[-1]

                root_item = self.tree.findItems(new_len, Qt.MatchExactly | Qt.MatchRecursive,0)  # [0]  # 第一个0是第几列的意思，本树仅一列，但递归有多个
                for node in root_item:
                    node_text = node.data(0, Qt.UserRole + 1)
                    if node_text == path:
                        self.deleteItem(node)
                        #self.my_signal.emit(6, node_text, node_text)
        except:
            stdinit.std_signal_gobal.stdprintln()
            #QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile00039！\n You can search it in stduino.com",QMessageBox.Yes)



    def file_moved(self, files_moved):
        try:
            del_source = []
            cre_target = []

            for i in files_moved:
                del_source.append(i[0])
                cre_target.append(i[1])
                self.my_signal.emit(5, i[0].replace("\\", "/"), i[1].replace("\\", "/"))

            self.file_deleted(del_source)
            self.file_created(cre_target)

        except:
            stdinit.std_signal_gobal.stdprintln()


        # print()

    def dir_moved(self, files_moved):
        # print(str(files_moved))
        # print(2)
        try:
            # r_path = sorted(files_moved, key=lambda i: len(i), reverse=True)
            # for path in r_path:
            #     #path = path.replace('\\', '/')
            #     print(path)
            # return 0
            del_source=[]
            cre_target=[]

            for i in files_moved:
                del_source.append(i[0])
                cre_target.append(i[1])

            self.file_deleted(del_source)
            self.file_created(cre_target)
        except:
            stdinit.std_signal_gobal.stdprintln()
            #QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile0041！\n You can search it in stduino.com",QMessageBox.Yes)

    def file_modify(self,modify_list):
        try:
            modify_ui=stdinit.profile_modify_ui
            modify_all=stdinit.profile_modify_all
            for i in modify_list:
                ii=i.replace('\\', '/')
                if ii in modify_all:
                    pass
                else:
                    stdinit.profile_modify_all.append(ii)
            modify_all = stdinit.profile_modify_all
            for i in modify_ui:
                if i in modify_all:
                    stdinit.profile_modify_all.remove(i)
                    stdinit.profile_modify_ui.remove(i)
            if len(stdinit.profile_modify_all)>0:
                stdinit.std_signal_gobal.std_file_modify()

        except:
            stdinit.std_signal_gobal.stdprintln()

    def checkSnapshot(self):
        try:
            snapshot = DirectorySnapshot(self.aim_path)
            diff = DirectorySnapshotDiff(self.snapshot, snapshot)
            self.snapshot = snapshot
            self.timer = None

            # print("files_created:", diff.files_created)
            # print("files_deleted:", diff.files_deleted)

            # print("files_moved:", diff.files_moved)
            # print("dirs_modified:", diff.dirs_modified)
            # print("dirs_moved:", diff.dirs_moved)
            # print("dirs_deleted:", diff.dirs_deleted)
            # print("dirs_created:", diff.dirs_created)
            if diff.files_deleted:

                self.file_deleted(diff.files_deleted)
            if diff.dirs_deleted:

                self.file_deleted(diff.dirs_deleted)
            if diff.dirs_moved:

                self.dir_moved(diff.dirs_moved)

            if diff.files_moved:

                self.file_moved(diff.files_moved)

            if diff.dirs_created:

                self.file_created(diff.dirs_created)
            if diff.files_created:

                self.file_created(diff.files_created)
            if diff.files_modified:
                self.file_modify(diff.files_modified)
                #print("files_modified:", diff.files_modified)

                # print("cre b"+diff.dirs_created)
                # print("cre f"+diff.files_created)




            # 调试变动输出

            # 接下来就是你想干的啥就干点啥，或者该干点啥就干点啥
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()
            #print("Unexpected error:", sys.exc_info()[1])  # 错误内容
            #QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile0042！\n You can search it in stduino.com",QMessageBox.Yes)


    # 节点点击事件
    def ondoubleClicked(self):
        try:
            item1 = self.tree.currentItem()
            item = item1.data(0, Qt.UserRole + 1)

            if os.path.isdir(item):
                #d_name=item1.text(0)
                c_file = item.split("/")
                if len(c_file)>6:
                    if c_file[5] == "Projects":
                        stdinit.project_name = c_file[6]
                        self.workspace_change()


                # if os.path.isdir(stdinit.projects_dir+d_name):
                #     stdinit.project_name = d_name
                #     self.workspace_change()
                # pass
            else:

                self.my_signal.emit(1, item1.text(0), item)
        except:
            stdinit.std_signal_gobal.stdprintln()
            #print("Unexpected error:", sys.exc_info()[1])  # 错误内容
            #QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile0043！\n You can search it in stduino.com",QMessageBox.Yes)


    def onTreeClicked(self):
        try:
            item = self.tree.currentItem()
            D = item.data(0, Qt.UserRole + 1)
            #print(D)
        except:
            stdinit.std_signal_gobal.stdprintln()
            #QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile0044！\n You can search it in stduino.com",QMessageBox.Yes)

        # print("key=%s " % (item.text(0)))

    # 删除控件树子节点/根节点
    def deleteItem(self, currNode):

        try:
            # 尝试删除子节点（通过其父节点，调用removeChild函数进行删除）

            parent1 = currNode.parent()
            parent1.removeChild(currNode)
        except Exception:
            # 遇到异常时删除根节点
            try:
                rootIndex = self.tree.indexOfTopLevelItem(currNode)
                self.tree.takeTopLevelItem(rootIndex)
            except Exception:
                stdinit.std_signal_gobal.stdprintln()

    # 添加节点
    def addTreeNodeBtn(self):
        #print('--- addTreeNodeBtn ---')
        item = self.tree.currentItem()

        node = QTreeWidgetItem(item)
        node.setText(0, 'newNode')
        node.setText(1, '10')
    def paste_fun(self,f):
        try:
            try:
                currentItem_object = self.tree.currentItem()  # 获取鼠标所在的树状列表的项
                # currentItem_object_text = currentItem_object.text(0)
                b = currentItem_object.data(0, Qt.UserRole + 1)  # 获取鼠标所在的树状列表的项path
                currentItem_parent_path = currentItem_object.parent().data(0, Qt.UserRole + 1)  # 获取鼠标所在的树状列表的项
                if os.path.isdir(b):
                    pass
                else:
                    b = currentItem_parent_path
            except:
                return 0

            f_path_name = f.split("/")[-1]
            topath1 = b + "/" + f_path_name
            # f_path_name = b + "/" + f_path_name
            if f in b:
                QMessageBox.warning(self,
                                    "禁止行为",
                                    "该步操作将不进行执行！",
                                    QMessageBox.Yes)
                return 0
            elif os.path.exists(topath1):
                reply = QMessageBox.warning(self,
                                            "文件\夹已存在",
                                            "文件\夹已存在,是否覆盖！",
                                            QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    return 0

            # _thread.start_new_thread(self.paste_fun(f, b))

            t1 = threading.Thread(target=self.paste_fun1, name='file1', args=(f, b,))
            t1.setDaemon(True)
            t1.start()
        except:
            stdinit.std_signal_gobal.stdprintln()


    def paste_fun1(self,f_path,topath):

        try:

            # self.pb12.setVisible(False)
            # the_window.pb1_2.setVisible(True)
            # the_window.pb1_2.setText(reso.downloading)
            stdinit.std_signal_gobal.std_process(1,"开始拷贝")

            if os.path.isdir(f_path):
                # if f_path in topath:
                #     QMessageBox.warning(self,
                #                         "禁止行为",
                #                         "该步操作将不进行执行！",
                #                         QMessageBox.Yes)
                #     return 0

                f_path_name = f_path.split("/")[-1]
                topath = topath + "/" + f_path_name
                if os.path.exists(topath):
                #     reply = QMessageBox.warning(self,
                #                                 "文件夹已存在",
                #                                 "是否覆盖！",
                #                                 QMessageBox.Yes | QMessageBox.No)
                #     if reply == QMessageBox.No:
                #         return 0
                    #the_window.pb12.setValue(65)

                    shutil.rmtree(topath)
                    shutil.copytree(f_path, topath)

                    #the_window.pb12.setValue(100)

                else:

                    shutil.copytree(f_path, topath)  # 每次会新建一个文件夹 被复制的仅仅是内容放至新建文件夹里




            #elif os.path.isfile(f_path):
            else:

                f_path_name = f_path.split("/")[-1]
                f_path_name = topath + "/" + f_path_name
                if os.path.exists(f_path_name):
                    #the_window.pb12.setValue(80)
                    os.remove(f_path_name)
                    #the_window.pb12.setValue(90)
                    shutil.copy2(f_path, topath)
                    #the_window.pb12.setValue(100)
                else:
                    pass
                    #the_window.pb12.setValue(80)
                    shutil.copy2(f_path, topath)
                    #the_window.pb12.setValue(100)

            stdinit.std_signal_gobal.std_process(0, "拷贝完成")
            #the_window.pb12.setVisible(False)

        except:
            stdinit.std_signal_gobal.std_echo_msg(1,"粘贴失败，请手动进入文件夹粘贴！\nPaste failed, please go to the folder manually and paste!")
            #self.my_paste.emit(0, 100,"粘贴失败，请手动进入文件夹粘贴！\nPaste failed, please go to the folder manually and paste!")
            #the_window.pb12.setVisible(False)
            # QMessageBox.warning(self,
            #                     "Paste failed",
            #                     "粘贴失败，请手动进入文件夹粘贴！\nPaste failed, please go to the folder manually and paste!",
            #                     QMessageBox.Yes)
            # pass




    #     pass
    def NewFileMenuShow(self):  # 当点击“source”和“header” 显示添加文件菜单；点击具体文件名时，显示删除文件菜单
        try:
            self.tree.popMenu = QMenu()
            add = QMenu(reso.add_file)
            add.setIcon(QIcon(res.img_addfile))
            #
            # addFile = QAction(,, self)
            addFile_ino = QAction(QIcon("appearance/img/img_ino.png"), ".ino File", self)
            addFile_cpp = QAction(QIcon("appearance/img/img_cpp.png"), ".c++ File", self)
            addFile_h = QAction(QIcon("appearance/img/img_h.png"), ".h File", self)
            addFile_c = QAction(QIcon("appearance/img/img_c.png"), ".c File", self)
            addFile_txt = QAction(QIcon("appearance/img/img_txt.png"), " File", self)
            adddirec = QAction(QIcon("appearance/img/img_folder.png"), reso.add_direc, self)

            add.addAction(adddirec)
            add.addAction(addFile_ino)
            add.addAction(addFile_cpp)
            add.addAction(addFile_c)
            add.addAction(addFile_h)
            add.addAction(addFile_txt)

            # 1open 2rename python3 delete 4 new
            addFile_ino.triggered.connect(lambda: self.new_file(".ino"))  # (lambda:self.toggleMenu3(1))
            addFile_h.triggered.connect(lambda: self.new_file(".h"))
            addFile_c.triggered.connect(lambda: self.new_file(".c"))
            addFile_cpp.triggered.connect(lambda: self.new_file(".cpp"))
            addFile_txt.triggered.connect(lambda: self.new_file(""))
            adddirec.triggered.connect(lambda: self.new_file("folder"))
            add.exec_(QCursor.pos())  # 在鼠标位置显示

        except:
            stdinit.std_signal_gobal.stdprintln()
            #QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile0045！\n You can search it in stduino.com",QMessageBox.Yes)
    def remove_readonly(self, func, path, _):
        "Clear the readonly bit and reattempt the removal"
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def delete_file(self, path):
        try:
            if os.path.isdir(path):
                try:
                    shutil.rmtree(path, onerror=self.remove_readonly)
                except:
                    stdinit.std_signal_gobal.std_echo_msg(1,
                                                          "Delete error:" + "\n 请手动至该文件夹处删除\nPlease manually delete to this folder")
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
                        # print("Unexpected error:", sys.exc_info()[1])  # 错误内容
                        stdinit.std_signal_gobal.std_echo_msg(1, "Delete error:" + "\n 请手动至该文件夹处删除\nPlease manually delete to this folder")

        except:
            stdinit.std_signal_gobal.stdprintln()



    def new_me(self, i_type):

        try:
            currentItem_object = self.tree.currentItem()  # 获取鼠标所在的树状列表的项
            currentItem_object_text =currentItem_object.text(0)
            currentItem_object_path=currentItem_object.data(0, Qt.UserRole + 1)  # 获取鼠标所在的树状列表的项path
            if currentItem_object_path==stdinit.stdenv+"/Documents/Stduino":
                currentItem_parent_path =currentItem_object_path
            else:
                currentItem_parent_path = currentItem_object.parent().data(0, Qt.UserRole + 1)  # 获取鼠标所在的树状列表的项

        except:
            stdinit.std_signal_gobal.stdprintln()
            return 0

        try:

            if i_type == 2:
                value, ok = QInputDialog.getText(self, "重命名", "输入文件名:", QLineEdit.Normal, currentItem_object_text)
                if ok == 1:
                    try:
                        os.rename(currentItem_object_path, currentItem_parent_path + "/" + value)
                    except:
                        pathn =currentItem_object_path.replace(currentItem_object_text, value)
                        os.rename(currentItem_object_path, pathn)
            elif i_type == 3:
                try:

                    t1 = threading.Thread(target=self.delete_file, name='fielde1', args=(currentItem_object_path,))
                    t1.setDaemon(True)
                    t1.start()
                except:
                    stdinit.std_signal_gobal.std_echo_msg(1, "Delete error",
                                        "Unexpected error:" + "\n 请手动至该文件夹处删除\nPlease manually delete to this folder")
                    pass
            elif i_type == 7:

                if os.path.isdir(currentItem_object_path):
                    #os.startfile()
                    if stdinit.platform_is == "Win":
                        os.startfile(currentItem_object_path)

                    elif stdinit.platform_is == "Linux":
                        os.startfile(currentItem_object_path)

                    elif stdinit.platform_is == "Darwin":
                        subprocess.call(["open", currentItem_object_path])



                else:
                    if stdinit.platform_is == "Win":
                        os.startfile(currentItem_parent_path)

                    elif stdinit.platform_is == "Linux":
                        os.startfile(currentItem_parent_path)

                    elif stdinit.platform_is == "Darwin":
                        subprocess.call(["open", currentItem_parent_path])

            elif i_type==8:
                clipboard = QApplication.clipboard()
                clipboard.setText(currentItem_object_path)
        except:
            stdinit.std_signal_gobal.stdprintln()

    def new_file(self,i_name):
        try:
            try:
                currentItem_object = self.tree.currentItem()  # 获取鼠标所在的树状列表的项
                # currentItem_object_text = currentItem_object.text(0)

                currentItem_object_path = currentItem_object.data(0, Qt.UserRole + 1)  # 获取鼠标所在的树状列表的项path
                if currentItem_object_path == stdinit.stdenv + "/Documents/Stduino":
                    currentItem_parent_path = currentItem_object_path
                else:
                    currentItem_parent_path = currentItem_object.parent().data(0, Qt.UserRole + 1)  # 获取鼠标所在的树状列表的项

                if os.path.isdir(currentItem_object_path):
                    pass
                else:
                    currentItem_object_path = currentItem_parent_path

            except:
                stdinit.std_signal_gobal.stdprintln()
                return 0
            value, ok = QInputDialog.getText(self, "新建", "输入文件名:", QLineEdit.Normal, "")
            if ok == 1:
                if i_name == "folder":

                    if os.path.exists(currentItem_object_path + "/" + value):
                        stdinit.std_signal_gobal.std_echo_msg(1, "The folder already exists")

                        pass
                    else:
                        os.makedirs(currentItem_object_path + "/" + value)

                    pass
                else:
                    if os.path.exists(currentItem_object_path + "/" + value + i_name):

                        stdinit.std_signal_gobal.std_echo_msg(1, "The file already exists")
                        pass
                    else:

                        p_name = currentItem_object_path + "/" + value + i_name
                        fo = open(p_name, "w+", encoding='UTF-8')
                        fo.write("")
                        fo.close()
                        self.my_signal.emit(4, p_name, "")
        except:
            stdinit.std_signal_gobal.stdprintln()



    def OnTreeRightMenuShow(self):  # 当点击“source”和“header” 显示添加文件菜单；点击具体文件名时，显示删除文件菜单
        try:
            self.tree.popMenu = QMenu()
            add = QMenu(reso.add_file)
            add.setIcon(QIcon(res.img_addfile))
            #
            # addFile = QAction(,, self)
            addFile_ino = QAction(QIcon("appearance/img/img_ino.png"), ".ino File", self)
            addFile_cpp = QAction(QIcon("appearance/img/img_cpp.png"), ".c++ File", self)
            addFile_h = QAction(QIcon("appearance/img/img_h.png"), ".h File", self)
            addFile_c = QAction(QIcon("appearance/img/img_c.png"), ".c File", self)
            addFile_txt = QAction(QIcon("appearance/img/img_txt.png"), " File", self)
            adddirec = QAction(QIcon("appearance/img/img_folder.png"), reso.add_direc, self)
            opendirec = QAction(QIcon(res.img_open), reso.open_folder, self)

            copy_action = QAction(QIcon("appearance/img/copy.png"), "Copy", self)
            #cut_action = QAction(QIcon("appearance/img/img_folder.png"), "Cut", self)
            paste_action=QAction(QIcon("appearance/img/paste.png"), "Paste", self)
            clipboard = QApplication.clipboard().text()
            path=clipboard.replace("file:///","")

            # for line in path:
            #     print(1)
            #     print(line)

            # ds.replace()
            #
            if os.path.isdir(path) or os.path.isfile(path):
                paste_action.setEnabled(True)
            else:
                paste_action.setEnabled(False)


            rename = QAction(reso.re_name, self)
            delete = QAction(reso.delete_f_d, self)
            add.addAction(adddirec)
            add.addAction(addFile_ino)
            add.addAction(addFile_cpp)
            add.addAction(addFile_c)
            add.addAction(addFile_h)
            add.addAction(addFile_txt)

            item1_text = self.tree.currentItem().text(0)  # 获取鼠标所在的树状列表的项


            # self.tree.popMenu.addAction(addFile)
            if item1_text == self.dic_name:
                self.tree.popMenu.addMenu(add)
                self.tree.popMenu.addAction(opendirec)
                self.tree.popMenu.addAction(copy_action)
                # self.tree.popMenu.addAction(cut_action)
                self.tree.popMenu.addAction(paste_action)
            else:
                self.tree.popMenu.addMenu(add)
                self.tree.popMenu.addAction(opendirec)
                self.tree.popMenu.addAction(rename)
                self.tree.popMenu.addAction(delete)
                self.tree.popMenu.addAction(copy_action)
                # self.tree.popMenu.addAction(cut_action)
                self.tree.popMenu.addAction(paste_action)

            # addFile.addAction(delete)

            # downtype.addAction(self.usblink)
            # downtype.addAction(self.stlink)
            # fileMenu = menubar.addMenu(reso.tool)
            # fileMenu.addAction(self.serialAction)
            # fileMenu.addAction(driver)
            # fileMenu.addMenu(downtype)

            #if os.path.isdir(path):

            # 1open 2rename python3 delete 4 new
            addFile_ino.triggered.connect(lambda: self.new_file(".ino"))  # (lambda:self.toggleMenu3(1))
            addFile_h.triggered.connect(lambda: self.new_file(".h"))
            addFile_c.triggered.connect(lambda: self.new_file(".c"))
            addFile_cpp.triggered.connect(lambda: self.new_file(".cpp"))
            addFile_txt.triggered.connect(lambda: self.new_file(""))
            adddirec.triggered.connect(lambda: self.new_file("folder"))

            opendirec.triggered.connect(lambda: self.new_me(7))

            # adddirec.triggered.connect(self.do_adddirec)
            rename.triggered.connect(lambda: self.new_me(2))
            delete.triggered.connect(lambda: self.new_me(3))
            paste_action.triggered.connect(lambda: self.paste_fun(path))
            #paste_action.triggered.connect(_thread.start_new_thread(self.paste_fun(path, item1)))
            copy_action.triggered.connect(lambda: self.new_me(8))#_thread.start_new_thread(self.startgdbserver, ("Thread-1", 1,))
            self.tree.popMenu.exec_(QCursor.pos())  # 在鼠标位置显示
        except:
            stdinit.std_signal_gobal.stdprintln()
            #QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile0045！\n You can search it in stduino.com",QMessageBox.Yes)



        # if '.' in item.text(0) and '.cbp' not in item.text(0):  # 该项是文件名，添加右键[删除菜单]

    # 节点更新
    def updateTreeNodeBtn(self):
        print('--- updateTreeNodeBtn ---')
        item = self.tree.currentItem()
        item.setText(0, 'updateNode')
        item.setText(1, '20')

    # 删除节点
    def delTreeNodeBtn(self):
        print('--- delTreeNodeBtn ---')
        item = self.tree.currentItem()
        root = self.tree.invisibleRootItem()
        for item in self.tree.selectedItems():
            (item.parent() or root).removeChild(item)

    def Open_Folder(self):
        try:
            path = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")

            self.tree.setColumnCount(1)
            self.tree.setColumnWidth(0, 50)
            self.tree.setHeaderLabels(["Stduino"])
            self.tree.setIconSize(QSize(25, 25))
            self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
            # self.actionfileopen.triggered.connect(self.Open_Folder)
            self.aim_path = path  # aim_path不可随意更换否则容易比对出错
            # print(path)

            dirs = os.listdir(path)

            fileInfo = QFileInfo(path)
            fileIcon = QFileIconProvider()
            icon = QIcon(fileIcon.icon(fileInfo))
            root = QTreeWidgetItem(self.tree)
            # root.setText(0, "projects")
            self.dic_name = path.split('/')[-1]
            root.setText(0, self.dic_name)
            root.setData(0, Qt.UserRole + 1, path)
            # C:\Users\debug\Desktop\ts  #path.split('/')[-1]
            root.setIcon(0, QIcon("appearance/img/img_p.png"))
            self.CreateTree(dirs, root, path)
            # self.setCentralWidget(self.tree)
            #self.mainLayout.addWidget(self.tree)
            QApplication.processEvents()
        except:
            stdinit.std_signal_gobal.stdprintln()
            #QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile0046！\n You can search it in stduino.com",QMessageBox.Yes)


    def init_open(self):
        try:
            self.tree.setColumnCount(1)
            self.tree.setColumnWidth(0, 50)
            self.tree.setHeaderLabels(["Stduino"])
            self.tree.setIconSize(QSize(25, 25))
            self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
            # self.actionfileopen.triggered.connect(self.Open_Folder)
            # path = r"C:\Users\debug\Desktop\ts"
            # self.aim_path= r"C:\Users\debug\Desktop\ts"
            path = self.aim_path

            dirs = os.listdir(path)

            fileInfo = QFileInfo(path)
            fileIcon = QFileIconProvider()
            icon = QIcon(fileIcon.icon(fileInfo))
            root = QTreeWidgetItem(self.tree)
            self.dic_name = path.split('/')[-1]
            root.setText(0, self.dic_name)
            # C:\Users\debug\Desktop\ts  #path.split('/')[-1]
            root.setData(0, Qt.UserRole + 1, path)
            # root.setIcon(0, QIcon(icon))
            root.setIcon(0, QIcon("appearance/img/img_p4.png"))
            root.setExpanded(True)

            #self.CreateTree(dirs, root, path)
            t1 = threading.Thread(target=self.CreateTree, name='dir1',args=(dirs, root, path,))
            t1.start()
            # self.setCentralWidget(self.tree)
            self.mainLayout.addWidget(self.tree)
            QApplication.processEvents()


        except:
            stdinit.std_signal_gobal.stdprintln()
            #QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile0047！\n You can search it in stduino.com",QMessageBox.Yes)
        # path = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        # self.tree = QTreeWidget()
    def CreateTree1(self, dirs, root, path):

        try:
            # pro_fo=0
            for i in dirs:
                path_new = path + '/' + i
                # print(path_new)
                if os.path.isdir(path_new):
                    # fileInfo = QFileInfo(path_new)
                    # fileIcon = QFileIconProvider()
                    # icon = QIcon(fileIcon.icon(fileInfo))
                    child = QTreeWidgetItem(root)
                    child.setText(0, i)
                    child.setData(0, Qt.UserRole + 1, path_new)
                    child.setIcon(0, QIcon("appearance/img/img_folder.png"))
                    # if pro_fo==0:
                    #     pro_fo=1
                    #     child.setExpanded(True)

                    dirs_new = os.listdir(path_new)
                    self.CreateTree1(dirs_new, child, path_new)
                else:
                    fileInfo = QFileInfo(path_new)
                    fileIcon = QFileIconProvider()
                    child = QTreeWidgetItem(root)
                    child.setText(0, i)
                    child.setData(0, Qt.UserRole + 1, path_new)

                    if ".ino" in i:
                        child.setIcon(0, QIcon("appearance/img/img_ino.png"))#
                    elif ".cpp" in i:
                        child.setIcon(0, QIcon("appearance/img/img_cpp.png"))
                    elif ".h" in i:
                        child.setIcon(0, QIcon("appearance/img/img_h.png"))
                    elif ".c" in i:
                        child.setIcon(0, QIcon("appearance/img/img_c.png"))
                    elif ".ini" in i:
                        child.setIcon(0, QIcon("appearance/img/piofavicon.svg"))
                    else:

                        icon = QIcon(fileIcon.icon(fileInfo))
                        child.setIcon(0, QIcon(icon))


        except:
            stdinit.std_signal_gobal.stdprintln()
           # QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile0048！\n You can search it in stduino.com",QMessageBox.Yes)



    def CreateTree(self, dirs, root, path):

        try:
            pro_fo=0
            for i in dirs:
                path_new = path + '/' + i
                # print(path_new)
                if os.path.isdir(path_new):
                    # fileInfo = QFileInfo(path_new)
                    # fileIcon = QFileIconProvider()
                    # icon = QIcon(fileIcon.icon(fileInfo))
                    child = QTreeWidgetItem(root)
                    child.setText(0, i)
                    child.setData(0, Qt.UserRole + 1, path_new)
                    child.setIcon(0, QIcon("appearance/img/img_folder.png"))
                    if pro_fo==0:
                        pro_fo=1
                        child.setExpanded(True)

                    dirs_new = os.listdir(path_new)
                    self.CreateTree1(dirs_new, child, path_new)
                else:
                    fileInfo = QFileInfo(path_new)
                    fileIcon = QFileIconProvider()
                    child = QTreeWidgetItem(root)
                    child.setText(0, i)
                    child.setData(0, Qt.UserRole + 1, path_new)

                    if ".ino" in i:
                        child.setIcon(0, QIcon("appearance/img/img_ino.png"))#
                    elif ".cpp" in i:
                        child.setIcon(0, QIcon("appearance/img/img_cpp.png"))
                    elif ".h" in i:
                        child.setIcon(0, QIcon("appearance/img/img_h.png"))
                    elif ".c" in i:
                        child.setIcon(0, QIcon("appearance/img/img_c.png"))
                    elif ".ini" in i:
                        child.setIcon(0, QIcon("appearance/img/piofavicon.svg"))
                    else:

                        icon = QIcon(fileIcon.icon(fileInfo))
                        child.setIcon(0, QIcon(icon))

            stdinit.File_tree_view.workspace_change()
            #stdinit.std_signal_gobal.std_echo_msg(0, "Stduino IDE初始化完毕，欢迎您的使用，若在使用过程中遇到任何问题，请至www.stduino.com进行发帖交流！")


        except:
            stdinit.std_signal_gobal.stdprintln()
            #QMessageBox.warning(self, "BUG Warning", "Waring|Error:stdfile0048！\n You can search it in stduino.com",QMessageBox.Yes)

