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


def PassOrFail(SN):
    log_dir = "/vault/Atlas/Archive/" + SN
    log_dir_list = os.listdir(log_dir)
    for i in log_dir_list:
        if len(i) == 17:
            log_file_list.append(i)
    log_file_list.sort(key=lambda fn: os.path.getmtime(log_dir + '/' + fn))  # 排序
    log_time = log_file_list[-1]
    trd_dir = log_dir + "/" + log_time + "/" + "AtlasLogs"
    for filename_c in os.listdir(trd_dir):
        if filename_c == 'Records.csv':
            csv_file = open(trd_dir + "/" + filename_c)
            reader = csv.reader(csv_file)
            for row in reader:
                result_list.append(row[4])
            #print(result_list)
            if "ERROR" in result_list:
                return "ERROR"
            elif "FAIL" in result_list:
                return "FAIL"
            else:
                return "PASS"


def run_check_log():
    now_size = getdirsize(monitor_dir)
    while True:
        new_size = getdirsize(monitor_dir)
        if now_size != new_size:
            lists = os.listdir(monitor_dir)  # 获得文件夹内所有文件
            for i in lists:
                if len(i) == 17:
                    log_list.append(i)
            log_list.sort(key=lambda fn: os.path.getmtime(monitor_dir + '/' + fn))  # 排序
            new_sn = log_list[-1]   # 最新的文件名
            print(new_sn + ":" + PassOrFail(new_sn))
        else:
            pass
        now_size = new_size


def get_newlog_res():
    lists = os.listdir(monitor_dir)  # 获得文件夹内所有文件
    for i in lists:
        if len(i) == 17:
            log_list.append(i)
    log_list.sort(key=lambda fn: os.path.getmtime(monitor_dir + '/' + fn))  # 排序
    new_sn = log_list[-1]  # 最新的文件名
    return new_sn, PassOrFail(new_sn)
