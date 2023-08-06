# -*- coding: utf-8 -*-

"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
from function.cores.stdedit import stdinit
from PyQt5.Qsci import QsciScintilla
from PyQt5.QtWidgets import QMessageBox
class Commenter():
    def __init__(self, sci, comment_str):
        self.sci = sci
        self.comment_str = comment_str
        self.sel_regions = []


    def toggle_comments(self):
        try:
            lines = self.selected_lines()
            if len(lines) <= 0:
                return
            all_commented = True
            for line in lines:
                if not self.sci.text(line).strip().startswith(self.comment_str):
                    all_commented = False
            if not all_commented:
                self.comment_lines(lines)
            else:
                self.uncomment_lines(lines)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def selections(self):
        try:
            regions = []
            for i in range(self.sci.SendScintilla(QsciScintilla.SCI_GETSELECTIONS)):
                regions.append({
                    'begin': self.sci.SendScintilla(QsciScintilla.SCI_GETSELECTIONNSTART, i),
                    'end': self.sci.SendScintilla(QsciScintilla.SCI_GETSELECTIONNEND, i)
                })

            return regions
        except:
            stdinit.std_signal_gobal.stdprintln()


    def selected_lines(self):
        try:
            self.sel_regions = []
            all_lines = []
            regions = self.selections()
            for r in regions:
                start_line = self.sci.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, r['begin'])
                end_line = self.sci.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, r['end'])
                for cur_line in range(start_line, end_line + 1):
                    if not cur_line in all_lines:
                        all_lines.append(cur_line)
                if r['begin'] <= r['end']:
                    self.sel_regions.append(r)
            return all_lines
        except:
            stdinit.std_signal_gobal.stdprintln()


    def comment_lines(self, lines):
        try:
            indent = self.sci.indentation(lines[0])
            for line in lines:
                indent = min(indent, self.sci.indentation(line))
            self.sci.beginUndoAction()
            for line in lines:
                self.adjust_selections(line, indent)
                self.sci.insertAt(self.comment_str, line, indent)
            self.sci.endUndoAction()
            self.restore_selections()
        except:
            stdinit.std_signal_gobal.stdprintln()


    def uncomment_lines(self, lines):
        try:
            self.sci.beginUndoAction()
            for line in lines:
                line_start = self.sci.SendScintilla(QsciScintilla.SCI_POSITIONFROMLINE, line)
                line_end = self.sci.SendScintilla(QsciScintilla.SCI_GETLINEENDPOSITION, line)
                if line_start == line_end:
                    continue
                if line_end - line_start < len(self.comment_str):
                    continue
                done = False
                for c in range(line_start, line_end - len(self.comment_str) + 1):
                    source_str = self.sci.text(c, c + len(self.comment_str))
                    if (source_str == self.comment_str):
                        self.sci.SendScintilla(QsciScintilla.SCI_DELETERANGE, c, len(self.comment_str))
                        break
            self.sci.endUndoAction()
        except:
            stdinit.std_signal_gobal.stdprintln()

    def restore_selections(self):
        try:
            if (len(self.sel_regions) > 0):
                first = True
                for r in self.sel_regions:
                    if first:
                        self.sci.SendScintilla(QsciScintilla.SCI_SETSELECTION, r['begin'], r['end'])
                        first = False
                    else:
                        self.sci.SendScintilla(QsciScintilla.SCI_ADDSELECTION, r['begin'], r['end'])
        except:
            stdinit.std_signal_gobal.stdprintln()


    def adjust_selections(self, line, indent):
        try:
            for r in self.sel_regions:
                if self.sci.positionFromLineIndex(line, indent) <= r['begin']:
                    r['begin'] += len(self.comment_str)
                    r['end'] += len(self.comment_str)
                elif self.sci.positionFromLineIndex(line, indent) < r['end']:
                    r['end'] += len(self.comment_str)
        except:
            stdinit.std_signal_gobal.stdprintln()



