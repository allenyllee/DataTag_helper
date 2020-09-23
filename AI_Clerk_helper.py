#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /lib/AIClerk_helper.py
# Project: suidice-text-detection
# Created Date: Monday, May 4th 2020, 3:06:41 pm
# Author: Allenyl(allen7575@gmail.com>)
# -----
# Last Modified: Tuesday, September 22nd 2020, 11:43:24 am
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
@Gooey(program_name="AI Clerk helper v0.6.1", navigation='TABBED')
def parse_args():
    # parser = argparse.ArgumentParser()
    parser = GooeyParser()
    subs = parser.add_subparsers(help='commands', dest='command')

    ### for original file
    sub_parser1 = subs.add_parser('original', prog='未標註原始檔案', help='未標註原始檔案')

    sub_parser1 = sub_parser1.add_argument_group('')

    sub_parser1.add_argument('-i', '--input_file', help='input filename (excel)', dest='input_file', default=None, widget='FileChooser')

    sub_parser1.add_argument('--emojilize', help='turn text to emoji (uncheck to reverse)', dest='emojilize', action='store_true')
    sub_parser1.set_defaults(emojilize=False)

    sub_parser1.add_argument('--to-excel', help='output excel file (uncheck to output json)', dest='to_excel', action='store_true')
    sub_parser1.set_defaults(to_excel=False)

    ### for unlabeled file
    sub_parser2 = subs.add_parser('labeled', prog='已標註檔案', help='已標註檔案')

    sub_parser2 = sub_parser2.add_argument_group('')
    sub_parser2.add_argument('-i', '--input_file', help='input filename (json)', dest='input_file', default=None, widget='FileChooser')


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

    dup_id = dataframe.duplicated(['ID'], keep=False)
    print("duplicated entries: {}".format(len(dataframe[dup_id])))
    print(dataframe[dup_id])

    samples_dict = dataframe.groupby(['ID']).apply(to_article_dict).to_dict()
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


# ### 清理資料格式
def clean_data(df):
    empty_entries = df["Content"].isnull()
    print("number of empty content entries: {}".format(len(df[empty_entries])))

    df_cleaned = df[~empty_entries].copy()
    if len(df[empty_entries]):
        print("drop empty!")

    drop_columns = df_cleaned.columns.str.contains("Unnamed")

    # print(any(df_cleaned.columns.str.contains("^ID$")))
    if not any(df_cleaned.columns.str.contains("^ID$")):
        leave_columns = ['ID'] + df_cleaned.columns[~drop_columns].tolist()
        df_cleaned['ID'] = df_cleaned[["Content"]].apply(lambda x: hashlib.md5(x[0].encode('utf-8')).hexdigest()[:10],axis=1)
        df_cleaned = df_cleaned[leave_columns]

        # print(df_cleaned.head())
        df_cleaned = df_cleaned.sort_values("ID").reset_index(drop=True)

    df_cleaned["Author"] = df_cleaned.apply(lambda x: x.Poster + '/' + x.Gender, axis=1)
    df_cleaned["Time"] = df_cleaned.apply(lambda x: str(x.Date) + '/' + str(x.Time), axis=1)

    df_cleaned = emoji_to_text(df_cleaned)

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


def extract_dict(df, id_column, dict_column):
    df_tmp = df[[id_column, dict_column]].set_index(id_column)
    df_tmp = pd.DataFrame(df_tmp.apply(
        lambda x: {'empty': float('nan')} if len(x[0]) == 0 else x[0], axis=1))

    df_tmp = df_tmp.apply(
        lambda x: pd.DataFrame.from_dict(x[0], orient='index').stack(), axis=1)

    df_tmp = df_tmp.reset_index(level=0)

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

    df1 = dataframe.T.sort_values(['TextID', 'Annotator']).reset_index(drop=True)
    df1 = df1[sorted(df1.columns)]

    columns_list = list(df1.columns)
    print(columns_list)
    columns_list = reorder_column(columns_list, 'TextID', 'Annotator')
    columns_list = reorder_column(columns_list, 'Title', 'Content')
    columns_list = reorder_column(columns_list, 'Author', 'Title')
    columns_list = reorder_column(columns_list, 'TextTime', 'Comment')
    print(columns_list)

    df2 = df1[columns_list]

    # extract document label
    df_document_label = extract_dict(df2, 'TextID', 'Summary')

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
    option_columns_list.remove('TextID')

    ### flatten all option columns
    for option_column in option_columns_list:
        df_document_label_tmp[option_column] = df_document_label[option_column].apply(lambda x: multi_selection_to_string(x), axis=1)

    df_document_label = df_document_label_tmp

    # extract sentence label
    df_sentence_label = extract_dict(df2, 'TextID', 'TermTab')

    sentence_label_index_dict = OrderedDict(df_sentence_label.columns.to_flat_index())
    sent_label_column_list = list(sentence_label_index_dict.keys())
    # print(sent_label_column_list)
    sent_label_column_list.remove('TextID')

    df_sentence_label_tmp = df_sentence_label.melt(id_vars=['TextID'], value_vars=sent_label_column_list, var_name='Sent_Label', value_name='Sentence')
    df_sentence_label_tmp = df_sentence_label_tmp.dropna()
    df_sentence_label_tmp = df_sentence_label_tmp.sort_values(['TextID', 'Sent_Label'])
    df_sentence_label_tmp['Sent_Label'] = df_sentence_label_tmp['Sent_Label'].apply(lambda x: x.split('_')[0])
    df_sentence_label_tmp.reset_index(drop=True, inplace=True)
    df_sentence_label_tmp = pd.merge(df_document_label, df_sentence_label_tmp, how='left', on=['TextID'])

    df_sentence_label = df_sentence_label_tmp

    # extract content
    drop_columns_list = reorder_column(columns_list, 'Summary', np.inf)
    drop_columns_list = reorder_column(drop_columns_list, 'TermTab', np.inf)
    print(drop_columns_list)

    ## explicit copy to avoid SettingWithCopyWarning warning
    df_content = df2[drop_columns_list].copy()

    ## remove tags in content
    df_content['Content(remove_tag)'] = df_content['Content'].apply(lambda x: re.sub('(＜(／)?＊(.+?)_\d{1,2}＊＞)', '', x))

    # write to excel
    with pd.ExcelWriter(save_path, options={'strings_to_urls': False}) as writer:
        df_content.to_excel(writer, sheet_name='contents', index=False)
        df_document_label.to_excel(writer, sheet_name='document_label', index=False)
        df_sentence_label.to_excel(writer, sheet_name='sentence_label', index=False)

    return df_content, df_document_label, df_sentence_label


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

    with pd.ExcelWriter('all_data.xlsx', options={'strings_to_urls': False}) as writer:
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

    try:
        common_filename = Path(args.input_file)
        # common_filename = "".join(args.input_file.split(".")[:-1])
        # print(common_filename)
    except:
        pass

    if args.command == 'original':
        df = pd.read_excel(args.input_file)

        if args.emojilize:
            df = clean_data(df)
            df = text_to_emoji(df)
            new_filename = common_filename.with_name(common_filename.stem + "_emojilized")
            print(args.input_file.split("."))
        else:
            new_filename = common_filename.with_name(common_filename.stem + "_demojilized")
            # print(args.input_file.split(".")[:-1])
            df = clean_data(df)

        ## unescape OOXML string
        df = df.applymap(lambda x: unescape_OOXML(x) if isinstance(x, str) else x)
        ## remove illegal characters
        df = remove_illegal_characters(df)

        if args.to_excel:
            output_filename = new_filename.with_suffix(".xlsx")
            df.to_excel(output_filename)
        else:
            output_filename = new_filename.with_suffix(".json")
            # ### 輸出工研院文章 json檔
            to_AI_clerk_batch_upload_json(df, output_filename)

    elif args.command == 'labeled':
        df = pd.read_json(args.input_file)
        ## unescape OOXML string
        df = df.applymap(lambda x: unescape_OOXML(x) if isinstance(x, str) else x)
        ## remove illegal characters
        df = remove_illegal_characters(df)

        ### 輸出標記資料excel檔
        output_filename = common_filename.with_suffix(".xlsx")
        to_excel_AI_clerk_labeled_data(df, output_filename)
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
