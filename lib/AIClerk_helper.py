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
from sklearn.utils import shuffle
import emoji
import hashlib
# from lib.AIClerk_helper import to_AIclerk_batch_upload_json

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_file', help='input filename (excel)', dest='input_file', default=None)
parser.add_argument('-o', '--output_file', help='output filename (json)', dest='output_file', default=None)

parser.add_argument('--emojilize', dest='emojilize', action='store_true')
parser.add_argument('--no-emojilize', dest='emojilize', action='store_false')
parser.set_defaults(emojilize=False)

parser.add_argument('--to-json', dest='to_json', action='store_true')
parser.add_argument('--to-excel', dest='to_json', action='store_false')
parser.set_defaults(to_json=True)

args, unknown = parser.parse_known_args()


def to_AIclerk_batch_upload_json(dataframe, save_path):
    def to_article_dict(x):
        return {'Title': x.Title.tolist()[0], 'Content': x.Content.tolist()[0],
                'Author': x.Author.tolist()[0], 'Time': x.Time.tolist()[0]}

    samples_dict = dataframe.groupby(['ID']).apply(to_article_dict).to_dict()

    sample_articles = defaultdict(defaultdict)
    sample_articles['Articles'].update(samples_dict)

    # output articles.json
    with open(save_path, 'w') as outfile:
        json.dump(sample_articles, outfile, ensure_ascii=False, indent=4)

    # read ouputed samples to test
    with open('./suicide_text_sample.json', 'r') as outfile:
        temp_dict = json.load(outfile)

    try:
        display(temp_dict)
    except:
        pass


# ### 清理資料格式
def clean_data(df):

    df_cleaned = df[~df["Content"].isnull()].copy()

    drop_columns = df_cleaned.columns.str.contains("Unnamed")
    leave_columns = ['ID'] + df_cleaned.columns[~drop_columns].tolist()
    df_cleaned['ID'] = df_cleaned[["Content"]].apply(lambda x: hashlib.md5(x[0].encode('utf-8')).hexdigest()[:10],axis=1)
    df_cleaned = df_cleaned[leave_columns]

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



if __name__ == '__main__':
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

    if args.to_json:
        output_filename = new_filename + ".json"
        # ### 輸出工研院文章 json檔
        to_AIclerk_batch_upload_json(df, output_filename)
    else:
        output_filename = new_filename+ ".xlsx"
        df.to_excel(output_filename)