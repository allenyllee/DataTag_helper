#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# ====psi-header====
# File: /test_module.py
# Project: tests
# Created Date: Friday, September 10th 2021, 10:02:16 am
# Author: Allenyl(allen7575@gmail.com)
# -----
# Last Modified: Thursday, January 1st 1970, 12:00:00 am
# Modified By: Allenyl(allen7575@gmail.com)
# -----
# Copyright 2018 - 2021 Allenyl Copyright, Allenyl Company
# -----
# license:
# All Rights Reserved.
# ------------------------------------
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
###


import filecmp
import os
import pathlib
import pandas as pd

from .. import DataTag_helper

# print(__name__)
test_directory = pathlib.Path(__file__).parent.resolve()


def test_txt_to_json_1():
    """
    test txt to json function for gun_20201102
    """
    print("test_directory", test_directory)
    test_file_path = test_directory / "input_data/gun_20201102"
    DataTag_helper.main(["original", "-d", str(test_file_path)])
    output_path = test_directory / "input_data/gun_20201102.json"
    expect_path = test_directory / "expect_result/gun_20201102.json"

    assert filecmp.cmp(output_path, expect_path)

    os.remove(output_path)


def test_txt_to_json_2():
    """
    test txt to json function for 分類和10篇txt檔(1), the txt file contained in 分類和10篇txt檔(1) are Big5 encoding
    """
    print("test_directory", test_directory)
    test_file_path = test_directory / "input_data/分類和10篇txt檔(1)"
    DataTag_helper.main(["original", "-d", str(test_file_path)])
    output_path = test_directory / "input_data/分類和10篇txt檔(1).json"
    expect_path = test_directory / "expect_result/分類和10篇txt檔(1).json"

    assert filecmp.cmp(output_path, expect_path)

    os.remove(output_path)


def test_excel_to_json_1():
    """
    test excel to json function for excel欄位測試1.xlsx
    """
    print("test_directory", test_directory)
    test_file_path = test_directory / "input_data/excel轉檔測試/excel欄位測試1.xlsx"
    DataTag_helper.main(["original", "-i", str(test_file_path)])
    output_path = test_directory / "input_data/excel轉檔測試/excel欄位測試1_demojilized.json"
    output_path2 = test_directory / "input_data/excel轉檔測試/excel欄位測試1_TextID_mapping.xlsx"
    expect_path = test_directory / "expect_result/excel轉檔測試/excel欄位測試1_demojilized.json"
    expect_path2 = test_directory / "expect_result/excel轉檔測試/excel欄位測試1_TextID_mapping.xlsx"

    assert filecmp.cmp(output_path, expect_path)

    # check mapping id
    output_df = pd.read_excel(output_path2, index_col=0, engine="openpyxl")
    expect_df = pd.read_excel(expect_path2, index_col=0, engine="openpyxl")

    diff_bool = output_df != expect_df
    difference_output_df = output_df[diff_bool].dropna(how='all')
    difference_expect_df = expect_df[diff_bool].dropna(how='all')
    diff_index = difference_output_df.index
    print(diff_index)

    if len(difference_output_df) != 0:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
            print(diff_bool)
            print("difference in output_df")
            print(difference_output_df)
            print("difference in expect_df")
            print(difference_expect_df)
            print("diff TextID:")
            print(output_df.loc[diff_index])
            # diff = difflib.ndiff(difference_output_df['content'].iloc[0], difference_expect_df['content'].iloc[0])
            # delta = ''.join(x[2:] for x in diff if x.startswith('- '))
            # print(delta)


    assert len(difference_output_df) == 0


    os.remove(output_path)
    os.remove(output_path2)
