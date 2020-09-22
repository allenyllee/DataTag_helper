#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /lib/AIClerk_helper.py
# Project: suidice-text-detection
# Created Date: Monday, May 4th 2020, 3:06:41 pm
# Author: Allenyl(allen7575@gmail.com>)
# -----
# Last Modified: Wednesday, July 1st 2020, 4:43:37 pm
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

## Non-ASCII output hangs execution in PyInstaller packaged app · Issue #520 · chriskiehl/Gooey
## https://github.com/chriskiehl/Gooey/issues/520
import codecs

if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'UTF-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


@Gooey(program_name="AI Clerk helper v0.3", navigation='TABBED')
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
    # extract sentence label
    df_sentence_label = extract_dict(df2, 'TextID', 'TermTab')

    # extract content
    drop_columns_list = reorder_column(columns_list, 'Summary', np.inf)
    drop_columns_list = reorder_column(drop_columns_list, 'TermTab', np.inf)
    print(drop_columns_list)
    df_content = df2[drop_columns_list]

    # write to excel
    with pd.ExcelWriter(save_path, options={'strings_to_urls': False}) as writer:
        df_content.to_excel(writer, sheet_name='contents')
        df_document_label.to_excel(writer, sheet_name='document_label')
        df_sentence_label.to_excel(writer, sheet_name='sentence_label')


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

    common_filename = Path(args.input_file)
    # common_filename = "".join(args.input_file.split(".")[:-1])
    # print(common_filename)

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


        if args.to_excel:
            output_filename = new_filename.with_suffix(".xlsx")
            df.to_excel(output_filename)
        else:
            output_filename = new_filename.with_suffix(".json")
            # ### 輸出工研院文章 json檔
            to_AI_clerk_batch_upload_json(df, output_filename)

    elif args.command == 'labeled':
        df = pd.read_json(args.input_file)
        output_filename = common_filename.with_suffix(".xlsx")
        ### 輸出標記資料excel檔
        to_excel_AI_clerk_labeled_data(df, output_filename)



if __name__ == '__main__':
    main()