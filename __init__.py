# __init__.py 为初始入口文件,工程代码的入口文件.

# 通过插件系统接入 esp32
from ascript.android.system import R, Device
from ascript.android import system
from ascript.android.screen import capture, FindColors, FindImages, Ocr
from ascript.android.node import Selector
from ascript.android.action import click, slide, Touch, gesture
# from ascript.android import plug
# plug.load("esp32")

from . import main
