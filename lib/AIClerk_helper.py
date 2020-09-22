#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /lib/AIClerk_helper.py
# Project: suidice-text-detection
# Created Date: Monday, May 4th 2020, 3:06:41 pm
# Author: Allenyl(allen7575@gmail.com>)
# -----
# Last Modified:
# Modified By:
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

    display(temp_dict)



