# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import logging.config
import os

import wx
from colorlog import ColoredFormatter

from ui.MainFrame import MainFrame


def setupLogging(default_path="res/values/logging.json", default_level=logging.INFO, env_key="LOG_CFG"):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as f:
            config = json.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

    for handler in logging.root.handlers:
        if isinstance(handler, logging.StreamHandler):
            console_handle = handler
            break
    print(console_handle)
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s %(pathname)s:%(lineno)d [%(levelname)s]%(module)s%(reset)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        })
    console_handle.setFormatter(formatter)


if __name__ == '__main__':
    setupLogging()
    app = wx.App(False)
    frame = MainFrame(None, u"Financial Assistant")
    frame.Show(True)  # 显示该窗口
    app.MainLoop()  # 应用程序消息处理
