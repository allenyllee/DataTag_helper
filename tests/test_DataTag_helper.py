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
