#!/usr/bin/env python
# -*- coding=utf-8 -*-
import time
import sys
import os
import datetime
import re
import csv
from os.path import join, getsize

monitor_dir = "/vault/Atlas/Archive"
log_dir = "/Users/wts-sw/Desktop/Log/"
day_time = datetime.datetime.now().strftime('%Y-%m-%d')
screen_time = datetime.datetime.now().strftime('%Y%m%d')
pattern = re.compile(screen_time)
log_list = []
row_list = []
result_list = []
log_file_list = []


def get_new_file(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        for i in dir_list:
            if i.startswith("."):
                dir_list.remove(i)
        dir_list = sorted(dir_list,  key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        # print(dir_list)
        return dir_list[-1]


def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return size


def del_oldlog(dir):
    list = os.listdir(dir)
    for i in range(0, len(list)):
        if bool(re.search(day_time, list[i])):
            os.remove(dir + list[i])


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def GetLogPath(SN):
    log_dir = "/vault/Atlas/Archive/" + SN
    log_time = get_new_file(log_dir)
    res = log_dir + "/" + log_time + "/" + "AtlasLogs"
    return res


def SNbyAttributes(SN):
    A_Value = []
    Attributes = GetLogPath(SN)
    for filename in os.listdir(Attributes):
        if filename == 'Attributes.csv':
            csv_file = open(Attributes + "/" + filename)
            reader = csv.reader(csv_file)
            for row in reader:
                A_Value.append(row[3])
    return A_Value[1]


def PassOrFail(SN):
    result_list = []
    trd_dir = GetLogPath(SN)
    for filename_c in os.listdir(trd_dir):
        if filename_c == 'Records.csv':
            csv_file = open(trd_dir + "/" + filename_c)
            reader = csv.reader(csv_file)
            for row in reader:
                result_list.append(row[4])
            print(result_list)
            if "ERROR" in result_list:
                return "ERROR"
            elif "FAIL" in result_list:
                return "FAIL"
            else:
                return "PASS"


def get_newlog_res():
    new_sn = get_new_file(monitor_dir)  # 最新的文件名
    sn_num = SNbyAttributes(new_sn)
    return sn_num, PassOrFail(new_sn)
