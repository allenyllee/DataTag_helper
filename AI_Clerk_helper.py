#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /lib/AIClerk_helper.py
# Project: suidice-text-detection
# Created Date: Monday, May 4th 2020, 3:06:41 pm
# Author: Allenyl(allen7575@gmail.com>)
# -----
# Last Modified: Monday, May 3rd 2021, 6:15:40 pm
# Modified By: Allenyl(allen7575@gmail.com)
# -----
# Copyright 2018 - 2020 Allenyl Copyright, Allenyl Company
# -----
# license:
# All shall be well and all shall be well and all manner of things shall be well.
# We're doomed!
# ------------------------------------
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
###
import json
from collections import defaultdict

import pandas as pd
# from sklearn.utils import shuffle
import emoji
import hashlib
# from lib.AIClerk_helper import to_AI_clerk_batch_upload_json

import sys
# import argparse
from gooey import Gooey, GooeyParser
import copy
from pathlib import Path
import numpy as np
from collections import OrderedDict
from functools import reduce
import re
from collections import Counter
from sklearn.model_selection import StratifiedShuffleSplit
import os
import platform
from openpyxl.styles import Font



## Non-ASCII output hangs execution in PyInstaller packaged app · Issue #520 · chriskiehl/Gooey
## https://github.com/chriskiehl/Gooey/issues/520
import codecs

if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'UTF-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# use sqlite db to share data between gui and cli
# because gui will excute this file with cli args to finish its work,
# it needs a way to know what data is change in gui screen.
from sqlitedict import SqliteDict

MY_DB_FILE='./my_db.sqlite'

mydict = SqliteDict(MY_DB_FILE, autocommit=True)

try:
    mydict['global_choies']
except KeyError:
    mydict['global_choies'] = []

# share args across different event callbacks
global_args = defaultdict(list)


import wx
from gooey.gui.lang.i18n import _

## [Feature request: Allow general callbacks for validation · Issue #293 · chriskiehl/Gooey]
## (https://github.com/chriskiehl/Gooey/issues/293)
# from gooey.gui.components.widgets.bases import TextContainer
# oldGetValue = TextContainer.getValue

# def newGetValue(self):
#     result = oldGetValue(self)
#     userValidator = self._options['validator']['callback']
#     message = self._options['validator']['message']
#     value = self.getWidgetValue()
#     validates = userValidator(value)
#     result['test'] = False
#     result['error'] = 'test'
#     return result

# TextContainer.getValue = newGetValue

# [Gooey/dropdown.py at 8c88980e12a968430df5cfd0779fab37db287680 · chriskiehl/Gooey]
# (https://github.com/chriskiehl/Gooey/blob/8c88980e12a968430df5cfd0779fab37db287680/gooey/gui/components/widgets/dropdown.py)
from gooey.gui.components.widgets.dropdown import Dropdown
Dropdown_oldGetWidget = Dropdown.getWidget

# from gooey.gui import formatters
# def newFormatOutput(self, metadata, value):
#     print("debug2")
#     print("metadata", metadata)
#     print("value", value)
#     return formatters.dropdown(metadata, value)

# def newSetValue(self, value):
#     ## +1 to offset the default placeholder value
#     index = self._meta['choices'].index(value) + 1
#     print("debug", self._meta['choices'])
#     self.widget.SetSelection(index)

# def newGetWidgetValue(self):
#     value = self.widget.GetValue()
#     # filter out the extra default option that's
#     # appended during creation
#     print(value)
#     if value == _('select_option'):
#         return None
#     return value

def Dropdown_newGetWidget(self, parent, *args, **options):
    widget = Dropdown_oldGetWidget(self, parent, *args, **options)
    # [wxPython ComboBox & Choice类 - WxPython教程™]
    # (https://www.yiibai.com/wxpython/wx_combobox_choice_class.html)
    # [wx.ComboBox — wxPython Phoenix 4.1.1a1 documentation]
    # (https://wxpython.org/Phoenix/docs/html/wx.ComboBox.html)
    widget.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.OnCombo)
    return widget

def Dropdown_newOnCombo(self, event):
    def get_choices(input_file):
        try:
            new_choices = list(pd.read_excel(input_file , sheet_name='document_label', index_col=0, nrows=0))
            message = ''
            self.setErrorString(message)
            self.showErrorString(False)
            # force refresh parent screen
            # python - Update/Refresh Dynamically–Created WxPython Widgets - Stack Overflow
            # https://stackoverflow.com/questions/10368948/update-refresh-dynamically-created-wxpython-widgets
            self.GetParent().Layout()
        except:
            message = "No sheet named 'document_label'"
            # print(message)
            self.setErrorString(message)
            self.showErrorString(True)
            # force refresh parent screen
            # python - Update/Refresh Dynamically–Created WxPython Widgets - Stack Overflow
            # https://stackoverflow.com/questions/10368948/update-refresh-dynamically-created-wxpython-widgets
            self.GetParent().Layout()
            new_choices = []

        return new_choices

    current_input_file = global_args['input_file']

    try:
        self.previous_input_file
    except:
        self.previous_input_file = ''

    if self.previous_input_file != current_input_file:
        self.new_choices = get_choices(current_input_file)
        self.previous_input_file = current_input_file

    # save self.new_choices into sqlite db for later access
    mydict['global_choies'] = self.new_choices
    # [python - Dynamically change the choices in a wx.ComboBox() - Stack Overflow]
    # (https://stackoverflow.com/questions/682923/dynamically-change-the-choices-in-a-wx-combobox)
    self.setOptions(self.new_choices)


Dropdown.getWidget = Dropdown_newGetWidget
Dropdown.OnCombo = Dropdown_newOnCombo
# Dropdown.setValue = newSetValue
# Dropdown.getWidgetValue = newGetWidgetValue
# Dropdown.formatOutput = newFormatOutput

# [Gooey/choosers.py at 8c88980e12a968430df5cfd0779fab37db287680 · chriskiehl/Gooey]
# (https://github.com/chriskiehl/Gooey/blob/8c88980e12a968430df5cfd0779fab37db287680/gooey/gui/components/widgets/choosers.py)
# [Gooey/chooser.py at 8c88980e12a968430df5cfd0779fab37db287680 · chriskiehl/Gooey]
# (https://github.com/chriskiehl/Gooey/blob/8c88980e12a968430df5cfd0779fab37db287680/gooey/gui/components/widgets/core/chooser.py#L65)
# [Gooey/chooser.py at 8c88980e12a968430df5cfd0779fab37db287680 · chriskiehl/Gooey]
# (https://github.com/chriskiehl/Gooey/blob/8c88980e12a968430df5cfd0779fab37db287680/gooey/gui/components/widgets/core/chooser.py#L13)
# [Gooey/text_input.py at 8c88980e12a968430df5cfd0779fab37db287680 · chriskiehl/Gooey]
# (https://github.com/chriskiehl/Gooey/blob/8c88980e12a968430df5cfd0779fab37db287680/gooey/gui/components/widgets/core/text_input.py#L7)
# [Gooey/bases.py at 8c88980e12a968430df5cfd0779fab37db287680 · chriskiehl/Gooey]
# (https://github.com/chriskiehl/Gooey/blob/8c88980e12a968430df5cfd0779fab37db287680/gooey/gui/components/widgets/bases.py#L170)
from gooey.gui.components.widgets.core.chooser import FileChooser
FileChooser_old_init = FileChooser.__init__

## monkey patch __init__
def FileChooser_new_init(self, parent, *args, **kwargs):
    FileChooser_old_init(self, parent, *args, **kwargs)
    # bind event wx.EVT_TEXT to trigger self.OnFileChooser when text change
    # [wx.TextCtrl — wxPython Phoenix 4.1.1a1 documentation]
    # (https://wxpython.org/Phoenix/docs/html/wx.TextCtrl.html)
    # [wxPython - TextCtrl Class - Tutorialspoint]
    # (https://www.tutorialspoint.com/wxpython/wx_textctrl_class.htm)
    self.widget.Bind(wx.EVT_TEXT, self.OnFileChooser)

## monkey patch OnFileChooser
def FileChooser_newOnFileChooser(self, event):
    # read text area value to global_args
    global_args['input_file'] = self.widget.getValue()
    # print(global_args)


FileChooser.__init__ = FileChooser_new_init
FileChooser.OnFileChooser = FileChooser_newOnFileChooser

# [Gooey/application.py at 8c88980e12a968430df5cfd0779fab37db287680 · chriskiehl/Gooey]
# (https://github.com/chriskiehl/Gooey/blob/8c88980e12a968430df5cfd0779fab37db287680/gooey/gui/containers/application.py#L29)
from gooey.gui.containers.application import GooeyApplication

## monkey patch onClose
def newOnClose(self, *args, **kwargs):
    """Cleanup the top level WxFrame and shutdown the process"""
    self.Destroy()
    # print("onClose")
    # remove db file when close
    # [sqlite - Python PermissionError: [WinError 32] The process cannot access the file..... but my file is closed - Stack Overflow]
    # (https://stackoverflow.com/questions/59482990/python-permissionerror-winerror-32-the-process-cannot-access-the-file-bu)
    mydict.close()
    os.remove(MY_DB_FILE)
    sys.exit()

GooeyApplication.onClose = newOnClose


# navigation option must be upper cased 'TABBED', instead of 'Tabbed'
@Gooey(program_name="AI Clerk helper v0.8.1", navigation='TABBED', tabbed_groups=False, default_size=(525, 670))
def parse_args():
    # parser = argparse.ArgumentParser()
    parser = GooeyParser()
    subs = parser.add_subparsers(help='commands', dest='command')

    ### for original file
    sub_parser1 = subs.add_parser('original', prog='未標註原始檔案', help='未標註原始檔案')

    sub_parser1_1 = sub_parser1.add_argument_group('input file(s)', 'choose unlabeled file(s)', gooey_options={
                                'show_border': True,
                                'show_underline': True,
                                'columns':1
                                })

    mutex_sub_parser1 = sub_parser1_1.add_mutually_exclusive_group(required=True, gooey_options={
                                'show_border': True,
                                'show_underline': True,
                                'columns':1
                                })

    #### input excel files
    mutex_sub_parser1.add_argument('-i', '--input_file', help='input filename (excel)', dest='input_file', default=None, widget='FileChooser')

    sub_parser1_2 = sub_parser1.add_argument_group('options', 'only works for input excel file', gooey_options={
                                'show_border': True,
                                'show_underline': True,
                                'columns':2
                                })

    sub_parser1_2.add_argument('--emojilize', help='turn text to emoji (uncheck to reverse)', dest='emojilize', action='store_true')
    sub_parser1_2.set_defaults(emojilize=False)

    sub_parser1_2.add_argument('--to-excel', help='output excel file (uncheck to output json)', dest='to_excel', action='store_true')
    sub_parser1_2.set_defaults(to_excel=False)

    #### input txt files
    mutex_sub_parser1.add_argument('-d', '--input-dir', help='dir that contains input files(.txt)', dest='input_dir', default=None, widget="DirChooser")


    ### for labeled file
    sub_parser2 = subs.add_parser('labeled', prog='已標註檔案', help='已標註檔案')

    sub_parser2 = sub_parser2.add_argument_group('labeled file to excel', 'choose the labeled file which want to be convert to Excel file(s)', gooey_options={
                                'show_border': True,
                                'show_underline': True,
                                'columns': 1
                                })

    sub_parser2.add_argument('-i', '--input_file', help='input filename (json)', dest='input_file', default=None, widget='FileChooser')

    ### for labeled file want to second upload
    sub_parser2_1 = subs.add_parser('second_upload', prog='標註二次上傳', help='已標註檔案二次上傳')

    sub_parser2_1 = sub_parser2_1.add_argument_group('second upload', 'choose the labeled file which want to be second upload (for double check purpose)', gooey_options={
                                'show_border': True,
                                'show_underline': True,
                                'columns': 1
                                })

    sub_parser2_1.add_argument('-i', '--input_file', help='input filename (json)', dest='input_file', default=None, widget='FileChooser')

    ### for second labeled file convert
    sub_parser2_2 = subs.add_parser('second_labeled', prog='二次標註轉換', help='二次標註轉換')

    sub_parser2_2 = sub_parser2_2.add_argument_group('second labeled convertion', 'choose the first and second labeled files which wants to be converted to final json', gooey_options={
                                'show_border': True,
                                'show_underline': True,
                                'columns': 1
                                })

    sub_parser2_2.add_argument('-i1', '--input_file_1', nargs='*', help='choose multiple files (first labeled json)', dest='input_file_1', default=None, widget='MultiFileChooser')

    sub_parser2_2.add_argument('-i2', '--input_file_2', help='input filename (second labeled json)', dest='input_file_2', default=None, widget='FileChooser')

    ### concat files
    sub_parser3 = subs.add_parser('concat', prog='合併檔案', help='合併檔案')
    sub_parser3 = sub_parser3.add_argument_group('')
    sub_parser3.add_argument('-i', '--input_file', help='input filenames (excel)', dest='input_files',
                            default=None, widget='MultiFileChooser')



    ### for random tran/test split
    sub_parser4 = subs.add_parser('split', prog='分割檔案', help='分割檔案')

    sub_parser4 = sub_parser4.add_argument_group('')
    sub_parser4.add_argument('-i', '--input_file', help='input filename (excel)', dest='input_file',
                            default=None, widget='FileChooser')
    sub_parser4.add_argument('-y', '--y_column', help='y column', dest='y_col',
                            default=None, widget='Dropdown', choices=mydict['global_choies'])
    # parser.add_argument('--type', '-t', choices=getLob())



    # args, unknown = parser.parse_known_args()
    args = parser.parse_args()

    return args



def to_AI_clerk_batch_upload_json(dataframe, save_path):
    def to_article_dict(x):
        return {'Title': x.Title.tolist()[0], 'Content': x.Content.tolist()[0],
                'Author': x.Author.tolist()[0], 'Time': x.Time.tolist()[0]}

    print("number of entries: {}".format(len(dataframe)))

    dup_id = dataframe.duplicated(['TextID'], keep=False)
    print("duplicated entries: {}".format(len(dataframe[dup_id])))
    print(dataframe[dup_id])

    samples_dict = dataframe.groupby(['TextID']).apply(to_article_dict).to_dict()
    print("keep first, drop duplicated!")


    content_length_lower_threshold = 100
    long_id = dataframe['Content'].apply(lambda x: True if len(x) < content_length_lower_threshold else False)
    print("number of entries which Content shorter then {} words: {}".format(content_length_lower_threshold, len(dataframe[long_id])))
    print("no drop, just show information.")

    sample_articles = defaultdict(defaultdict)
    sample_articles['Articles'].update(samples_dict)

    print("number of remaining entries: {}".format(len(sample_articles['Articles'])))

    # output articles.json
    with open(save_path, 'w', encoding='utf-8') as outfile:
        json.dump(sample_articles, outfile, ensure_ascii=False, indent=4)

    # read ouputed samples to test
    # with open('./suicide_text_sample.json', 'r') as outfile:
    #     temp_dict = json.load(outfile)

    # try:
    #     display(temp_dict)
    # except:
    #     pass

def get_TextID(df):
    return df.apply(lambda x: hashlib.md5(x[0].encode('utf-8')).hexdigest()[:10],axis=1)

# ### 清理資料格式
def clean_data(df):
    empty_entries = df["Content"].isnull()
    print("number of empty content entries: {}".format(len(df[empty_entries])))

    df_cleaned = df[~empty_entries].copy()
    if len(df[empty_entries]):
        print("drop empty!")

    drop_columns = df_cleaned.columns.str.contains("Unnamed")

    # print(any(df_cleaned.columns.str.contains("^ID$")))
    # if not any(df_cleaned.columns.str.contains("^TextID$")):
    leave_columns = df_cleaned.columns[~drop_columns].tolist()
    # df_cleaned['ID'] = df_cleaned[["Content"]].apply(lambda x: hashlib.md5(x[0].encode('utf-8')).hexdigest()[:10],axis=1)
    df_cleaned = df_cleaned[leave_columns]

    # print(df_cleaned.head())
    df_cleaned = df_cleaned.sort_values("TextID").reset_index(drop=True)

    df_cleaned["Author"] = df_cleaned.apply(lambda x: x.Poster + '/' + x.Gender, axis=1)
    df_cleaned["Time"] = df_cleaned.apply(lambda x: str(x.Date) + '/' + str(x.Time), axis=1)

    return df_cleaned


def emoji_to_text(df):
    df_deemojilized = df.copy()
    ## 轉換 emoji 格式成 :emoji:
    ## python - How to replace emoji to word in a text? - Stack Overflow
    ## https://stackoverflow.com/questions/57580288/how-to-replace-emoji-to-word-in-a-text
    df_deemojilized["Content"] = df[["Content"]].apply(lambda x: emoji.demojize(x[0]), axis=1)
    df_deemojilized["Title"] = df[["Title"]].apply(lambda x: emoji.demojize(x[0]), axis=1)
    return df_deemojilized


def text_to_emoji(df):
    df_emojilized = df.copy()
    ## 將:emoji: 換回 unicode character
    df_emojilized["Content"] = df[["Content"]].apply(lambda x: emoji.emojize(x[0]), axis=1)
    df_emojilized["Title"] = df[["Title"]].apply(lambda x: emoji.emojize(x[0]), axis=1)

    return df_emojilized


def reorder_column(columns_list, selected_column_name, insert_before_column_name=None):
    """
    columns_list: the list of columns to be reordered
    selected_column_name: the column name which wants to be inserted to the point before column `insert_before_column_name`
    insert_before_column_name: the column name which act as fix point relative to the `selected_column_name`
    """
    columns_list = copy.copy(columns_list)
    selected_index = columns_list.index(selected_column_name)
    selected_item = columns_list.pop(selected_index)

    # drop selected column when insert_before_column_name is infinity
    if insert_before_column_name is np.inf:
        return columns_list

    # print(insert_before_column_name is float('inf'))

    # insert to the end of column list when insert_before_column_name is None
    if insert_before_column_name is None:
        insert_point_index = len(columns_list)
    else:
        insert_point_index = columns_list.index(insert_before_column_name)

    columns_list.insert(insert_point_index, selected_item)

    return columns_list


def extract_dict(df, id_column_list, dict_column):
    df_tmp = df[id_column_list + [dict_column]].set_index(id_column_list)
    df_tmp = pd.DataFrame(df_tmp.apply(
        lambda x: {'empty': 'nan'} if len(x[0]) == 0 else x[0], axis=1))

    df_tmp = df_tmp.apply(
        lambda x: pd.DataFrame.from_dict(x[0], orient='index').stack(), axis=1)

    df_tmp = df_tmp.reset_index(level=id_column_list)

    return df_tmp



# these illegal characters is represented by octal escape
# [Regular Expressions Reference: Special and Non-Printable Characters]
# (https://www.regular-expressions.info/refcharacters.html)
# [(1条消息)openpyxl.utils.exceptions.IllegalCharacterError 错误原因分析及解决办法_村中少年的专栏-CSDN博客]
# (https://blog.csdn.net/javajiawei/article/details/97147219)
ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

# [openpyxl.utils.escape — openpyxl 3.0.5 documentation]
# (https://openpyxl.readthedocs.io/en/stable/_modules/openpyxl/utils/escape.html)
ESCAPED_REGEX = re.compile("_x([0-9A-Fa-f]{4})_")

def unescape_OOXML(string):

    def remove_character(char):
        print("removed illegal char!")
        return r''

    def _sub(match):
        """
        Callback to unescape chars
        """
        char = chr(int(match.group(1), 16))
        # [Convert regular Python string to raw string - Stack Overflow]
        # (https://stackoverflow.com/questions/4415259/convert-regular-python-string-to-raw-string)
        # [python - Pythonic way to do base conversion - Stack Overflow]
        # (https://stackoverflow.com/questions/28824874/pythonic-way-to-do-base-conversion)
        print("found char {}, which int in octal number is: {}".format(char.encode('unicode_escape'), oct(ord(char))))

        # remove carriage return
        if char == '\r':
            print("removed!")
            char = ''
        else:
            # remove illegal characters
            char = ILLEGAL_CHARACTERS_RE.sub(remove_character, char)

        return char

    string = ESCAPED_REGEX.sub(_sub, string)

    return string


## [pandas - How to remove illegal characters so a dataframe can write to Excel - Stack Overflow]
## (https://stackoverflow.com/questions/42306755/how-to-remove-illegal-characters-so-a-dataframe-can-write-to-excel)
def remove_illegal_characters(dataframe):
    # dataframe = dataframe.applymap(lambda x: x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x)
    dataframe = dataframe.applymap(lambda x: ILLEGAL_CHARACTERS_RE.sub(r'', x) if isinstance(x, str) else x)
    return dataframe


def to_excel_AI_clerk_labeled_data(dataframe, save_path):
    ## unescape OOXML string
    dataframe = dataframe.applymap(lambda x: unescape_OOXML(x) if isinstance(x, str) else x)
    ## remove illegal characters
    dataframe = remove_illegal_characters(dataframe)

    df1 = dataframe.T.sort_values(['TextID', 'Annotator']).rename_axis('SerialID').reset_index()
    df1 = df1[sorted(df1.columns)]

    columns_list = list(df1.columns)
    print(columns_list)
    columns_list = reorder_column(columns_list, 'TextID', 'Annotator')
    columns_list = reorder_column(columns_list, 'SerialID', 'TextID')
    columns_list = reorder_column(columns_list, 'Title', 'Content')
    columns_list = reorder_column(columns_list, 'Author', 'Title')
    columns_list = reorder_column(columns_list, 'TextTime', 'Comment')
    print(columns_list)

    df2 = df1[columns_list]

    ########### extract document label #############
    df_document_label = extract_dict(df2, ['TextID', 'Annotator'], 'Summary')

    ## reduce multi-selection option into string
    def multi_selection_to_string(option_columns):
        # print(option_columns)
        option_columns_list = list(filter(lambda y: pd.notnull(y), option_columns))

        # check if option_columns_list is empty or ['']
        if len(option_columns_list) == 0:
            result = np.nan
        elif len(option_columns_list) == 1 and option_columns_list[0] == '':
            result = np.nan
        else:
            result = reduce(lambda a,b: a+', '+b, option_columns_list)
            if result == '':
                # print(list(option_columns))
                # print(len(option_columns_list))
                result = np.nan

        return result

    ### use ordered set to keep columns order
    od = OrderedDict(df_document_label.columns.to_flat_index())
    option_columns_list = list(od.keys())

    df_document_label_tmp = pd.DataFrame(columns=option_columns_list)
    df_document_label_tmp['TextID'] = df_document_label['TextID']
    df_document_label_tmp['Annotator'] = df_document_label['Annotator']
    option_columns_list.remove('TextID')
    option_columns_list.remove('Annotator')

    ### flatten all option columns
    for option_column in option_columns_list:
        df_document_label_tmp[option_column] = df_document_label[option_column].apply(lambda x: multi_selection_to_string(x), axis=1)

    df_document_label = pd.merge(df2[['TextID', 'Annotator']], df_document_label_tmp, how='left', on=['TextID', 'Annotator'])


    ########## create doc label compare view ##########
    df_doc_label_cmp = pd.pivot_table(df_document_label, values=option_columns_list,
                                        index=['TextID'], columns=['Annotator'], aggfunc=lambda x: x.iloc[0])

    df_doc_label_cmp = df_doc_label_cmp.reset_index()


    ########## extract sentence label ############
    df_sentence_label_tmp = extract_dict(df2, ['TextID', 'Annotator'], 'TermTab')
    sentence_label_index_dict = OrderedDict(df_sentence_label_tmp.columns.to_flat_index())
    sent_label_column_list = list(sentence_label_index_dict.keys())
    # print(sent_label_column_list)
    sent_label_column_list.remove('TextID')
    sent_label_column_list.remove('Annotator')
    ## drop unused level of multi index to avoid KeyError
    df_sentence_label_tmp = df_sentence_label_tmp.droplevel(1, axis=1)

    df_sentence_label_tmp = df_sentence_label_tmp.melt(id_vars=['TextID', 'Annotator'], value_vars=sent_label_column_list, var_name='Sent_Label', value_name='Sentence')
    df_sentence_label_tmp = df_sentence_label_tmp.dropna()
    df_sentence_label_tmp['Sent_Label'] = df_sentence_label_tmp['Sent_Label'].apply(lambda x: x.split('_')[0])
    df_sentence_label_tmp.reset_index(drop=True, inplace=True)
    df_sentence_label = pd.merge(df_document_label, df_sentence_label_tmp, how='left', on=['TextID', 'Annotator'])
    df_sentence_label = df_sentence_label.sort_values(['TextID', 'Annotator', 'Sent_Label'])


    ######### create sent label cmp long view ########
    # this will group sentence by 'TextID', 'Annotator' and 'Sent_Label'
    df_sentence_sector = df_sentence_label_tmp.groupby(['TextID', 'Annotator', 'Sent_Label'])

    # because there may be many sentences belong to one Sent_Label,
    # when arragate, save these sentence into a list
    df_sent_label_cmp_long_tmp = df_sentence_sector.agg(lambda x: [y for y in x])

    # this will separate each sentence into columns,
    # so if there are 21 sentence, column's name will be a list of 0-20
    df_sent_label_cmp_long_tmp = df_sent_label_cmp_long_tmp['Sentence'].apply(lambda x: pd.Series(x))

    # add new column level: Sentence
    column_level_list =  [['Sentence'], df_sent_label_cmp_long_tmp.columns]
    df_sent_label_cmp_long_tmp.columns = pd.MultiIndex.from_product(column_level_list, names=['', 'Sent_num'])
    # stack 'Sent_num' column as row index
    df_sent_label_cmp_long_tmp = df_sent_label_cmp_long_tmp.stack()
    # reset_index will turn all row index into columns
    df_sent_label_cmp_long_tmp = df_sent_label_cmp_long_tmp.reset_index()
    # set multilevel index with this order: 'TextID', 'Annotator', 'Sent_Label', 'Sent_num'
    df_sent_label_cmp_long_tmp = df_sent_label_cmp_long_tmp.set_index(['TextID', 'Annotator', 'Sent_Label', 'Sent_num'])


    def merge(x, y):
        if isinstance(x, list):
            new_x = x + y
        else:
            new_x = 'error'
        return new_x

    # use 'TextID', 'Sent_Label', 'Sent_num' as index,
    # and turn 'Annotator''s value into columns, eg.
    # if there were four possible values of Annotator: A,B,C,D
    # then use A,B,C,B as new column names, pivot under value column 'Sentence'
    # in case there are multiple items with same index, aggfunc will be used.
    # it will pass a pd.Series object into aggfunc,
    # we cae use reduce to return sum over the series,
    # if each item in series is a list object,
    # we can define a merge function to sum these list up into one list.
    df_sent_label_cmp_long = pd.pivot_table(df_sent_label_cmp_long_tmp, values=['Sentence'],
                                        index=['TextID', 'Sent_Label', 'Sent_num'], columns=['Annotator'], aggfunc=lambda x: reduce(merge, x))

    # add additional level in the multiindex: 'Sent'
    # for sent_doc_cmp use
    col_index_names = list(df_sent_label_cmp_long.columns.names)
    df_sent_label_cmp_long.columns = pd.MultiIndex.from_tuples(map(lambda x: (x[0], 'Sent', x[1]), df_sent_label_cmp_long.columns), names=[col_index_names[0], '', col_index_names[1]])


    ######### create sentence label wide view ##########
    df_sentence_label_wide = df_sent_label_cmp_long.unstack().unstack()
    df_sentence_label_wide.columns = df_sentence_label_wide.columns.swaplevel(3, 4)
    df_sentence_label_wide.sort_index(axis=1, level=3, inplace=True)
    df_sentence_label_wide.columns = pd.MultiIndex.from_tuples(map(lambda x: (x[2], str(x[3]) + '_' + '{:0>2d}'.format(x[4])), df_sentence_label_wide.columns))
    df_sentence_label_wide = df_sentence_label_wide.stack(level=0)
    df_sentence_label_wide.index = df_sentence_label_wide.index.rename(['TextID', 'Annotator'])
    df_sentence_label_wide = df_sentence_label_wide.reset_index()

    df_sentence_label_wide = pd.merge(df_document_label, df_sentence_label_wide, how='left', on=['TextID', 'Annotator'])

    empty_cols_exclude_first = df_sentence_label_wide.columns[df_sentence_label_wide.columns.str.contains('empty_(?:[0][1-9]|[1-9][0-9])')]
    df_sentence_label_wide = df_sentence_label_wide.drop(empty_cols_exclude_first ,axis=1)



    ######### create sent label cmp wide views ##########
    df_sent_label_cmp_wide = df_sent_label_cmp_long.unstack()
    df_sent_label_cmp_wide.columns = df_sent_label_cmp_wide.columns.swaplevel(2, 3)
    df_sent_label_cmp_wide.sort_index(axis=1, level=2, inplace=True)



    ######## create sent_doc_cmp views #########
    df_doc_tmp = df_doc_label_cmp.set_index('TextID')
    df_doc_tmp = pd.concat({'Doc_Label': df_doc_tmp}, names=['label_kind'], axis=1)

    df_sent_tmp = df_sent_label_cmp_long.reset_index()
    # to prevent warning: PerformanceWarning: dropping on a non-lexsorted multi-index without a level parameter may impact performance.
    # need to sort multi-index
    # see: [python - What exactly is the lexsort_depth of a multi-index Dataframe? - Stack Overflow](https://stackoverflow.com/questions/27116739/what-exactly-is-the-lexsort-depth-of-a-multi-index-dataframe)
    df_sent_tmp.sort_index(axis=1, level=0, inplace=True)


    df_sent_doc_cmp_tmp = pd.merge(df_doc_tmp, df_sent_tmp, how='left', on=['TextID'])

    df_sent_doc_cmp_tmp.columns = df_sent_doc_cmp_tmp.columns.swaplevel(1, 2)
    df_sent_doc_cmp_tmp.columns = df_sent_doc_cmp_tmp.columns.swaplevel(0, 1)

    df_sent_doc_cmp_tmp.sort_index(axis=1, level=0, inplace=True)

    sent_doc_cols = list(df_sent_doc_cmp_tmp.columns)
    new_sent_doc_cols = reorder_column(sent_doc_cols, ('', 'TextID', ''), ('', 'Sent_Label', ''))
    df_sent_doc_cmp = df_sent_doc_cmp_tmp[new_sent_doc_cols]
    df_sent_doc_cmp = df_sent_doc_cmp.set_index([('', 'TextID', ''), ('', 'Sent_Label', ''), ('', 'Sent_num', '')])
    df_sent_doc_cmp.index = df_sent_doc_cmp.index.rename(['TextID', 'Sent_Label', 'Sent_num'])


    ########## extract content ##########
    drop_columns_list = reorder_column(columns_list, 'Summary', np.inf)
    drop_columns_list = reorder_column(drop_columns_list, 'TermTab', np.inf)
    print(drop_columns_list)

    ## explicit copy to avoid SettingWithCopyWarning warning
    df_content = df2[drop_columns_list].copy()

    ## remove tags in content
    df_content['Content(remove_tag)'] = df_content['Content'].apply(lambda x: re.sub('(＜(／)?＊(.+?)_\d{1,2}＊＞)', '', x))

    # write to excel
    with pd.ExcelWriter(save_path, options={'strings_to_urls': False}, engine='openpyxl') as writer:
        df_sent_doc_cmp.to_excel(writer, sheet_name='sent_doc_cmp', index=True)
        df_doc_label_cmp.to_excel(writer, sheet_name='doc_label_cmp', index=True)
        df_sent_label_cmp_long.to_excel(writer, sheet_name='sent_label_cmp(long)', index=True)
        df_sent_label_cmp_wide.to_excel(writer, sheet_name='sent_label_cmp(wide)', index=True)
        df_sentence_label_wide.to_excel(writer, sheet_name='sentence_label(wide)', index=False)
        df_content.to_excel(writer, sheet_name='contents', index=False)
        df_document_label.to_excel(writer, sheet_name='document_label', index=False)
        df_sentence_label.to_excel(writer, sheet_name='sentence_label', index=False)

        for ws in writer.sheets.values():
            """
            fix column headers and row headers no font name issue
            need to use engine='openpyxl'
            """
            # row_level = df_sent_doc_cmp.index.nlevels
            # print(row_level)
            for row in ws.iter_rows(min_row=1, max_row=1):
                """
                walk through each cell of first row to assign font name
                """
                for cell in row:
                    # print(cell)
                    font_params = cell.font.__dict__
                    if font_params["name"] is None:
                        font_params["name"] = "Calibri"
                        cell.font = Font(**font_params)


    return df_content, df_document_label, df_sentence_label, df_sentence_label_wide, df_doc_label_cmp, df_sent_label_cmp_long, df_sent_label_cmp_wide, df_sent_doc_cmp


def split_train_test_to_target(X, y, target):
    sss = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=1234)

    for index, (train_index, test_index) in enumerate(sss.split(X, y)):
    #     print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        print("split {}".format(index))
        print("train:", Counter(y_train))
        print("test:", Counter(y_test))

        df_train = pd.DataFrame({'TextID':X_train}).reset_index(drop=True)
        df_test = pd.DataFrame({'TextID':X_test}).reset_index(drop=True)

        df_target_train = pd.merge(df_train, target, how='left', on=['TextID'])
        df_target_test = pd.merge(df_test, target, how='left', on=['TextID'])

        filename = 'train_test_split.xlsx'
        # if file does not exist write header
        if index != 0 and os.path.isfile(filename):
            mode = 'a'
        else:
            mode = 'w'

        with pd.ExcelWriter(filename, options={'strings_to_urls': False}, mode=mode, engine='openpyxl') as writer:
            df_target_train.to_excel(writer, sheet_name='train{:02}'.format(index), index=False)
            df_target_test.to_excel(writer, sheet_name='test{:02}'.format(index), index=False)


def concat_files(files_list):
    print(files_list)
    df_content = pd.read_excel(files_list[0], sheet_name='contents')
    df_document_label = pd.read_excel(files_list[0], sheet_name='document_label')
    df_sentence_label = pd.read_excel(files_list[0], sheet_name='sentence_label')

    for filepath in files_list[1:]:
        df_content = df_content.append(pd.read_excel(filepath, sheet_name='contents'))
        df_document_label = df_document_label.append(pd.read_excel(filepath, sheet_name='document_label'))
        df_sentence_label = df_sentence_label.append(pd.read_excel(filepath, sheet_name='sentence_label'))

    ## sort data by TextID
    df_content = df_content.sort_values(by=['TextID'])
    df_document_label = df_document_label.sort_values(by=['TextID'])
    df_sentence_label = df_sentence_label.sort_values(by=['TextID'])

    ## unescape OOXML string
    df_content = df_content.applymap(lambda x: unescape_OOXML(x) if isinstance(x, str) else x)
    df_document_label = df_document_label.applymap(lambda x: unescape_OOXML(x) if isinstance(x, str) else x)
    df_sentence_label = df_sentence_label.applymap(lambda x: unescape_OOXML(x) if isinstance(x, str) else x)

    # write to excel
    ## remove illegal characters
    df_content = remove_illegal_characters(df_content)
    df_document_label = remove_illegal_characters(df_document_label)
    df_sentence_label = remove_illegal_characters(df_sentence_label)

    with pd.ExcelWriter('all_data.xlsx', options={'strings_to_urls': False}, engine='openpyxl') as writer:
        df_content.to_excel(writer, sheet_name='contents', index=False)
        df_document_label.to_excel(writer, sheet_name='document_label', index=False)
        df_sentence_label.to_excel(writer, sheet_name='sentence_label', index=False)

    return df_content, df_document_label, df_sentence_label


def main():
    # check if user pass any argument, if yes, use command line, otherwise use gooey
    ## python - Argparse: Check if any arguments have been passed - Stack Overflow
    ## https://stackoverflow.com/questions/10698468/argparse-check-if-any-arguments-have-been-passed
    if len(sys.argv) > 1:
        ## How to strip decorators from a function in Python - Stack Overflow
        ## https://stackoverflow.com/questions/1166118/how-to-strip-decorators-from-a-function-in-python
        args = parse_args.__closure__[0].cell_contents()
    else:
        args = parse_args()

    # print(args.command)

    # try:
    #     common_filename = Path(args.input_file)
    #     # common_filename = "".join(args.input_file.split(".")[:-1])
    #     # print(common_filename)
    # except:
    #     pass

    if args.command == 'original':
        if args.input_file:
            common_filename = Path(args.input_file)
            df = pd.read_excel(args.input_file)
            df['TextID'] = get_TextID(df[["Content"]])

            if args.emojilize:
                # df = clean_data(df)
                df = text_to_emoji(df)
                new_filename = common_filename.with_name(common_filename.stem + "_emojilized")
                print(args.input_file.split("."))
            else:
                new_filename = common_filename.with_name(common_filename.stem + "_demojilized")
                # print(args.input_file.split(".")[:-1])
                # df = clean_data(df)
                df = emoji_to_text(df)


            ## unescape OOXML string
            df = df.applymap(lambda x: unescape_OOXML(x) if isinstance(x, str) else x)
            ## remove illegal characters
            df = remove_illegal_characters(df)

            ######## calculate processed TextID ########
            ## remove emoji text for calculate TextID
            delimiters = (':', ':')
            pattern = re.compile(u'(%s[a-zA-Z0-9\\+\\-_&.ô’Åéãíç()!#*]+%s)' % delimiters)

            df_remove_emoji_text = df.applymap(lambda x: pattern.sub('', x) if isinstance(x, str) else x)

            ## replace strange characters for calculate TextID
            pattern2 = re.compile(u'\\\\\\\\%')
            df_remove_emoji_text = df_remove_emoji_text.applymap(lambda x: pattern2.sub('%', x) if isinstance(x, str) else x)
            df['TextID(processed)'] = get_TextID(df_remove_emoji_text[["Content"]])


            if args.to_excel:
                output_filename = new_filename.with_suffix(".xlsx")
                with pd.ExcelWriter(output_filename, options={'strings_to_urls': False}, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
            else:
                output_filename = new_filename.with_suffix(".json")
                # ### 輸出工研院文章 json檔
                df = clean_data(df)
                to_AI_clerk_batch_upload_json(df, output_filename)

            id_mapping_filename = common_filename.with_name(common_filename.stem + "_TextID_mapping").with_suffix(".xlsx")
            with pd.ExcelWriter(id_mapping_filename, options={'strings_to_urls': False}, engine='openpyxl') as writer:
                reserved_columns = df.columns.str.contains('^TextID.*')
                reserved_columns = df.columns[reserved_columns].tolist()
                df[reserved_columns].to_excel(writer, index=False)

        elif args.input_dir:
            common_path = Path(args.input_dir)
            print("input path:", common_path)

            filename_pattern = '*/**/*.txt'
            save_path = Path(common_path).with_name(Path(common_path).stem).with_suffix(".json")
            print("output path:", save_path)

            glob_path = Path(common_path)
            filepathes=glob_path.glob(filename_pattern)

            articles_dict = defaultdict(dict)

            for filepath in filepathes:
                content_dict = {}
                content_dict['Title'] = filepath.stem
                content_dict['Content'] = ''
                content_dict['Author'] = ''
                content_dict['Time'] = ''

                with open(filepath, 'r', encoding='utf-8') as f:
                    content_dict['Content'] = f.read()
                    text_id = hashlib.md5(content_dict['Content'].encode('utf-8')).hexdigest()[:10]

                articles_dict['Articles'].update({text_id: content_dict})


            # read into dataframe will automatically sort by index
            dataframe = pd.DataFrame.from_dict(articles_dict)

            # because articles_dict['Articles'] use text_id as key to update,
            # if there were duplicate text_id, it'll replace by later items.
            # so no need to check duplicate.
            ###
            # dataframe.reset_index(inplace=True)
            # dup_id = dataframe.duplicated(['index'], keep=False)
            # print("duplicated entries: {}".format(len(dataframe[dup_id])))
            # print(dataframe[dup_id])

            # dataframe = dataframe.groupby(['index']).apply(lambda x: x.iloc[0])
            # print("keep first, drop duplicated!")

            # dataframe.set_index('index', inplace=True)

            with open(save_path, 'w', encoding='utf-8') as outfile:
                json.dump(dataframe.to_dict(), outfile, ensure_ascii=False, indent=4)


    elif args.command == 'labeled':
        common_filename = Path(args.input_file)
        df = pd.read_json(args.input_file)

        ### 輸出標記資料excel檔
        output_filename = common_filename.with_suffix(".xlsx")
        to_excel_AI_clerk_labeled_data(df, output_filename)

    elif args.command == 'second_upload':
        ## 二次上傳時，由於工研院系統的限制，會把他們內部的 SerialID 當成是 TextID
        ## 因此，這一步的作用就是將 TextID 複製到原本 SerialID 的欄位，
        ## 再次上傳後下載回來才會是正確的 TextID
        common_filename = Path(args.input_file)
        # df = pd.read_json(args.input_file)
        with open(common_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        data2 = {}

        for key, value in data.items():
            # pprint(data[key])
            data2.update({data[key]['TextID']: data[key]})

        save_path = Path(common_filename).with_name(common_filename.stem + '_second_upload').with_suffix('.json')

        with open(save_path, 'w', encoding='utf-8') as outfile:
            json.dump(data2, outfile, ensure_ascii=False, indent=4)

    elif args.command == 'second_labeled':
        ## 二次標註結果下載後，會發現檔案大小是一次標註的兩倍大，
        ## 這是因為二次標註下載回來的檔案還包含一次標註的檔案，
        ## 那些沒有 Annotator 的資料，即為一次標註的資料，可以直接丟棄
        ## 只要留下有 Annotator 的資料，並且 assign 正確的 TextID 上去
        # print(args.input_file_1)
        # print(args.input_file_2)
        common_filename_1 = [Path(path) for path in args.input_file_1]
        common_filename_2 = Path(args.input_file_2)
        # df = pd.read_json(args.input_file)
        data1 = {}
        for path in common_filename_1:
            with open(path, 'r', encoding='utf-8') as f:
                data1.update(json.load(f))

        with open(common_filename_2, 'r', encoding='utf-8') as f:
            data2 = json.load(f)

        data3 = {}

        for key, value in data2.items():
            if value['Annotator'] == '':
                continue

            value['TextID'] = data1[value['TextID']]['TextID']
            data3.update({key: value})

        save_path = Path(common_filename_2).with_name(common_filename_2.stem + '_second_labeled').with_suffix('.json')

        with open(save_path, 'w', encoding='utf-8') as outfile:
            json.dump(data3, outfile, ensure_ascii=False, indent=4)

    elif args.command == 'concat':
        os_type = platform.system()
        if os_type == 'Windows':
            files_list = args.input_files.split(';')
        else:
            files_list = args.input_files.split(':')
        concat_files(files_list)
    elif args.command == 'split':
        # df_content = pd.read_excel(args.input_file, sheet_name='contents')
        df_document = pd.read_excel(args.input_file, sheet_name='document_label')
        df_sentence = pd.read_excel(args.input_file, sheet_name='sentence_label')

        ## unescape OOXML string
        # df_content = df_content.applymap(lambda x: unescape_OOXML(x) if isinstance(x, str) else x)
        df_document = df_document.applymap(lambda x: unescape_OOXML(x) if isinstance(x, str) else x)
        df_sentence = df_sentence.applymap(lambda x: unescape_OOXML(x) if isinstance(x, str) else x)

        ## remove illegal characters
        # df_content = remove_illegal_characters(df_content)
        df_document = remove_illegal_characters(df_document)
        df_sentence = remove_illegal_characters(df_sentence)


        X = df_document['TextID']
        y = df_document[args.y_col]
        target = df_sentence

        split_train_test_to_target(X, y, target)






if __name__ == '__main__':
    main()
