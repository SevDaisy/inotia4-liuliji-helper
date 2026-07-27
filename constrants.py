# from esp32 import BleDevice
from ascript.android import screen
from ascript.android.action import click, slide, Touch, gesture
# 导入控件检索相关
from ascript.android.node import Selector
# 导入图色相关
from ascript.android.screen import capture, FindColors, FindImages, Ocr
# 导入系统相关
from ascript.android import system
# 环境设备相关
from ascript.android.system import R, Device
# 模拟动作相关
from ascript.android import action

import time

# 全局变量声明
px = 'center_x'
py = 'center_y'
MilliSeconds = 0.001


def with_delay(func):
    """装饰器：在执行核心操作前后插入延迟"""
    def wrapper(*args, before=0, after=0, **kwargs):
        if before > 0:
            # print(f"执行前等待 {before} 毫秒")
            time.sleep(before*MilliSeconds)
        result = func(*args, **kwargs)
        if after > 0:
            # print(f"执行前等待 {after} 毫秒")
            time.sleep(after*MilliSeconds)
        return result
    return wrapper


def pin(debug=False):
    now = screen.capture()
    screen.bitmap_to_file(R.sd("1.png"), now)
    if debug:
        print(now)
    return now


@with_delay
def ocrFind(txt: str, img: None, debug=False):
    """
    在屏幕上查找文字，返回第一个匹配结果。
    :param txt: 指定查找文本, img: 传入源图, None=自动截屏
    :return: dict {text, rect, center_x, center_y, confidence} 或 None
    """
    if img is None:
        return Ocr.find(text=txt, image=pin())
    return Ocr.find(text=txt, image=img)


@with_delay
def doClick(x, y, dur=20):
    return action.click(x, y, dur)


@with_delay
def doSlide(x1, y1, x2, y2, dur=300):
    return action.slide(x1, y1, x2, y2, dur)
