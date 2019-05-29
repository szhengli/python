#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
读取配置文件
"""
from configparser import ConfigParser
import os


def GetConfig(section, key):
    d = os.path.dirname(__file__)
    config_file = "%s/config.cfg" % d
    cfg = ConfigParser()
    cfg.read(config_file, encoding='utf-8')
    return cfg.get(section, key)

