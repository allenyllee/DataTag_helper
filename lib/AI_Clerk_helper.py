#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /lib/AIClerk_helper.py
# Project: suidice-text-detection
# Created Date: Monday, May 4th 2020, 3:06:41 pm
# Author: Allenyl(allen7575@gmail.com>)
# -----
# Last Modified: Monday, May 4th 2020, 4:34:06 pm
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

## Non-ASCII output hangs execution in PyInstaller packaged app · Issue #520 · chriskiehl/Gooey
## https://github.com/chriskiehl/Gooey/issues/520
import codecs

if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'UTF-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


@Gooey(program_name="AI Clerk helper v0.2")
def parse_args():
    # parser = argparse.ArgumentParser()
    parser = GooeyParser()
    parser.add_argument('-i', '--input_file', help='input filename (excel)', dest='input_file', default=None, widget='FileChooser')

    parser.add_argument('--emojilize', help='turn text to emoji (uncheck to reverse)', dest='emojilize', action='store_true')
    parser.set_defaults(emojilize=False)

    parser.add_argument('--to-excel', help='output excel file (uncheck to output json)', dest='to_excel', action='store_true')
    parser.set_defaults(to_excel=False)

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


    df = pd.read_excel(args.input_file)

    if args.emojilize:
        df = clean_data(df)
        df = text_to_emoji(df)
        new_filename = "".join(args.input_file.split(".")[:-1]) + "_emojilized"
        print(args.input_file.split("."))
    else:
        new_filename = "".join(args.input_file.split(".")[:-1]) + "_demojilized"
        # print(args.input_file.split(".")[:-1])
        df = clean_data(df)


    if args.to_excel:
        output_filename = new_filename+ ".xlsx"
        df.to_excel(output_filename)
    else:
        output_filename = new_filename + ".json"
        # ### 輸出工研院文章 json檔
        to_AI_clerk_batch_upload_json(df, output_filename)


if __name__ == '__main__':
    main()