#!/usr/bin/env python
# coding=utf-8

import math
import re
import xlsxwriter

import BaseCrash as crash

class BaseReport:
    def __init__(self, wd):
        self.wd = wd
        self._crashM = ["Test"]
        self.seed = "0"

    def monitor(self, info):
        for t in info:
            for wrap in t:
                for item in t[wrap]:
                    print(t[wrap])
                    print(t[wrap]["header"]["phone_name"])
                    self.getCrashMessage(t[wrap]["header"]["monkey_log"])
                    break


    def get_seed(self):
        """
        get the seed
        """
        with open(log, encoding="utf-8") as monkey_log:
            lines = monkey_log.readlines()
            for line in lines:
                if re.findall("seed=", line):
                    self.seed = line
                    
    def getCrashMessage(self, log):
        with open(log, encoding="utf-8") as monkey_log:
            lines = monkey_log.readlines()
            for line in lines:
                if re.findall(crash.ANR, line):
                    print("存在anr错误:" + line)
                    self._crashM.append(line)
                if re.findall(crash.CRASH, line):
                    print("存在crash错误:" + line)
                    self._crashM.append(line)
                if re.findall(crash.EXCEPTION, line):
                    print("存在exception错误:" + line)
                    self._crashM.append(line)

    def crash(self):
        if len(self._crashM):
            print(self._crashM)
            worksheet = self.wd.add_worksheet("Crash Detail")
            _write_center(worksheet, "A1", 'Crash', self.wd)
            _write_center(worksheet, "B1", 'Type', self.wd)
            _write_center(worksheet, "C1", 'Seed', self.wd)
            temp = 2
            for item in self._crashM:
                _write_center(worksheet, "A" + str(temp), item, self.wd)
                _write_center(worksheet, "B" + str(temp), self.seed, self.wd)
                temp = temp + 1


    def close(self):
        self.wd.close()

def get_format(wd, option={}):
    return wd.add_format(option)

def get_format_center(wd, num=1):
    return wd.add_format({'align': 'center', 'valign': 'vcenter', 'border': num})

def set_border_(wd, num=1):
    return wd.add_format({}).set_border(num)

def _write_center(worksheet, cl, data, wd):
    return worksheet.write(cl, data, get_format_center(wd))

def set_row(worksheet, num, height):
    worksheet.set_row(num, height)