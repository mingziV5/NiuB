#!/usr/bin/python
#coding:utf-8
import os, os.path
#from os import path
import time
import json
import base64
import hashlib
import traceback
import ConfigParser
import logging,logging.config
#from logging import config

work_dir = os.path.dirname(os.path.realpath(__file__))
#
def get_config(section=''):
    config = ConfigParser.ConfigParser()
    service_conf = os.path.join(work_dir, 'conf/service.conf')
    config.read(service_conf)

    conf_items = dict(config.items('common')) if config.has_section('common') else {}
    #print conf_items
    if section and config.has_section(section):
        conf_items.update(config.items(section))
    return conf_items
